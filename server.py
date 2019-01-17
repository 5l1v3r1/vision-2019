#"import time
from networktables import NetworkTables

# To see messages from networktables, you must setup logging
# import logging
# logging.basicConfig(level=logging.DEBUG)

NetworkTables.initialize()
sd = NetworkTables.getTable("datatable")
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")
    
i = 0
input = "false"
while True:
    # print('dsTime:', sd.getNumber('dsTime', 'N/A'))
    
    if(input == "true"):
        sd.putBoolean('visionTrigger',str2bool("true"))
    elif(input == "false"):
        sd.putBoolean('visionTrigger',str2bool("false"))
    # time.sleep(1)
    i += 1