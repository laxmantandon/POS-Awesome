import frappe

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