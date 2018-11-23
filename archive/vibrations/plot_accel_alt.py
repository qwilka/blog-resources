#from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import glob
import re
import struct

def extract_wav_data(filename):
    fid = open(filename, 'rb')
    str1 = fid.read(4)
    if str1 == b'RIFF':
        print("{} is RIFF".format(filename))
    print(str1)
    print(str1.decode("utf-8"))
    fmt = '<I'
    fsize = struct.unpack(fmt, fid.read(4))[0] + 8
    print("fsize = {} ".format(fsize))
    str2 = fid.read(4)
    if str2 == b'WAVE':
        print("{} is WAVE".format(filename))
    print(str2)
    while (fid.tell() < fsize):
        chunk_id = fid.read(4)
        if chunk_id == b'fmt ':
            fmt = '<'
            res = struct.unpack(fmt+'iHHIIHH',fid.read(20))
            size, comp, noc, rate, sbytes, ba, bits = res
        elif chunk_id == b'data':
            fmt = '<i'
            size = struct.unpack(fmt,fid.read(4))[0]
            print("size = {} ".format(size))
            _bytes = bits//8
            dtype = '<'
            dtype += 'i%d' % _bytes
            start = fid.tell()
            data = np.fromstring(fid.read(size), dtype=dtype)
            fid.seek(start + size)                         
        else:
            print("Cannot handle this!!")
            continue
    fid.close()
    return rate, data 


opfileh = open("plot_accelerations_notes.txt", "w")

wavfilenames = []
filelist = glob.glob("*_x.wav")
for fname in filelist:
    kk = re.match("(^.*)_x\.wav$", fname)
    if kk:
        wavfilenames.append(kk.group(1))


max_acceleration=2.5   # g
output_resolution= 0.75 # 0.75 mm/s2 per LSB (5g/216)


def plot_accels(dataname):
    opfileh.write("plotting data {}\n".format(dataname))
    xfile = dataname + '_x.wav'
    yfile = dataname + '_y.wav'
    zfile = dataname + '_z.wav'
    
    try:
        #sampfreq, x_acc = wavfile.read(xfile)
        sampfreq, x_acc = extract_wav_data(xfile)
    except:
        opfileh.write("Error: cannot extract data from {}\n".format(xfile))
        xfile = False
    try:
        #sampfreq, y_acc = wavfile.read(yfile)
        sampfreq, y_acc = extract_wav_data(yfile)
    except:
        opfileh.write("Error: cannot extract data from {}\n".format(yfile))
        yfile = False
    try:
        #sampfreq, z_acc = wavfile.read(zfile)
        sampfreq, z_acc = extract_wav_data(zfile)
    except:
        opfileh.write("Error: cannot extract data from {}\n".format(zfile))
        zfile = False
 
    if not xfile and not yfile and not zfile:
        return
   
    if xfile: x_acc = x_acc.astype(float) * output_resolution
    if yfile: y_acc = y_acc.astype(float) * output_resolution
    if zfile: z_acc = z_acc.astype(float) * output_resolution
    
    dt = 1.0/sampfreq
    
    starttime = 0
    npoints = len(x_acc)
    endtime = starttime + (npoints -1 ) * dt
    tt = np.linspace(starttime, endtime, npoints)
    
    tt = np.linspace(starttime, endtime, npoints)
    plt.title(dataname)
    plt.xlabel("time (sec)")
    plt.ylabel("acceleration (mm/s2)")
    if xfile: plt.plot(tt, x_acc, 'r', label='x')
    if yfile: plt.plot(tt, y_acc, 'g', label='y')
    if zfile: plt.plot(tt, z_acc, 'b', label='z')
    plt.legend(loc='best')
    plt.savefig(dataname+"_accel.png")
    plt.close()


for dataname in wavfilenames:
    plot_accels(dataname)

opfileh.close()
