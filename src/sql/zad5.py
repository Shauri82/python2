# Zainstaluj i zainicjuj Alembic w programie z poprzednich ćwiczeń.
# • Wygeneruj pierwszą migrację i zaaplikuj ją na bazie danych.
# • Dodaj nową tabelę Subject z kolumnami: id: int, gdpr_accepted: bool(domyślnie na False).
# • Stwórz relację wiele-do-wielu pomiędzy Subject i Experiment.
# • Wygeneruj nową migrację i zaaplikuj ją na bazie danych.

from sqlalchemy import create_engine, Integer, Column,String, DateTime, Boolean, Float, select, update, delete,ForeignKey, Table
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import declarative_base, Session, relationship
import datetime
import random


engine = create_engine("sqlite:///baza5.db",echo=True)
print(engine.connect())

Base = declarative_base()
# class Experiment(Base):
#     __tablename__ = 'experiment'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(30))
#     created_at = Column(DateTime,default=datetime.datetime.now())
#     type = Column(Integer)
#     finished= Column(Boolean, default=False)
#     data_points = relationship("DataPoint", back_populates="experiment")
#
# class DataPoint(Base):
#     __tablename__ = 'data_point'
#
#     id = Column(Integer, primary_key=True)
#     real_value = Column(Float)
#     target_value = Column(Float)
#     experiment_id = Column(Integer, ForeignKey('experiment.id'))
#     experiment = relationship("Experiment", back_populates="data_points")

# NOWA RELACJA WIELE-DO-WIELU

association_table= Table(
    'experiments_subjects',
    Base.metadata,
    Column("experiment_id",ForeignKey('experiment.id')),
    Column("subject_id",ForeignKey('subject.id'))
                         )
class Experiment(Base):
    __tablename__ = 'experiment'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    created_at = Column(DateTime,default=datetime.datetime.now())
    type = Column(Integer)
    finished= Column(Boolean, default=False)
    data_points = relationship("DataPoint", back_populates="experiment")
    subject = relationship("Subject", secondary =association_table,back_populates="experiment")

class DataPoint(Base):
    __tablename__ = 'data_point'

    id = Column(Integer, primary_key=True)
    real_value = Column(Float)
    target_value = Column(Float)
    experiment_id = Column(Integer, ForeignKey('experiment.id'))
    experiment = relationship("Experiment", back_populates="data_points")

class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    gdpr_accepted = Column(Boolean,default=False)
    experiment = relationship("Experiment", secondary=association_table, back_populates="subject")


# with Session(engine) as session:
#     # 1. Utworzenie Exeriment i subjects
#     experiment1 = Experiment(name="experiment1", type=1)
#     data_point = [DataPoint(real_value=random.random(), target_value=random.random(),experiment=experiment1) for _ in range(10)]
#     subject1 = Subject(gdpr_accepted=True)
#     subject2 = Subject(gdpr_accepted=False)
#     experiment1.subject.append(subject1)
#     experiment1.subject.append(subject2)
#     session.add(experiment1)
#     session.commit()
