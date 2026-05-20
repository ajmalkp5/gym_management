# Copyright (c) 2026, Ajmal Kp and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import time_diff_in_hours

class TrainingSchedule(Document):

    def validate(self):

        self.calculate_duration()

    def calculate_duration(self):

        if self.start_time and self.end_time:

            self.duration = time_diff_in_hours(
                self.end_time,
                self.start_time
            )
