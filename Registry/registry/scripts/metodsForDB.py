import transaction
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models.mymodel import *

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,)
from sqlalchemy import create_engine
from pyramid.threadlocal import get_current_request
from sqlalchemy.orm.exc import NoResultFound
Base = declarative_base()
engine = create_engine('sqlite:///Registry.sqlite')
Base.metadata.bind = engine

def getUser(login, passw):
    session_factory = get_session_factory(engine)
    dbsession = get_tm_session(session_factory, transaction.manager)
    query = dbsession.query(Patient).filter((Patient.policy==login) & (Patient.password==passw))
    try:
        u=query.one()
        return u
    except NoResultFound:
        return None

def getSectionNumber(address):
    session_factory = get_session_factory(engine)
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        section = dbsession.query(Address.section_number).filter(Address.address==address).first()
    return section

def getDataPatient(policy):
    session_factory = get_session_factory(engine)
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        dataPatient = dbsession.query(Patient.firstName, Patient.middleName, Patient.lastName, Patient.policy, Patient.sex, Patient.phone,
                                  Patient.address).filter(Patient.policy == policy).first()
    return dataPatient

def getDiagnose(id):
    session_factory = get_session_factory(engine)
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        diagnose = dbsession.query(Diagnose.name).filter(Diagnose.id == id).first()[0]
    return diagnose

def getSchedule():
    session_factory = get_session_factory(engine)
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        schedule = dbsession.query(ScheduleOfReception.id, ScheduleOfReception.doctor, ScheduleOfReception.date, ScheduleOfReception.time).\
            filter(ScheduleOfReception.status == 0).all()
    return schedule

def getSection(passport):
    session_factory = get_session_factory(engine)
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        section = dbsession.query(Doctor.section_number).filter(Doctor.passport == passport).first()[0]
        # print(songs[0].directPath)
    return section

def getDoctorName(passport):
    session_factory = get_session_factory(engine)
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        doctor = dbsession.query(Doctor.firstName, Doctor.middleName, Doctor.lastName).filter(Doctor.passport == passport).first()
    return doctor

def getSpecialty(passport):
    session_factory = get_session_factory(engine)
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        specialtyId = dbsession.query(Doctor.specialty_id).filter(Doctor.passport == passport).first()
        specialty = dbsession.query(Specialty.name).filter(Specialty.id == specialtyId[0]).first()[0]
    return specialty

def getHistory(policy):
    session_factory = get_session_factory(engine)
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        history = dbsession.query(History.id, History.date, History.diagnose, History.sickLeaveUntil, History.comment, History.doctor).filter(History.patient == policy).all()
        print(history)
    return history

def getActiveHistory(policy):
    session_factory = get_session_factory(engine)
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        acthistory = dbsession.query(ActiveHistory.id, ActiveHistory.date, ActiveHistory.doctor).filter(ActiveHistory.patient == policy).all()
        print(acthistory)
    return acthistory

def makeAnAppointment(id, policy):
    from sqlalchemy import update
    from sqlalchemy import insert
    session_factory = get_session_factory(engine)
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        update_stmt=update(ScheduleOfReception).where(ScheduleOfReception.id == id).values(status=1, patient = policy )
        con = engine.connect()
        res = con.execute(update_stmt)
        schedule = dbsession.query(ScheduleOfReception.doctor, ScheduleOfReception.date,
                                   ScheduleOfReception.time, ScheduleOfReception.status, ScheduleOfReception.patient).filter(ScheduleOfReception.id == id).first()
        insert_stmt = insert(ActiveHistory).values(doctor=schedule.doctor, date=schedule.date, patient=policy)
        con = engine.connect()
        res = con.execute(insert_stmt)
        act = dbsession.query(ActiveHistory.id, ActiveHistory.date,ActiveHistory.doctor).first()
    return {}