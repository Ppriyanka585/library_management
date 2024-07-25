# Copyright (c) 2024, priyanka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
from datetime import datetime



class LibraryMembership(Document):
    def validate(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            frappe.throw("From Date must be earlier than To Date")
            self.from_date = None
            self.to_date = None

        

    def before_submit(self):
        print("llllloooo")
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

        loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
        self.to_date = frappe.utils.add_days(self.from_date, loan_period )
        datee = self.to_date 
        print(datee)
      
class CustomLibraryMembership(Document):
    def validate(self):
        member = frappe.get_doc("Library Member", self.library_member)
        if member.date_of_birth:
            age = self.calculate_age(member.date_of_birth)
            if age < 18:
                frappe.throw("For Membership requires members to be at least 18 years old.")

    def calculate_age(self, date_of_birth):
        today = datetime.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        return age
        

    
