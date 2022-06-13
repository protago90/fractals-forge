from fastapi import Depends, FastAPI, Request, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastforge.conf import Config
from fastforge.service.rest.auth import AuthCtrl
from fastforge.service.rest.base import DBClient, Token


PUB_TAG = 'static'
PUB_DIR = 'fastforge/service/public'
PUB_TMPL = Jinja2Templates(directory=f'{PUB_DIR}/tmpl')


auth_scheme = OAuth2PasswordBearer(tokenUrl='login')
auth_ctrl = AuthCtrl(**Config().jwtoken.dict())

db_cli = DBClient()


from fastforge.service.rest.user import user_api  # dependency hell


app = FastAPI()
app.include_router(user_api)
app.mount(f'/{PUB_TAG}', StaticFiles(directory=PUB_DIR), name=PUB_TAG)


@app.post('/login', response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = db_cli.read_user(form.username)
    auth_ctrl.assert_crypto(form.password, user.password)
    tk = auth_ctrl.make_token_from_payload({'sub': user.username})
    return Token(access_token=tk, token_type='bearer')

@app.get("/")
def home(request: Request) -> Response:
    return PUB_TMPL.TemplateResponse('home.html', context={'request': request})
