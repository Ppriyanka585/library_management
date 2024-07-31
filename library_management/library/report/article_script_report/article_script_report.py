# Copyright (c) 2024, priyanka and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = [
        {
            "fieldname": "name",
            "label": _("Article Name"),
            "fieldtype": "Link",
            "options": "Article",
        },
        {
            "fieldname": "author",
            "label": _("Author"),
            "fieldtype": "Data",
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Select",
            "options": ["Issued", "Available"],
        },
        {
            "fieldname": "isbn",
            "label": _("ISBN"),
            "fieldtype": "Data",
        },
        {
            "fieldname": "publisher",
            "label": _("Publisher"),
            "fieldtype": "Data",
        },
        {
            "fieldname": "price",
            "label": _("Price"),
            "fieldtype": "Currency",
        },
        {
            "fieldname": "issue_count",
            "label": _("Issue Count"),
            "fieldtype": "Int",
        },
        {
            "fieldname": "return_count",
            "label": _("Return Count"),
            "fieldtype": "Int",
        }
    ]
    article_list = frappe.db.get_all("Article", fields=["name", "author", "status", "isbn", "publisher", "price"])
     
    sub_trans = frappe.db.get_list("Library Transaction", {"docstatus": 1}, pluck="name")

    for i in article_list:
        Issue_count = frappe.db.count("Add Article", {"article": i.name, "type": "Issue", "parent": ["in", sub_trans]})
        Return_count = frappe.db.count("Add Article", {"article": i.name, "type": "Return", "parent": ["in", sub_trans]})
    
        data.append({
             "name": i.name,
             "author": i.author,
             "status": i.status,
             "isbn": i.isbn,
             "publisher": i.publisher,
             "price": i.price,
             "issue_count": Issue_count,
             "return_count": Return_count
        })

    return columns, data
