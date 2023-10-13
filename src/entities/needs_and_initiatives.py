from dataclasses import dataclass


@dataclass
class Organization:
    id: str
    timestamp: str
    org_name: str
    contact_name: str
    phone_number: str
    city: str
    address: str
    email: str
    donation_type: str
    org_size: str
    year_of_founding: int
    role: str
    org_logo: str
    org_description: str
    resource_needs: str
    additional_info: str
    our_contact_name: str
    notes_for_donation: str
    our_contact_phone_number: str
    ask_or_give: str