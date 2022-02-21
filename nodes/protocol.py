from app.services.neo4j import driver





def make_protocol(name):
    session = driver.session()
    query = "create (n:protocol {id:apoc.create.uuid() , name:$name})  return n.id as id"
    result = session.run(query,name=name)
    data = []
    for each in result:
        data = each['id']
    session.close()
    return data

def connect_to_idies(nodeId,idies:list):
    session = driver.session()
    query = "match (firstNode {id:$id}), (secondNode {id:$secId}) " \
            "with firstNode , secondNode " \
            "create (firstNode)<-[:partOf]-(secondNode) "
    for each in idies:
        session.run(query,id=nodeId,secId=each)
    session.close()

