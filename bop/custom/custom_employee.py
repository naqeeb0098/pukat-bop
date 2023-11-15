import frappe

from erpnext.setup.doctype.employee.employee import Employee
class customEmployee(Employee):
    def validate(self):
        super().validate()
        self.name = self.old_no
        self.assign_position_based_roles()

    def assign_position_based_roles(self):
        if self.position or self.additional_position_1 or self.additional_position_2 or self.additional_position_3:
            positions = [self.position, self.additional_position_1, self.additional_position_2, self.additional_position_3]
            role_list = []
            for position in positions:
                if position:  # Check if position is not None or empty
                    role_to_be_assigned = frappe.db.get_value("Position", position, "role")
                    if role_to_be_assigned and role_to_be_assigned not in role_list:
                        role_list.append(role_to_be_assigned)

            roles_to_be_removed = frappe.db.get_all("Position","role",pluck="role")
            if self.user_id:
                user_doc = frappe.get_doc("User", self.user_id)
                existing_roles = [d.role for d in user_doc.roles]

                # Remove roles that are not in role_list, except for 'Employee'
                for role in existing_roles:
                    if role in roles_to_be_removed and role not in role_list and role != "Employee":
                        user_doc.remove_roles(role)

                # Add new roles from role_list
                for role in role_list:
                    if role not in existing_roles:
                        user_doc.append('roles', {'role': role})

                user_doc.save()



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


