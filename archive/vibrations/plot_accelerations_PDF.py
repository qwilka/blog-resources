from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

# http://matplotlib.org/examples/pylab_examples/multipage_pdf.html
from matplotlib.backends.backend_pdf import PdfPages




datanames = ["2014-06-19_23,29,39", "2014-06-19_22,29,40"]



max_acceleration=2.5   # g
output_resolution= 0.75 # 0.75 mm/s2 per LSB (5g/216)


def plot_accels(dataname):
    xfile = dataname + '_x.wav'
    yfile = dataname + '_y.wav'
    zfile = dataname + '_z.wav'
    
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
    
    tt = np.linspace(starttime, endtime, npoints)
    plt.title(dataname)
    plt.xlabel("sec")
    plt.ylabel("mm/s2")
    plt.plot(tt, x_acc, 'r', label='x')
    plt.plot(tt, y_acc, 'g', label='y')
    plt.plot(tt, z_acc, 'b', label='z')
    plt.legend(loc='best')
    #plt.savefig("ttest.pdf", papertype='a4')
    plt.savefig()
    plt.close()


with PdfPages('multipage_pdf.pdf') as pdf:
    for dataname in datanames:
        plot_accels(dataname)
