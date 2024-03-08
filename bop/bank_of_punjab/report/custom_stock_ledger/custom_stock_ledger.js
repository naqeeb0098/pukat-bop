// Copyright (c) 2024, Pukat Digital and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Custom Stock Ledger"] = {
	"filters":[
	
		{
			"fieldname":"fromdate",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default" : frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname":"todate",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default" : frappe.datetime.add_days(frappe.datetime.get_today()),
		},
		// {
		// 	"fieldname":"warehouse",
		// 	"label": __("Warehouse"),
		// 	"fieldtype": "Link",
		// 	"options": "Warehouse",
        //     // 'reqd':1,
		// },
		{
			"fieldname":"item",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item",
			// 'reqd':1,
		},
	
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
            "options": ["","Draft","Submitted"],
			"default":""
		}
		
	]
};