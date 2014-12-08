__author__ = 'elpoohy'

import sched
import math
import datetime

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pymongo import MongoClient


scheduler = sched.scheduler()
cmdGen = cmdgen.CommandGenerator()
client = MongoClient('172.16.5.185', 27017)

db = client.prt

printers = db.printers


def snmp_read(ip):
    """

    :rtype : object
    """
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData('public', mpModel=0),
            cmdgen.UdpTransportTarget((ip, 161)),
            "1.3.6.1.2.1.43.11.1.1.8.1.1",
            "1.3.6.1.2.1.43.11.1.1.9.1.1")
#    print('Data for %s on %s' % (printer["model"], printer["ip"]))
    percent = 100*varBinds[1][1]/varBinds[0][1]
    await = int(18*math.sqrt(percent))

    print (percent, ip, datetime.datetime.utcnow())
    scheduler.enter(await,1,snmp_read,kwargs={'ip': ip})



def check_start():
    """

    :rtype : object
    """
    for printer in printers.find():
        try:
            ip = printer["ip"]
            snmp_read (ip)
        except KeyError:
            print("No IP for %s" % printer["model"])
    scheduler.run()


check_start()