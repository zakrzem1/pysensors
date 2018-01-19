
def getTemperature(oneWireDeviceAddress):
    w1="/sys/bus/w1/devices/"+oneWireDeviceAddress+"/w1_slave"
    raw = open(w1, "r").read()
    splitted = raw.split("t=")
    return float(float(splitted[-1])/1000)

def read(addr):
    return (getTemperature(addr),)
