from app.services.neo4j import driver

def connect_to_idies(nodeId,idies:list):
    session = driver.session()
    query = "match (firstNode {id:$id}), (secondNode {id:$secId}) " \
            "with firstNode , secondNode " \
            "create (firstNode)<-[:partOf]-(secondNode) "
    for each in idies:
        session.run(query,id=nodeId,secId=each)
    session.close()

def create_result(experiment_id, result_name, text):

    with driver.session() as session:
        node = session.run("match (e:Experiment {id:$experiment_id}) "
                           "create (r:Result {experiment_name:e.name, "
                           "result_name:$result_name, "
                           "id: apoc.create.uuid(), "
                           "created_at:datetime() ,"
                           "content:$text}) "
                           "create (e) - [:Created_at{Created_at:datetime()}] -> (r)",
                           experiment_id=experiment_id,
                           text=text,
                           result_name=result_name)