import subprocess,os
import calculate, draw
filepath='/home/hakem/Documents/AG/'
lines= list()
ips=list()
fin = open('/home/hakem/pox/pox/misc/lab_firewall.config')
p=[]
h=[]
vulports=list()
fwconfig=list()
for line in fin:
    fwconfig = line.split()
    if (len(fwconfig) > 0):
        lines.append(fwconfig)
        if (fwconfig[0] not in ips):
           ips.append(fwconfig[0])
        if (fwconfig[2] not in ips):
           ips.append(fwconfig[2])
        print (fwconfig)
print (ips)
v=1
for rule in lines:
    if (rule[3] not in vulports):

        p.append("vulProperty(" + "'" + "CVE-2011-143"+ str(v) + "'" + ",remoteExploit,privEscalation).")

        # p.append("vulExists(" + "'" + str(n) + ".0.0.1" + "'" + ",'" + "CVE-2012-0053" + "'" + ",http_server).")
        # p.append("vulExists(" + "'" + str(n) + ".0.0.1" + "'" + ",'" + "CVE-2013-2566" + "'" + ",safari).")
        p.append("vulExists(" + "'" + str(rule[2]) + "'" + ",'" + "CVE-2011-143" + str(v) + "'" + ",netqmail).")

        # p.append("cvss("+"'"+"CVE-2008-5161"+"'"+",h).")
        #         p.append("networkServiceInfo('"+str(n)+".0.0.1',http_server,tcp,"+"'"+str(80)+"'"+",someUser).")
        #         p.append("networkServiceInfo('" + str(n) + ".0.0.1',safari,tcp," + "'" + str(25) + "'" + ",someUser).")
        p.append("networkServiceInfo('" + str(rule[2]) + "'"+ ",netqmail,tcp," + "'" + str(rule[3]) + "'" + ",someUser).")
        # h.append("hacl(" + "'" + str(n) + ".0.0.1" + "'," + "'" + str(m) + ".0.0.1" + "',tcp,'" + str(P[t]) + "').")
        h.append("hacl(" + "'" + str(rule[0]) + "'," + "'" + str(rule[2])  + "',tcp,'" +str(rule[3])+ "').")
        # h.append("inCompetent(" + "'" + str(rule[2]) + "_victem'" + ").")
        # h.append("hasAccount(" + "'" + str(rule[2]) + "'," + "'" + str(rule[2]) + "', someuser).")
        # h.append("attackGoal(execCode(" + "'" + str(rule[2]) + "',_)).")
        v+=1
        vulports.append(rule[3])
origin=fwconfig[2]
# attacker=str(fwconfig[0])

# h.append("hacl(" + "'" + str(rule[0]) + "'," + "'" + str(rule[2])  + "',tcp,'" +str(rule[3])+ "').")
h.append("inCompetent(" + "'" + str(rule[2]) + "_victem'" + ").")
h.append("hasAccount(" + "'" + str(rule[2]) + "'," + "'" + str(rule[2]) + "', someuser).")
h.append("attackGoal(execCode(" + "'" + str(rule[2]) + "',_)).")


h.append("attackerLocated(Internet).")
# h.append("attackerLocated('" +attacker +"').")
h.append("hacl(internet,'"+str(ips[0]) +"',_,_).")
file=open(filepath+"hugeF.P","w")

file.writelines(p[x]+ '\n' for x in range(len(p)))
file.writelines(h[x]+ '\n' for x in range(len(h)))
# os.system('export MULVALROOT=/home/hakem/Desktop/mulval')
# os.system('export PATH="$MULVALROOT/utils/":$PATH')
# os.system('export PATH="$MULVALROOT/bin/":$PATH')
# os.system('export XSBROOT=/home/hakem/Desktop/XSB')
# os.system('export PATH="$XSBROOT/bin/":$PATH')
# os.system('export PATH="$XSBROOT/utils/":$PATH')
#
# cmd="cd "+filepath +" && graph_gen.sh hugeF.P -v -p"
#
# os.system(cmd)
# calculate.calcumprob()
# draw.JsonGen()