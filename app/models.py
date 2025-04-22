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
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(320), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(16), nullable=False)
    password: Mapped[str] = mapped_column(db.String(100), nullable=False)

     # One-to-Many relationship with Service_Ticket
    servicetickets: Mapped[List["ServiceTicket"]] = db.relationship(back_populates="customers", cascade="all, delete")





class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(15))
    salary: Mapped[float] = mapped_column(db.Float(), nullable=False)


    # Many-to-Many relationship with Service_Ticket
    servicetickets: Mapped[List["ServiceTicket"]] = db.relationship(
        secondary="service_mechanics",  
        back_populates="mechanics"
    )


class ServiceMechanic(Base):
    __tablename__ = 'service_mechanics'

    ticket_id: Mapped[int] = mapped_column(db.ForeignKey('servicetickets.id'),primary_key=True)
    mechanic_id: Mapped[int] = mapped_column(db.ForeignKey('mechanics.id'), primary_key=True)


class ServiceTicket(Base):
    __tablename__ = 'servicetickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(db.String(17), nullable=False)
    service_date: Mapped[date] = mapped_column(db.Date, nullable=False)
    service_description: Mapped[str] = mapped_column(db.String(255))
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'), nullable=False)

    #Many to One relationship with Customer
    customers: Mapped["Customer"] = db.relationship( back_populates="servicetickets")

    # Many-to-Many relationship with Mechanic
    mechanics: Mapped[List["Mechanic"]] = db.relationship(secondary="service_mechanics", back_populates="servicetickets", cascade="all, delete")

    #Many to many relationship with Inventory
    inventory: Mapped[List["Inventory"]] = db.relationship(
        secondary="service_inventory",
        back_populates="servicetickets"
    )

class Inventory(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable = False)
    price: Mapped[float] = mapped_column(db.Float, nullable = False)


    #Many to Many relaionship with ServiceTicket
    servicetickets: Mapped[List["ServiceTicket"]] = db.relationship(
        secondary="service_inventory",
        back_populates="inventory"
    )


Service_Inventory = db.Table(
    'service_inventory', Base.metadata,
    db.Column('serviceticket_id', db.ForeignKey('servicetickets.id')),
    db.Column('inventory_id', db.ForeignKey('inventory.id'))
)