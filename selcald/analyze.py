# Run with "ipython -i --matplotlib=qt analyze.py <file>.wav"
#
import sys
import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.signal import butter, lfilter
from math import log10

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

FLT_LEN = 2000  # Samples

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


# analyze wav file
def analyze(file_name):
    try:
        sig_rate, sig_noise = read(file_name)
    except Exception:
        print 'Error opening {}'.format(file_name)
        return

    print 'file: ', file_name, ' rate: ', sig_rate, ' len: ', len(sig_noise)

    if sig_rate == 44100:
        decimate = 4  # rate = 11025, Fmax = 5512.5 Hz
    elif sig_rate == 48000:
        decimate = 5  # rate = 9600, Fmax = 4800 Hz
    elif sig_rate == 22050:
        decimate = 2  # rate = 11025, Fmax = 5512.5 Hz
    elif sig_rate == 11025:
        decimate = 1  # rate = 11025, Fmax = 5512.5 Hz
    else:
        print 'Sample rate {} not supported.'.format(sig_rate)
        return

    if decimate > 1:
        sig_noise = signal.decimate(sig_noise, decimate)
        sig_rate = sig_rate / decimate
    print 'length after decimation: ', len(sig_noise)

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

    corrA = np.abs(signal.correlate(sig_noise, sigA, mode='same'))
    print 'A: {}'.format(log10(corrA.sum()))

    corrB = np.abs(signal.correlate(sig_noise, sigB, mode='same'))
    print 'B: {}'.format(log10(corrB.sum()))

    corrC = np.abs(signal.correlate(sig_noise, sigC, mode='same'))
    print 'C: {}'.format(log10(corrC.sum()))

    corrD = np.abs(signal.correlate(sig_noise, sigD, mode='same'))
    print 'D: {}'.format(log10(corrD.sum()))

    corrE = np.abs(signal.correlate(sig_noise, sigE, mode='same'))
    print 'E: {}'.format(log10(corrE.sum()))

    corrF = np.abs(signal.correlate(sig_noise, sigF, mode='same'))
    print 'F: {}'.format(log10(corrF.sum()))

    corrG = np.abs(signal.correlate(sig_noise, sigG, mode='same'))
    print 'G: {}'.format(log10(corrG.sum()))

    corrH = np.abs(signal.correlate(sig_noise, sigH, mode='same'))
    print 'H: {}'.format(log10(corrH.sum()))

    corrJ = np.abs(signal.correlate(sig_noise, sigJ, mode='same'))
    print 'J: {}'.format(log10(corrJ.sum()))

    corrK = np.abs(signal.correlate(sig_noise, sigK, mode='same'))
    print 'K: {}'.format(log10(corrK.sum()))

    corrL = np.abs(signal.correlate(sig_noise, sigL, mode='same'))
    print 'L: {}'.format(log10(corrL.sum()))

    corrM = np.abs(signal.correlate(sig_noise, sigM, mode='same'))
    print 'M: {}'.format(log10(corrM.sum()))

    corrP = np.abs(signal.correlate(sig_noise, sigP, mode='same'))
    print 'P: {}'.format(log10(corrP.sum()))

    corrQ = np.abs(signal.correlate(sig_noise, sigQ, mode='same'))
    print 'Q: {}'.format(log10(corrQ.sum()))

    corrR = np.abs(signal.correlate(sig_noise, sigR, mode='same'))
    print 'R: {}'.format(log10(corrR.sum()))

    corrS = np.abs(signal.correlate(sig_noise, sigS, mode='same'))
    print 'S: {}'.format(log10(corrS.sum()))


    fig, (ax_A, ax_B, ax_C, ax_D, ax_E, ax_F, ax_G, ax_H, ax_J, ax_K,
          ax_L, ax_M, ax_P, ax_Q, ax_R, ax_S) = plt.subplots(16, 1, sharex=True,
                                                             sharey=True)

    # ax_sig.plot(sig_noise)
    # ax_sig.set_title('Signal with noise')
    # ax_sig.axis('off')
    # ax_sig.margins(0, 0.1)

    ax_A.plot(corrA)
    ax_A.axhline(np.average(corrA), ls=':')
    # ax_A.set_title(label='Alpha')
    ax_A.axis('off')

    ax_B.plot(corrB)
    ax_B.axhline(np.average(corrB), ls=':')
    # ax_B.set_title(label='Bravo')
    ax_B.axis('off')

    ax_C.plot(corrC)
    ax_C.axhline(np.average(corrC), ls=':')
    # ax_C.set_title(label='Charlie')
    ax_C.axis('off')

    ax_D.plot(corrD)
    ax_D.axhline(np.average(corrD), ls=':')
    # ax_D.set_title(label='Delta')
    ax_D.axis('off')

    ax_E.plot(corrE)
    ax_E.axhline(np.average(corrE), ls=':')
    # ax_E.set_title(label='Echo')
    ax_E.axis('off')

    ax_F.plot(corrF)
    ax_F.axhline(np.average(corrF), ls=':')
    # ax_F.set_title(label='Foxtrot')
    ax_F.axis('off')

    ax_G.plot(corrG)
    ax_G.axhline(np.average(corrG), ls=':')
    # ax_G.set_title(label='Golf')
    ax_G.axis('off')

    ax_H.plot(corrH)
    ax_H.axhline(np.average(corrH), ls=':')
    # ax_H.set_title(label='Hotel')
    ax_H.axis('off')

    ax_J.plot(corrJ)
    ax_J.axhline(np.average(corrJ), ls=':')
    # ax_J.set_title(label='Juliette')
    ax_J.axis('off')

    ax_K.plot(corrK)
    ax_K.axhline(np.average(corrK), ls=':')
    # ax_K.set_title(label='Kilo')
    ax_K.axis('off')

    ax_L.plot(corrL)
    ax_L.axhline(np.average(corrL), ls=':')
    # ax_L.set_title(label='Lima')
    ax_L.axis('off')

    ax_M.plot(corrM)
    ax_M.axhline(np.average(corrM), ls=':')
    # ax_M.set_title(label='Mike')
    ax_M.axis('off')

    ax_P.plot(corrP)
    ax_P.axhline(np.average(corrP), ls=':')
    # ax_P.set_title(label='Papa')
    ax_P.axis('off')

    ax_Q.plot(corrQ)
    ax_Q.axhline(np.average(corrQ), ls=':')
    # ax_Q.set_title(label='Quebec')
    ax_Q.axis('off')

    ax_R.plot(corrR)
    ax_R.axhline(np.average(corrR), ls=':')
    # ax_R.set_title(label='Romeo')
    ax_R.axis('off')

    ax_S.plot(corrS)
    ax_S.axhline(np.average(corrS), ls=':')
    # ax_S.set_title(label='Sierra')
    ax_S.axis('off')

    fig.set_tight_layout(True)
    fig.show()


if __name__ == "__main__":
    analyze(sys.argv[1])
