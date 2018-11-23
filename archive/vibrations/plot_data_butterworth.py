from scipy.io import wavfile
from scipy.integrate import cumtrapz
#from scipy.signal import detrend
from scipy.signal import butter, lfilter


import matplotlib.pyplot as plt
import numpy as np


# http://wiki.scipy.org/Cookbook/ButterworthBandpass
def butter_highpass(lowcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    b, a = butter(order, low, btype='highpass')
    return b, a


def butter_highpass_filter(data, lowcut, fs, order=5):
    b, a = butter_highpass(lowcut, fs, order=order)
    y = lfilter(b, a, data)
    return y



dataname = "2014-06-19_23,29,39"

xfile = dataname + '_x.wav'
yfile = dataname + '_y.wav'
zfile = dataname + '_z.wav'

max_acceleration=2.5   # g
output_resolution= 0.75 # 0.75 mm/s2 per LSB (5g/216)

lowcut = 1.0 # lower cut-off frequency for high-pass filter
filterorder = 6

sampfreq, x_acc = wavfile.read(xfile)
sampfreq, y_acc = wavfile.read(yfile)
sampfreq, z_acc = wavfile.read(zfile)

x_acc = x_acc.astype(float) * output_resolution
y_acc = y_acc.astype(float) * output_resolution
z_acc = z_acc.astype(float) * output_resolution

dt = 1.0/sampfreq

starttime = 0
npoints = len(x_acc)
endtime = starttime + (npoints -1 ) * dt
tt = np.linspace(starttime, endtime, npoints)

#x_vel = cumtrapz(x_acc, tt)
#y_vel = cumtrapz(y_acc, tt)
#z_vel = cumtrapz(z_acc, tt)
fltred = butter_highpass_filter(x_acc, lowcut, sampfreq, order=filterorder)
x_vel = cumtrapz(fltred, tt)
fltred = butter_highpass_filter(y_acc, lowcut, sampfreq, order=filterorder)
y_vel = cumtrapz(fltred, tt)
fltred = butter_highpass_filter(z_acc, lowcut, sampfreq, order=filterorder)
z_vel = cumtrapz(fltred, tt)



if False:
    tt = np.linspace(starttime, endtime, npoints)
    plt.title(dataname)
    plt.xlabel("sec")
    plt.ylabel("mm/s2")
    plt.plot(tt, x_acc, 'r', label='x')
    plt.plot(tt, y_acc, 'g', label='y')
    plt.plot(tt, z_acc, 'b', label='z')
    plt.legend(loc='best')


if False:
    plt.title(dataname)
    plt.xlabel("sec")
    plt.ylabel("mm/s")
    plt.plot(tt[:-1], x_vel, 'r', label='x')
    plt.plot(tt[:-1], y_vel, 'g', label='y')
    plt.plot(tt[:-1], z_vel, 'b', label='z')
    plt.legend(loc='best')


if True:
    fltred = butter_highpass_filter(x_vel, lowcut, sampfreq, order=filterorder)
    x_disp = cumtrapz(fltred, tt[:-1])
    fltred = butter_highpass_filter(y_vel, lowcut, sampfreq, order=filterorder)
    y_disp = cumtrapz(fltred, tt[:-1])
    fltred = butter_highpass_filter(z_vel, lowcut, sampfreq, order=filterorder)
    z_disp = cumtrapz(fltred, tt[:-1])
    plt.title(dataname)
    plt.xlabel("sec")
    plt.ylabel("mm")
    plt.plot(tt[:-2], x_disp, 'r', label='x')
    plt.plot(tt[:-2], y_disp, 'g', label='y')
    plt.plot(tt[:-2], z_disp, 'b', label='z')
    plt.legend(loc='best')


