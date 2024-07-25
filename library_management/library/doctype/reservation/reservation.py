# Copyright (c) 2024, priyanka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Reservation(Document):
      @frappe.whitelist()
      def custom_query(doctype,txt,searchfield,start,page_len,filter):
           today= datetime.now().date()
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
