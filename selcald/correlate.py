# Run with "ipython -i --matplotlib=qt correlate.py"
#
from __future__ import print_function
import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

RATE = 44100
Alpha = 312.6


# See http://www.dsprelated.com/showarticle/908.php
def voss(nrows, ncols=16):
    """Generates pink noise using the Voss-McCartney algorithm.

    nrows: number of values to generate
    rcols: number of random sources to add

    returns: NumPy array
    """
    array = np.empty((nrows, ncols))
    array.fill(np.nan)
    array[0, :] = np.random.random(ncols)
    array[:, 0] = np.random.random(nrows)

    # the total number of changes is nrows
    n = nrows
    cols = np.random.geometric(0.5, n)
    cols[cols >= ncols] = 0
    rows = np.random.randint(nrows, size=n)
    array[rows, cols] = np.random.random(n)

    df = pd.DataFrame(array)
    df.fillna(method='ffill', axis=0, inplace=True)
    total = df.sum(axis=1)

    return (total.values - (ncols/2))


# tone synthesis
def note(freq, len, amp=1, rate=RATE):
    t = np.linspace(0, len, len * rate)
    if freq is 0:
        data = np.zeros(int(len * rate))
    else:
        data = np.sin(2*np.pi*freq*t)*amp
    return data


sig = note(Alpha, 0.10)
sig_tx = np.concatenate((note(0, 0.50),
                         note(Alpha, 0.20),
                         note(0, 0.10),
                         note(Alpha, 0.75),
                         note(0, 0.10),
                         note(Alpha, 0.10),
                         note(0, 0.10),))
# sig_noise = 0.33 * sig_tx + 0.66 * np.random.randn(len(sig_tx))
sig_noise = 0.50 * sig_tx + 0.50 * voss(len(sig_tx))
corr = np.abs(signal.correlate(sig_noise, sig, mode='same'))

fig, (ax_orig, ax_sig, ax_noise, ax_corr) = plt.subplots(4, 1, sharex=True)

ax_orig.plot(sig)
ax_orig.set_title('Reference')

ax_sig.plot(sig_tx)
ax_sig.set_title('Signal without noise')

ax_noise.plot(sig_noise)
ax_noise.set_title('Signal with noise')

ax_corr.plot(corr)
ax_corr.axhline(np.average(corr), ls=':')
ax_corr.set_title('Cross-correlated with Reference')

ax_orig.margins(0, 0.1)

fig.set_tight_layout(True)
fig.show()

write('test.wav', 44100, sig_noise)
