import Adafruit_DHT
DHT_TYPE = Adafruit_DHT.DHT22

def read(addr):
    humidity, temp = Adafruit_DHT.read(DHT_TYPE, addr)
    if not humidity or not temp:
        return None
    return (temp, humidity)
