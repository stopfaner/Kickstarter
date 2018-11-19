import uuid
import datetime
from sqlalchemy.engine import Connection
from service_api.models import Base
from sqlalchemy import Column, String, inspect, select
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    first_name = Column(String)

    last_name = Column(String)

    email = Column(String, unique=True)

    password = Column(String)

    timestamp = Column(String)

    @classmethod
    def _prepare_item(cls, data):
        if not data.get("timestamp"):
            data["timestamp"] = datetime.datetime.utcnow().isoformat()
        mapper = inspect(cls)
        columns = mapper.attrs.keys()
        # filter out keys that not in DB schema
        return {k: v for k, v in data.items() if k in columns}

    @classmethod
    async def insert(cls, conn: Connection, data: dict):

        item = cls._prepare_item(data)
        query = cls.__table__.insert().values(**item)
        await conn.execute(query)

        query = cls.__table__.select().where(User.email == item.get("email"))
        result = await conn.execute(query)
        row = await result.fetchone()

        if row:
            cur = dict(row)
            cur["id"] = str(cur["id"])
            cur.pop("password")
            return cur
        else:
            return None

    @classmethod
    async def login(cls, conn: Connection, data: dict):

        query = cls.__table__.select().where((User.email == data["email"]) & (User.password == data["password"]))

        result = await conn.execute(query)
        row = await result.fetchone()

        if row:
            return dict(row)

        return None

    @classmethod
    async def select(cls, conn: Connection, user_id: str):
        query = cls.__table__.select().where((User.id == user_id))

        result = await conn.execute(query)
        row = await result.fetchone()

        if row:
            return dict(row)

        return None
