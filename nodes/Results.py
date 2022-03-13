from app.services.neo4j import driver


def existance_of_result_name(result_name):
    with driver.session() as session:
        node = session.run("match (r:Result {result_name:$result_name}) "
                           "WHERE not exists(r.deleted_at) "
                           "return r",
                           result_name=result_name)
        if not node.data():
            return False
        else:
            return True


def create_result(experiment_id, result_name, text):
    with driver.session() as session:
        node = session.run("match (e:Experiment {id:$experiment_id}) "
                           "create (r:Result {experiment_name:e.name, "
                           "result_name:$result_name, "
                           "id: apoc.create.uuid(), "
                           "created_at:datetime() ,"
                           "content:$text}) "
                           "create (e) - [:Created_at{Created_at:datetime()}] -> (r) "
                           "return r.id",
                           experiment_id=experiment_id,
                           text=text,
                           result_name=result_name)
        return node.data()[0]['r.id']


def find_result_by_experiment_id(experiment_id):
    with driver.session() as session:
        node = session.run("match (e:Experiment {id:$experiment_id}) - [rel] -> (r:Result) "
                           "WHERE not exists(r.deleted_at) "
                           " return r",
                           experiment_id=experiment_id)
        result = []
        for each in node.data():
            result.append(each['r'])
        return result


def format_seperator(result_id):
    all_paths = []
    videos = []
    images = []
    audios = []
    with driver.session() as session:
        node = session.run("match (u:Result{id:$result_id}) - [r] -> (f:File) "
                           "WHERE not exists(u.deleted_at) "
                           " return f",
                           result_id=result_id)
        node = node.data()
        image_formats = ['apng', 'gif', 'ico', 'cur', 'jpg', 'jpeg', 'jfif', 'pjpeg', 'pjp', 'png', 'svg']
        video_formats = ['mp4', 'webm', 'ogg']
        audio_formats = ['mp3', 'wav']
        for node in node:
            path = node['f']['path']
            if path.split('.')[-1] in image_formats:
                images.append(path.split('vendors\\')[-1].replace('\\', '/'))
                all_paths.append(path.split('vendors\\')[-1].replace('\\', '/'))
            elif path.split('.')[-1] in video_formats:
                videos.append(path.split('vendors\\')[-1].replace('\\', '/'))
                all_paths.append(path.split('vendors\\')[-1].replace('\\', '/'))
            elif path.split('.')[-1] in audio_formats:
                audios.append(path.split('vendors\\')[-1].replace('\\', '/'))
                all_paths.append(path.split('vendors\\')[-1].replace('\\', '/'))
            else:
                all_paths.append(path.split('vendors\\')[-1].replace('\\', '/'))
        # print('audios = ', audios)
        # print('images = ', images)
        # print('videos = ', videos)
        # print('all_paths = ', all_paths)
        return all_paths, videos, images, audios


def get_files_by_result_id(result_id):
    with driver.session() as session:
        node = session.run("match (u:Result{id:$result_id}) - [r] -> (f:File) "
                           "WHERE not exists(u.deleted_at) "
                           " return f",
                           result_id=result_id)
        result = []
        for each in node.data():
            result.append(each['f'])
        return result


def get_result_by_id(result_id):
    with driver.session() as session:
        node = session.run("match (r:Result{id:$result_id}) "
                           "WHERE not exists(r.deleted_at) "
                           " return r",
                           result_id=result_id)
        result = []
        for each in node.data():
            result.append(each['r'])
        return result

def give_path_by_file_id(file_id):
    with driver.session() as session:
        node = session.run("match (f:File{id:$file_id}) "
                           "WHERE not exists(f.deleted_at) "
                           " return f",
                           file_id=file_id)
        result = []
        for each in node.data():
            result.append(each['f'])
        return result

def get_experiment_by_result_id(id):
    with driver.session() as session:
        node = session.run("match (result:Result{id:$id}) <- [r:Created_at] - (e:Experiment) "
                           "WHERE not exists(result.deleted_at) "
                           "return e.id",
                           id=id)
        result = []
        for each in node.data():
            result.append(each['e.id'])
        return result