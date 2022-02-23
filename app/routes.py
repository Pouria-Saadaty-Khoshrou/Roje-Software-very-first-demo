from app import app
from flask import render_template, request , make_response
import json

from nodes import users as uFunc
from nodes import projects as pFunc
from nodes import experiments as exFunc
from nodes import protocol as prFunc
@app.route('/',methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():
    form = request.form.to_dict()
    userDict = uFunc.loginUser(userName=form['userName'],password=form['password'])
    resp = make_response(render_template('index.html'))
    resp.set_cookie("User_id",userDict['id'])
    return resp

@app.route('/index',methods=['GET'])
def show_dashboard():
    userId=request.cookies.get('User_id')
    if userId:
        resp = make_response(render_template('index.html'))
    else:
        resp = make_response(render_template('login.html'))
    return resp

@app.route('/projects',methods=['GET'])
def show_projects():
    userId=request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    userProjects = pFunc.findUserProjects(userId)
    resp = make_response(render_template('projects.html',userProjects=userProjects))
    return resp
@app.route('/projects',methods=['post'])
def create_projects():
    userId=request.cookies.get('User_id')
    if not userId:
        resp = make_response(render_template('login.html'))
        return resp
    form = request.form.to_dict()
    pFunc.createProject(userId=userId,name=form['projectName'])
    userProjects = pFunc.findUserProjects(userId)
    resp = make_response(render_template('projects.html',userProjects=userProjects))
    return resp


@app.route("/projects/<id>",methods=['GET'])
def read_project(id):
    project = pFunc.getProjectById(id)
    experiments = pFunc.getProjectExperiments(id)
    resp = make_response(render_template('project.html',project=project,experiments=experiments))
    return resp
@app.route("/projectsdel/<id>",methods=['GET'])
def delete_project(id):
    pFunc.deleteProjectById(id)
    userId=request.cookies.get('User_id')
    userProjects = pFunc.findUserProjects(userId)
    resp = make_response(render_template('projects.html',userProjects=userProjects))
    return resp

@app.route("/experiment",methods=['POST'])
def makeExperiment():
    userId = request.cookies.get('User_id')
    form = request.form.to_dict()
    exFunc.createExperiment(form['projectId'],form['experimentName'])
    project = pFunc.getProjectById(form['projectId'])
    experiments = pFunc.getProjectExperiments(form['projectId'])
    resp = make_response(render_template('project.html',project=project,experiments=experiments))
    return resp
@app.route('/experiment/<id>',methods=['GET'])
def read_experiment(id):
    experiment = exFunc.getExperimentById(id)
    my_tree = exFunc.getTree(id)
    if len(my_tree[0]) ==0:
        tree_levels = [0]
    else:
        tree_levels = list(my_tree[0].keys())
    tree_dict = my_tree[0]
    tree_graph = my_tree[1]
    protocols = {}
    for each in tree_dict:
        protocols[each]=[]
        for every in tree_dict[each]:
            # print(tree_graph.nodes[every])
            protocols[each].append(tree_graph.nodes[every])
    print(protocols)
    del(protocols[0])
    res = make_response(render_template('experiment.html',experiment=experiment,tree_levels=tree_levels,protocols=protocols))
    return res

@app.route('/protocols',methods=['POST'])
def create_protocol():
    data = request.form.to_dict()
    experiment = exFunc.getExperimentById(data["experiment_id"])
    protocol_id = prFunc.make_protocol(data['name'])
    my_tree = exFunc.getTree(data["experiment_id"])
    tree_level = data['tree_level']
    tree_level = int(tree_level)
    if len(my_tree[0]) ==0:
        tree_levels = [0]
        prFunc.connect_to_idies(protocol_id,[experiment['id']])
    else:

        parent_list = my_tree[0][tree_level]
        parent_idies = []
        for each in parent_list:
            parent_idies.append(my_tree[1].nodes[each]['properties']['id'])
        prFunc.connect_to_idies(protocol_id, parent_idies)
        tree_levels = list(my_tree[0].keys())

    res = make_response(render_template('experiment.html',experiment=experiment,tree_levels=tree_levels))
    return res


@app.route('/create_account',methods=['POST'])
def make_account():
    data = request.form.to_dict()
    uFunc.create_user(data)
    return {"response":"user created"}