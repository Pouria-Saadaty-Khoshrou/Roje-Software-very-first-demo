from typing import Optional
import random
from app.services.neo4j import driver

import pandas as pd
import networkx as nx


def createExperiment(projectId, name):
    session = driver.session()
    query = "create (n:Experiment {id:apoc.create.uuid(), " \
            "name:$name, " \
            "created_at: datetime()}) " \
            "with n " \
            "match (p:Project {id:$projectId}) " \
            "with n,p " \
            "create (p)-[r:partOf {id:apoc.create.uuid()} ]->(n)"
    session.run(query, name=name, projectId=projectId)
    session.close()


def getExperimentById(id):
    session = driver.session()
    query = "match (experiment:Experiment {id:$id}) " \
            "WHERE not exists(experiment.deleted_at) " \
            "return experiment"
    # TODO: have to add protocols
    result = session.run(query, id=id)
    for each in result:
        experiment = {
            "name": each['experiment']['name'],
            "id": each['experiment']['id'],
            "created at": each['experiment']['created_at']
        }
    session.close()
    return experiment


def getTree(id: str):
    query = "match (n {id:$id})-[r*]->(en) return n,r,en"
    session = driver.session()
    result = session.run(query, id=id)
    data = []
    for each in result:
        data.append(each)
    session.close()

    x = data
    g = nx.DiGraph()
    our_dict = {}
    graph_dict = {}

    for each in x:
        g.add_node(each['en'].id)
        nx.set_node_attributes(g, {each['en'].id: list(each['en'].labels)}, name="label")
        nx.set_node_attributes(g, {each['en'].id: dict(each['en'])}, name="properties")

    rels = []
    for eachPath in x:
        for eachRel in eachPath['r']:
            reltup = (eachRel.nodes[0].id, eachRel.nodes[1].id)
            if reltup not in rels:
                rels.append(reltup)

    if len(x) != 0:

        g.add_node(x[0]['n'].id)
        nx.set_node_attributes(g, {x[0]['n'].id: list(x[0]['n'].labels)}, name="label")
        nx.set_node_attributes(g, {x[0]['n'].id: dict(x[0]['n'])}, name="properties")

        g.add_edges_from(rels)

        search_list = list(nx.bfs_tree(g, source=x[0]['n'].id).edges())

        root_node = x[0]['n'].id
        our_df = pd.DataFrame(search_list)

        # unique levels
        unique_levels = set(list(our_df[0]))

        level = 0
        our_dict[level] = [root_node]
        level = +1
        our_dict[level] = list(our_df.loc[our_df[0] == root_node][1])

        # our_dict[level + 1] = list(our_df[our_df[0].isin(our_dict[level])][1])
        # if len(our_dict[level+1]) == 0:
        #    print("x")
        while True:
            our_dict[level + 1] = list(our_df[our_df[0].isin(our_dict[level])][1])
            level += 1
            if len(list(our_df[our_df[0].isin(our_dict[level])][1])) == 0:
                break
        for each in our_dict:
            if len(our_dict[each]) != 0:
                graph_dict[each] = our_dict[each]

    return graph_dict, g


def getTree_Pouria(id: str, type):
    with driver.session() as session:
        result = session.run(f"match (n {{id:'{id}'}})-[r*]->(en:{type}) "
                             f"WHERE not exists(en.deleted_at) "
                             f"return n,r,en")
        data = []
        for each in result:
            data.append(each)

    x = data
    g = nx.DiGraph()
    our_dict = {}
    graph_dict = {}

    for each in x:
        g.add_node(each['en'].id)
        nx.set_node_attributes(g, {each['en'].id: list(each['en'].labels)}, name="label")
        nx.set_node_attributes(g, {each['en'].id: dict(each['en'])}, name="properties")

    rels = []
    for eachPath in x:
        for eachRel in eachPath['r']:
            reltup = (eachRel.nodes[0].id, eachRel.nodes[1].id)
            if reltup not in rels:
                rels.append(reltup)

    if len(x) != 0:

        g.add_node(x[0]['n'].id)
        nx.set_node_attributes(g, {x[0]['n'].id: list(x[0]['n'].labels)}, name="label")
        nx.set_node_attributes(g, {x[0]['n'].id: dict(x[0]['n'])}, name="properties")

        g.add_edges_from(rels)

        search_list = list(nx.bfs_tree(g, source=x[0]['n'].id).edges())

        root_node = x[0]['n'].id
        our_df = pd.DataFrame(search_list)

        # unique levels
        unique_levels = set(list(our_df[0]))

        level = 0
        our_dict[level] = [root_node]
        level = +1
        our_dict[level] = list(our_df.loc[our_df[0] == root_node][1])

        # our_dict[level + 1] = list(our_df[our_df[0].isin(our_dict[level])][1])
        # if len(our_dict[level+1]) == 0:
        #    print("x")
        while True:
            our_dict[level + 1] = list(our_df[our_df[0].isin(our_dict[level])][1])
            level += 1
            if len(list(our_df[our_df[0].isin(our_dict[level])][1])) == 0:
                break
        for each in our_dict:
            if len(our_dict[each]) != 0:
                graph_dict[each] = our_dict[each]

    return graph_dict, g


def find_project_by_experiment_id(id):
    with driver.session() as session:
        node = session.run("match (e:Experiment{id:$id}) <- [r:partOf] - (p:Project) "
                           "WHERE not exists(e.deleted_at) "
                           "return p.id",
                           id=id)
        result = []
        for each in node.data():
            result.append(each['p.id'])
        return result
