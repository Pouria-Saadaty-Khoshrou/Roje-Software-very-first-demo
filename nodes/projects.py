from typing import Optional
import random
from app.services.neo4j import driver



def findUserProjects(User_id):
    session = driver.session()
    query = "match (project:Project)<-[rel:Created]-(user:User {id:$userId}) return project"
    result = session.run(query,userId=User_id)
    projects = []
    for record in result:
        eachProject = {}
        eachProject['name'] = record['project']['name']
        eachProject['id'] = record['project']['id']
        projects.append(eachProject)
    session.close()
    return projects

def createProject(userId:str,name:str):
    session = driver.session()
    query = "match (User:User {id:$id}) with User " \
            "create (P:Project {name:$name, " \
            "id:apoc.create.uuid(), " \
            "created_at:datetime()})" \
            "<-[R:Created {created_at:datetime()}]-(User)"
    session.run(query,id=userId,name=name)
    session.close()
import calendar
import time
def getProjectById(id:str):
    query = "match (project:Project {id:$id}) return project"
    session = driver.session()
    result = session.run(query,id=id)
    project={}
    for each in result:
        project['name']=each['project']['name']
        project['id']=each['project']['id']
        project['Created_at']=each['project']['created_at']
    session.close()

    return project

def deleteProjectById(id:str):
    query = "match (p:Project {id:$id}) DETACH DELETE p"
    session = driver.session()
    session.run(query,id=id)
    session.close()

def getProjectExperiments(id:str):
    query = "match (n:Project {id:$id})-[r]->(experiments:Experiment) return experiments "
    session = driver.session()
    result = session.run(query,id=id)
    experiments = []
    for each in result:
        experiment = {
            "name":each['experiments']['name'],
            "id":each['experiments']['id'],
            'Created at':each['experiments']['created_at']
        }
        experiments.append(experiment)
    session.close()
    return experiments







