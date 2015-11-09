import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# tone synthesis
def note(freq, len, amp=1, rate=44100):
 t = np.linspace(0,len,len*rate)
 data = np.sin(2*np.pi*freq*t)*amp
 # return data.astype(int16) # two byte integers
 return data

sig = np.repeat([0., 1., 1., 0., 1., 0., 0., 1.], 128)
#sig = note(357, 0.01)
sig_noise = sig + np.random.randn(len(sig))
corr = signal.correlate(sig_noise, np.ones(128), mode='full') / 128

clock = np.arange(64, len(sig), 128)
fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1, sharex=True)

ax_orig.plot(sig)
ax_orig.plot(clock, sig[clock], 'ro')
ax_orig.set_title('Original signal')

ax_noise.plot(sig_noise)
ax_noise.set_title('Signal with noise')

ax_corr.plot(corr)
ax_corr.plot(clock, corr[clock], 'ro')
ax_corr.axhline(0.1, ls=':')
ax_corr.set_title('Cross-correlated with rectangular pulse')

ax_orig.margins(0, 0.1)

fig.set_tight_layout(True)
fig.show()
