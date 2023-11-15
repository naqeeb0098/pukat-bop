// Copyright (c) 2023, Pukat Digital and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Details with Children"] = {
	"filters": [
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
		},
		{
			"fieldname": "employee_status",
			"label": __("Employee Status"),
			"fieldtype": "Select",
			"options": [
				{ "value": "Active", "label": __("Active") },
				{ "value": "Inactive", "label": __("Inactive") },
				{ "value": "Suspended", "label": __("Suspended") },
				{ "value": "Left", "label": __("Left") },
			],
			"default": "Active",
		}
	]
};
