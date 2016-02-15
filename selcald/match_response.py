# Run with "ipython -i --matplotlib=qt correlate.py"
#
import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt

RATE = 44100

# tone synthesis
def tone(freq, cycles, amp=1, rate=RATE):
    len = cycles * (1.0/freq)
    t = np.linspace(0, len, len * rate)
    if freq is 0:
        data = np.zeros(int(len * rate))
    else:
        data = np.sin(2 * np.pi * freq * t) * amp
    return data

freqs = range(600, 722, 2)  # Frequency range

fig, ax = plt.subplots(1, 1, sharex=True)

for length in [32, 64, 100, 128, 256]:
    print "len = ", length

    sig = tone(660.0, length)  # Reference tone
    response = []

    for freq in freqs:
        sig_tx = tone(freq * 1.0, length)  # Test tone
        resp = np.abs(signal.correlate(sig, sig_tx, mode='same'))
        response.append(resp.sum())

    ax.semilogy(freqs, response, label='len = {}'.format(length))
    ax.set_title('Matched filter response')

    ax.axvline(626.67, ls=':')  # Guardband markers
    ax.axvline(695.01, ls=':')

    ax.legend(loc='best')
    ax.margins(0, 0.1)

fig.set_tight_layout(True)
fig.show()

