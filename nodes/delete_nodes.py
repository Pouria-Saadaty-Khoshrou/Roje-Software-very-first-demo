from app.services.neo4j import driver


def delete_node_by_id(id):
    with driver.session() as session:
        node = session.run("match (n {id:$id}) "
                           "set n.deleted_at=datetime()"
                           "return n",
                           id=id)