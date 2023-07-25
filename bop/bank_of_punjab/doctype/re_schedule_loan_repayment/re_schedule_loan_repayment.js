// Copyright (c) 2023, Pukat Digital and contributors
// For license information, please see license.txt

frappe.ui.form.on("Re Schedule Loan Repayment", {
  refresh: function (frm) {
    frm.add_custom_button(
      __("Update Repayment Scedule"),
      function () {
        return frappe.call({
          doc: frm.doc,
          method: "update_repayments",
          callback: function () {
            frm.refresh();
          },
        });
      },
      __("Actions")
    );
  },

  //   update_repayment_schedule: function (frm) {
  //     if (frm.doc.re_schedule_loan_repayment_table) {
  //       // Call the server-side function to fetch data
  //       frappe.call({
  //         method:
  //           ".myapp.doctype.custom_module.custom_module.get_repayment_schedules",
  //         args: {
  //           start_date: frappe.datetime.get_formatted_js_date(firstDayOfMonth),
  //           end_date: frappe.datetime.get_formatted_js_date(lastDayOfMonth),
  //         },
  //         callback: function (response) {
  //           // Handle the response data
  //           if (response.message) {
  //             // Do something with the data
  //           }
  //         },
  //       });
  //     }
  //   },
});
