# Copyright (c) 2024, Pukat Digital and contributors
# For license information, please see license.txt

import frappe 
from frappe import _

def execute(filters=None):
	data = []
	columns = [
		{"label": _("Item Code"),"fieldname": "item_code","fieldtype": "Data","width": 100},
		{"label": _("Item Name"),"fieldname": "item_name","fieldtype": "Data","width": 130},
		{"label": _("Posting Date"),"fieldname": "posting_date","fieldtype": "Data","width": 110},
		{"label": _("Status"),"fieldname": "docstatus","fieldtype": "Data","width": 100},
		{"label": _("Stock UOM"), "fieldname": "uom", "fieldtype": "Data", "width": 100},  
		{"label": _("SE Type"),"fieldname": "stock_entry_type","fieldtype": "Data","width": 130},
  		{"label": _("T Warehouse"),"fieldname": "t_warehouse","fieldtype": "Data","width": 130},
		{"label": _("S Warehouse"),"fieldname": "s_warehouse","fieldtype": "Data","width": 130},
		{"label": _("In Qty"),"fieldname": "in_qty","fieldtype": "Int","width": 80},
		{"label": _("Out Qty"),"fieldname": "out_qty","fieldtype": "Int","width": 80},
		{"label": _("Balance Qty"),"fieldname": "balance_qty","fieldtype": "Int","width": 100}
	
		]
 
	from_date = filters.get('fromdate')
	to_date = filters.get('todate')
	if from_date and to_date:
		date = f"AND date(se.posting_date) BETWEEN '{from_date}' AND '{to_date}'"
	else:
		date = ""
 
	# if filters.get('item'):
	# 	item = filters.get('item')
	# 	item = f"AND sed.item_code ={item}"
	# else:
	# 	item=''
	if filters.get('item'):
		item = filters.get('item')
		# Check if there are any stock entries associated with the item
		stock_entries_exist = frappe.db.exists(
			"Stock Entry Detail",
			{"item_code": item}
		)
		if stock_entries_exist:
			item = f"AND sed.item_code = '{item}'"
		else:
			frappe.throw("There is no stock entry against this item")
	else:
		item = ''

	if filters.get('status'):
		status = filters.get('status')
		if status == 'Draft':
			status = 0
		else:
			status = 1
		status = f"AND sed.docstatus ='{status}'"
	else:
		status = ''
     

	data=frappe.db.sql(f"""
					SELECT 
						se.NAME,	
						se.stock_entry_type,
						sed.NAME,
						se.posting_date,
						sed.s_warehouse,
						sed.t_warehouse,
						sed.item_code,
						sed.item_name,
						date(sed.creation),
						sed.DESCRIPTION,
						sed.qty,
						CASE WHEN sed.docstatus = 1 THEN 'Submitted' ELSE 'Draft' END AS docstatus,
						CASE WHEN se.stock_entry_type = 'Material Receipt' THEN sed.qty ELSE 0 END AS in_qty,
						CASE WHEN se.stock_entry_type = 'Material Issue' THEN sed.qty ELSE 0 END AS out_qty,
						(
							SELECT 
								SUM(CASE WHEN se_inner.stock_entry_type = 'Material Receipt' THEN sed_inner.qty ELSE -sed_inner.qty END)
							FROM 
								`tabStock Entry` AS se_inner
							INNER JOIN 
								`tabStock Entry Detail` AS sed_inner ON se_inner.name = sed_inner.parent
							WHERE 
								sed_inner.item_code = sed.item_code AND date(se_inner.posting_date) <= date(se.posting_date)
						) AS balance_qty,
						sed.actual_qty,
						sed.uom,
						sed.parent

					FROM 
						`tabStock Entry` AS se
					INNER JOIN 
						`tabStock Entry Detail` AS sed ON se.name = sed.parent
					WHERE 
						1=1 {item} {status} {date} 
					ORDER BY sed.item_name
				""",as_dict =1,debug=True)
		
	return columns, data