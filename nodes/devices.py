from app.services.neo4j import driver


def Existance_of_Device_Id(device_id):
    with driver.session() as session:
        node = session.run("match (d:Device{device_id:$device_id})"
                           " return d",
                           device_id=device_id)
        if not node.data():
            return False
        return True


def Create_Devices(device_name, device_description, device_id, lab_id):
    if not Existance_of_Device_Id(device_id):
        with driver.session() as session:
            session.run(
                "match (p:Place{id:$lab_id})"
                " create (d:Device{device_name:$device_name,"
                " id: apoc.create.uuid(),"
                " device_id: $device_id,"
                " device_description: $device_description,"
                " created_at:datetime()}),"
                " (p) - [:Created_at{Created_at:datetime()}] -> (d)"
                " return p",
                lab_id=lab_id,
                device_name=device_name,
                device_id=device_id,
                device_description=device_description
            )
    else:
        return 'ERROR'


def Get_Devices_By_Place_Id(place_id):
    with driver.session() as session:
        node = session.run("match (p:Place{id:$place_id}) - [r] -> (d:Device)"
                           " return d",
                           place_id=place_id)
        result = []
        for each in node.data():
            result.append(each['d'])
        return result


def Delete_Device_By_Id(device_id):
    with driver.session() as session:
        session.run("match (d:Device{id:$device_id})"
                    " detach delete d",
                    device_id=device_id)

def Get_Device_by_USer_Id(user_id):
    with driver.session() as session:
        node = session.run("match (u:User{id:$user_id}) - [r*] -> (d:Device)"
                           " return d",
                           user_id=user_id)
        result = []
        for each in node.data():
            result.append(each['d'])
        return result