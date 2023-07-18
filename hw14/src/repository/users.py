from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()
    """
    Retrieves a single contact with the specified email for a specific user.

    :param email: The email of the contact to retrieve.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified email, or None if it does not exist.
    :rtype: Contacts | None
    """

async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()
    """
    Commit a response for the validation request.

    :param email: The email of the contact to retrieve.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: Commit confirmed field for user 
    """

async def update_avatar(email, url: str, db: Session) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
    """
    Retrieves a single contact with the specified email for a specific user.

    :param email: The email of the contact to retrieve.
    :type email: str
    :param url: The url of the contact to retrieve.
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: The user with the specified email and url, or None if it does not exist
    :rtype: Users | None
    """

async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    """
    Creates a new note for a specific user.

    :param body: The data for the user to create.
    :type body: UsersModel
    :param db: The database session.
    :type db: Session
    :return: The newly created user.
    :rtype: Users
    """

async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()
    """
    Updates token for a specific user.

    :param user: The user to create the contacts for.
    :type user: User
    :param token: The token created for user.
    :type token: str
    :param db: The database session.
    :type db: Session
    """