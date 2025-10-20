# CWICZENIE 4
# Dodaj relację jeden do wielu tak, by jeden Experimentposiadał wiele DataPoint’ów.

from sqlalchemy import create_engine, Integer, Column,String, DateTime, Boolean, Float, select, update, delete,ForeignKey
from sqlalchemy.orm import declarative_base, Session, relationship
import datetime
import random

engine = create_engine("sqlite:///zad4.db",echo=True)
print(engine.connect())

Base = declarative_base()

class Experiment(Base):
    __tablename__ = 'experiment'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    created_at = Column(DateTime,default=datetime.datetime.now())
    type = Column(Integer)
    finished= Column(Boolean, default=False)
    data_points = relationship("DataPoint", back_populates="experiment")

class DataPoint(Base):
    __tablename__ = 'data_point'

    id = Column(Integer, primary_key=True)
    real_value = Column(Float)
    target_value = Column(Float)
    experiment_id = Column(Integer, ForeignKey('experiment.id'))
    experiment = relationship("Experiment", back_populates="data_points")

Base.metadata.create_all(engine)


with Session(engine) as session:
    # 1. Utworzenie Exeriment i datapoints
    experiment1 = Experiment(name="experiment1", type=1)
    data_point = [DataPoint(real_value=random.random(), target_value=random.random(),experiment=experiment1) for _ in range(10)]
    session.add(experiment1)
    session.commit()

