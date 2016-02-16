# Run with "ipython -i --matplotlib=qt match_frequency.py"
#
import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt

RATE = 44100

# tone synthesis
def tone(freq, cycles, amp=1, rate=RATE):
    len = cycles * (1.0/rate)
    t = np.linspace(0, len, len * rate)
    if freq is 0:
        data = np.zeros(int(len * rate))
    else:
        data = np.sin(2 * np.pi * freq * t) * amp
    return data

fig, ax = plt.subplots(1, 1, sharex=True)

for carrier in [312, 473, 716, 1084, 1479]:
    print "carrier = ", carrier

    freqs = range(carrier-20, carrier+22, 2)
    sig = tone(carrier * 1.0, 2000)  # Reference tone
    response = []

    for freq in freqs:
        sig_tx = tone(freq * 1.0, 2000)  # Test tone
        resp = np.abs(signal.correlate(sig, sig_tx, mode='same'))
        response.append(resp.sum())

    ax.semilogy(freqs, response, label='tone = {}'.format(carrier))
    ax.set_title('Matched filter response')

    #ax.axvline(626.67, ls=':')  # Guardband markers
    #ax.axvline(695.01, ls=':')

    ax.legend(loc='best')
    ax.margins(0, 0.1)

fig.set_tight_layout(True)
fig.show()

