from app import app
from flask import render_template, request, make_response, redirect
import json

from nodes import users as uFunc
from nodes import projects as pFunc
from nodes import experiments as exFunc
# from nodes import protocol as prFunc

from nodes import users as uFunc
from nodes import projects as pFunc
from nodes import standrad as sFunc
from nodes import places as placeFunc
from nodes import devices as deviceFunc
from nodes import protocol as protocolFunc
from nodes import BOMs as bomFunc
from nodes import tasks as taskFunc


@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    form = request.form.to_dict()
    userDict = uFunc.loginUser(userName=form['userName'], password=form['password'])
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
    experiments = pFunc.getProjectExperiments(id)
    resp = make_response(render_template('project.html', project=project, experiments=experiments))
    return resp


@app.route("/projectsdel/<id>", methods=['GET'])
def delete_project(id):
    pFunc.deleteProjectById(id)
    userId = request.cookies.get('User_id')
    userProjects = pFunc.findUserProjects(userId)
    resp = make_response(render_template('projects.html', userProjects=userProjects))
    return resp


@app.route("/experiment", methods=['POST'])
def makeExperiment():
    userId = request.cookies.get('User_id')
    form = request.form.to_dict()
    exFunc.createExperiment(form['projectId'], form['experimentName'])
    project = pFunc.getProjectById(form['projectId'])
    experiments = pFunc.getProjectExperiments(form['projectId'])
    resp = make_response(render_template('project.html', project=project, experiments=experiments))
    return resp


@app.route('/experiment/<id>', methods=['GET'])
def read_experiment(id):
    experiment = exFunc.getExperimentById(id)

    #my_tree = exFunc.getTree(id)
    my_tree = exFunc.getTree_Pouria(id, 'Protocol')


    if len(my_tree[0]) == 0:
        tree_levels = [0]
    else:
        tree_levels = list(my_tree[0].keys())
    tree_dict = my_tree[0]
    tree_graph = my_tree[1]
    protocols = {}
    for each in tree_dict:
        protocols[each] = []
        for every in tree_dict[each]:
            # print(tree_graph.nodes[every])
            protocols[each].append(tree_graph.nodes[every])
    # del(protocols[0])
    if 0 in protocols:
        del (protocols[0])
    res = make_response(
        render_template('experiment.html', experiment=experiment, tree_levels=tree_levels, protocols=protocols))
    return res


@app.route('/protocols', methods=['POST'])
def create_protocol():
    data = request.form.to_dict()
    experiment = exFunc.getExperimentById(data["experiment_id"])
    protocol_id = protocolFunc.make_protocol(data['name'])


    #my_tree = exFunc.getTree(data["experiment_id"])
    my_tree = exFunc.getTree_Pouria(data["experiment_id"], 'Protocol')



    tree_level = data['tree_level']
    tree_level = int(tree_level)
    if len(my_tree[0]) == 0:
        tree_levels = [0]
        protocolFunc.connect_to_idies(protocol_id, [experiment['id']])
    else:
        parent_list = my_tree[0][tree_level]
        parent_idies = []
        for each in parent_list:
            parent_idies.append(my_tree[1].nodes[each]['properties']['id'])
        protocolFunc.connect_to_idies(protocol_id, parent_idies)
        #tree_levels = list(my_tree[0].keys())
    # tree_dict = my_tree[0]
    # tree_graph = my_tree[1]
    # protocols = {}
    # for each in tree_dict:
    #     protocols[each] = []
    #     for every in tree_dict[each]:
    #         protocols[each].append(tree_graph.nodes[every])
    # # del(protocols[0])
    #
    # if 0 in protocols:
    #     del (protocols[0])

    #res = make_response(
        #render_template('experiment.html', experiment=experiment, tree_levels=tree_levels, protocols=protocols))

    return redirect(f'/experiment/{data["experiment_id"]}')

    #return res


@app.route('/create_account', methods=['POST'])
def make_account():
    data = request.form.to_dict()
    uFunc.create_user(data)
    return {"response": "user created"}


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
# @app.route("/Protocols", methods=['GET'])
# def show_Porotocols():
#     userId = request.cookies.get('User_id')
#     if not userId:
#         resp = make_response(render_template('login.html'))
#         return resp
#
#     protocols = protocolFunc.Get_Protocols_by_USer_Id(userId)
#     devices = deviceFunc.Get_Device_by_USer_Id(userId)
#     standard = sFunc.Get_Standard_by_USer_Id(userId)
#     BOM = bomFunc.Get_BOMs_by_USer_Id(userId)
#
#     resp = make_response(render_template('Protocols.html',
#                                          protocols=protocols,
#                                          devices=devices,
#                                          standard=standard,
#                                          BOM=BOM))
#     return resp
#
#
# @app.route('/Protocols', methods=['post'])
# def add_protocols():
#     userId = request.cookies.get('User_id')
#     if not userId:
#         resp = make_response(render_template('login.html'))
#         return resp
#     form = request.form.to_dict()
#     protocolFunc.create_Protocol(form['Protocol_Name'], form['id'], userId)
#
#     protocols = protocolFunc.Get_Protocols_by_USer_Id(userId)
#     devices = deviceFunc.Get_Device_by_USer_Id(userId)
#     standard = sFunc.Get_Standard_by_USer_Id(userId)
#     BOM = bomFunc.Get_BOMs_by_USer_Id(userId)
#
#     resp = make_response(render_template('Protocols.html',
#                                          protocols=protocols,
#                                          devices=devices,
#                                          standard=standard,
#                                          BOM=BOM))
#     return resp


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
    standards = sFunc.Get_Standard_by_USer_Id(userId)
    user_boms = bomFunc.Get_BOMs_by_USer_Id(userId)
    devices = deviceFunc.Get_Device_by_USer_Id(userId)
    tasks = taskFunc.get_tasks_by_protocol_id(id)
    place_names = placeFunc.find_places_by_device_id(protocolFunc.get_id_device_by_protocol_id(id))
    resp = make_response(render_template('Protocol.html',
                                         standards_list=standards_list,
                                         device_list=device_list,
                                         BOM_list=BOM_list,
                                         standards=standards,
                                         protocol_id=id,
                                         user_boms=user_boms,
                                         devices=devices,
                                         tasks=tasks,
                                         place_names=place_names))
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
    BOM_value = form['BOM_Values'][0].split('-')
    if form['BOM_Values'] == ['']:
        BOM_value = form['BOM_Values'] = []
    print(form['Label'][0])
    if len(form['BOM_id_List']) == len(BOM_value):
        bomFunc.Create_BOM(userId,
                           form['BOM_id_List'],
                           form['BOM_Name'][0],
                           form['BOM_Description'][0],
                           BOM_value,
                           form['ph'][0],
                           form['volume'][0],
                           form['Type_of_material'][0])
    bom_names = bomFunc.Get_BOMs_by_USer_Id(userId)
    resp = make_response(render_template('BOMs.html',
                                         bom_names=bom_names))
    return resp


# -----------------added by hossein 2/23/2022--------------
@app.route('/add_standard_to_protocol', methods=['post'])
def add_standard_to_protocol():
    userId = request.cookies.get('User_id')
    form = request.form.to_dict(flat=False)
    id = form['protocol_id'][0]
    protocolFunc.connect_to_idies(id, form['standard_list'])
    standards_list = protocolFunc.get_standards_by_protocol_id(id)
    device_list = protocolFunc.get_device_by_protocol_id(id)
    BOM_list = protocolFunc.get_BOM_by_protocol_id(id)
    standards = sFunc.Get_Standard_by_USer_Id(userId)
    user_boms = bomFunc.Get_BOMs_by_USer_Id(userId)
    devices = deviceFunc.Get_Device_by_USer_Id(userId)
    tasks = taskFunc.get_tasks_by_protocol_id(id)
    place_names = placeFunc.find_places_by_device_id(protocolFunc.get_id_device_by_protocol_id(id))
    resp = make_response(render_template('Protocol.html',
                                         standards_list=standards_list,
                                         device_list=device_list,
                                         BOM_list=BOM_list,
                                         standards=standards,
                                         protocol_id=id,
                                         user_boms=user_boms,
                                         devices=devices,
                                         tasks=tasks,
                                         place_names=place_names))

    return resp


@app.route('/add_bom_to_protocol', methods=['post'])
def add_bom_to_protocol():
    userId = request.cookies.get('User_id')
    form = request.form.to_dict(flat=False)
    id = form['protocol_id'][0]
    protocolFunc.connect_to_idies(id, form['bom_list'])
    standards_list = protocolFunc.get_standards_by_protocol_id(id)
    device_list = protocolFunc.get_device_by_protocol_id(id)
    BOM_list = protocolFunc.get_BOM_by_protocol_id(id)
    standards = sFunc.Get_Standard_by_USer_Id(userId)
    tasks = taskFunc.get_tasks_by_protocol_id(id)
    user_boms = bomFunc.Get_BOMs_by_USer_Id(userId)
    devices = deviceFunc.Get_Device_by_USer_Id(userId)
    place_names = placeFunc.find_places_by_device_id(protocolFunc.get_id_device_by_protocol_id(id))

    resp = make_response(render_template('Protocol.html',
                                         standards_list=standards_list,
                                         device_list=device_list,
                                         BOM_list=BOM_list,
                                         standards=standards,
                                         protocol_id=id,
                                         user_boms=user_boms,
                                         devices=devices,
                                         tasks=tasks,
                                         place_names=place_names))

    return resp


@app.route('/add_device_to_protocol', methods=['post'])
def add_device_to_protocol():
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp

    form = request.form.to_dict(flat=False)
    protocolFunc.connect_to_idies(form['protocol_id'][0], form['devices_id_List'])
    protocol_id = form['protocol_id'][0]
    place_names = placeFunc.find_places_by_device_id(protocolFunc.get_id_device_by_protocol_id(protocol_id))
    standards_list = protocolFunc.get_standards_by_protocol_id(protocol_id)
    device_list = protocolFunc.get_device_by_protocol_id(protocol_id)
    BOM_list = protocolFunc.get_BOM_by_protocol_id(protocol_id)
    devices = deviceFunc.Get_Device_by_USer_Id(userId)
    standards = sFunc.Get_Standard_by_USer_Id(userId)
    tasks = taskFunc.get_tasks_by_protocol_id(protocol_id)
    user_boms = bomFunc.Get_BOMs_by_USer_Id(userId)
    resp = make_response(render_template('Protocol.html',
                                         standards_list=standards_list,
                                         device_list=device_list,
                                         BOM_list=BOM_list,
                                         devices=devices,
                                         standards=standards,
                                         protocol_id=protocol_id,
                                         user_boms=user_boms,
                                         tasks=tasks,
                                         place_names=place_names))
    return resp


@app.route('/add_task_to_protocol', methods=['post'])
def add_task_to_protocol():
    userId = request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    form = request.form.to_dict()
    id = form['protocol_id']
    taskFunc.create_tasks(form['task'].split('\r\n'), id)
    tasks = taskFunc.get_tasks_by_protocol_id(id)
    place_names = placeFunc.find_places_by_device_id(protocolFunc.get_id_device_by_protocol_id(id))
    standards_list = protocolFunc.get_standards_by_protocol_id(id)
    device_list = protocolFunc.get_device_by_protocol_id(id)
    BOM_list = protocolFunc.get_BOM_by_protocol_id(id)
    standards = sFunc.Get_Standard_by_USer_Id(userId)
    user_boms = bomFunc.Get_BOMs_by_USer_Id(userId)
    devices = deviceFunc.Get_Device_by_USer_Id(userId)
    resp = make_response(render_template('Protocol.html',
                                         standards_list=standards_list,
                                         device_list=device_list,
                                         BOM_list=BOM_list,
                                         standards=standards,
                                         protocol_id=id,
                                         user_boms=user_boms,
                                         devices=devices,
                                         tasks=tasks,
                                         place_names=place_names))

    return resp
