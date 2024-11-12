from app.database.models import *
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import select
import os

class Database():
    def __init__(self):
        self.db_host = os.getenv('DB_HOST')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_name = os.getenv('DB_NAME')
        self.connect = f'mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}?charset=utf8mb4'
        self.async_engine = create_async_engine(self.connect)
        self.Session = async_sessionmaker(bind=self.async_engine, class_=AsyncSession)

    async def create_db(self):
        async with self.async_engine.begin() as connect:
            await connect.run_sync(Base.metadata.create_all)

    async def get_user(self, user_id):
        async with self.Session() as request:
            result = await request.execute(select(User).where(User.tg_id == user_id))
        return result.scalar()

    async def add_user(self, tg_id, name, age, gender, diseases, psy_gender, first_time,
                       info, issue, experience, number):
        async with self.Session() as request:
            request.add(User(
                tg_id=tg_id,
                name=name,
                age=age,
                gender=gender,
                diseases=diseases,
                psy_gender=psy_gender,
                first_time=first_time,
                info=info,
                issue=issue,
                experience=experience,
                number=number
            ))
            await request.commit()

    async def get_psy(self, user_id):
        async with self.Session() as request:
            result = await request.execute(select(Psychologist).where(Psychologist.tg_id == user_id))
        return result.scalar()

    async def add_psy(self, tg_id, psy_name, psy_age, psy_gender, psy_graduation, psy_language,
                      psy_how_find, psy_info, psy_how_work, psy_number):
        async with self.Session() as request:
            request.add(Psychologist(
                tg_id=tg_id,
                psy_name=psy_name,
                psy_age=psy_age,
                psy_gender=psy_gender,
                psy_graduation=psy_graduation,
                psy_language=psy_language,
                psy_how_find=psy_how_find,
                psy_info=psy_info,
                psy_how_work=psy_how_work,
                psy_number=psy_number
            ))
            await request.commit()



# Асинхронная функция для получения списка таблиц
