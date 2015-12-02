import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# tone synthesis
def note(freq, len, amp=1, rate=8000):
 t = np.linspace(0,len,len*rate)
 data = np.sin(2*np.pi*freq*t)*amp
 # return data.astype(int16) # two byte integers
 return data

#sig = np.repeat([0., 1., 1., 0., 1., 0., 0., 1.], 128)
sig = note(312.6, 0.10)
sig_tx = np.concatenate( (note(310.0, 0.05), np.zeros(800), note(310.0, 0.10), np.zeros(800), note(310.0, 0.05)) )
sig_noise = 0.50 * sig_tx + 0.50 * np.random.randn(len(sig_tx))
corr = signal.correlate(sig_noise, sig, mode='same')

clock = np.arange(50, len(sig), 100)
fig, (ax_orig, ax_sig, ax_noise, ax_corr) = plt.subplots(4, 1, sharex=True)

ax_orig.plot(sig)
ax_orig.plot(clock, sig[clock], 'ro')
ax_orig.set_title('Reference')

ax_sig.plot(sig_tx)
ax_sig.set_title('Signal without noise')

ax_noise.plot(sig_noise)
ax_noise.set_title('Signal with noise')

ax_corr.plot(corr)
ax_corr.plot(clock, corr[clock], 'ro')
ax_corr.axhline(75.0, ls=':')
ax_corr.set_title('Cross-correlated with original')

ax_orig.margins(0, 0.1)

fig.set_tight_layout(True)
fig.show()
