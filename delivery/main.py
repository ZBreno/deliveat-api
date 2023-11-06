from fastapi import FastAPI, Depends
from api import ticket
from configuration.config import FacultySettings, ServerSettings

app = FastAPI()
app.include_router(ticket.router)


def build_config():
    return FacultySettings()


def fetch_config():
    return ServerSettings()


@app.get('/index')
def index_faculty(config: FacultySettings = Depends(build_config), fconfig: ServerSettings = Depends(fetch_config)):
    return {
        'project_name': config.application,
        'webmaster': config.webmaster,
        'created': config.created,
        'production_server': fconfig.production_server,
        'prod_port': fconfig.prod_port
    }


class ServerSettings(BaseSettings):
    production_server: str
    prod_port: int
    development_server: str
    dev_port: int

    class Config:
        env_file = os.getcwd() + '/configuration/erp_settings.properties'
