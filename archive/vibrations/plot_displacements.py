import sys
#import os
sys.path.insert(0, 'E:/transfer/vibrations/pjabardo-pysignal-cf2a0351c330')
#filedir = os.path.dirname(os.path.realpath(__file__))
#print(filedir)
import pysignal as sig

from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import glob
import re

opfileh = open("plot_displacements_notes.txt", "w")

wavfilenames = []
filelist = glob.glob("*_x.wav")
for fname in filelist:
    kk = re.match("(^.*)_x\.wav$", fname)
    if kk:
        wavfilenames.append(kk.group(1))


max_acceleration=2.5   # g
output_resolution= 0.75 # 0.75 mm/s2 per LSB (5g/216)
lowcut = 1.0 # lower cut-off frequency for high-pass filter

def plot_displ(dataname):
    opfileh.write("plotting data {}\n".format(dataname))
    xfile = dataname + '_x.wav'
    yfile = dataname + '_y.wav'
    zfile = dataname + '_z.wav'
    
    try:
        sampfreq, x_acc = wavfile.read(xfile)
    except:
        opfileh.write("Error: cannot extract data from {}\n".format(xfile))
        xfile = False
    try:
        sampfreq, y_acc = wavfile.read(yfile)
    except:
        opfileh.write("Error: cannot extract data from {}\n".format(yfile))
        yfile = False
    try:
        sampfreq, z_acc = wavfile.read(zfile)
    except:
        opfileh.write("Error: cannot extract data from {}\n".format(zfile))
        zfile = False
 
    if not xfile and not yfile and not zfile:
        return
   
    if xfile:
        x_acc = x_acc.astype(float) * output_resolution
        x_acc_f = sig.hpfilter(x_acc, lowcut, sampfreq)
        npoints = len(x_acc)
    if yfile:
        y_acc = y_acc.astype(float) * output_resolution
        y_acc_f = sig.hpfilter(y_acc, lowcut, sampfreq)
        npoints = len(y_acc)
    if zfile:
        z_acc = z_acc.astype(float) * output_resolution
        z_acc_f = sig.hpfilter(z_acc, lowcut, sampfreq)
        npoints = len(z_acc)
    
    dt = 1.0/sampfreq
    
    starttime = 0
    endtime = starttime + (npoints -1 ) * dt
    tt = np.linspace(starttime, endtime, npoints)
    
    if False:
        plt.title(dataname)
        plt.xlabel("time (sec)")
        plt.ylabel("acceleration (mm/s2)")
        #if xfile: plt.plot(tt, x_acc, 'r', label='x')
        #if yfile: plt.plot(tt, y_acc, 'g', label='y')
        if zfile:
            plt.plot(tt, z_acc, 'b', label='z')
            plt.plot(tt, z_acc_f, 'g', label='z filtered')
        plt.legend(loc='best')
        plt.savefig(dataname+"_accel.png")
        plt.close()
    if True:
        plt.title(dataname)
        plt.xlabel("time (sec)")
        plt.ylabel("displacement (mm)")
        if xfile:
            x_disp = sig.integral(x_acc_f, 2, sampfreq)
            plt.plot(tt, x_disp, 'r', label='x')
        if yfile:
            y_disp = sig.integral(y_acc_f, 2, sampfreq)
            plt.plot(tt, y_disp, 'g', label='y')
        if zfile:
            z_disp = sig.integral(z_acc_f, 2, sampfreq)
            plt.plot(tt, z_disp, 'b', label='z')
        plt.legend(loc='best')
        plt.savefig(dataname+"_displ.png")
        plt.close()



for dataname in wavfilenames:
    plot_displ(dataname)


opfileh.close()
