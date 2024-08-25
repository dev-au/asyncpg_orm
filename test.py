import asyncio

from database_orm.base_data import Database
from database_orm.column import Column, String, Integer
from database_orm.connector import PostgreSQL
from database_orm.models import Table

psql = PostgreSQL(
    'postgres',
    '0890',
    'localhost',
    'postgres'
)
db = Database(psql, echo=True)


class Car(Table):
    number = Column(Integer(), primary_key=True)
    name = Column(String())


cars = Car.connect_to_database(db)


async def main():
    await db.start_session()
    await cars.create_table()
    await cars.add_new(number=3, name='Lacetti Gentra G-12')
    await cars.select_all()
    await db.stop_session()


asyncio.run(main())
