from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from typing import List


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(15), nullable=False)



class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(15))
    salary: Mapped[float] = mapped_column(db.Float)

    # Many-to-Many relationship with Service_Ticket
    service_tickets: Mapped[List["Service_Ticket"]] = relationship(
        "Service_Ticket",
        secondary="service_mechanics",  # Association table name
        back_populates="mechanics"
    )


class Service_Mechanic(Base):
    __tablename__ = 'service_mechanics'

    ticket_id: Mapped[int] = mapped_column(db.ForeignKey('servicetickets.id'),primary_key=True)
    mechanic_id: Mapped[int] = mapped_column(db.ForeignKey('mechanics.id'), primary_key=True)


class Service_Ticket(Base):
    __tablename__ = 'servicetickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(db.String(20), unique=True, nullable=False)
    service_date: Mapped[date] = mapped_column(db.Date, nullable=False)
    service_description: Mapped[str] = mapped_column(db.String(255))
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))

    # Many-to-Many relationship with Mechanic
    mechanics: Mapped[List["Mechanic"]] = db.relationship(
        "Mechanic",
        secondary="service_mechanics",  # Association table name
        back_populates="service_tickets", cascade="all, delete"
    )
