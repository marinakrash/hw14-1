from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel, UserDb, UserResponse
from src.repository.notes import (
    get_user_by_email,
    update_avatar,
    create_user)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(email=test@com.ua)

    async def test_get_user_by_email_found(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email=self.email, db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email=self.email, db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        body = UserModel(title="test", description="test user")
        result = await create_user(body=body, email=self.email, db=self.session)
        self.assertEqual(result.title, body.title)
        self.assertEqual(result.description, body.description)


    async def test_update_avatar_found(self):
        body =UserModel(title="test", description="test user")
        user = User()
        self.session.query().filter().first.return_value = user
        self.session.commit.return_value = None
        result = await update_avatar(body=body, email=self.email, db=self.session)
        self.assertEqual(result, user)

    async def test_update_avatar_not_found(self):
        body = UserModel(title="test", description="test user")
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_avatar(body=body, email=self.email, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()