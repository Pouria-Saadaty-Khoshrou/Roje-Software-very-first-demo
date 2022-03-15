from app.services.neo4j import driver


def copy_nodes(node_id):
    with driver.session() as session:
        node = session.run("MATCH (old_node {id:$node_id}) "
                           "where old_node.updated_at is NULL and old_node.deleted_at is NULL "
                           "CALL apoc.refactor.cloneNodesWithRelationships([old_node]) "
                           "YIELD input,output "
                           "CALL apoc.create.relationship(old_node, 'Created_at', {created_at:datetime()}, output) "
                           "yield rel "
                           "set output.id = apoc.create.uuid() "
                           "set output.created_at = datetime() "
                           "set old_node.updated_at = datetime() "
                           "RETURN output.id",
                           node_id=node_id)
        return node.data()[0]['output.id']


def update_node(dic: dict, id):
    for key in dic:
        with driver.session() as session:
            node = session.run(f"match (n {{id:$id}}) "
                               f"where not exists (n.updated_at) and not exists(n.deleted_at) "
                               f"set n.{key} = '{dic[key]}' "
                               f"return n",
                               id=id)

# def update_rels()
#
#
# def copy_singel_node(node_id, type):
#     with driver.session() as session:
#         node = session.run("MATCH (old_node {id:$node_id}) "
#                            "where old_node.updated_at is NULL and old_node.deleted_at is NULL "
#                            "CALL apoc.refactor.cloneNodes([old_node]) "
#                            "YIELD input,output "
#                            "match (old_node) - [r] - (b) "
#                            f"where not (b:Project) "
#                            "set output.id = apoc.create.uuid() "
#                            "set output.created_at = datetime() "
#                            "return r",
#                            node_id=node_id)
#         result = []
#         for i in node.data():
#             result.append(i)
#         print('This is result:\n\n\n', result)

