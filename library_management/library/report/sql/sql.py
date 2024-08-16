# import frappe
# from frappe import _

# def execute(filters=None):
#     columns, data = [], []

#     # Define the columns for the report
#     columns = [
#         {
#             'fieldname': 'name',
#             'label': _('Member ID'),
#             'fieldtype': 'Link',
#             'options': 'Library Member'
#         },
#         {
#             'fieldname': 'full_name',
#             'label': _('Name'),
#             'fieldtype': 'Data',
#         },
#         {
#             'fieldname': 'email_address',
#             'label': _('Email'),
#             'fieldtype': 'Data',
#         },
#         {
#             'fieldname': 'membership_count',
#             'label': _('Membership Count'),
#             'fieldtype': 'Int',
#         },
#         {
#             'fieldname': 'membership_status',
#             'label': _('Membership Status'),
#             'fieldtype': 'Data',
#         },
#         {
#             'fieldname': 'membership_from',
#             'label': _('Membership From'),
#             'fieldtype': 'Date',
#         },
#         {
#             'fieldname': 'membership_to',
#             'label': _('Membership To'),
#             'fieldtype': 'Date',
#         }
#     ]

#     # SQL query to get all necessary member data in one go
#     query = """
#         SELECT 
#             lm.name AS member_id,
#             lm.full_name,
#             lm.email_address,
#             COUNT(DISTINCT lmship.name) AS membership_count,
#             MAX(lmship.to_date) >= CURDATE() AS has_valid_membership,
#             MIN(lmship.from_date) AS membership_from,
#             MAX(lmship.to_date) AS membership_to
#         FROM 
#             `tabLibrary Member` lm
#         LEFT JOIN 
#             `tabLibrary Membership` lmship ON lmship.library_member = lm.name AND lmship.docstatus = 1
#         GROUP BY 
#             lm.name
#     """

#     # Execute the SQL query
#     member_data = frappe.db.sql(query, as_dict=True)

#     # Process the results
#     for member in member_data:
#         membership_status = "Valid Membership" if member['has_valid_membership'] else "No Membership"
#         data.append({
#             'name': member['member_id'],
#             'full_name': member['full_name'],
#             'email_address': member['email_address'],
#             'membership_count': member['membership_count'],
#             'membership_status': membership_status,
#             'membership_from': member['membership_from'],
#             'membership_to': member['membership_to'],
#         })

#     return columns, data
from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    """
    Generates a report with library member details including membership status, period, and current articles.

    Args:
        filters (dict, optional): Dictionary containing filter values for the report.

    Returns:
        columns (list): List of dictionaries defining the columns of the report.
        data (list): List of dictionaries containing the member data for the report.
    """
    columns = [
        {
            'fieldname': 'name',
            'label': _('Member ID'),
            'fieldtype': 'Link',
            'options': 'Library Member'
        },
        {
            'fieldname': 'full_name',
            'label': _('Name'),
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'email_address',
            'label': _('Email'),
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'membership_count',
            'label': _('Membership Count'),
            'fieldtype': 'Int',
        },
        {
            'fieldname': 'late_membership',
            'label': _('Membership Status'),
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'membership_from',
            'label': _('Membership From'),
            'fieldtype': 'Date',
        },
        {
            'fieldname': 'membership_to',
            'label': _('Membership To'),
            'fieldtype': 'Date',
        },
        {
            'fieldname': 'transaction_count',
            'label': _('Transaction Count'),
            'fieldtype': 'Int',
        },
        {
            'fieldname': 'transaction_date',
            'label': _('Last Transaction'),
            'fieldtype': 'Date',
        },
        {
            'fieldname': 'issued_art',
            'label': _('Issued Articles'),
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'returned_art',
            'label': _('Returned Articles'),
            'fieldtype': 'Data',
        },
    ]

    today = frappe.utils.nowdate()

    query = """
    SELECT
        lm.name,
        lm.full_name,
        lm.email_address,
        COUNT(DISTINCT lms.name) AS membership_count,
        IF(MAX(
            CASE
                WHEN lms.from_date <= %(today)s AND lms.to_date >= %(today)s THEN 1
                ELSE 0
            END
        ) = 1, 'Valid Membership', 'No Membership') AS late_membership,
        MIN(lms.from_date) AS membership_from,
        MAX(lms.to_date) AS membership_to,
        COUNT(DISTINCT lt.name) AS transaction_count,
        MAX(lt.date) AS transaction_date,
        GROUP_CONCAT(DISTINCT CASE WHEN laa.type = 'Issue' THEN laa.article END ORDER BY laa.article SEPARATOR ', ') AS issued_art,
        GROUP_CONCAT(DISTINCT CASE WHEN laa.type = 'Return' THEN laa.article END ORDER BY laa.article SEPARATOR ', ') AS returned_art
    FROM
        `tabLibrary Member` lm
    LEFT JOIN
        `tabLibrary Membership` lms ON lm.name = lms.library_member
        AND lms.docstatus = 1
        AND lms.from_date <= %(today)s
        AND lms.to_date >= %(today)s
    LEFT JOIN
        `tabLibrary Transaction` lt ON lm.name = lt.library_member
        AND lt.docstatus = 1
    LEFT JOIN
        `tabAdd Article` laa ON lt.name = laa.parent
    GROUP BY
        lm.name, lm.full_name, lm.email_address
    """

    data = frappe.db.sql(query, {"today": today}, as_dict=True)

    return columns, data
