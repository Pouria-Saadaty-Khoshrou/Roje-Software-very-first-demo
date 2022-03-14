from app.services.neo4j import driver


def copy_nodes(node_id):
    with driver.session() as session:
        node = session.run("MATCH (old_node {id:$node_id}) "
                           "where not exists (old_node.updated_at) and not exists(old_node.deleted_at) "
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
