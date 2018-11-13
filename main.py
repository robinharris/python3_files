import t1
import wifi
import time
import network
# ÷flashLED(10, 250)
# print("Before calling wifi: ", sta.ifconfig())
print("After calling wifi: ", wifi.wifiConnect())

import machine
pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 4, 5, 12, 13, 14, 15)]
p2 = machine.Pin(2, machine.Pin.OUT)
pwm = machine.PWM(p2)
pwm
pwm.freq = (0.3)
pwm.duty = (500)

html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pins</title> </head>
    <body> <h1>ESP8266 Pins</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""

import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()