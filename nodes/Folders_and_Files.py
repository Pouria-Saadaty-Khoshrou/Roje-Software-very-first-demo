from app.services.neo4j import driver


def Create_Folder(folder_name, top_folder):
    with driver.session() as session:
        node = session.run(
            "create (f:Folder {name:$folder_name, "
            " id: apoc.create.uuid(),"
            " created_at:datetime()})"
            " return f.id",
            folder_name=folder_name)
        folder_id = node.data()[0]['f.id']
        print(folder_id)
        if not top_folder:
            with driver.session() as session:
                session.run(
                    "match (top:Main_Folder)"
                    "create  (top) - [:Created_at{Created_at:datetime()}] -> (f {id:$folder_id})",
                    folder_id=folder_id)

        else:
            print(node.data)
            connect_file_or_folder_to_folder(folder_id, top_folder)


def connect_file_or_folder_to_folder(file_or_folder_id, top_folder_id):
    with driver.session() as session:
        node = session.run(
            "match (top:Folder {id:$top_folder_id}), "
            "(f {id:$file_or_folder_id}) "
            "create (top) - [:Created_at{Created_at:datetime()}] -> (f)",
            top_folder_id=top_folder_id,
            file_or_folder_id=file_or_folder_id)


def Create_File(file_name, content, top_folder):
    with driver.session() as session:
        node = session.run(
            "create (f:File {name:$file_name, "
            " content:$content,"
            " id: apoc.create.uuid(),"
            " created_at:datetime()})"
            " return f.id",
            file_name=file_name,
            content=content)
        node=node.data()[0]['f.id']
        if not top_folder:
            with driver.session() as session:
                session.run(
                    "match (top:Main_Folder)"
                    "create  (top) - [:Created_at{Created_at:datetime()}] -> (f {id:$node})",
                    node=node)
        else:
            connect_file_or_folder_to_folder(node, top_folder)


def show_what_inside_folder(folder_id):
    with driver.session() as session:
        node = session.run("match (f:Folder{id:$folder_id}) - [r] -> (p)"
                           " return p",
                           folder_id=folder_id)
        result = []
        for each in node.data():
            result.append(each['p'])
        return result


def get_folder_name():
    with driver.session() as session:
        node = session.run("match (f:Folder)"
                           " return f")
        result = []
        for each in node.data():
            result.append(each['f'])
        return result
