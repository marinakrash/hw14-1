from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contacts, User
from src.schemas import ContactsModel, ContactsResponse


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contacts]:
    return db.query(Contacts).filter(Contacts.user_id == user.id).offset(skip).limit(limit).all()
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param skip: The number of notes to skip.
    :type skip: int
    :param limit: The maximum number of notes to return.
    :type limit: int
    :param user: The user to retrieve notes for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contacts]
    """

async def get_contact(contact_id: int, user: User, db: Session) -> Contacts:
    return db.query(Contacts).filter(and_(Contacts.id == contact_id, Contacts.user_id == user.id)).first()
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param note_id: The ID of the note to retrieve.
    :type note_id: int
    :param user: The user to retrieve the note for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The note with the specified ID, or None if it does not exist.
    :rtype: Contacts | None
    """

async def create_contact(body: ContactsModel, user: User, db: Session) -> Contacts:
    contact = Contacts(name=body.name, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact
    """
    Creates a new note for a specific user.

    :param body: The data for the note to create.
    :type body: ContactsModel
    :param user: The user to create the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contacts
    """

async def update_contact(contact_id: int, body: ContactsModel, user: User, db: Session) -> Contacts | None:
    contact = db.query(Contacts).filter(and_(Contacts.id == contact_id, Contacts.user_id == user.id)).first()
    if contact:
        contact.name = body.name
        db.commit()
    return contact
    """
    Updates a single contact with the specified ID for a specific user.

    :param note_id: The ID of the note to update.
    :type note_id: int
    :param body: The updated data for the note.
    :type body: ContactsUpdate
    :param user: The user to update the note for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: Contacts | None
    """

async def remove_contact(contact_id: int, user: User, db: Session) -> Contacts | None:
    contact = db.query(Contacts).filter(and_(Contacts.id == contact_id, Contacts.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
    """
    Removes a single contact with the specified ID for a specific user.

    :param note_id: The ID of the note to remove.
    :type note_id: int
    :param user: The user to remove the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed note, or None if it does not exist.
    :rtype: Contacts | None
    """