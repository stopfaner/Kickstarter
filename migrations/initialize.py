import asyncio
from sqlalchemy import create_engine

from service_api.models.user import User
from service_api.models.petition import Petition
from service_api.models import Base
from config import (DATABASE_USER as user, DATABASE_PASSWORD as password, DATABASE_HOST as host,
                    DATABASE_PORT as port, DATABASE_NAME as db)


engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
Base.metadata.create_all(engine)

