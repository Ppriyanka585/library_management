# Copyright (c) 2024, Priyanka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
from datetime import datetime

class LibraryMembership(Document):
    def validate(self):
        """
        Ensures that the 'from date' is earlier than the 'to date'.

        Args:
            self: Contains the current instance of the membership.
        """
        if self.from_date and self.to_date and self.from_date > self.to_date:
            frappe.throw("From Date must be earlier than To Date")
            self.from_date = None
            self.to_date = None

    def before_submit(self):
        """
        Calculates the 'to date' based on the loan period.

        Args:
            self: Contains the current instance of the membership.
        """
        # Check for active memberships that overlap with the new membership period
        exists = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                "to_date": (">", self.from_date),
            },
        )
        if exists:
            frappe.throw("There is an active membership for this member")

        # Calculate the to_date based on the loan period from Library Settings
        loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
        self.to_date = frappe.utils.add_days(self.from_date, loan_period)

class CustomLibraryMembership(Document):
    """
    Validates that the library member applying for membership is at least 18 years old.

    Args:
        self: Contains the current instance of the membership.
    """
    def validate(self):
        # Retrieve the library member's date of birth
        member = frappe.get_doc("Library Member", self.library_member)
        if member.date_of_birth:
            age = self.calculate_age(member.date_of_birth)
            if age < 18:
                frappe.throw("Membership requires members to be at least 18 years old.")

    def calculate_age(self, date_of_birth):
        """
        Calculates the age of a member based on their date of birth.

        Args:
            date_of_birth (datetime): The member's date of birth.

        Returns:
            int: The age of the member.
        """
        today = datetime.today()
        age = today.year - date_of_birth.year - (
            (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
        )
        return age
