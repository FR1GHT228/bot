from sqlalchemy import String, LargeBinary, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[str] = mapped_column(String(50))
    gender: Mapped[str] = mapped_column(String(50))
    diseases: Mapped[str] = mapped_column(String(150))
    psy_gender: Mapped[str] = mapped_column(String(25))
    first_time: Mapped[str] = mapped_column(String(200))
    info: Mapped[str] = mapped_column(String(250))
    issue: Mapped[str] = mapped_column(String(250))
    experience: Mapped[str] = mapped_column(String(250))
    number: Mapped[str] = mapped_column(String(100))
    psy_id: Mapped[str] = mapped_column(String(100))


class Psychologist(Base):
    __tablename__ = 'psychologist'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[str] = mapped_column(String(100))
    psy_name: Mapped[str] = mapped_column(String(100))
    psy_age: Mapped[str] = mapped_column(String(100))
    psy_gender: Mapped[str] = mapped_column(String(100))
    psy_graduation: Mapped[str] = mapped_column(String(100))
    psy_language: Mapped[str] = mapped_column(String(100))
    psy_how_find: Mapped[str] = mapped_column(String(100))
    psy_info: Mapped[str] = mapped_column(String(250))
    psy_how_work: Mapped[str] = mapped_column(String(250))
#    psy_diploma: Mapped[bytes] = mapped_column(LargeBinary)
    psy_number: Mapped[str] = mapped_column(String(100))

