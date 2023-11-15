# Copyright (c) 2023, Pukat Digital and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime

def execute(filters=None):
	if not filters:
		filters = {}

	data = get_employees(filters)

	max_length = 0
	for emp in data:
		emp_doc = frappe.get_doc('Employee',emp[0])
		table_length = len(emp_doc.children)

		if table_length > max_length:
			max_length = table_length

		if len(emp_doc.children):
			childs = emp_doc.get("children")
			for ch in childs:
				ch_list = [ch.name1, ch.gender, ch.date_of_birth]
				emp.extend(ch_list)
				
				dob = ch.date_of_birth
				current_date = datetime.now()
				age = current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day))

				ch_list2 = [age, ch.not_eligible, ch.remarks]
				emp.extend(ch_list2)

	columns = get_columns(max_length)

	for row in data:
		n = len(columns) - len(row)
		if n > 0:
			row += [None] * n

	return columns, data


def get_columns(max_length):
	columns = [
		_("Employee") + ":Link/Employee:120",
		_("Employee Name") + ":Data:200",
		_("Date of Joining") + ":Date:100",
		_("Designation") + ":Link/Designation:120",
		_("Branch") + ":Link/Branch:120",
		_("Zone") + ":Link/Zone:120",
	]

	for i in range(max_length):
		columns = (
			columns
			+ [
				_("Name"+str(i+1)) + ":Data:120",
				_("Gender"+str(i+1)) + ":Data:120",
				_("Date of Birth"+str(i+1)) + ":Date:120",
				_("Age"+str(i+1)) + ":Data:120",
				_("Not Eligible"+str(i+1)) + ":Check:120",
				_("Remarks"+str(i+1)) + ":Data:120",
			]
		)
	

	return columns


def get_employees(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		"""select name, employee_name, date_of_joining, designation,
	branch, zone from tabEmployee where %s"""
		% conditions,
		as_list=1,
	)


def get_conditions(filters):
	conditions = ""
	if filters.get("employee_status"):
		conditions += " status = '%s'" % filters["employee_status"]
	#conditions += " name = 'HR-EMP-14'"

	if filters.get("employee"):
		conditions += " and name = '%s'" % filters["employee"]	

	return conditions
