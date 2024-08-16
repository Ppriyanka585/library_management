// Copyright (c) 2024, priyanka and contributors
// For license information, please see license.txt

frappe.ui.form.on("Library Transaction", {
    onload(frm) {
        frm.set_query("library_member", () => {
            return {
                query: "library_management.library.doctype.library_transaction.library_transaction.custom_query",
            };
        });
    },
});

frappe.ui.form.on("Library Transaction", {
    refresh: function(frm) {
        frm.add_custom_button("Create Membership", () => {
            frappe.new_doc("Library Membership", {
                library_transaction: frm.doc.name,
            });
        });
        frm.add_custom_button("Reserve Book", () => {
            frappe.new_doc("Reservation", {
                library_transaction: frm.doc.name,
            });
        });
    },
});
fetch('http://<base-url>/api/method/frappe.auth.get_logged_user', {
    headers: {
        'Authorization': 'token api_key:api_secret'
    }
})
.then(r => r.json())
.then(r => {
    console.log(r);
})
