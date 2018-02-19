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
# from mpl_toolkits.mplot3d import Axes3D

FRAME_TIME = 0.1  # Frame time in seconds

TONES = [312.6,
         346.7,
         384.6,
         426.6,
         473.2,
         524.8,
         582.1,
         645.7,
         716.1,
         794.3,
         881.0,
         977.2,
         1083.9,
         1202.3,
         1333.5,
         1479.1]

ALPHABET = ['Alpha',
            'Bravo',
            'Charlie',
            'Delta',
            'Echo',
            'Foxtrot',
            'Golf',
            'Hotel',
            'Juliette',
            'Kilo',
            'Lima',
            'Mike',
            'Papa',
            'Quebec',
            'Romeo',
            'Sierra']

FILTER_LEN = 1000  # Samples


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

    frame_len = int(sig_rate * FRAME_TIME)
    frames = (len(sig_noise) / frame_len) + 1

    sig_noise = butter_bandpass_filter(sig_noise,
                                       270,
                                       1700,
                                       sig_rate,
                                       order=8)

    template = []
    for tone in range(0, len(TONES)):
        template.append(note(TONES[tone], frame_len, rate=sig_rate))

    # See http://stackoverflow.com/questions/23507217/
    #         python-plotting-2d-data-on-to-3d-axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    y = np.arange(len(TONES))
    print(' Index     A      B      C      D      E      F      G', end='')
    print('      H      J      K      L      M      P      Q      R', end='')
    print('      S     Avg')

    x = range(0, frames)
    X, Y = np.meshgrid(y, x)
    Z = np.zeros((len(x), len(y)))

    for frame in range(0, frames):

        beg = frame * frame_len
        end = (frame+1) * frame_len

        corr = np.zeros(len(TONES))

        for tone in range(0, len(TONES)):
            corr[tone] = log10(np.abs(signal.correlate(sig_noise[beg:end],
                                                       template[tone],
                                                       mode='same')).sum())
            Z[frame, tone] = corr[tone]

        max1 = 0.0
        for tone in range(0, len(TONES)):
            if corr[tone] > max1:
                max1 = corr[tone]
                max1idx = tone

        max2 = 0.0
        for tone in range(0, len(TONES)):
            if tone != max1idx and corr[tone] > max2:
                max2 = corr[tone]
                max2idx = tone

        print('{0:6d}: '.format(frame), end='')
        avg = np.mean(corr)
        for tone in range(0, len(TONES)):
            if tone == max1idx or tone == max2idx:
                print('[{0:2.2f}]'.format(corr[tone]), end='')
            else:
                if corr[tone] > avg:
                    print(' {0:2.2f} '.format(corr[tone]), end='')
                else:
                    print('   .   ', end='')

        print(' {0:2.2f}'.format(avg))

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1000, color='w', shade=True,
                    lw=.5)
    # ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1000, lw=.5)

    ax.set_title(file_name)
    ax.set_xlabel("Tone")
    ax.set_ylabel("Frame")
    ax.set_zlabel("Log Correlation")

    ax.set_zlim(10.0, 15.0)
    ax.set_ylim(0, frames)

    ax.view_init(30, -130)

    plt.show()


if __name__ == "__main__":
    receiver(sys.argv[1])
