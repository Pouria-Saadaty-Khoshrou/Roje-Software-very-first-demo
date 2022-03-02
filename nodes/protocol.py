from app.services.neo4j import driver





def make_protocol(name):
    session = driver.session()
    query = "create (n:Protocol {id:apoc.create.uuid() , name:$name})  return n.id as id"
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


def Existance_of_protocol_exist(name):
    with driver.session() as session:
        node = session.run("match (p:Protocol{Protocol_name:$name}) "
                           "return p",
                           name=name)
        node = node.data()

        if not node:
            return False
        else:
            return True

def create_Protocol(name, uid, user_id):

    if not Existance_of_protocol_exist(name):
        with driver.session() as session:
            session.run("match (n) where n.id=$uid "
                        "match (user:User) where user.id=$user_id "
                        "create (p:Protocol{Protocol_name:$name, "
                        "id: apoc.create.uuid(), "
                        "created_at:datetime()}), "
                        "(user) - [:Created_at{Created_at:datetime()}] -> (p) - [:Created_at{Created_at:datetime()}] -> (n)",
                        name=name,
                        uid=uid,
                        user_id=user_id)
    else:
        with driver.session() as session:
            session.run("match (p:Protocol{Protocol_name:$name}) "
                        "match (n) where n.id=$uid "
                        "create (p) - [:Created_at{Created_at:datetime()}] -> (n)",
                        uid=uid,
                        name=name)


def Get_Protocols_by_USer_Id(user_id):
    with driver.session() as session:
        node = session.run("match (u:User{id:$user_id}) - [r] -> (p:Protocol)"
                           " return p",
                           user_id=user_id)
        result = []
        for each in node.data():
            result.append(each['p'])
        return result

def get_standards_by_protocol_id(protocol_id):
    with driver.session() as session:
        node = session.run("match (p:Protocol {id:$protocol_id}) <- [r] - (s:Standard) "
                           "return s",
                           protocol_id=protocol_id)
        result = []
        for each in node.data():
            result.append(each['s'])
        return result

def get_device_by_protocol_id(protocol_id):
    with driver.session() as session:
        node = session.run("match (p:Protocol {id:$protocol_id}) <- [r] - (d:Device) "
                           "return d",
                           protocol_id=protocol_id)
        result = []
        for each in node.data():
            result.append(each['d'])
        return result

def get_id_device_by_protocol_id(protocol_id):
    with driver.session() as session:
        node = session.run("match (p:Protocol {id:$protocol_id}) <- [r] - (d:Device) "
                           "return d.id",
                           protocol_id=protocol_id)
        result = []
        for each in node.data():
            result.append(each['d.id'])
        return result

def get_BOM_by_protocol_id(protocol_id):
    with driver.session() as session:
        node = session.run("match (p:Protocol {id:$protocol_id}) <- [r] - (b:BOM) "
                           "return b",
                           protocol_id=protocol_id)
        result = []
        for each in node.data():
            result.append(each['b'])
        return result