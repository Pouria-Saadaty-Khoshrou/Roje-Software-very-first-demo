from app.services.neo4j import driver

def existance_of_result_name(result_name):

    with driver.session() as session:
        node = session.run("match (r:Result {result_name:$result_name}) "
                           "return r",
                           result_name=result_name)
        if not node.data():
            return False
        else:
            return True

def create_result(experiment_id, result_name, text):

    with driver.session() as session:
        node = session.run("match (e:Experiment {id:$experiment_id}) "
                           "create (r:Result {experiment_name:e.name, "
                           "result_name:$result_name, "
                           "id: apoc.create.uuid(), "
                           "created_at:datetime() ,"
                           "content:$text}) "
                           "create (e) - [:Created_at{Created_at:datetime()}] -> (r) "
                           "return r.id",
                           experiment_id=experiment_id,
                           text=text,
                           result_name=result_name)
        return node.data()[0]['r.id']

def find_result_by_experiment_id(experiment_id):

    with driver.session() as session:
        node = session.run("match (e:Experiment {id:$experiment_id}) - [rel] -> (r:Result)"
                           " return r",
                           experiment_id=experiment_id)
        result = []
        for each in node.data():
            result.append(each['r'])
        return result