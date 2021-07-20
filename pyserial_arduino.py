import matplotlib.pyplot as plt
import numpy as np
import serial

y = []
u = []
t = []

ang_ref = 90
Tend = 3
uref = 2
ang = 0

with serial.Serial('COM6',115200,timeout=1) as ser:
    while ser.isOpen() == True:

        uref = 0
        if ang_ref - ang > 0:
            uref = 3
        if ang_ref - ang < 0:
            uref = -3
        
        msg = str(uref) + 'e'
        ser.write(msg.encode())
        ser.flush()

        buf = ser.readline().decode('utf8').strip()
        line = buf.split()
        if len(line) > 2:
            ang = float(line[1])
            t = np.append(t,float(line[0]))
            y = np.append(y,float(line[1]))
            u = np.append(u,float(line[2]))

            if float(line[0]) >= Tend:
                break
    ser.close()
fig,ax=plt.subplots(1,2)
ax[0].plot(t,y)
ax[0].axhline(ang_ref,color="k",linewidth=0.5)
ax[1].plot(t,u)
fig.tight_layout()
    
