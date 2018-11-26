#
import subprocess,os


i=250
# file=open("/home/hakem/Desktop/"+str(i)+"/before.P","w")
file=open("/home/hakem/Desktop/case4/"+str(i)+"/"+str(i)+"after.P","w")
y=80
v=5
p=[]
h=[]
n=201
m=202
P=[]
for x in range(v):
    P.append(y+x)
    print P[x]
for x in range(i):

    # for t in range(v):
    #     p.append("vulProperty(" + "'" + "CVE-2012-0053" + "'" + ",remoteExploit,privEscalation).")
        p.append("vulProperty(" + "'" + "CVE-2013-2566" + "'" + ",remoteExploit,privEscalation).")
        p.append("vulProperty(" + "'" + "CVE-2011-0411" + "'" + ",remoteExploit,privEscalation).")
        # p.append("vulProperty(" + "'" + "CVE-2011-1431" + "'" + ",remoteExploit,privEscalation).")
        # p.append("vulProperty(" + "'" + "CVE-2011-1557 " + "'" + ",remoteExploit,privEscalation).")

        # p.append("vulExists(" + "'" + str(n) + ".0.0.1" + "'" + ",'" + "CVE-2012-0053" + "'" + ",http_server).")
        p.append("vulExists(" + "'" + str(n) + ".0.0.1" + "'" + ",'" + "CVE-2013-2566" + "'" + ",safari).")
        p.append("vulExists(" + "'" + str(n) + ".0.0.1" + "'" + ",'" + "CVE-2011-0411" + "'" + ",postfix).")
        # p.append("vulExists(" + "'" + str(n) + ".0.0.1" + "'" + ",'" + "CVE-2011-1431" + "'" + ",netqmail).")
        # p.append("vulExists(" + "'" + str(n) + ".0.0.1" + "'" + ",'" + "CVE-2011-1557" + "'" + ",mail).")

# p.append("cvss("+"'"+"CVE-2008-5161"+"'"+",h).")
#         p.append("networkServiceInfo('" + str(n) + ".0.0.1',mail_server,tcp," + "'" + str(10) + "'" + ",someUser).")
#         p.append("networkServiceInfo('"+str(n)+".0.0.1',http_server,tcp,"+"'"+str(80)+"'"+",someUser).")
        p.append("networkServiceInfo('" + str(n) + ".0.0.1','safari',tcp,'"  + str(25) + "',someUser).")
        p.append("networkServiceInfo('" + str(n) + ".0.0.1','postfix',tcp,'"  + str(27) +"',someUser).")
        # p.append("networkServiceInfo('" + str(n) + ".0.0.1','netqmail',tcp,'"  + str(14) + "',someUser).")

# h.append("hacl(" + "'" + str(n) + ".0.0.1" + "'," + "'" + str(m) + ".0.0.1" + "',tcp,'" + str(P[t]) + "').")
#         h.append("hacl(" + "'" + str(n) + ".0.0.1" + "'," + "'" + str(m) + ".0.0.1" + "','tcp',80"  + ").")
        h.append("hacl(" + "'" + str(n) + ".0.0.1" + "'," + "'" + str(m) + ".0.0.1" + "','tcp',25" + ").")
        h.append("hacl(" + "'" + str(n) + ".0.0.1" + "'," + "'" + str(m) + ".0.0.1" + "','tcp',27" + ").")
        # h.append("hacl(" + "'" + str(n) + ".0.0.1" + "'," + "'" + str(m) + ".0.0.1" + "','tcp',14" + ").")
# y=y+1
        n=n+1
        m=m+1
        # y=22
n=201
m=202
# h.append("hacl(Internet,_,_,_).")
h.append("attackerLocated(Internet).")
h.append("hacl(internet,'201.0.0.1',_,_).")


for x in range(i):
    h.append("inCompetent(" +"'"+str(n)+".0.0.1_victem'" + ").")
    h.append("hasAccount("  +"'"+str(n)+".0.0.1" + "',"  +"'"+str(n)+".0.0.1'"+", someuser).")
    h.append("attackGoal(execCode(" +"'"+str(n)+".0.0.1" +"',_)).")
    n=n+1
    m=m+1

# for x in range((i)):



for x in range(len(p)):
    file.writelines(p[x] + '\n')
for x in range(len(h)):
    file.writelines(h[x] + '\n')
file.close()

# from timeit import default_timer as timer
#
# start = timer()
# os.system("cd ~/Desktop/ && graph_gen.sh huge4.P -v -p ")
# end = timer()
# print(end - start)

# import time
#
# start = time.time()
# end = time.time()
# print(end - start)