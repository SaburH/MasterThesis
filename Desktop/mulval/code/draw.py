import pandas as pd
import csv
import array
import numpy as np
import json
p=[]
# f = pd.read_csv("/home/hakem/ag/d3/ARCS.CSV")
PATH='/home/hakem/Documents/AG/'
def JsonGen():
    with open(PATH+'ARCS1.CSV', 'w') as out:
        writer = csv.writer(out)
        writer.writerow(["source", "Destination", 'dump'])
        with open(PATH+'ARCS.CSV', 'rb') as incsv:
            reader=csv.reader(incsv)
            writer.writerows(row  for row in reader)
    x=pd.read_csv(PATH+'ARCS1.CSV')
    x.index.name = 'number'
    x=x.drop(columns='dump')
    final1=x.to_csv(PATH+'ARCS2.CSV', index=True)
    final1=pd.read_csv(PATH+'ARCS2.CSV')
    for i in range(len(final1)):
        final1['source'][i]-=1
        final1['Destination'][i]-=1


    with open(PATH+'myfile1.CSV', 'w') as out1:
        writer = csv.writer(out1)
        writer.writerow(["id", "type", 'probability'])
        with open(PATH+'myfile.CSV', 'rb') as incsv1:
            reader=csv.reader(incsv1)
            writer.writerows(row  for row in reader)
    y=pd.read_csv(PATH+'myfile1.CSV')
    y.index.name = 'number'
    final=y.to_csv(PATH+'NewVERTICES.CSV', index=True)
    final=pd.read_csv(PATH+'NewVERTICES.CSV')

    # res = pd.merge(final, final1, on='number')
    # res1 = pd.read_csv("/home/hakem/ag/d3/final.csv")
    for i in range(len(final)):
        if final['type'][i] == "OR":
            final['type'][i] = "diamond"
        elif final['type'][i] == "AND":
            final['type'][i] = "circle"
        else:
            final['type'][i] = "square"


    ###############################
    # p.append("{" + '\n' + '  "graph": [],' + '\n' + '  "links": ['+ '\n')
    # for i in range(len(final1) - 1):
    #     p.append('    {"source": ' + str(final1['source'][i]) + ',' + ' "target": ' + str(final1['Destination'][i]) + '},' +  '\n')
    #
    # p.append('    {"source": ' + str(final1['source'][i+1]) + ',' + ' "target": ' + str(final1['Destination'][i+1]) + '}],' +   '\n' + '  "nodes": [')
    #
    # for t in range(len(final)-1 ):
    #     p.append('    {"size": ' + '70, ' + '"score": ' + str(final["probability"][t]) + ',' + ' "id": "' + str(
    #         final["id"][t]) + '",' + ' "type": "' + str(final["type"][t]) + '"},' + '\n' )
    # p.append('    {"size": ' + '70, ' + '"score": ' + str(final["probability"][t+1]) + ',' + ' "id": "' + str(
    #     final["id"][t+1]) + '",' + ' "type": "' + str(final["type"][t+1]) + '"}],' + '\n')
    #
    # # p.append('{"id": "Intruder", "type": "square"}],' + '\n')
    # p.append('"directed": false, ' + '\n' + '"multigraph": false ' + '\n' + '}')

    p.append("{"  + '  "graph": [],'  + '  "links": [' )
    for i in range(len(final1) - 1):
        p.append('    {"source": ' + str(final1['source'][i]) + ',' + ' "target": ' + str(
            final1['Destination'][i]) + '},' )

    p.append('    {"source": ' + str(final1['source'][i + 1]) + ',' + ' "target": ' + str(
        final1['Destination'][i + 1]) + '}],'  + '  "nodes": [')

    for t in range(len(final) - 1):
        p.append('    {"size": ' + '150, ' + '"score": ' + str(final["probability"][t]) + ',' + ' "id": "' + str(
            final["id"][t]) + '",' + ' "type": "' + str(final["type"][t]) + '"},' )
    p.append('    {"size": ' + '150, ' + '"score": ' + str(final["probability"][t + 1]) + ',' + ' "id": "' + str(
        final["id"][t + 1]) + '",' + ' "type": "' + str(final["type"][t + 1]) + '"}],' )

    # p.append('{"id": "Intruder", "type": "square"}],' + '\n')
    p.append('"directed": false, '  + '"multigraph": false '  + '}')

    test = open(PATH+"graph.json", 'w')
    test.truncate()
    for q in range(len(p)):
        test.writelines(p[q])

    test.close()
    return p
# JsonGen()




#
# csvfile = open("/home/hakem/ag/d3/finaloutput.csv", "r")
# jsonfile = open("/home/hakem/ag/d3/isittheone.json", "w")
# fieldnames = ("Source", "Destination")
# reader = csv.DictReader(csvfile, fieldnames)
# for row in reader:
#     json.dump(row, jsonfile)
#     jsonfile.write('\n')
# fieldnames1 = ("id","type","probability")
# reader1 = csv.DictReader(csvfile,fieldnames)
# for row1 in reader1:
#    json.dump(row1,jsonfile)
#    jsonfile.write('\n')






