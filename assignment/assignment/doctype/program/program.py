# Copyright (c) 2024, Gursewak Singh and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from frappe.model.document import Document
from dateutil.relativedelta import relativedelta
from datetime import datetime

class Program(Document):
    def validate(self):
        if self.start_date and self.end_date:
            start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            end_date = datetime.strptime(self.end_date, '%Y-%m-%d')

            if start_date > end_date:
                frappe.throw("Start date cannot be after the end date.")

            self.duration = self.calculate_duration(start_date, end_date)
            self.credit=self.calculate_total_credits()

    def calculate_duration(self, start_date, end_date):
        delta = relativedelta(end_date, start_date)
        months = delta.years * 12 + delta.months + delta.days / 30.0
        return round(months, 2)

    def calculate_total_credits(self):
        total_credits = 0.0
        for co in self.course:
            print(co)
            credit=frappe.get_doc("Course",co).credits
            print("credit",credit)
            total_credits+=credit
        return total_credits 
