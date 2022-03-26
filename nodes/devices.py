from app.services.neo4j import driver


def Existance_of_Device_Id(device_id):
    with driver.session() as session:
        node = session.run("match (d:Device{device_id:$device_id}) "
                           "where not exists (d.updated_at) and not exists(d.deleted_at) "
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
        node = session.run("match (p:Place{id:$place_id}) - [r] -> (d:Device) "
                           "where not exists (d.updated_at) and not exists(d.deleted_at) "
                           " return d",
                           place_id=place_id)
        result = []
        for each in node.data():
            result.append(each['d'])
        return result


# def Delete_Device_By_Id(device_id):
#     with driver.session() as session:
#         session.run("match (d:Device{id:$device_id})"
#                     " detach delete d",
#                     device_id=device_id)

def Get_Device_by_USer_Id(user_id):
    with driver.session() as session:
        node = session.run("match (u:User{id:$user_id}) - [r*] -> (d:Device) "
                           "where not exists (d.updated_at) and not exists(d.deleted_at) "
                           " return d",
                           user_id=user_id)
        result = []
        for each in node.data():
            result.append(each['d'])
        return result






# <div class="col-md-6 grid-margin stretch-card">
#     <div class="card">
#         <div class="card-body">
#             <h4 class="card-title">Update Device Form</h4>
#
#             <form class="forms-sample" action="{{ url_for('update_device') }}" method="post">
#
#                 <div class="form-group" data-select2-id="7">
#                     <label>Device Name</label>
#                     <select class="js-example-basic-single w-100 select2-hidden-accessible" name="device_id"
#                             data-select2-id="1" tabindex="-1" aria-hidden="true">
#                         {% for each in devices %}
#                         <option value="{{each['id']}}" data-select2-id="3">{{each['device_name']}}</option>
#                         {% endfor %}
#                     </select>
#                 </div>
#
#
#                 <div class="form-group">
#                     <label>Device Name</label>
#                     <input type="text" class="form-control" id="exampleInputUsername1" name="device_name"
#                            placeholder="Device Name">
#                 </div>
#
#                 <div class="form-group">
#                     <label>Device ID</label>
#                     <input type="number" class="form-control" id="exampleInputUsername1" name="device_id"
#                            placeholder="Device ID">
#                 </div>
#
#                 <div class="form-group">
#                     <label>Device Description</label>
#                     <input type="text" class="form-control" id="exampleInputUsername1" name="device_description"
#                            placeholder="Device Description">
#                 </div>
#
#                 <div class="form-group" data-select2-id="7">
#                     <label>Lab Name</label>
#                     <select class="js-example-basic-single w-100 select2-hidden-accessible" name="place_id"
#                             data-select2-id="1" tabindex="-1" aria-hidden="true">
#                         {% for each in Lab %}
#                         <option value="{{each['id']}}" data-select2-id="3">{{each['Place_name']}}</option>
#                         {% endfor %}
#                     </select>
#                 </div>
#
#                 <button type="submit" class="btn btn-primary me-2">Update</button>
#             </form>
#         </div>
#     </div>
# </div>