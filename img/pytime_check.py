#!/usr/bin/python
#coding=utf-8
import sys,re,time,os
maxdata = 1024000 #单位B
memfilename = '/tmp/newnetcardtransdata.txt'
netcard = '/proc/net/dev'
def checkfile(filename):
    if os.path.isfile(filename):
        pass
    else:
        f = open(filename, 'w')
        f.write('0')
        f.close()
def get_net_data():
    nc = netcard or '/proc/net/dev'
    fd = open(nc, "r")
    netcardstatus = False
    for line in fd.readlines():
        if line.find("eth0") > 0:
            netcardstatus = True
            field = line.split()
            recv = field[0].split(":")[1]
            recv = recv or field[1]
            send = field[8]
    if not netcardstatus:
        fd.close()
        print 'Please setup your netcard'
        sys.exit()
    fd.close()
    return (float(recv), float(send))
    
def net_loop():
    (recv, send) = get_net_data()
    checkfile(memfilename)
    lasttransdaraopen = open(memfilename,'r')
    lasttransdata = lasttransdaraopen.readline()
    lasttransdaraopen.close()
    totaltrans = int(lasttransdata) or 0
    while True:
        time.sleep(3)
        nowtime = time.strftime('%d %H:%M',time.localtime(time.time()))
        sec = time.localtime().tm_sec
        if nowtime == '27 15:53':
            if sec < 10:
                totaltrans = 0
        (new_recv, new_send) = get_net_data()
        recvdata = new_recv - recv
        print recvdata
        recv = new_recv
        senddata = new_send - send
        print senddata
        send = new_send
        totaltrans += int(recvdata)
        totaltrans += int(senddata)
        memw = open(memfilename,'w')
        memw.write(str(totaltrans))
        memw.close()
        print totaltrans / 1024
        if totaltrans >= maxdata:
            os.system('init 0')
if __name__ == "__main__":
    net_loop()
