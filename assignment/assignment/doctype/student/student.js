frappe.ui.form.on("Student", {
    savebutton(frm) {
        console.log(frm.doc);
        frappe.call({
            method: 'frappe.client.insert',
            args: {
                doc: {
                    'doctype': 'User',
                    'email': frm.doc.email,
                    'first_name': frm.doc.first_name,
                    'last_name': frm.doc.last_name,
                    'enabled': 1,
                    'user_type': 'System User',
                    'roles': [{
                        'role': 'Student'
                    }]
                }
            },
            callback: function (response) {
                if (response.message) {
                    frappe.msgprint(__('User created successfully'));
                }
            }
        });
    },
    refresh: function (frm) {
        update_combined_address(frm);
    },
    default_address: function (frm) {
        update_combined_address(frm);
    },
    link_address: function (frm) {
        update_combined_address(frm);
    }
});

function update_combined_address(frm) {
    if (frm.doc.link_address) {
        frappe.call({
            method: 'frappe.client.get',
            args: {
                doctype: 'Address',
                name: frm.doc.link_address
            },
            callback: function (r) {
                if (r.message) {
                    let address = r.message;
                    let html_address = `Address:-<br><p>${address.address_line1 || ''}<br> ${address.address_line2 || ''}<br> ${address.city || ''}<br> ${address.state || ''}<br> ${address.country || ''}<br> ${address.pincode || ''}</p>`;
                    frm.fields_dict.html_address.$wrapper.html(html_address);
                } else {
                    frm.fields_dict.html_address.$wrapper.html('No address found.');
                }
            }
        });
    } else {
        frm.fields_dict.html_address.$wrapper.html('Please select an address.');
    }
}
 