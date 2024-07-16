// Copyright (c) 2024, priyanka and contributors
// For license information, please see license.txt


frappe.ui.form.on('Food', {
    validate: function(frm) {
        calculate_totals(frm);
    },
    fooddetail_add: function(frm, cdt, cdn) {
        update_rate_and_amount(frm, cdt, cdn);
    },
    fooddetail_remove: function(frm) {
        calculate_totals(frm);
    }
});

frappe.ui.form.on('Food Details', {
    food_type: function(frm, cdt, cdn) {
        update_rate_and_amount(frm, cdt, cdn);
    },
    count: function(frm, cdt, cdn) {
        update_amount_and_totals(frm, cdt, cdn);
    },
    rate: function(frm, cdt, cdn) {
        update_amount_and_totals(frm, cdt, cdn);
    },
    amount: function(frm, cdt, cdn) {
        calculate_totals(frm);
    }
});

function update_rate_and_amount(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let rate = 0;

    if (row.food_type === 'Normal') {
        rate = frm.doc.normal_rate || 0;
    } else if (row.food_type === 'Special') {
        rate = frm.doc.special_rate || 0;
    }

    frappe.model.set_value(cdt, cdn, 'rate', rate);
    update_amount_and_totals(frm, cdt, cdn);
}

function update_amount_and_totals(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    row.amount = row.count * row.rate;
    frappe.model.set_value(cdt, cdn, 'amount', row.amount);

    calculate_totals(frm);
}

function calculate_totals(frm) {
    let total_count = 0;
    let total_amount = 0;

    frm.doc.daily_food_details.forEach(function(row) {
        total_count += row.count || 0;
        total_amount += row.amount || 0;
    });

    frm.set_value('total_count', total_count);
    frm.set_value('total_amount', total_amount);

    frm.refresh_field('total_count');
    frm.refresh_field('total_amount');
}
