// Copyright (c) 2024, priyanka and contributors
// For license information, please see license.txt


frappe.ui.form.on("Reservation", {
	onload(frm) {
        frm.set_query('library_member', () => {
            return {
                query: 'library_management.library.doctype.reservation.reservation.custom_query',
                
            }  
        })
	},  
});

// frappe.ui.form.on("Reservation", {
// 	onload(frm) {
//         frm.set_query('library_member', () => {
//             return {
//                 query: 'library_management.library.doctype.reservation.reservation.custom_queryss',
                
//             }  
//         })
// 	},  
// });
