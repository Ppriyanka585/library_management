# Copyright (c) 2024, priyanka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, getdate
from datetime import datetime

class LibraryTransaction(Document):
    def before_save(self):
        """
            method calculate the fine
            Args:
                self: contains the current instance
            Returns:
                Calculated total fine amount
        """          
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
                issued_transactions = frappe.get_all(
                    "Library Transaction",
                    filters={"library_member": self.library_member, "type": "Issue", "docstatus": 1},
                    fields=["name", "date"],
                    order_by="date desc"
                )
                issue_date = None
                for transaction in issued_transactions:
                    print("in loop")
                    if frappe.db.exists("Add Article", {"article": i.article, "parent": transaction["name"]}):
                        issue_date = transaction["date"]
                        break
                if issue_date:
                    overdue_days = date_diff(getdate(self.date), getdate(issue_date)) - borrow_period
                    if overdue_days > 0:
                        fine = overdue_days * lost_fine
                        total_return_fine += fine
                fine_type = i.get("fine")
                if fine_type == "Damage Fine":
                    fine = (price / 2) + damage_fine
                elif fine_type == "Lost Fine":
                    fine = price + lost_factor
                else:
                    fine = 0
                total_fine = fine + total_return_fine
        self.total_amount = total_fine

    def before_submit(self):
        """
            method update status field of article if criteria met
            Args:
                self: contains the current instance
            Returns:
                update status field
        """ 
        for i in self.add_articles:
            print(i.article)
            print("first")
            if i.type == "Issue":
                self.validate_issue()
                self.validate_maximum_limit()
                article = frappe.get_doc("Article", i.article)
                print(article.status, article.article_name)
                article.status = "Issued"
                article.save()

            elif i.type == "Return":
                self.validate_return()
                article = frappe.get_doc("Article", i.article)
                article.status = "Available"
                article.save()

    def validate_issue(self):
        """
            method validate if type is issue
            Args:
                self: contains the current instance
            Returns:
                ture if validate issue otherwise throw error
        """ 
        self.validate_membership()
        print("hlo")
        for i in self.add_articles:
            print(i.article)
            print("for issue check")
            article = frappe.get_doc("Article", i.article)
            if article.status == "Issued":
                frappe.throw(f"Article {article.name} is already issued by another member")
            else:
                break

    def validate_return(self):
        """
            method validate if type is return
            Args:
                self: contains the current instance
            Returns:
                true if validate return otherwise throw error
        """ 
        for i in self.add_articles:
            print(i.article)
            print("for return check")
            article = frappe.get_doc("Article", i.article)
            if article.status == "Available":
                frappe.throw(f"Article {article.name} cannot be returned without being issued first")

    # def validate_maximum_limit(self):
    #     max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
    #     count = frappe.db.count(
    #         "Library Transaction",
    #         {"library_member": self.library_member, "type": "Issue", "docstatus": 1},
    #     )
    #     print("validated max limit")
    #     if count + len(self.add_articles) > max_articles:
    #         frappe.throw("Maximum limit reached for issuing articles")

    def validate_maximum_limit(self):
        """
            method check the Member meets the maximum limit of borrowing books
            Args:
                self: contains the current instance
            Returns:
                true if validate maximum limit otherwise throw error
        """ 
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
        count = 0
        issued_tran = frappe.get_all(
                        "Library Transaction",
                        filters={"library_member": self.library_member, "docstatus": 1},
                        fields=["name"],
                    )
        print(issued_tran)
        for tran in issued_tran:
            if frappe.db.exists(
                "Add Article",
                {
                "type": "Issue",
                "parent": tran["name"]
                },
            ):
                count += 1
  
        print(count)
        if count + len(self.add_articles) > max_articles:
            frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        """
            method check the Member has a valid membership
            Args:
                self: contains the current instance
            Returns:
                true if have valid membership otherwise throw error
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
        print("validated membership")
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")

@frappe.whitelist()
def custom_query(doctype, txt, searchfield, start, page_len, filter):
    """
        method filters library member who has valid membership
        Args:
            doctype: contains Library Member doctype
        Returns:
            List of members whose membership is valid
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
