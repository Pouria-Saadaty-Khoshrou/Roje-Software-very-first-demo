 #---------------started by pouria - date : 6/2/2022 ---------------#
from app.services.neo4j import driver


# This func check if node exist or not if it exists return True else return False
# def Existance_Of_Standrad(node_id):
#     with driver.session() as session:
#         node = session.run("match (n:Standard{ID:$node_id}) return n",
#                            node_id=node_id)
#         if not node.data():
#             return False
#         return True
#
#
# # This func will allow experts to see their Standards
# def See_Standards(expert_name):
#     if expert_existance(expert_name):
#         with driver.session() as session:
#             nodes = session.run("MATCH (a:Experts {name: $expert_name})-[r:Created_by]->(b)"
#                                 " RETURN b",
#                                 expert_name=expert_name)
#             node = []
#             for n in nodes.data():
#                 node.append(n['b'])
#             return node
#     return {'ERROR', f'There is no {expert_name}'}
#
#
# # This func find out if expert exist or not
# def expert_existance(name):
#     with driver.session() as session:
#         node = session.run('match (n:Experts{name:$name}) return n',
#                            name=name)
#         if not node.data():
#             return False
#         return True


# This func create rel between standard and expert
def Create_Rel(project_id, standard_id):

    with driver.session() as session:
        rel = session.run("match (e:Project{id:$project_id})"
                          " match (s:Standard{id:$standard_id})"
                          " CALL apoc.create.relationship(e, 'Created_at', {created_at:datetime()}, s)"
                          " yield rel"
                          " return rel",
                          project_id=project_id,
                          standard_id=standard_id)


    # This function Create Standard


def Create_Standards(Content, project_id, Standard_name):

    with driver.session() as session:
        node = session.run(
            "create (s:Standard{Standard_name:$Standard_name,"
            " Content:$Content,"
            " id: apoc.create.uuid(),"
            " created_at:datetime()})"
            "return s.id",
            Standard_name=Standard_name,
            Content=Content)
        Create_Rel(project_id, node.data()[0]['s.id'])


def get_standards_by_project_id(project_id):
    result = []
    with driver.session() as session:
        node = session.run("match (p:Project{id:$project_id}) - [r] -> (s:Standard)"
                           " return s",
                           project_id=project_id)
        for each in node.data():
            result.append(each['s'])
        return result

def delete_standards_by_id(standard_id):

    with driver.session() as session:
        session.run("match (s:Standard{id:$standard_id}) detach delete s",
                    standard_id=standard_id)

def Get_Standard_by_USer_Id(user_id):
    with driver.session() as session:
        node = session.run("match (u:User{id:$user_id}) - [r*] -> (s:Standard)"
                           " return s",
                           user_id=user_id)
        result = []
        for each in node.data():
            result.append(each['s'])
        return result
#def update_standards(standard_id):

# Delete all relations and node
# def delete_Standard(ID):
#     with driver.session() as session:
#         session.run('match (n:Standard {ID:$ID}) detach delete n',
#                     ID=ID)
#
#     # This func will add Standards to other nodes
#
#
# def add_to_other_nodes(name, code, Standard_ID, expert_name):
#     with driver.session() as session:
#         node = session.run(f'match (p:{name}{{code:$code}}) return p',
#                            code=code)
#         if not node.data():
#             return {'ERROR': 'Code dosn\'t exist'}
#         elif Existance_Of_Standrad(Standard_ID):
#             with driver.session() as session:
#                 rel = session.run(f'match (n:{name}{{code:$code}}),'
#                                   ' (s:Standard{ID:$Standard_ID})'
#                                   ' CALL apoc.create.relationship(s, "Has",{Name:[$expert_name]}, n)'
#                                   ' yield rel'
#                                   ' return rel',
#                                   code=code,
#                                   Standard_ID=Standard_ID,
#                                   expert_name=expert_name)
#                 return {'Job': 'Done'}

# --------------ended by Pouria - date : ------------