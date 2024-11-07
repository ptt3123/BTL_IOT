# db connect here
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, DateTime, Float, Text


DATABASE_URL = "mysql+mysqlconnector://root:taip7547@localhost/iot_db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(metadata=MetaData())


class Data(Base):
    __tablename__ = "data"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    tem = Column("tem", Float, nullable=False)
    hum = Column("hum", Float, nullable=False)
    lig = Column("lig", Float, nullable=False)
    ws = Column("ws", Integer, nullable=False)
    tim = Column("tim", DateTime, default=datetime.now)


class Action(Base):
    __tablename__ = "action"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    hw = Column("hw", String(5), nullable=False)
    act = Column("act", String(5), nullable=False)
    tim = Column("tim", DateTime, default=datetime.now)