import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import MyModel


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def fillSpecialty(dbsession):
    from ..models.mymodel import Specialty
    list = []
    list.append(Specialty(name='терапевт'))
    list.append(Specialty(name='хирург'))
    list.append(Specialty(name='окулист'))
    list.append(Specialty(name='лор'))
    dbsession.add_all(list)

def fillSection(dbsession):
    from ..models.mymodel import Section
    list = []
    list.append(Section(number=1))
    list.append(Section(number=2))
    list.append(Section(number=3))
    list.append(Section(number=4))
    dbsession.add_all(list)

def fillDiagnose(dbsession):
    from ..models.mymodel import Diagnose
    list = []
    list.append(Diagnose(name='ангина'))
    list.append(Diagnose(name='фарингит'))
    list.append(Diagnose(name='перелом'))
    list.append(Diagnose(name='гастрит'))
    dbsession.add_all(list)

def fillCabinet(dbsession):
    from ..models.mymodel import Cabinet
    list = []
    list.append(Cabinet(number=1))
    list.append(Cabinet(number=2))
    list.append(Cabinet(number=3))
    list.append(Cabinet(number=4))
    list.append(Cabinet(number=5))
    list.append(Cabinet(number=6))
    list.append(Cabinet(number=7))
    list.append(Cabinet(number=8))
    dbsession.add_all(list)

def fillDoctor(dbsession):
    from ..models.mymodel import Doctor
    from datetime import date
    list = []
    list.append(Doctor(passport=1746534526, firstName='Иван', middleName='Алексеевич', lastName='Воронцов', sex=True,
                       birthDay=date(1968, 1, 11), specialty_id=1, section_number=1, cabinet=1))
    list.append(Doctor(passport=2847365827, firstName='Инна', middleName='Евгеньевна', lastName='Лысенко', sex=False,
                       birthDay=date(1954, 4, 12), specialty_id=2, cabinet=2))
    list.append(Doctor(passport=3097467836, firstName='Анна', middleName='Семеновна', lastName='Махнутина', sex=False,
                       birthDay=date(1975, 3, 9), specialty_id=3, cabinet=3))
    list.append(Doctor(passport=3987465734, firstName='Петр', middleName='Антонович', lastName='Михеев', sex=True,
                       birthDay=date(1970, 6, 4), specialty_id=4,  cabinet=4))
    list.append(Doctor(passport=4893762546, firstName='Ольга', middleName='Анатольевна', lastName='Синицина', sex=False,
                       birthDay=date(1976, 3, 1), specialty_id=1, section_number=2, cabinet=5))
    list.append(Doctor(passport=93746583, firstName='Максим', middleName='Петрович', lastName='Иванов', sex=True,
                       birthDay=date(1957, 1, 5), specialty_id=1, section_number=3, cabinet=6))
    list.append(Doctor(passport=2847653984, firstName='Татьяна', middleName='Игоревна', lastName='Никулина', sex=False,
                       birthDay=date(1955, 3, 8), specialty_id=1, section_number=4, cabinet=7))
    dbsession.add_all(list)

def fillAddress(dbsession):
    from ..models.mymodel import Address
    list = []
    list.append(Address(address='Высоцкого 6, 63', section_number = 1))
    list.append(Address(address='Сыромолотого 11, 123', section_number = 1))
    list.append(Address(address='Новгородцевой 5, 129', section_number = 2))
    list.append(Address(address='Новгородцевой 17, 34', section_number=2))
    list.append(Address(address='40 лет комсомола 22, 101', section_number=3))
    list.append(Address(address='Сиреневый бульвар 1, 111', section_number=3))
    list.append(Address(address='Рассветная 109, 23', section_number=4))
    list.append(Address(address='Рассветная 23, 102', section_number = 4))
    dbsession.add_all(list)

def fillPatient(dbsession):
    from ..models.mymodel import Patient
    from datetime import date
    list = []
    list.append(Patient(password = '1234',policy=736463728423, firstName='Анна', middleName='Семеновна', lastName='Иванова', sex=False,
                       birthDay=date(1968, 1, 11), phone = 89364512237, address='Высоцкого 6, 63'))
    list.append(Patient(password = '1234',policy=473654783746, firstName='Петр', middleName='Евгеньевич', lastName='Лысенко', sex=True,
                       birthDay=date(1954, 4, 12), phone=89326452245, address='Сыромолотого 11, 123'))
    list.append(Patient(password = '1234',policy=847635638764, firstName='Ольга', middleName='Ивановна', lastName='Хотиенкова', sex=False,
                       birthDay=date(1975, 3, 9), phone=89543658176, address='Новгородцевой 5, 129'))
    list.append(Patient(password = '1234',policy=374689274634, firstName='Ирина', middleName='Петровна', lastName='Сокольвак', sex=False,
                       birthDay=date(1970, 6, 4), phone=89025437654,  address='Новгородцевой 17, 34'))
    list.append(Patient(password = '1234',policy=398762564736, firstName='Михаил', middleName='Васильевич', lastName='Рудацкий', sex=True,
                       birthDay=date(1976, 3, 1), phone=89653417653, address='40 лет комсомола 22, 101'))
    list.append(Patient(password = '1234',policy=987692375643, firstName='Анатолий', middleName='Михайлович', lastName='Гамов', sex=True,
                       birthDay=date(1957, 1, 5), phone=89123331010, address='Сиреневый бульвар 1, 111'))
    list.append(Patient(password = '1234',policy=296494765683, firstName='Татьяна', middleName='Игоревна', lastName='Еремеева', sex=False,
                       birthDay=date(1955, 3, 8), phone=89452678865, address='Рассветная 109, 23'))
    dbsession.add_all(list)

def fillSchedule(dbsession):
    from ..models.mymodel import ScheduleOfReception
    from datetime import date
    from datetime import time
    list = []
    list.append(ScheduleOfReception(doctor=1746534526, date=date(2016, 6, 1), time=time(11, 30), status=0,
                                    patient=736463728423))
    list.append(ScheduleOfReception(doctor=2847365827, date=date(2016, 6, 1), time=time(13, 30), status=1,
                                    patient=473654783746))
    list.append(ScheduleOfReception(doctor=3097467836, date=date(2016, 6, 2), time=time(11, 30), status=1,
                                    patient=847635638764))
    list.append(ScheduleOfReception(doctor=3987465734, date=date(2016, 6, 3), time=time(10, 30), status=0,
                                    patient=374689274634))
    list.append(ScheduleOfReception(doctor=4893762546, date=date(2016, 6, 3), time=time(11, 30), status=0,
                                    patient=398762564736))
    list.append(ScheduleOfReception(doctor=1746534526, date=date(2016, 6, 4), time=time(11, 30), status=0,
                                    patient=987692375643))
    list.append(ScheduleOfReception(doctor=1746534526, date=date(2016, 6, 4), time=time(11, 30), status=1,
                                    patient=296494765683))
    dbsession.add_all(list)

def fillHistory(dbsession):
    from ..models.mymodel import History
    from datetime import date
    from datetime import time
    list = []
    list.append(History(doctor=2847365827, date=date(2016, 6, 1), diagnose=1, patient=473654783746))
    list.append(History(doctor=3097467836, date=date(2016, 6, 3), diagnose=4, patient=473654783746))
    list.append(History(doctor=3097467836, date=date(2016, 6, 2), diagnose=2, patient=847635638764))
    list.append(History(doctor=1746534526, date=date(2016, 6, 4), diagnose=3, patient=296494765683))
    dbsession.add_all(list)

def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        fillSpecialty(dbsession)
        fillSection(dbsession)
        fillDiagnose(dbsession)
        fillCabinet(dbsession)
        fillDoctor(dbsession)
        fillAddress(dbsession)
        fillPatient(dbsession)
        fillSchedule(dbsession)
        fillHistory(dbsession)
