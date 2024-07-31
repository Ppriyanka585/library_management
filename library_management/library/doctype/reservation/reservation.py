# Copyright (c) 2024, priyanka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime


class Reservation(Document):
	def before_submit(self):
		"""
			method updates status of article to reserved
			Args:
				self: contains current instance
		"""
		article = frappe.get_doc("Article", self.article_name)
		article.status = "Reserved"
		article.save()
				

@frappe.whitelist()
def custom_query(doctype,txt,searchfield,start,page_len,filter):
	"""
        method filters library member who has valid membership
        Args:
            doctype: contains Library Member doctype
        Returns:
			List of members whose membership is valid
    """
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

# def custom_query(doctype,txt,searchfield,start,page_len,filter):
#     today= datetime.now().date()
#     issued_articles = frappe.get_all(
#         "Article",
#         filters={
#             "status": "Issued",
#            },
#             pluck="article_name",
#     )
#     return [[member] for member in issued_articles] or []

