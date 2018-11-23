from scipy.io import wavfile



xfile = '2014-06-26_00,29,39_x.wav'
yfile = '2014-06-26_00,29,39_y.wav'
zfile = '2014-06-26_00,29,39_z.wav'

sampfreq, xdata = wavfile.read(xfile)
sampfreq, ydata = wavfile.read(yfile)
sampfreq, zdata = wavfile.read(zfile)

dt = 1.0/sampfreq

plot(xdata, 'r')
plot(ydata, 'g')
plot(zdata, 'b')
