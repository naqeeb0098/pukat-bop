import frappe

from erpnext.setup.doctype.employee.employee import Employee
class customEmployee(Employee):
    def validate(self):
        super().validate()
        self.name = self.old_no


@frappe.whitelist(allow_guest=True)
def employee_enqueue_updates():
    frappe.enqueue(update_employees)

def update_employees():
    try:
        employees = frappe.get_all("Employee", fields=["name", "old_no"])
        for emp in employees:
            frappe.log_error(str(emp), 'Employee before')
            if emp.name not in ("HR-EMP-823","HR-EMP-694","HR-EMP-673","HR-EMP-663","HR-EMP-654","HR-EMP-630","HR-EMP-625","HR-EMP-455","HR-EMP-295"):
                if emp.old_no and emp.old_no != emp.name:
                    frappe.rename_doc('Employee', emp.name, emp.old_no, force=True)
                    frappe.db.commit()  # Commit after each successful rename
                frappe.log_error(str(emp), 'Employee after')
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Employee Rename Error')
        frappe.db.rollback()  # Rollback in case of any exception


