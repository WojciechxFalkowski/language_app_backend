from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.modules.user import models as user_modules, controller as user_controller
from src.modules.set import models as set_modeles, controller as set_controller
from src.modules.term import models as term_models, controller as term_controller
from src.modules.settings import models as settings_models, controller as settings_controller

from src.modules.sql_app.database import engine
import sqlalchemy

user_modules.Base.metadata.create_all(bind=engine)
set_modeles.Base.metadata.create_all(bind=engine)
term_models.Base.metadata.create_all(bind=engine)
settings_models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    '*'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_controller.router)
app.include_router(set_controller.router)
app.include_router(term_controller.router)
app.include_router(settings_controller.router)
