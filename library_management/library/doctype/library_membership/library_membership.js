// Copyright (c) 2024, priyanka and contributors
// For license information, please see license.txt

frappe.ui.form.on("Library Membership", {
    from_date: function(frm) {
        if (frm.doc.from_date && frm.doc.to_date && (frm.doc.from_date > frm.doc.to_date)) {
            frm.set_value("from_date", "");
            frappe.throw({
                message: __("From Date must be earlier than To Date"),
                indicator: "white"
            });
        }
    },
    to_date: function(frm) {
        if (frm.doc.from_date && frm.doc.to_date && (frm.doc.from_date > frm.doc.to_date)) {
            frm.set_value("to_date", "");
            frappe.throw({
                message: __("To Date must be later than From Date"),
                indicator: "white"
            });
        }
    }
});
