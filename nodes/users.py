from typing import Optional
import random
from app.services.neo4j import driver



def loginUser(userName,password):
    session = driver.session()
    query = "match (n {user_name:$username, password:$password}) return n as user"
    result = session.run(query,username=userName,password=password)
    user = {}
    for record in result:
        user['name'] = record['user']['name']
        user['user_name'] = record['user']['user_name']
        user['id']=record['user']['id']
        user['employee_id']=record['user']['employee_id']
        user['created_at']=record['user']['created_at']
        user['created_at']=record['user']['created_at']
    session.close()
    return user


