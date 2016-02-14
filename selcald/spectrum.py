# Run with "ipython -i --matplotlib=qt spectrum.py <file>.wav"
#
import sys
import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from scipy.io.wavfile import read

Tones = dict( { 'Alpha': 312.6,
                'Bravo': 346.7,
                'Charlie': 384.6,
                'Delta': 426.6,
                'Echo': 473.2,
                'Foxtrot': 524.8,
                'Golf': 582.1,
                'Hotel': 645.7,
                'Juliette': 716.1,
                'Kilo': 794.3,
                'Lima': 881.0,
                'Mike': 977.2,
                'Papa': 1083.9,
                'Quebec': 1202.3,
                'Romeo': 1333.5,
                'Sierra': 1479.1, } )

# wav file spectrum
def spectrum(file_name):
    try:
        sig_rate, sig_noise = read(file_name)
    except Exception:
        print 'Error opening {}'.format(file_name)
        return

    print 'file: ', file_name, ' rate: ', sig_rate, ' len: ', len(sig_noise)

    if sig_rate == 44100:
        decimate = 12  # rate = 3675, Fmax = 1837.5 Hz
    elif sig_rate == 48000:
        decimate = 15  # rate = 3200, Fmax = 1600 Hz
    elif sig_rate == 22050:
        decimate = 6  # rate = 3675, Fmax = 1837.5 Hz
    elif sig_rate == 11025:
        decimate = 3  # rate = 3675, Fmax = 1837.5 Hz
    else:
        print 'Sample rate {} not supported.'.format(sig_rate)
        return

    sig_noise = signal.decimate(sig_noise, decimate)
    sig_rate = sig_rate/decimate
    print 'length after decimation: ', len(sig_noise)

    sig_f, welch_spec = signal.periodogram(sig_noise, sig_rate,
                                     nfft=65536, scaling='spectrum')

    plt.title(file_name)
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD')
    plt.xlim(270, 1700)
    plt.ylim([1e-2, 1e7])
    for tone in Tones:
        plt.axvspan(Tones[tone]*0.99,
                    Tones[tone]*1.01, facecolor='r', alpha=0.5)
    plt.grid()

    #plt.semilogy(sig_f, welch_spec)
    plt.loglog(sig_f, welch_spec)
    plt.axhline(np.average(welch_spec), ls=':', color='r')

    plt.show()


if __name__ == "__main__":
   spectrum(sys.argv[1])
