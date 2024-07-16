import frappe
# from frappe.model.document import Document

def after_migrate():
    print("Migrated Successfully")

# def on_save(doc,method):
#     if doc.Doctype =="Library Member":
#         if doc.last_name == "P":
#             Members = frappe.db.get_doc('Library Member',filter={"doc.last_name "="P"})
#             Members.last_name = "AAA"
#             Members.save()
#             print("last name updated successfully")


# myapp/myapp/hooks/user_hooks.py


def after_insert(doc, method):
    if doc.doctype == "User":
        frappe.msgprint(f"New user {doc.first_name} created successfully")


def before_insert(doc, method):
    if doc.doctype == "Library Member":
        if doc.last_name == "P":
            doc.last_name = "KPP"





            

            

