# Run with "ipython -i --matplotlib=qt analyze.py <file>.wav"
#
import sys
import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from scipy.io.wavfile import read

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


# tone synthesis
def note(freq, len, amp=32767.0, rate=44100):
 t = np.linspace(0,len,len*rate)
 if freq is 0:
   data = np.zeros(int(len * rate))
 else:
   data = np.sin(2*np.pi*freq*t)*amp
 return data.astype(int)


# analyze wav file
def analyze(file_name):
    sig_rate, sig_noise = read(file_name)
    print 'file: ', file_name, ' rate: ', sig_rate, ' len: ', len(sig_noise)
    sig_x = signal.decimate(sig_noise, 10)
    rate_x = sig_rate/10
    
    sigA = note(Alpha, 0.10, rate=sig_rate)
    sigB = note(Bravo, 0.10, rate=sig_rate)
    sigC = note(Charlie, 0.10, rate=sig_rate)
    sigD = note(Delta, 0.10, rate=sig_rate)
    sigE = note(Echo, 0.10, rate=sig_rate)
    sigF = note(Foxtrot, 0.10, rate=sig_rate)
    sigG = note(Golf, 0.10, rate=sig_rate)
    sigH = note(Hotel, 0.10, rate=sig_rate)
    sigJ = note(Juliette, 0.10, rate=sig_rate)
    sigK = note(Kilo, 0.10, rate=sig_rate)
    sigL = note(Lima, 0.10, rate=sig_rate)
    sigM = note(Mike, 0.10, rate=sig_rate)
    sigP = note(Papa, 0.10, rate=sig_rate)
    sigQ = note(Quebec, 0.10, rate=sig_rate)
    sigR = note(Romeo, 0.10, rate=sig_rate)
    sigS = note(Sierra, 0.10, rate=sig_rate)
    
    corrA = np.abs(signal.correlate(sig_noise, sigA, mode='same'))
    corrB = np.abs(signal.correlate(sig_noise, sigB, mode='same'))
    corrC = np.abs(signal.correlate(sig_noise, sigC, mode='same'))
    corrD = np.abs(signal.correlate(sig_noise, sigD, mode='same'))
    corrE = np.abs(signal.correlate(sig_noise, sigE, mode='same'))
    corrF = np.abs(signal.correlate(sig_noise, sigF, mode='same'))
    corrG = np.abs(signal.correlate(sig_noise, sigG, mode='same'))
    corrH = np.abs(signal.correlate(sig_noise, sigH, mode='same'))
    corrJ = np.abs(signal.correlate(sig_noise, sigJ, mode='same'))
    corrK = np.abs(signal.correlate(sig_noise, sigK, mode='same'))
    corrL = np.abs(signal.correlate(sig_noise, sigL, mode='same'))
    corrM = np.abs(signal.correlate(sig_noise, sigM, mode='same'))
    corrP = np.abs(signal.correlate(sig_noise, sigP, mode='same'))
    corrQ = np.abs(signal.correlate(sig_noise, sigQ, mode='same'))
    corrR = np.abs(signal.correlate(sig_noise, sigR, mode='same'))
    corrS = np.abs(signal.correlate(sig_noise, sigS, mode='same'))
    
    fig, (ax_A, ax_B, ax_C, ax_D, ax_E, ax_F, ax_G, ax_H, ax_J, ax_K,
          ax_L, ax_M, ax_P, ax_Q, ax_R, ax_S) = plt.subplots(16, 1, sharex=True,
                                                             sharey=True)
    
    #ax_sig.plot(sig_noise)
    #ax_sig.set_title('Signal with noise')
    #ax_sig.axis('off')
    #ax_sig.margins(0, 0.1)
    
    ax_A.plot(corrA)
    ax_A.axhline(np.average(corrA), ls=':')
    #ax_A.set_title(label='Alpha')
    ax_A.axis('off')
    
    ax_B.plot(corrB)
    ax_B.axhline(np.average(corrB), ls=':')
    #ax_B.set_title(label='Bravo')
    ax_B.axis('off')
    
    ax_C.plot(corrC)
    ax_C.axhline(np.average(corrC), ls=':')
    #ax_C.set_title(label='Charlie')
    ax_C.axis('off')
    
    ax_D.plot(corrD)
    ax_D.axhline(np.average(corrD), ls=':')
    #ax_D.set_title(label='Delta')
    ax_D.axis('off')
    
    ax_E.plot(corrE)
    ax_E.axhline(np.average(corrE), ls=':')
    #ax_E.set_title(label='Echo')
    ax_E.axis('off')
    
    ax_F.plot(corrF)
    ax_F.axhline(np.average(corrF), ls=':')
    #ax_F.set_title(label='Foxtrot')
    ax_F.axis('off')
    
    ax_G.plot(corrG)
    ax_G.axhline(np.average(corrG), ls=':')
    #ax_G.set_title(label='Golf')
    ax_G.axis('off')
    
    ax_H.plot(corrH)
    ax_H.axhline(np.average(corrH), ls=':')
    #ax_H.set_title(label='Hotel')
    ax_H.axis('off')
    
    ax_J.plot(corrJ)
    ax_J.axhline(np.average(corrJ), ls=':')
    #ax_J.set_title(label='Juliette')
    ax_J.axis('off')
    
    ax_K.plot(corrK)
    ax_K.axhline(np.average(corrK), ls=':')
    #ax_K.set_title(label='Kilo')
    ax_K.axis('off')
    
    ax_L.plot(corrL)
    ax_L.axhline(np.average(corrL), ls=':')
    #ax_L.set_title(label='Lima')
    ax_L.axis('off')
    
    ax_M.plot(corrM)
    ax_M.axhline(np.average(corrM), ls=':')
    #ax_M.set_title(label='Mike')
    ax_M.axis('off')
    
    ax_P.plot(corrP)
    ax_P.axhline(np.average(corrP), ls=':')
    #ax_P.set_title(label='Papa')
    ax_P.axis('off')
    
    ax_Q.plot(corrQ)
    ax_Q.axhline(np.average(corrQ), ls=':')
    #ax_Q.set_title(label='Quebec')
    ax_Q.axis('off')
    
    ax_R.plot(corrR)
    ax_R.axhline(np.average(corrR), ls=':')
    #ax_R.set_title(label='Romeo')
    ax_R.axis('off')
    
    ax_S.plot(corrS)
    ax_S.axhline(np.average(corrS), ls=':')
    #ax_S.set_title(label='Sierra')
    ax_S.axis('off')
    
    fig.set_tight_layout(True)
    fig.show()

if __name__ == "__main__":
   analyze(sys.argv[1])
