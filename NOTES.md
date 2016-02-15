Notes
=====

Matched Filtering
-----------------

Currently, we are cross-correlating against standard tones in the alphabet that
are of constant duration. This is probably a mistake because the length of 
the tone we are correlating signal against will determine the matched filter 
bandwidth; they should be a constant number of cycles instead. Otherwise, the 
bandwidth for each tone in the alphabet will be different than the others,
with the high tones having a narrower bandwidth than the lower ones.

I need to characterize the cross-correlation frequency response more precisely. 
I suspect that the longer the reference tone is, the trade off is that there
is more integration of the desired signal, but the frequency response becomes
narrower.

![Frequency response vs. filter length](filter-response.png "Frequency response vs. filter length")

Also, the duration of the cross-correlation needs to be considered: A perfect
cross-correlation would be one second of a SELCAL code correlated with one 
second of received data. However, this would result is a very narrow receiver
bandwidth. The compromise could be correlating one second of received data 
with an appropriately sized reference tone.

Alternatively, the received signal could be broken into frames, each one being
the same size as the reference tone.

Sample Processing
-----------------

Some live captures have very strong signals, and the SciPy spectrogram seems to
show spurious signals in many of these. Perhaps some AGC pre-processing is 
warranted.

Some unwanted high-frequency roll-off is observed if large decimations are 
taken. This was seen with decimations down to ~3700 samples/second, which
should be sufficient to deal with the highest frequency of ~1400 Hz. It is not
clear if this is related to excessive decimation or not, but the roll-off seems
less if the decimation is reduced to ~11000 samples/second.