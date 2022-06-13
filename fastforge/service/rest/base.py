from fastapi import HTTPException, status
from pydantic import BaseModel
from typing import List, NoReturn


class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    password: str
    tasks_id: List[str] = []


# TODO: This is just a demo! Here service users/tasks db is hardcoded.
USERS_FAKE_DB = {
    'johndoe': User(
        username='johndoe',
        password='$2b$12$ug.xo7UIzJDrCPTkyjbTzOq7hlq1rnwQWTl8Se1J7ccwwXxTsWCr.',  # 'secret'
        tasks_id=[]
    ),
    'johnlemon': User(
        username='johnlemon', 
        password='$2b$12$ug.xo7UIzJDrCPTkyjbTzOq7hlq1rnwQWTl8Se1J7ccwwXxTsWCr.',  # 'secret'
        tasks_id=[]
    )
}


class DBClient():
    db_client = USERS_FAKE_DB

    def read_user(self, username: str) -> User:
        user = self.db_client.get(username)
        if user is None:
            self.raise_access_exc('Failed ID: unfamiliar user.')
        return user

    def update_user_tasks(self, username: str, uuid: str) -> None:
        user = self.db_client.get(username)
        if user is None:
            self.raise_access_exc('Failed ID: unfamiliar user.')
        user.tasks_id.append(uuid)
        self.db_client[username] = user

    @staticmethod
    def raise_access_exc(msg: str) -> NoReturn:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=msg)
