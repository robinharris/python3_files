def wifiConnect():
	import network
	sta = network.WLAN(network.STA_IF)
	sta.active(True)
	sta.connect("Kercem2", "E0E3106433F4")
	return(sta.ifconfig())


print(sta.ifconfig)
sta.status()
sta.isconnected()

