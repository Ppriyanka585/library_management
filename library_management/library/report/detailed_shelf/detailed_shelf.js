// Copyright (c) 2024, priyanka and contributors
// For license information, please see license.txt

// frappe.query_reports["Detailed Shelf"] = {
// 	"filters": [

// 	]
// };
frappe.query_reports["Detailed Shelf"] = {
    filters: [
        {
            fieldname: "shelf",
            label: __("Shelf"),
            fieldtype: "Link",
            options: "Shelf",
        },
        
    ]
}

