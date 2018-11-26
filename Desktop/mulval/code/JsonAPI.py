import json
import pandas as pd
from flask import Flask, request,jsonify
from flask_restful import Resource, Api,reqparse
import requests
import subprocess,os
from lxml import etree
import xmltodict
import calculate
from sqlalchemy import create_engine
import draw
import csv

app = Flask(__name__)
api = Api(app)

@app.route('/graphGen', methods=['GET'])
def graphGen():
    engine = create_engine('mysql+mysqlconnector://root:1111@localhost:3306/nvd', echo=False)
    filename = "/home/hakem/Desktop/newJson.json"
    path = "/home/hakem/ag/d3/"
    out = "output.P"
    data = pd.read_json(filename)
    # df =pd.DataFrame(pd.read_json(filename)['tenant_id']['hosts']['ip'] )
    li = []
    hosts = []
    for item in data["systems"]:
        hosts.append(item['floating_ip'])
        for host in item["services"]:
            for CVE in host["vulnerability"]:

                if (CVE['cve_ids'] != 'NOCVE'):
                    li.append([item['floating_ip'], CVE['cve_ids'], CVE['cvss_score'], host['port'], host['protocol'],
                               host['name']])

    df = pd.read_sql("select * from nvd", engine)
    df.to_csv("/home/hakem/Desktop/all.csv")
    b = [i[1] for i in li]
    df = df[df.id.isin(b)]


    file = open(path+out, "w")


    scan_res = pd.DataFrame(li, columns=['ip', 'id', 'score', 'port', 'protocol', 'service_name'])
    final = pd.merge(df, scan_res)
    p = []

    for index, row in final.iterrows():
        p.append('cvss(' + "'" + row['id'] + "'" + ',' + row['access'] + ').')
        p.append('vulProperty(' + "'" + row['id'] + "'" + ',' + row['rng'][
                                                                1:len(row['rng']) - 1] + ',' + 'privEscalation' + ').')

        p.append('networkServiceInfo(' + "'" + row['ip'] + "'" + ',' + "'" + row['soft'].strip('.') + "'" + ',' + row[
            'protocol'] + ',' + "'" + str(row['port']) + "'" + ',' + 'someuser' + ').')
        p.append('vulExists(' + "'" + row['ip'] + "'" + ',' + "'" + row['id'] + "'" + ',' + "'" + row['soft'].strip(
            '.') + "'" + ').')
    for i in range(len(hosts)):
        victem = "'" + hosts[i] + "_victem'"
        p.append("inCompetent(" + victem + ").")
        p.append("hasAccount(" + victem + ",'" + hosts[i] + "', user).")
        p.append("attackerLocated(Internet).")
        p.append("attackGoal(execCode('" + hosts[i] + "', _)).")
    p.append('hacl(_,_,_,_).')

    for i in range(len(p)):
        file.writelines(p[i] + '\n')

    file.close()
    cmd="cd "+path+" && /home/hakem/Desktop/mulval/utils/graph_gen.sh "+out +" -v"
    os.system(cmd)

    calculate.calcumprob()
    outputF=draw.JsonGen()
    #returning the JSON file of the Attack graph, you can find the pdf file as well in the path where you run mulval
    xml =open(path+"AttackGraph.xml")
    jsonString=json.dumps(xmltodict.parse(xml), indent=4)
    yy=json.dumps(outputF, indent=4)
    return str(outputF)

@app.route('/ARCS', methods=['GET'])
def getARCS():
    # Open the CSV
    f = open('/home/hakem/Downloads/masterproject/ARCS.CSV')
    reader = csv.DictReader(f)
    # Parse the CSV into JSON
    # reader = reader.drop(columns='dump')

    out = json.dumps([row for row in reader])
    print "JSON parsed!"
    # Save the JSON
    f = open('/home/hakem/Downloads/masterproject/ARCS.json', 'w')
    f.write(out)
    print "JSON saved!"


    return out

@app.route('/VERTICES', methods=['GET'])
def getVERTICES():
    # Open the CSV
    f = open('/home/hakem/Downloads/masterproject/VERTICES.CSV')
    # Change each fieldname to the appropriate field name. I know, so difficult.
    reader = csv.DictReader(f, fieldnames=("Index", "Node", "type", "prob"))
    # Parse the CSV into JSON
    # reader = reader.drop(columns='dump')
    out = json.dumps([row for row in reader])
    print "JSON parsed!"
    # Save the JSON
    # f = open('/home/hakem/Downloads/masterproject/Vertices..json', 'w')
    # f.write(out)
    print "JSON saved!"

    # file = json.load(f)

    return out

#api.add_resource(readJ, '/graphGen', methods=['GET'])
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000, debug=True)