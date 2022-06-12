from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from fastforge.service.main import auth_ctrl, auth_scheme, db_cli
from fastforge.service.rest.base import User
from fastforge.worker import create_task, read_tasks_info


user_api = APIRouter(prefix="/user", tags=['user'])


async def get_current_user(token: str = Depends(auth_scheme)) -> User:
    username = auth_ctrl.get_payload_from_token(token).get('sub')
    if username is None:
        db_cli.raise_access_exc('Failed ID: invalid payload.')
    return db_cli.read_user(username)


@user_api.get('', response_model=User)
async def get_user(user: User = Depends(get_current_user)) -> User:
    return user

@user_api.post('/tasks/new', response_model=User, status_code=201)
async def make_task(user: User = Depends(get_current_user)) -> User:
    task = create_task.delay()
    db_cli.update_user_tasks(user.username, task.id)
    return User(username=user.username, password='', tasks_id=[task.id])

@user_api.get('/tasks')
async def get_tasks_info(user: User = Depends(get_current_user)) -> JSONResponse:
    return JSONResponse(read_tasks_info(user.tasks_id))
