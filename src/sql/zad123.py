# ĆWICZENIE 1,2,3
# Stwórz dwie tabele:
# 1.Experiment z kolumnami: id: int, title: string, created_at: datetime, type: int, finished: boolean(domyślnie False).
# 2.DataPointz kolumnami:id: int, real_value: float, target_value: float.
#
# Stwórz wszystkie zdefiniowane tabele wraz z plikiem bazy danych

# Rozszerz program z poprzednich ćwiczeń by:
# 1. Dodał 2 wiersze do tabeli Experiments.
# 2. Dodał 10 wierszy do tabeli DataPoints.
# 3. Pobrał dodane przed chwilą dane i wyświetlił informację o nich.
# 4. Zaktualizował wszystkie wierszy Experimentspoprzez ustawienie finishedna True.
# 5. Usunął wszystkie wiersze z obu tabel.

from sqlalchemy import create_engine, Integer, Column,String, DateTime, Boolean, Float, select, update, delete
from sqlalchemy.orm import declarative_base, Session
import datetime
import random

engine = create_engine("sqlite:///zad1.db",echo=True)
print(engine.connect())

Base = declarative_base()

class Experiment(Base):
    __tablename__ = 'experiment'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    created_at = Column(DateTime,default=datetime.datetime.now())
    type = Column(Integer)
    finished= Column(Boolean, default=False)

class DataPoint(Base):
    __tablename__ = 'data_point'

    id = Column(Integer, primary_key=True)
    real_value = Column(Float)
    target_value = Column(Float)

Base.metadata.create_all(engine)


with Session(engine) as session:
    # 1. Utworzenie Exeriment
    experiment1 = Experiment(name="experiment1", type=1)
    session.add(experiment1)
    experiment2 = Experiment(name="experiment2", type=2)
    session.add(experiment2)
    session.commit()

    # 2. Utworzenie 10 losowych DataPoint
    data_point = [DataPoint(real_value=random.random(), target_value=random.random()) for _ in range(10)]
    session.add_all(data_point)
    session.commit()

    # 3. Pobranie i wypisanie wszystkich danych
    experiments = session.scalars(select(Experiment)).all()
    for experiment in experiments:
        print(f"{experiment.id} {experiment.name} {experiment.finished}")
        print("\n")

    dataset = session.scalars(select(DataPoint)).all()
    for dataset in dataset:
        print(f"{dataset.id} {dataset.real_value} {dataset.target_value}")

    # 4. Udpade Experiment
    stmt = update(Experiment).values(finished=True)
    session.execute(stmt)
    session.commit()

    experiments = session.scalars(select(Experiment)).all()
    for experiment in experiments:
        print(f"{experiment.id} {experiment.name} {experiment.finished}")
        print("\n")

    # 5. Usuniecie danych
    delete_statement = delete(Experiment)
    session.execute(delete_statement)
    delete_data_point = delete(DataPoint)
    session.execute(delete_data_point)
    session.commit()