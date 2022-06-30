from operator import itemgetter
import networkx as nx
import numpy as np


def read_graph_query():
    '''This function reads the graph in the gpickle file and the query inputted via command line
    and returns the baseset, rootset, graph object, nodelist and edgelist'''
    graph = nx.read_gpickle("web_graph.gpickle")

    pgcont = []  # stores the pagecontent from networkx gpickle
    nodelist = list(graph.nodes)
    edgelist = list(graph.edges)

    for i in range(100):
        pgcont.append(graph.nodes[i]["page_content"])
    
    print(pgcont)
    exit()

    qr = input("Enter query:")

    root = []
    base = []

    for idx, pg in enumerate(pgcont):
        if pg.find(qr.lower()) != -1:
            base.append(idx)
            root.append(idx)

    for r in root:
        ins = graph.in_edges(r)
        outs = graph.out_edges(r)

        for i in ins:
            if i[0] not in base:
                base.append(i[0])

        for o in outs:
            if o[1] not in base:
                base.append(o[1])

    return graph, base, root, nodelist, edgelist


def get_adjmats(graph, base, edgelist):
    '''This function takes the graph object, baseset and list of edges as input
    and returns the adjacency matrix, transposed adjacency matrix and lists of outdegs and indegs'''
    AdjMat = []

    for b1 in base:
        tmp = []

        for b2 in base:
            if (b1, b2) in edgelist:
                tmp.append(1)
            else:
                tmp.append(0)
        AdjMat.append(tmp)

    outdeg = []
    indeg = []

    for b in base:
        outdeg.append(len(graph.out_edges(b)))
        indeg.append(len(graph.in_edges(b)))

    M = np.array(AdjMat)
    TransAdjMat = M.T

    return AdjMat, TransAdjMat, outdeg, indeg


def create_scores(base, TransAdjMat, AdjMat, outdeg, indeg):
    '''This function takes baseset, TransposedAdjacency matrix, Adjacency matrix, lists of outdegs and indegs
    and returns the hubs and authority scores'''
    hubs = np.ones(len(base))
    auths = np.ones(len(base))

    while True:
        auths = np.dot(TransAdjMat, hubs)
        auths = auths / np.linalg.norm(auths)

        hubs = np.dot(AdjMat, auths)
        hubs = hubs / np.linalg.norm(hubs)

        subhubs = np.subtract(outdeg, hubs)
        subauths = np.subtract(indeg, auths)

        chk = 0
        for x in subhubs:
            if abs(x) > 0.001:
                chk = 1

        for x in subauths:
            if abs(x) > 0.001:
                chk = 1

        if chk == 0:
            break
        else:
            outdeg = hubs
            indeg = auths

    hubsorted = []
    authsorted = []

    for ix, hub in enumerate(hubs):
        hubsorted.append([ix + 1, hub])

    for ix, auth in enumerate(auths):
        authsorted.append([ix + 1, auth])

    hubsorted = sorted(hubsorted, key=itemgetter(1), reverse=True)
    authsorted = sorted(authsorted, key=itemgetter(1), reverse=True)
    return hubsorted, authsorted


graph = nx.DiGraph()  # Graph object to store the graph in gpickle
base = []  # Base stores the baseset as a list
root = []  # Root stores the rootset as a list
nodes = []  # List to store the nodes in the graph
edges = []  # List to store the edges in the graph

graph, base, root, nodes, edges = read_graph_query()
# Stores the Adjacency Matrix, Transposed Adjacency Matrix and list of outdegs and indegs
AM, TAM, outdeg, indeg = get_adjmats(graph, base, edges)
# To Store the hub and authority scores
hubs, auths = create_scores(base, TAM, AM, outdeg, indeg)

print("Root set: ", root)
print("Base set: ", base)

print("Hub Scores:\nNode\tScore")  # Prints the hub scores for each node

for hub in hubs:
    print(base[hub[0] - 1], end="\t")
    print(hub[1], end="\n")

# Prints the authority scores for each node
print("Authority Scores:\nNode\tScore")

for auth in auths:
    print(base[auth[0] - 1], end="\t")
    print(auth[1], end="\n")
