from typing import Optional
import random
from app.services.neo4j import driver




def createExperiment(projectId,name):
    session = driver.session()
    query = "create (n:Experiment {id:apoc.create.uuid(), " \
            "name:$name, " \
            "created_at: datetime()}) " \
            "with n " \
            "match (p:Project {id:$projectId}) " \
            "with n,p " \
            "create (p)-[r:partOf {id:apoc.create.uuid()} ]->(n)"
    session.run(query,name=name,projectId=projectId)
    session.close()

def getExperimentById(id):
    session = driver.session()
    query = "match (experiment:Experiment {id:$id}) return experiment"
    # TODO: have to add protocols
    result = session.run(query,id=id)
    for each in result:
        experiment = {
            "name":each['experiment']['name'],
            "id":each['experiment']['id'],
            "created at":each['experiment']['created_at']
        }
    session.close()
    return experiment





