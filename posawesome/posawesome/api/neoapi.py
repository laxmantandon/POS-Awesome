import frappe
from frappe.utils import get_time, getdate, now_datetime

@frappe.whitelist()
def create_pet(
    pet_name,
    pet_breed=None,
    pet_type=None,
    color=None,
    gender=None,
    date_of_birth=None,
    weight_in_kgs=None,
    customer=None,
):
    pet = frappe.get_doc(
        {
            "doctype": "Pet",
            "pet_name": pet_name,
            "pet_breed": pet_breed,
            "pet_type": pet_type,
            "color": color,
            "gender": gender,
            "date_of_birth": date_of_birth,
            "weight_in_kgs": weight_in_kgs,
            "customer": customer,
        }
    )
    pet.save(ignore_permissions=True)
    return pet

@frappe.whitelist()
def get_groomer_services(groomer):
    groomer = frappe.get_doc("Neo Groomer", groomer)
    return groomer.services

@frappe.whitelist()
def get_breeds():
    return frappe.db.get_all("Pet Breed")

@frappe.whitelist()
def get_territory():
    return frappe.db.get_all("Territory")


@frappe.whitelist()
def get_time_slot(groomer, booking_date):
    slots = []
    doc = frappe.get_doc("Neo Groomer", groomer)
    for ts in doc.time_slot:
        tsb = frappe.db.count("Neo Time Slot Booking", filters={"hair_stylist": groomer, "booking_date": booking_date, "start_time": ts.start_time, "end_time": ts.end_time, "booking_for": "Dog Salon"})

        if tsb >= 1:
            pass #ts.availability = "Booked"
        else:
            current_date = getdate(now_datetime())
            current_time = get_time(now_datetime())
            start_time = get_time(ts.start_time)
            if start_time > current_time and ts.day == current_date.strftime('%A'):
                slot = { "slot_id": f"{ts.start_time} {ts.end_time}"}
                slots.append(slot)
    return slots