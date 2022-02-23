from app import app
from flask import render_template, request, make_response

from nodes import users as uFunc
from nodes import projects as pFunc
from nodes import standrad as sFunc
from nodes import places as placeFunc
from nodes import devices as deviceFunc
from nodes import Protocols as protocolFunc
from nodes import BOMs as bomFunc


@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    form = request.form.to_dict()
    userDict = uFunc.loginUser(userName=form['userName'], password=form['password'])
    print(userDict['id'])
    resp = make_response(render_template('index.html'))
    resp.set_cookie("User_id", userDict['id'])
    return resp


@app.route('/index', methods=['GET'])
def show_dashboard():
    userId = request.cookies.get('User_id')
    if userId:
        resp = make_response(render_template('index.html'))
    else:
        resp = make_response(render_template('login.html'))
    return resp


@app.route('/projects', methods=['GET'])
def show_projects():
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    userProjects = pFunc.findUserProjects(userId)
    resp = make_response(render_template('projects.html', userProjects=userProjects))
    return resp


@app.route('/projects', methods=['post'])
def create_projects():
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    form = request.form.to_dict()
    pFunc.createProject(userId=userId, name=form['projectName'])
    userProjects = pFunc.findUserProjects(userId)
    resp = make_response(render_template('projects.html', userProjects=userProjects))
    return resp


@app.route("/projects/<id>", methods=['GET'])
def read_project(id):
    project = pFunc.getProjectById(id)
    # Pouria
    standards = sFunc.get_standards_by_project_id(id)
    # Pouria
    resp = make_response(render_template('project.html', project=project, standards=standards))
    return resp


@app.route("/projectsdel/<id>", methods=['GET'])
def delete_project(id):
    pFunc.deleteProjectById(id)
    userId = request.cookies.get('User_id')
    userProjects = pFunc.findUserProjects(userId)
    resp = make_response(render_template('projects.html', userProjects=userProjects))
    return resp


# ---------------started by pouria - date : 6/2/2022 ---------------# #
@app.route("/projects_standard", methods=['GET'])
def show_standards():
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    userProjects = pFunc.findUserProjects(userId)
    resp = make_response(render_template('standard_form.html', userProjects=userProjects))
    return resp


@app.route('/projects_standard', methods=['post'])
def add_standards():
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    form = request.form.to_dict()
    sFunc.Create_Standards(form['standard_content'], form['project_id'], form["standard_name"])
    userProjects = pFunc.findUserProjects(userId)
    resp = make_response(render_template('standard_form.html', userProjects=userProjects))
    return resp


@app.route('/delete_standards/<id>')
def delete_standards(id):
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    sFunc.delete_standards_by_id(id)
    userProjects = pFunc.findUserProjects(userId)
    resp = make_response(render_template('projects.html', userProjects=userProjects))
    return resp


# @app.route()
# def update_standards(id):

# ---------------started by pouria - date : 6/2/2022 ---------------#

# ---------------started by pouria - date : 7/2/2022 ---------------#

@app.route("/Places", methods=['GET'])
def show_Places():
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    places = placeFunc.Get_Places_by_USer_Id(userId)
    resp = make_response(render_template('Places.html', places=places))
    return resp


@app.route('/Places', methods=['post'])
def add_places():
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    form = request.form.to_dict()
    placeFunc.Create_Places(form['Place_Name'], userId)
    places = placeFunc.Get_Places_by_USer_Id(userId)
    resp = make_response(render_template('Places.html', places=places))
    return resp

@app.route("/Places/<id>", methods=['GET'])
def read_place(id):
    place = placeFunc.Show_Place_With_Id(id)[0]
    device = deviceFunc.Get_Devices_By_Place_Id(id)
    resp = make_response(render_template('Place.html', place=place, device=device))
    return resp

@app.route('/delete_place/<id>')
def delete_place(id):
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    placeFunc.Delete_Place_With_Id(id)
    places = placeFunc.Get_Places_by_USer_Id(userId)
    resp = make_response(render_template('Places.html', places=places))
    return resp


@app.route('/Devices', methods=['GET'])
def show_devices():
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    Lab = placeFunc.Get_Places_by_USer_Id(userId)
    resp = make_response(render_template('Devices.html', Lab=Lab))
    return resp

@app.route('/Devices', methods=['post'])
def add_devices():
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    form = request.form.to_dict()
    deviceFunc.Create_Devices(form['device_name'], form['device_description'], form['device_id'], form['place_id'])
    Lab = placeFunc.Get_Places_by_USer_Id(userId)
    resp = make_response(render_template('Devices.html', Lab=Lab))
    return resp

@app.route('/delete_device/<id>')
def delete_device(id):
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    deviceFunc.Delete_Device_By_Id(id)
    places = placeFunc.Get_Places_by_USer_Id(userId)
    resp = make_response(render_template('Places.html', places=places))
    return resp

# ---------------ended by pouria - date : 7/2/2022 ---------------#

# ---------------started by pouria - date : 7/2/2022 ---------------#
@app.route("/Protocols", methods=['GET'])
def show_Porotocols():
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp

    protocols = protocolFunc.Get_Protocols_by_USer_Id(userId)
    devices = deviceFunc.Get_Device_by_USer_Id(userId)
    standard = sFunc.Get_Standard_by_USer_Id(userId)
    BOM = bomFunc.Get_BOMs_by_USer_Id(userId)

    resp = make_response(render_template('Protocols.html',
                                         protocols=protocols,
                                         devices=devices,
                                         standard=standard,
                                         BOM=BOM))
    return resp

@app.route('/Protocols', methods=['post'])
def add_protocols():
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    form = request.form.to_dict()
    # print(form)
    # print(form['Protocol_Name'])
    protocolFunc.create_Protocol(form['Protocol_Name'], form['id'], userId)

    protocols = protocolFunc.Get_Protocols_by_USer_Id(userId)
    devices = deviceFunc.Get_Device_by_USer_Id(userId)
    standard = sFunc.Get_Standard_by_USer_Id(userId)
    BOM = bomFunc.Get_BOMs_by_USer_Id(userId)

    resp = make_response(render_template('Protocols.html',
                                         protocols=protocols,
                                         devices=devices,
                                         standard=standard,
                                         BOM=BOM))
    return resp


# ---------------ended by pouria - date : 7/2/2022 ---------------#
# ---------------started by pouria - date : 7/2/2022 ---------------#

@app.route("/Protocols/<id>", methods=['GET'])
def read_protocol(id):
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    standards_list = protocolFunc.get_standards_by_protocol_id(id)
    device_list = protocolFunc.get_device_by_protocol_id(id)
    BOM_list = protocolFunc.get_BOM_by_protocol_id(id)
    resp = make_response(render_template('Protocol.html',
                                         standards_list=standards_list,
                                         device_list=device_list,
                                         BOM_list=BOM_list))
    return resp

# ---------------ended by pouria - date : 7/2/2022 ---------------#

# ---------------started by pouria - date : 7/2/2022 ---------------#

@app.route("/BOMs", methods=['GET'])
def show_BOMs():
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    bom_names = bomFunc.Get_BOMs_by_USer_Id(userId)
    resp = make_response(render_template('BOMs.html',
                                         bom_names=bom_names))
    return resp


@app.route('/BOMs', methods=['post'])
def add_BOMs():
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    form = request.form.to_dict(flat=False)
    if 'BOM_id_List' not in form:
        form['BOM_id_List'] = []
    bomFunc.Create_BOM(userId, form['BOM_id_List'], form['BOM_Name'][0], form['BOM_Description'][0])
    bom_names = bomFunc.Get_BOMs_by_USer_Id(userId)
    resp = make_response(render_template('BOMs.html',
                         bom_names=bom_names))
    return resp










# ---------------ended by pouria - date : 7/2/2022 ---------------#