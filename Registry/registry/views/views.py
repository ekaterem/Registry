from pyramid.view import view_config
from ..scripts.metodsForDB import *
from pyramid.security import remember, authenticated_userid, forget
from pyramid.httpexceptions import HTTPFound, HTTPForbidden


#@notfound_view_config(renderer='../templates/404.jinja2')
@view_config(route_name='login', renderer='../templates/login.jinja2')
def notfound_view(request):
    if ('login' in request.POST and 'password' in request.POST):
        user = getUser(request.POST["login"],request.POST["password"])
        if user:
            h = remember(request, user.policy)
            return HTTPFound(location=request.route_url('aboutme', name=user.policy), headers=h)
    if 'commit' in request.POST and request.POST["commit"] == "Выйти":
        h = forget(request)
        return HTTPFound(location=request.route_url('login', name='log out!!!'),
                         headers=h)
        #request.response.status = 404
    return {}


@view_config(route_name='aboutme', renderer='../templates/aboutme.jinja2')
def aboutme_view(request):
    if request.authenticated_userid:
        patient = getDataPatient(request.authenticated_userid)
        sectionNumber = getSectionNumber(patient[6])
        return {"patient":patient,
                "section":sectionNumber}
    else:
        return HTTPFound(location=request.route_url('login', name='log out!!!'))

@view_config(route_name='registration', renderer='../templates/registration.jinja2')
def schedule_view(request):
    if 'reg' in request.POST and request.POST["reg"] == "Записаться":
        makeAnAppointment(request.POST["number"], request.authenticated_userid)

    schedule = getSchedule()
    listSpecialty = []
    listSection = []
    listDoctor=[]
    for i in schedule:
        specialty = getSpecialty(i[1])
        listSpecialty.append(specialty)
        section = getSection(i[1])
        listSection.append(section)
        doctor = getDoctorName(i[1])
        listDoctor.append(doctor)
    result = []
    result.append(schedule)
    result.append(listSpecialty)
    result.append(listSection)
    result.append(listDoctor)
    return {"schedule":result }

@view_config(route_name='history', renderer='../templates/history.jinja2')
def history_view(request):
    history = getHistory(request.authenticated_userid)
    listSpecialty=[]
    listDiagnose =[]
    for i in history:
        specialty = getSpecialty(i[5])
        listSpecialty.append(specialty)
        diagnose = getDiagnose(i[2])
        listDiagnose.append(diagnose)
    result1 = []
    result1.append(history)
    result1.append(listSpecialty)
    result1.append(listDiagnose)
    acthistory = getActiveHistory(request.authenticated_userid)
    listSpecialty = []
    for i in acthistory:
        specialty = getSpecialty(i[2])
        listSpecialty.append(specialty)
    result2 = []
    result2.append(acthistory)
    result2.append(listSpecialty)
    return {"history":result1, "activeHistory":result2}