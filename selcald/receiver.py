# Run with "ipython --matplotlib=qt receiver.py <file>.wav"
#
from __future__ import print_function
import sys
import numpy as np
from scipy import signal
from scipy.io.wavfile import read
from scipy.signal import butter, lfilter
from math import log10

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

FRAME = 0.1  # Frame time in seconds

Alpha = 312.6
Bravo = 346.7
Charlie = 384.6
Delta = 426.6
Echo = 473.2
Foxtrot = 524.8
Golf = 582.1
Hotel = 645.7
Juliette = 716.1
Kilo = 794.3
Lima = 881.0
Mike = 977.2
Papa = 1083.9
Quebec = 1202.3
Romeo = 1333.5
Sierra = 1479.1

FLT_LEN = 1000  # Samples

# Shamelessly lifted from
# https://scipy.github.io/old-wiki/pages/Cookbook/ButterworthBandpass
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


# tone synthesis
def note(freq, cycles, amp=32767.0, rate=44100):
    len = cycles * (1.0/rate)
    t = np.linspace(0, len, len * rate)
    if freq is 0:
        data = np.zeros(int(len * rate))
    else:
        data = np.sin(2 * np.pi * freq * t) * amp
    return data.astype(int)


# analyze wav file by chunks
def receiver(file_name):
    try:
        sig_rate, sig_noise = read(file_name)
    except Exception:
        print('Error opening {}'.format(file_name))
        return

    print('file: ', file_name, ' rate: ', sig_rate, ' len: ', len(sig_noise))

    if sig_rate == 44100:
        decimate = 4  # rate = 11025, Fmax = 5512.5 Hz
    elif sig_rate == 48000:
        decimate = 5  # rate = 9600, Fmax = 4800 Hz
    elif sig_rate == 22050:
        decimate = 2  # rate = 11025, Fmax = 5512.5 Hz
    elif sig_rate == 11025:
        decimate = 1  # rate = 11025, Fmax = 5512.5 Hz
    else:
        print('Sample rate {} not supported.'.format(sig_rate))
        return

    if decimate > 1:
        sig_noise = signal.decimate(sig_noise, decimate)
        sig_rate = sig_rate / decimate
    print('length after decimation: ', len(sig_noise))

    sig_noise = butter_bandpass_filter(sig_noise, 270, 1700, sig_rate, order=8)

    sigA = note(Alpha, FLT_LEN, rate=sig_rate)
    sigB = note(Bravo, FLT_LEN, rate=sig_rate)
    sigC = note(Charlie, FLT_LEN, rate=sig_rate)
    sigD = note(Delta, FLT_LEN, rate=sig_rate)
    sigE = note(Echo, FLT_LEN, rate=sig_rate)
    sigF = note(Foxtrot, FLT_LEN, rate=sig_rate)
    sigG = note(Golf, FLT_LEN, rate=sig_rate)
    sigH = note(Hotel, FLT_LEN, rate=sig_rate)
    sigJ = note(Juliette, FLT_LEN, rate=sig_rate)
    sigK = note(Kilo, FLT_LEN, rate=sig_rate)
    sigL = note(Lima, FLT_LEN, rate=sig_rate)
    sigM = note(Mike, FLT_LEN, rate=sig_rate)
    sigP = note(Papa, FLT_LEN, rate=sig_rate)
    sigQ = note(Quebec, FLT_LEN, rate=sig_rate)
    sigR = note(Romeo, FLT_LEN, rate=sig_rate)
    sigS = note(Sierra, FLT_LEN, rate=sig_rate)

    # See http://stackoverflow.com/questions/23507217/python-plotting-2d-data-on-to-3d-axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    y = np.arange(16)
    print(' Index     A      B      C      D      E      F      G      H      J      K      L      M      P      Q      R      S     Avg')

    x = range(0, len(sig_noise)-(sig_rate/10), (sig_rate/10))
    X, Y = np.meshgrid(x, y)
    Z = np.zeros((len(y), len(x)))

    for index in range(0, len(sig_noise)-(sig_rate/10), (sig_rate/10)):

        corr = np.zeros(16)

        corr[0]  = log10(np.abs(signal.correlate(sig_noise[index:index+FLT_LEN], sigA, mode='same')).sum())
        corr[1]  = log10(np.abs(signal.correlate(sig_noise[index:index+FLT_LEN], sigB, mode='same')).sum())
        corr[2]  = log10(np.abs(signal.correlate(sig_noise[index:index+FLT_LEN], sigC, mode='same')).sum())
        corr[3]  = log10(np.abs(signal.correlate(sig_noise[index:index+FLT_LEN], sigD, mode='same')).sum())
        corr[4]  = log10(np.abs(signal.correlate(sig_noise[index:index+FLT_LEN], sigE, mode='same')).sum())
        corr[5]  = log10(np.abs(signal.correlate(sig_noise[index:index+FLT_LEN], sigF, mode='same')).sum())
        corr[6]  = log10(np.abs(signal.correlate(sig_noise[index:index+FLT_LEN], sigG, mode='same')).sum())
        corr[7]  = log10(np.abs(signal.correlate(sig_noise[index:index+FLT_LEN], sigH, mode='same')).sum())
        corr[8]  = log10(np.abs(signal.correlate(sig_noise[index:index+FLT_LEN], sigJ, mode='same')).sum())
        corr[9]  = log10(np.abs(signal.correlate(sig_noise[index:index+FLT_LEN], sigK, mode='same')).sum())
        corr[10] = log10(np.abs(signal.correlate(sig_noise[index:index+FLT_LEN], sigL, mode='same')).sum())
        corr[11] = log10(np.abs(signal.correlate(sig_noise[index:index+FLT_LEN], sigM, mode='same')).sum())
        corr[12] = log10(np.abs(signal.correlate(sig_noise[index:index+FLT_LEN], sigP, mode='same')).sum())
        corr[13] = log10(np.abs(signal.correlate(sig_noise[index:index+FLT_LEN], sigQ, mode='same')).sum())
        corr[14] = log10(np.abs(signal.correlate(sig_noise[index:index+FLT_LEN], sigR, mode='same')).sum())
        corr[15] = log10(np.abs(signal.correlate(sig_noise[index:index+FLT_LEN], sigS, mode='same')).sum())

        for i in range(len(y)):
            Z[i, index/(sig_rate/10)] = corr[i]

        max1 = 0.0
        for tone in range(0, 16):
            if corr[tone] > max1:
                max1 = corr[tone]
                max1idx = tone

        max2 = 0.0
        for tone in range(0, 16):
            if tone != max1idx and corr[tone] > max2:
                max2 = corr[tone]
                max2idx = tone

        print('{0:6d}: '.format(index), end='')
        avg = np.mean(corr)
        for tone in range(0, 16):
            if tone == max1idx or tone == max2idx:
                print('[{0:2.2f}]'.format(corr[tone]), end='')
            else:
                if corr[tone] > avg:
                    print(' {0:2.2f} '.format(corr[tone]), end='')
                else:
                    print('   .   ', end='')

        print(' {0:2.2f}'.format(avg))

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1000, shade=False, lw=.5)

    ax.set_xlabel("Sample")
    ax.set_ylabel("Tone")
    ax.set_zlabel("Correlation")

    ax.view_init(40, 160)

    plt.show()

if __name__ == "__main__":
    receiver(sys.argv[1])
