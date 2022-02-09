from os import path
import networkx as nx
from networkx.readwrite import json_graph
import json
from flask import Flask, render_template, jsonify
from super_stable_matching import main_session
basepath = path.dirname(__file__)
app = Flask(__name__)

def graph_to_dict(graph):
    '''
    Returns a dictionary representation of the given graph.
    '''
    return json_graph.node_link_data(graph)


def d3_format(graph_dict):
    '''
    Formats a graph dictionary for d3 visualization
    '''
    graph_dict.pop("multigraph")
    graph_dict.pop("directed")
    graph_dict.pop("graph")
    return graph_dict

def export_json(dictionary):
    '''
    Exports the given dictionary to a json file.
    '''
    filepath = path.abspath(path.join(basepath, "static", "json", "graph.json"))
    with open(filepath, 'w') as file:
        json.dump(dictionary, file, indent=4, default=lambda x: x.__dict__)


def create_matching_graph():
    res = main_session()
    print("Start Creating Graph")
    G = nx.Graph()
    index = 0
    for i in res:
        [pa, pb] =  i          
        G.add_node(index, name=pa, man=pa, woman=pb, bipartite=0)
        G.add_node(index+1, name=pb, man=pa, woman=pb, bipartite=1)
        G.add_edge(index, index+1)
        index += 2
    graph_dict = graph_to_dict(G)
    d3_graph_dict = d3_format(graph_dict)
    return d3_graph_dict

@app.route('/superStableMatching')
def superStableMatching():
    # client will ask for graph data from /data route
    return render_template("superStableMatching.html")


@app.route('/data')
def get_data():
    # create a random graph and return json via flask
    d3_graph_dict = create_matching_graph()
    return jsonify(dict(data=d3_graph_dict))


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    host_name = 'localhost'
    port_num = 5000
    app.run(debug=True, host=host_name, port=port_num)