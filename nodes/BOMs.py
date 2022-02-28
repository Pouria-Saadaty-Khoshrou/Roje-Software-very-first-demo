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


def Create_BOM(user_id, list_id, name, description, list_values):
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
            if list_id != [] and list_values != []:
                connect_new_bom_to_other_bom(BOM_id, list_id, list_values)


def connect_new_bom_to_other_bom(BOM_id, list_id, list_values):
    with driver.session() as session:
        for counter in range(len(list_id)):
            session.run("match (main_bom:BOM{id:$B_id}), "
                        "(new_bom:BOM{id:$BOM_id})"
                        "create (main_bom) - [:Gives_us{Created_at:datetime(), value:$B_value}] -> (new_bom)",
                        B_id=list_id[counter],
                        B_value=list_values[counter],
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
