from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    BigInteger, Boolean, Date, Time, Float, ForeignKey
)

from .meta import Base


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)


Index('my_index', MyModel.name, unique=True, mysql_length=255)

class Specialty(Base):
    __tablename__ = 'specialties'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)


class Section(Base):
    __tablename__ = 'sections'
    number = Column(Integer, primary_key=True)


class Diagnose(Base):
    __tablename__ = 'diagnoses'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)


class Cabinet(Base):
    __tablename__ = 'cabinets'
    number = Column(Integer, primary_key=True)


class Doctor(Base):
	__tablename__ = 'doctors'
	passport = Column(Integer, primary_key=True)
	firstName = Column(Text, nullable=False, unique=False)
	middleName = Column(Text, nullable=False, unique=False)
	lastName = Column(Text, nullable=False, unique=False)
	sex = Column(Integer, nullable=False, unique=False)
	birthDay = Column(Date, nullable=False, unique=False)
	specialty_id = Column(Integer, ForeignKey("specialties.id"), nullable=False)
	section_number = Column(Integer, ForeignKey("sections.number"), nullable=True)
	cabinet = Column(Integer, ForeignKey("cabinets.number"), nullable=False)


class Address(Base):
    __tablename__ = 'addresses'
    address = Column(Text, primary_key=True)
    section_number = Column(Integer, ForeignKey("sections.number"), nullable=False)


class Patient(Base):
	__tablename__ = 'patients'
	policy = Column(Integer, primary_key=True)
	password = Column(Text, nullable=False)
	firstName = Column(Text, nullable=False, unique=False)
	middleName = Column(Text, nullable=False, unique=False)
	lastName = Column(Text, nullable=False, unique=False)
	sex = Column(Integer, nullable=False, unique=False)
	birthDay = Column(Date, nullable=False, unique=False)
	phone = Column(Integer, nullable=True, unique=False)
	address = Column(Integer, ForeignKey("addresses.address"), nullable=False)


class ScheduleOfReception(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)
    doctor = Column(Integer, ForeignKey("doctors.passport"), nullable=False)
    date = Column(Date, nullable=False, unique=False)
    time = Column(Time, nullable=False, unique=False)
    status = Column(Integer, nullable=False, unique=False)
    patient = Column(Integer, ForeignKey("patients.policy"), nullable=True)


class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, unique=False)
    patient = Column(Integer, ForeignKey("patients.policy"), nullable=False)
    doctor = Column(Integer, ForeignKey("doctors.passport"), nullable=False)
    diagnose = Column(Integer, ForeignKey("diagnoses.id"), nullable=False)
    sickLeaveUntil = Column(Date, nullable=True, unique=False)
    comment = Column(Text, nullable=True, unique=False)

class ActiveHistory(Base):
    __tablename__ = 'activeHistory'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, unique=False)
    patient = Column(Integer, ForeignKey("patients.policy"), nullable=False)
    doctor = Column(Integer, ForeignKey("doctors.passport"), nullable=False)