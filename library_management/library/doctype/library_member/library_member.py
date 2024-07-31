# Copyright (c) 2024, priyanka and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LibraryMember(Document):
    """
        method updates full name by concatenate first and last name 
        Args:
            self: contains the current instance
        Returns:
            provide the full name
    """ 
    def before_save(self):
        self.full_name = f'{self.first_name} {self.last_name or ""}'


