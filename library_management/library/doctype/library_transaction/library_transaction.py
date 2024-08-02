import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, getdate
from datetime import datetime

class LibraryTransaction(Document):
    def before_save(self):
        """
        Calculate the fine for late return, damage, or lost articles.

        Args:
            self: Contains the current instance of the transaction.
        """
        # Retrieve fines and settings from Library Settings
        lost_fine = frappe.db.get_single_value("Library Settings", "late_return_fine")
        damage_fine = frappe.db.get_single_value("Library Settings", "damage_fine_factor")
        lost_factor = frappe.db.get_single_value("Library Settings", "lost_fine_factor")
        borrow_period = frappe.db.get_single_value("Library Settings", "book_borrow_period")
        
        total_fine = 0

        for i in self.add_articles:
            total_return_fine = 0.0
            trans_type = i.get("type")
            article = frappe.get_doc("Article", i.article)
            price = article.price  

            if trans_type == "Return":
                # Get issued transactions for the library member
                issued_transactions = frappe.get_all(
                    "Library Transaction",
                    filters={"library_member": self.library_member, "type": "Issue", "docstatus": 1},
                    fields=["name", "date"],
                    order_by="date desc"
                )
                
                issue_date = None
                for transaction in issued_transactions:
                    if frappe.db.exists("Add Article", {"article": i.article, "parent": transaction["name"]}):
                        issue_date = transaction["date"]
                        break

                # Calculate fine for overdue return
                if issue_date:
                    overdue_days = date_diff(getdate(self.date), getdate(issue_date)) - borrow_period
                    if overdue_days > 0:
                        fine = overdue_days * lost_fine
                        total_return_fine += fine

                # Calculate fine for damage or loss
                fine_type = i.get("fine")
                if fine_type == "Damage Fine":
                    fine = (price / 2) + damage_fine
                elif fine_type == "Lost Fine":
                    fine = price + lost_factor
                else:
                    fine = 0

                total_fine = fine + total_return_fine

        # Set the total fine amount
        self.total_amount = total_fine

    def before_submit(self):
        """
        Update the status field of the article if criteria are met.
        """
        for i in self.add_articles:
            if i.type == "Issue":
                print(f"Issuing article: {i.article}") 
                self.validate_issue(i.article)  
                self.validate_maximum_limit()
                article = frappe.get_doc("Article", i.article)
                article.status = "Issued"
                article.save()

            elif i.type == "Return":
                print(f"Returning article: {i.article}")
                self.validate_return(i.article)
                print(f"Returning article: {i.article}")
                article = frappe.get_doc("Article", i.article)
                article.status = "Available"
                article.save()

    def validate_issue(self, article_id):
        """
        Validate if the transaction type is an issue for the given article.

        Args:
            article_id: The ID of the article being validated.
        """
        self.validate_membership()
        article = frappe.get_doc("Article", article_id)
        if article.status == "Issued":
            frappe.throw(f"Article {article.name} is already issued by another member")

    def validate_return(self, article_id):
        """
        Validate if the transaction type is a return for the given article.

        Args:
            article_id: The ID of the article being validated.
        """
        article = frappe.get_doc("Article", article_id)
        if article.status == "Available":
            frappe.throw(f"Article {article.name} cannot be returned without being issued first")

    def validate_maximum_limit(self):
        """
        Check if the member meets the maximum limit of borrowing books.

        Args:
            self: Contains the current instance of the transaction.
        """
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
        count = 0

        issued_tran = frappe.get_all(
            "Library Transaction",
            filters={"library_member": self.library_member, "docstatus": 1},
            fields=["name"],
        )

        for tran in issued_tran:
            if frappe.db.exists(
                "Add Article",
                {
                    "type": "Issue",
                    "parent": tran["name"]
                },
            ):
                count += 1

        if count >= max_articles:
            frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        """
        Check if the member has a valid membership.

        Args:
            self: Contains the current instance of the transaction.
        """
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": 1,
                "from_date": ("<", self.date),
                "to_date": (">", self.date),
            },
        )

        if not valid_membership:
            frappe.throw("The member does not have a valid membership")

@frappe.whitelist()
def custom_query(doctype, txt, searchfield, start, page_len, filter):
    """
    Filters library members who have a valid membership.

    Args:
        doctype: Contains Library Member doctype.
    Returns:
        List of members whose membership is valid.
    """
    today = datetime.now().date()
    valid_memberships = frappe.get_all(
        "Library Membership",
        filters={
            "docstatus": 1,
            "from_date": ("<=", today),
            "to_date": (">=", today),
        },
        pluck="library_member",
    )

    return [[member] for member in valid_memberships] or []
