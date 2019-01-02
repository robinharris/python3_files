class device:
    def __init__(self, temperature, pressure, humidity, pm10, pm25, voc):
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.pm10 = pm10
        self.pm25 = pm25
        self.voc = voc


aq1 = device(None, None, None, None, None, None)
aq2 = device(None, None, None, None, None, None)

deviceDict = {"aq1": aq1, "aq2":aq2}
print(aq1.pm10)
aq1.pm10 = 30
aq2.pm10 = 60
print(aq1.pm10)
pointer = aq1
print(pointer.pm10)
key = 'aq2'
pointer = deviceDict[key]
print(deviceDict[key].pm10)