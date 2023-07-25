# Copyright (c) 2023, Pukat Digital and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ReScheduleLoanRepayment(Document):
	# pass


	@frappe.whitelist()
	def update_repayments(self):
		for loan in self.re_schedule_loan_repayment_table:
			loan_doc = frappe.get_doc("Loan",loan.loan)
			for row in loan_doc.repayment_schedule:
				if row.is_accrued != 1:
					new_date = frappe.utils.add_months(row.payment_date,1)
					frappe.msgprint(frappe.as_json(new_date))
					frappe.db.sql(f"""update `tabRepayment Schedule` set payment_date = '{new_date}' where name = '{row.name}'""")