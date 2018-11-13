import matplotlib.pyplot as plt
import math

xAxis=[]
y1Axis=[]
y2Axis=[]

fig = plt.figure(figsize=(8,6))
fig.suptitle('Trig Functions')
ax1 = plt.subplot2grid((2,1),(0,0))
ax2 = plt.subplot2grid((2,1),(1,0))

for x in range (0,720):
	xAxis.append(x)

for y in range (0, 720):
	y1Axis.append(math.sin(math.radians(y)))
	y2Axis.append(math.cos(math.radians((y/10)*(y/10))))

for tick in ax1.xaxis.get_ticklabels():
	tick.set_rotation(90)

for tick in ax2.xaxis.get_ticklabels():
	tick.set_rotation(90)

plt.subplots_adjust(hspace = 0.5)
ax1.plot(xAxis, y1Axis,  'r-', label='Sine')
ax1.set_title('Sine')
ax2.plot(xAxis, y2Axis, label='Cos')
ax2.set_title('Cos Squared')
plt.ylabel('Value')
plt.xlabel('Range')
plt.legend()
plt.subplots_adjust(left=0.1, bottom = 0.1, right = 0.9, top = 0.9)
plt.show()