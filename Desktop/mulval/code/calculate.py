import networkx as nx
import matplotlib.pyplot as plt
import xml.etree.cElementTree as ET
import pandas as pd
import draw
# app = Flask(__name__)

PATH='/home/hakem/Documents/AG/'
# @app.route('/')
def calcumprob(filename=PATH+"AttackGraph.xml", alpha=0.5):
    prob = []
    list1 = []
    prob_for_node = {}
    from pymongo import MongoClient
    client = MongoClient()
    db = client.cvedb
    collection = db.cves

    G = nx.DiGraph()
    tree = ET.parse(filename)
    root = tree.getroot()
    vertices = root.find('vertices')
    arcs = root.find('arcs')
    leafs = []
    vulnodes = []
    delta = []
    cveids = []
    output = []


    for arc in arcs.findall('arc'):
        # print (arc.find('src').text,arc.find('dst').text)
        if arc.find('dst').text != "1":
            G.add_edge(arc.find('src').text, arc.find('dst').text)

    for vertex in vertices:
        # print (vertex.find('id').text,vertex.find('fact').text,
        # vertex.find('metric').text,vertex.find('type').text)
        if vertex.find('type').text == 'LEAF':
            if 'attackerLocated' in vertex.find('fact').text:
                attacker = vertex.find('id').text
            else:
                leafs.append(vertex.find('id').text)

        basescore = 1  # do not move from here

        # Following code is not needed but it helps in undrestanding and making changess
        if vertex.find('type').text == 'OR':
            basescore = 1

        if vertex.find('type').text == 'AND':
            basescore = 1

        if vertex.find('type').text == 'LEAF':
            basescore = alpha

        if 'vulExists' in vertex.find('fact').text:
            fact = vertex.find('fact').text.split(',')
            vul = collection.find_one({"id": fact[1].replace("'", "")})
            basescore = vul.get('cvss', -1) / 10
            vertex.set('score', basescore)
            vulnodes.append(vertex.find('id').text)
            cveids.append(vertex.find('id').text + ': ' + vul.get('id'))

        G.add_node(vertex.find('id').text, fact=vertex.find('fact').text,
                   metric=vertex.find('metric').text, type=vertex.find('type').text,
                   basescore=basescore, solved=False)

    G.nodes(data=True)
    G.remove_node(attacker)

    G = G.reverse(True)
    # use only copies of actual graph
    G1 = G.copy()

    prob1 = solve(G1, '1', [], [],output, list1, prob_for_node, prob)

    for item in output:
        print (item)

    # calcuate delta
    # for vul in vulnodes:
    #     G2 = G.copy()
    #     G2.node[vul]['basescore'] = 0.005
    #     tdelta = prob1 - solve(G2, '1', [],[],output)
    #     delta.append({'vul': vul, 'delta': tdelta})

    # print(list(delta))
    # maxdelta = max(delta, key=lambda x: x['delta'])

    nx.draw(G, with_labels=True)

    # cveid = ''
    # for item in cveids:
    #     if maxdelta['vul'] in item:
    #         cveid = item

    csvfile=PATH+"VERTICES.CSV"
    df=pd.read_csv(csvfile, header=None,index_col=0)

    # import json
    # with open('/home/hakem/ag/jsonoutput.txt', 'w+') as outfile:
        # json.dump(output, outfile)

    nod = df.index.values
    for i in nod:

        if not bool(prob_for_node.get(str(i))):
            prob_for_node[str(i)]=0
        list1.append(prob_for_node[str(i)])
    df[3]=list1
    df.to_csv(PATH+'myfile.CSV',header=None)
    #draw.JsonGen()
    return ('done')
    # return jsonify(output,{"Cumulative Probability":prob1},{"CVEID":cveid})


def solve(G, node, coverednodes, path,output, list1, prob_for_node, prob):
    if node in coverednodes:
        return G.node[node]['basescore']
    else:
        coverednodes.append(node)
        path.append(node)
    print('{} : {}'.format(node, G.node[node]['type']))

    # Code to find and return prob of a LEAF node
    if G.node[node]['type'] == "LEAF":
        # Flag to say if vulnerability exists
        vx = "Not a VulExists"
        if "vulExists" in G.node[node]['fact']:
            vx = "VulExists"

        dicto = {"Path":','.join(map(str, coverednodes)),"Probability":G.node[node]['basescore'],"Type":G.node[node]['type'],"Property":vx}
        output.append(dicto)
        coverednodes.pop()
        dicto1 = {"id": (node), "Probability":  round(G.node[node]['basescore'],3)}
        prob.append(dicto1)
        # Save and send
        prob_for_node[node] = G.node[node]['basescore']
        return round(G.node[node]['basescore'],3)

    # Code to find and return prob of an OR node
    if G.node[node]['type'] == "OR":
        for predecessor in sorted(G.predecessors(node)):
            try:
                G.node[node]['basescore'] = (G.node[node]['basescore']) * (
                            1 - prob_for_node[predecessor])
            except KeyError:
               G.node[node]['basescore'] = (G.node[node]['basescore'])*(1-solve(G,predecessor,coverednodes,path,output, list1, prob_for_node, prob))

        dicto = {"Path": ','.join(map(str, coverednodes)), "Probability": 1 - round(G.node[node]['basescore'],3), "Type": G.node[node]['type'],
                 "Property": "Rule"}
        coverednodes.pop()
        # Save and send
        prob_for_node[node] = 1 - round(G.node[node]['basescore'],3)
        return 1 - round(G.node[node]['basescore'],3)

    # Code to find and return prob of a AND node
    for predecessor in sorted(G.predecessors(node)):
        try:
            G.node[node]['basescore'] = round(G.node[node]['basescore']) * (prob_for_node[predecessor])
        except KeyError:
            G.node[node]['basescore'] = round(G.node[node]['basescore'])*(solve(G,predecessor,coverednodes,path,output, list1, prob_for_node, prob))

    dicto = {"Path": ','.join(map(str, coverednodes)), "Probability": round(G.node[node]['basescore'], 3),
             "Type": G.node[node]['type'],
             "Property": "Rule"}

    # prob.append(str(round(G.node[node]['basescore'], 3))+" "+str(node))
    coverednodes.pop()

    # Save and send
    prob_for_node[node] = round(G.node[node]['basescore'],3)
    return round(G.node[node]['basescore'],3)


# if __name__ == '__main__':
    # app.run(port=8080)
# calcumprob()
    # print("=====\n{}\n=====\n".format(prob_for_node))