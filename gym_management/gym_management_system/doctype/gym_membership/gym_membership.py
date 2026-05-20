# Copyright (c) 2026, Ajmal Kp and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days, date_diff, nowdate

class GymMembership(Document):

    def validate(self):

        self.set_end_date()
        self.calculate_remaining_days()
        self.validate_freeze_days()

    def set_end_date(self):

        if not self.end_date:

            duration = frappe.db.get_value(
                "Membership Plan",
                self.membership_plan,
                "duration_days"
            )

            self.end_date = add_days(
                self.start_date,
                duration
            )

    def calculate_remaining_days(self):

        self.remaining_days = date_diff(
            self.end_date,
            nowdate()
        )

        if self.remaining_days <= 0:
            self.status = "Expired"

    def validate_freeze_days(self):

        total_freeze_days = 0

        for row in self.freeze_history:

            freeze_days = date_diff(
                row.freeze_end_date,
                row.freeze_start_date
            )

            row.freeze_days = freeze_days

            total_freeze_days += freeze_days

        allowed_days = frappe.db.get_value(
            "Membership Plan",
            self.membership_plan,
            "allowed_freeze_days"
        )

        if total_freeze_days > allowed_days:

            frappe.throw(
                f"Allowed freeze days exceeded. Max: {allowed_days}"
            )

        self.end_date = add_days(
            self.end_date,
            total_freeze_days
        )