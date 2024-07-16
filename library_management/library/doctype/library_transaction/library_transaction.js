// Copyright (c) 2024, priyanka and contributors
// For license information, please see license.txt

frappe.ui.form.on("Library Transaction", {
	onload(frm) {
        frm.set_query('library_member', () => {
            return {
                query: 'library_management.library.doctype.library_transaction.library_transaction.custom_query',
                
            }  
        })
	},
});
