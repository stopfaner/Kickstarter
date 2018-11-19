import uuid
import datetime
from sqlalchemy.engine import Connection
from service_api.models import Base
from sqlalchemy import Column, String, inspect, Text, Integer
from sqlalchemy.dialects.postgresql import UUID


class Petition(Base):
    __tablename__ = "petition"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    timestamp = Column(String)

    user_id = Column(String)

    petition_name = Column(String)

    petition_description = Column(Text)

    petition_current_money = Column(String)

    petition_current_like = Column(Integer)

    image_url = Column(String)

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

    @classmethod
    async def select(cls, conn: Connection, petition_id: str = None):
        if petition_id:
            query = cls.__table__.select().where((Petition.id == petition_id))

            result = await conn.execute(query)
            row = await result.fetchone()

            if row:
                cur = dict(row)
                cur["id"] = str(cur["id"])
                return cur
            else:
                return None
        else:
            query = cls.__table__.select()

            result = await conn.execute(query)

            res = list()
            for row in result:
                cur = dict(row)
                cur["id"] = str(cur["id"])
                res.append(cur)

            if res:
                return res
            else:
                return None

    @classmethod
    async def update(cls, conn: Connection, petition_id: str, data: dict):
        query = cls.__table__.update().where((Petition.id == petition_id)).values(
            **data
        )

        await conn.execute(query)

    @classmethod
    async def delete(cls, conn: Connection, petition_id: str):

        query = cls.__table__.delete().where((Petition.id == petition_id))

        await conn.execute(query)

