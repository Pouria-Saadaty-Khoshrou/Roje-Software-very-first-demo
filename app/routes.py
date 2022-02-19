from app import app
from flask import render_template, request , make_response


from nodes import users as uFunc
from nodes import projects as pFunc
from nodes import experiments as exFunc
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
    res = make_response(render_template('experiment.html',experiment=experiment))
    return res

@app.route('/protocols',methods=['POST'])
def read_protocol():
    return True



