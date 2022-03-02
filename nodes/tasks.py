from app.services.neo4j import driver


def existance_of_task_in_protocol(protocol_id):
    with driver.session() as session:
        node = session.run("match (p:Protocol {id:$protocol_id}), "
                           "(p) - [r] -> (t:Task) "
                           "return t",
                           protocol_id=protocol_id)
        if not node.data():
            return False
        return True


def create_tasks(list_of_descriptions, protocol_id):
    if not existance_of_task_in_protocol(protocol_id):
        description = list_of_descriptions[0]
        with driver.session() as session:
            session.run("match (p:Protocol {id:$protocol_id}) "
                        "create (t:Task {description:$description, "
                        "id: apoc.create.uuid(), "
                        "created_at:datetime()}), "
                        "(p) - [:Created_at{Created_at:datetime()}] -> (t)",
                        description=description,
                        protocol_id=protocol_id)
        if len(list_of_descriptions) > 1:
            create_linked_list_for_tasks(list_of_descriptions[1::], protocol_id)
    else:
        create_linked_list_for_tasks(list_of_descriptions, protocol_id)



def create_linked_list_for_tasks(list_of_descriptions, protocol_id):

    with driver.session() as session:
        for description in list_of_descriptions:
            node = session.run("match (p:Protocol{id:$protocol_id}) - [r*..] -> (t:Task)"
                               "return t",
                               protocol_id=protocol_id)
            last_node = node.data()[-1]['t']['id']
            session.run("match (last_task:Task{id:$last_node}) "
                        "create (t:Task {description:$description, "
                        "id: apoc.create.uuid(), "
                        "created_at:datetime()}), "
                        "(last_task) - [:Created_at{Created_at:datetime()}] -> (t)",
                        last_node=last_node,
                        description=description)


# def connect_to_idies(nodeId,idies:list):
#     session = driver.session()
#     query = "match (firstNode {id:$id}), (secondNode {id:$secId}) " \
#             "with firstNode , secondNode " \
#             "create (firstNode)<-[:partOf]-(secondNode) "
#     for each in idies:
#         session.run(query,id=nodeId,secId=each)
#     session.close()

def get_tasks_by_protocol_id(protocol_id):
    with driver.session() as session:
        node = session.run("match (p:Protocol{id:$protocol_id}) - [r*] -> (t:Task)"
                           " return t",
                           protocol_id=protocol_id)
        result = []
        for each in node.data():
            result.append(each['t'])
        return result


def get_tasks_by_user_id(user_id):
    with driver.session() as session:
        node = session.run("match (u:User{id:$user_id}) - [r*] -> (t:Task)"
                           " return t",
                           user_id=user_id)
        result = []
        for each in node.data():
            result.append(each['t'])
        return result
