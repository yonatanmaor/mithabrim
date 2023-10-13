from common import csv_utils, uuid_generator
import os
from tqdm import tqdm

from db import db_access
from entities.needs_and_initiatives import Organization


def _create_organization_entity(data_dict: dict):
    try:
        year_of_founding = int(data_dict['שנת הקמה'])
    except ValueError:
        year_of_founding = -1
    data = Organization(
        id=str(uuid_generator.generate_uuid()),
        timestamp=data_dict['Timestamp'],
        org_name=data_dict['שם הארגון'],
        contact_name=data_dict['איש קשר'],
        phone_number=data_dict['טלפון'],
        city=data_dict['עיר'],
        address=data_dict['כתובת'],
        email=data_dict['אימייל'],
        donation_type=data_dict['סוג תרומה'],
        org_size=data_dict['גודל הארגון'],
        year_of_founding=year_of_founding,
        role=data_dict['תפקיד'],
        org_logo=data_dict['לוגו של הארגון'],
        org_description=data_dict['כמה מילים על הארגון'],
        resource_needs=data_dict['משאבים נדרשים להמשך פעילות'],
        additional_info=data_dict['פרטים נוספים'],
        our_contact_name=data_dict['שם המתנדב מטעמנו (מתחברים)'],
        notes_for_donation=data_dict['הערות לתרומה'],
        our_contact_phone_number=data_dict['טלפון המתנדב מטעמנו (מתחברים)'],
        ask_or_give=data_dict['מבקשים/מציעים תרומה'],
    )
    return data


def migrate(csv_file_path: str):
    rows = csv_utils.load_csv(csv_file_path=csv_file_path)
    for row in tqdm(rows):
        organization_entity = _create_organization_entity(row)
        for donation_type in organization_entity.donation_type.split(","):
            donation_type = donation_type.strip()

        db_access.insert_organzation(entity=organization_entity)



if __name__ == '__main__':
    file_path = os.path.expanduser('~/Downloads/mithabrim_sheet.csv')
    migrate(file_path)