from pydantic import BaseModel, BaseSettings, Field


class JWToken(BaseSettings):
    exp_time: int = Field(30, env='JWT_EXP_TIME')
    hasher: str = Field('HS256', env='JWT_HASHER')
    secret: str = Field('The secret of life? 42!', env='JWT_SECRET')

class Celery(BaseSettings):
    broker_url: str = Field('redis://localhost:6379', env='CELERY_BROKER_URL')
    result_url: str = Field('redis://localhost:6379', env='CELERY_RES_URL')


class Config(BaseModel):
    jwtoken: JWToken = JWToken()
    celery: Celery = Celery()
