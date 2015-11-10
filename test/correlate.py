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
sig = np.concatenate( (np.zeros(200), note(1000, 0.05) ) )
sig = np.concatenate( (sig, np.zeros(50) ) )
sig_noise = 0.33 * sig + 0.67 * np.random.randn(len(sig))
corr = signal.correlate(sig_noise, note(1000, 0.08), mode='same')

clock = np.arange(50, len(sig), 100)
fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1, sharex=True)

ax_orig.plot(sig)
ax_orig.plot(clock, sig[clock], 'ro')
ax_orig.set_title('Original signal')

ax_noise.plot(sig_noise)
ax_noise.set_title('Signal with noise')

ax_corr.plot(corr)
ax_corr.plot(clock, corr[clock], 'ro')
ax_corr.axhline(25.0, ls=':')
ax_corr.set_title('Cross-correlated with original')

ax_orig.margins(0, 0.1)

fig.set_tight_layout(True)
fig.show()
