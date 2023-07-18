from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactsModel
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactsResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    contacts= await repository_contacts.get_contact(skip, limit, current_user, db)
    return contacts
    """
    Rout and function to get a list of contacts for specific user.

    :param skip: The number of notes to skip.
    :type skip: int
    :param limit: The maximum number of notes to return.
    :type limit: int
    :param db: The database session.
    :type db: Session
    :return: List of contacts
    :rtype: contacts 
    """

@router.get("/{contact_id}", response_model=ContactsResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contact
    """
    Rout and function to get a specific contact for specific user.

    :param contact_id: The id for specific contact.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :return: List of contacts
    :rtype: contact
    """

@router.post("/", response_model=ContactsResponse, status_code=status.HTTP_201_CREATED, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))]))
async def create_contact(body: ContactsModel, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, current_user, db)
    """
    Rout and function to create a contact.
    
    :param body: The data for contact to create.
    :type body: ContactsModel
    :param db: The database session.
    :type db: Session
    :return: Contact creation in repository.
    :rtype: repository contact
    """

@router.put("/{contact_id}", response_model=ContactsResponse)
async def update_contact(body: ContactsModel, contact_id: int, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contact
    """
    Rout and function to update a specific contact for specific user.

    :param body: The data for contact to update.
    :type body: ContactsModel
    :param contact_id: The id for specific contact.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :return: Updated contact.
    :rtype: contact
    """

@router.delete("/{contact_id}", response_model=ContactsResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contact
    """
    Rout and function to remove a specific contact.

    :param contact_id: The id for specific contact.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :return: Deleted contact.
    :rtype: contact
    """

