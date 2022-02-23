from app.services.neo4j import driver


def Existance_of_BOM(name):
    with driver.session() as session:
        node = session.run("match (b:BOM{BOM_name:$name}) "
                           "return b",
                           name=name)
        node = node.data()
        if not node:
            return False
        else:
            return True


def Create_BOM(user_id, list_id, name, description):
    if not Existance_of_BOM(name):
        with driver.session() as session:
            node = session.run("match (u:User {id:$user_id}) "
                               "create (b:BOM{BOM_name:$name, "
                               "description:$description, "
                               "id:apoc.create.uuid(), "
                               "created_at:datetime()}), "
                               "(u) - [:Created_at{Created_at:datetime()}] -> (b) "
                               "return b.id",
                               user_id=user_id,
                               name=name,
                               description=description)
            BOM_id = node.data()[0]['b.id']
            if list_id != []:
                connect_new_bom_to_other_bom(BOM_id, list_id)

        BOM_id = node.data()


def connect_new_bom_to_other_bom(BOM_id, list_id):
    with driver.session() as session:
        for B_id in list_id:
            session.run("match (main_bom:BOM{id:$B_id}), "
                        "(new_bom:BOM{id:$BOM_id})"
                        "create (main_bom) - [:Created_at{Created_at:datetime()}] -> (new_bom)",
                        B_id=B_id,
                        BOM_id=BOM_id)

def Get_BOMs_by_USer_Id(user_id):
    with driver.session() as session:
        node = session.run("match (u:User{id:$user_id}) - [r] -> (b:BOM)"
                           " return b",
                           user_id=user_id)
        result = []
        for each in node.data():
            result.append(each['b'])
        return result