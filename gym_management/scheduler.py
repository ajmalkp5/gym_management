import frappe
from frappe.utils import today, add_days, getdate


def update_membership_status():

    memberships = frappe.get_all(
        "Gym Membership",
        filters={"status": ["in", ["Active", "Frozen"]]},
        fields=["name", "end_date"]
    )

    for m in memberships:

        if not m.end_date:
            continue

        if getdate(m.end_date) < getdate(today()):

            doc = frappe.get_doc("Gym Membership", m.name)
            doc.status = "Expired"
            doc.save(ignore_permissions=True)

    frappe.db.commit()


def expiry_notifications():

    today_date = today()

    expiring_soon = frappe.get_all(
        "Gym Membership",
        filters={
            "status": "Active",
            "end_date": ["between", [
                today_date,
                add_days(today_date, 7)
            ]]
        },
        fields=["member", "end_date"]
    )

    for m in expiring_soon:

        email = frappe.db.get_value("Gym Member", m.member, "email")

        if not email:
            continue

        frappe.get_doc({
            "doctype": "Notification Log",
            "subject": "Membership Expiry Alert",
            "for_user": email,
            "type": "Alert",
            "email_content": f"Your membership expires on {m.end_date}"
        }).insert(ignore_permissions=True)

    frappe.db.commit()


def update_dashboard_stats():

    total_members = frappe.db.count("Gym Member")

    active_memberships = frappe.db.count(
        "Gym Membership",
        {"status": "Active"}
    )

    expired_memberships = frappe.db.count(
        "Gym Membership",
        {"status": "Expired"}
    )

    frappe.cache().set_value("gym_dashboard_stats", {
        "total_members": total_members,
        "active_memberships": active_memberships,
        "expired_memberships": expired_memberships
    })

    frappe.db.commit()


# # 4. Freeze Period Validation
# def validate_freeze_period():

#     frozen_memberships = frappe.get_all(
#         "Gym Membership",
#         filters={"status": "Frozen"},
#         fields=["name", "freeze_end_date"]
#     )

#     for m in frozen_memberships:

#         if not m.freeze_end_date:
#             continue

#         if getdate(m.freeze_end_date) <= getdate(today()):

#             doc = frappe.get_doc("Gym Membership", m.name)
#             doc.status = "Active"
#             doc.save(ignore_permissions=True)

#     frappe.db.commit()