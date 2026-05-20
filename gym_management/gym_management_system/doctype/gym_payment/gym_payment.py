# Copyright (c) 2026, Ajmal Kp and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class GymPayment(Document):

    def validate(self):

        self.calculate_paid_amount()
        self.calculate_outstanding()
        self.set_status()

    def calculate_paid_amount(self):

        total = 0

        for row in self.payment_history:
            total += row.amount

        self.paid_amount = total

    def calculate_outstanding(self):

        self.outstanding_amount = (
            self.total_amount - self.paid_amount
        )

    def set_status(self):

        if self.outstanding_amount <= 0:
            self.status = "Paid"

        elif self.paid_amount > 0:
            self.status = "Partially Paid"

        else:
            self.status = "Unpaid"

        if (
            self.due_date
            and self.due_date < nowdate()
            and self.outstanding_amount > 0
        ):
            self.status = "Overdue"
