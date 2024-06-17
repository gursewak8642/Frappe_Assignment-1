# Copyright (c) 2024, Gursewak Singh and contributors
# For license information, please see license.txt

import re
import frappe
from frappe import _
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import flt, cint



class Student(Document):

	def validate(self):
		self.full_name = f"{self.first_name} {self.middle_name or '' } {self.last_name}" 
		 #combines the full name and save it to first name, middle name and last name 
		# frappe.msgprint(self.link_address)

		if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
			frappe.throw("Invalid email address format. Please enter a valid email address.")# Email Check if valid or not
		
		# self.joining_date(datetime.today().date)
		self.validate_date_of_birth()
	


	@frappe.whitelist(allow_guest=True)
	def get_instructors(doctype, txt, searchfield, start, page_len, filters):
		return frappe.db.get_list('Employee', 
			filters={'designation': 'Instructor'}, 
			fields=['name', 'employee_name'], 
			as_list=True)



	
	def validate_date_of_birth(self):
		if self.date_of_birth:
			dob = datetime.strptime(self.date_of_birth, '%Y-%m-%d').date()
			today = datetime.today().date()
			max_allowed_date = datetime.strptime('2023-12-31','%Y-%m-%d').date()
			if dob > max_allowed_date:
				frappe.throw("DAte of Birth cannot be greater than 2023-12-31")
			if dob > today:
				frappe.throw("Date of Birth cannot be in the future.")


	@frappe.whitelist()
	def create_student(doc):
		try:
			student = frappe.new_doc('Student')
			student.update(doc)
			student.insert()
			frappe.db.commit()
			return student.name
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), 'API Error')
			frappe.throw(_('Failed to create student: {0}').format(str(e)))

	@frappe.whitelist()
	def get_student(name):
		return frappe.get_doc('Student', name)

	@frappe.whitelist()
	def update_student(doc):
		try:
			student = frappe.get_doc('Student', doc.get('name'))
			student.update(doc)
			student.save()
			frappe.db.commit()
			return student.name
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), 'API Error')
			frappe.throw(_('Failed to update student: {0}').format(str(e)))

	@frappe.whitelist()
	def delete_student(name):
		try:
			student = frappe.get_doc('Student', name)
			student.delete()
			frappe.db.commit()
			return _('Student {0} deleted successfully.').format(name)
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), 'API Error')
			frappe.throw(_('Failed to delete student: {0}').format(str(e)))





