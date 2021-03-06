selcald
=======

Selcal decoder daemon
---------------------

![Cross-correlation Waterfall](doc/fsek.png "Cross-correlation waterfall diagram for SELCAL FSEK")

A Linux/BSD daemon that monitors an audio stream and looks for selcal
(Selective Calling; see <https://en.wikipedia.org/wiki/SELCAL>) calls and
emits a timestamp, followed by the selcal code received. The daemon is
intended to be as simple and lightweight as possible, and should rely
on existing frameworks such as fftw where possible.

[Selective Calling (SELCAL)][1]
--------------------------

SELCAL is a technique that allows a ground radio operator to alert an
aircrew that the operator wishes to communicate with that aircraft.

Because of the background noise level experienced on HF radio frequencies,
aircrews usually prefer to turn down the audio level of their HF receiver
until alerted via SELCAL of a message specifically intended for their
aircraft. When the ground station operator wishes to communicate with an
aircraft, he enters into the SELCAL encoder the 4-letter code of that aircraft,
which is usually included in its flight plan, and transmits that code over the
assigned radio channel. All aircraft monitoring that channel receive the
SELCAL broadcast, but only those (preferably only one) that have been
programmed with that 4-letter code will respond by sounding a chime or
otherwise alerting the crew. The crew will then set their volume control
higher to listen to the voice traffic and, using ICAO recommended radio
procedures, assure that the message is intended for them.

[Selcal Specification][2]
--------------------
The official specification for the selcal system is found in
"ARINC Characteristic 714-6-1990", published on August 15, 1990. The key
attributes of selcal codes are as follows:

### General

Selective calling is accomplished by the coder of the ground transmitter
sending coded tone pulses to the aircraft receiver and decoder. Each
transmitted code is made up of two consecutive tone pulses, with each pulse
containing two simultaneously-transmitted tones.

### Transmitted Code

When the ground operator desires to call a particular aircraft, he depresses
the buttons corresponding to the code assigned to that aircraft. The coder
then keys the transmitter on the air causing to be transmitted two
consecutive tone pulses of 1.0 +/- 0.25 sec. duration, separated by an
interval of 0.2 +/- 0.1 sec. which makes up the code. Each tone pulse
consists of two simultaneously-transmitted tones. The call should consist
of one transmitted code without repetition.

### Stability

The frequency of transmitted codes should be held to +/- 0.15% tolerance to
insure proper operation of the airborne decoder.

**NOTE:** The specification does not indicate the required frequency accuracy of
the receiver. Given that [research][3] seems to [show][4] that doppler spreads of
5-20 Hz over polar paths are possible, it seems that as a practical matter,
the receiver frequency tolerances have to be more relaxed than the transmitter
frequency tolerances. In addition, practical experience has shown that various
ground stations do not appear to follow the +/- 0.15% tolerance regardless. An
initial estimate of a receiver tolerance of 2-2.5% for the tones should be
sufficient to mitigate transmitter, receiver, and sound card frequency errors.
This issue more or less disappears if the source of audio is an AM receiver,
rather than a SSB one, since the SELCALs are sent as SC-USB, they can be
demodulated with an AM receiver with no frequency error, other than the transmitter
and ionospheric contributions. Based on a cursory analysis of the live
data available, it seems that it is quite easy to have a combination of
receiver frequency and soundcard clock errors that sum to 50 Hz or more.
This easily puts the tones out of any reasonable detection band.

### Distortion

Overall audio distortion present on the transmitted RF signal should not
exceed 15%.

### Percent Modulation

The RF signals transmitted by the ground radio station should contain within
3 dB of equal amounts of the two modulating tones. The combination of tones
should result in a modulation envelope having a nominal modulation percentage
of 90% and in no case less than 60%.

### Transmitted Tones

Tone codes are made up of various combinations of the following tones and
are designated by letter as indicated:

Note: The tones are spaced by 10^(0.045)-1 (approximately 10.9%)

| Designation | Nominal Frequency (Hz) | Minimum  | Maximum  | Width |
| ----------- | ---------------------- | -------- | -------- | ----- |
| A           | 312.60                 | 312.13   | 313.07   | 0.94  |
| B           | 346.70                 | 346.18   | 347.22   | 1.04  |
| C           | 384.60                 | 384.02   | 385.18   | 1.15  |
| D           | 426.60                 | 425.96   | 427.24   | 1.28  |
| E           | 473.20                 | 472.49   | 473.91   | 1.42  |
| F           | 524.80                 | 524.01   | 525.59   | 1.57  |
| G           | 582.10                 | 581.23   | 582.97   | 1.75  |
| H           | 645.70                 | 644.73   | 646.67   | 1.94  |
| J           | 716.10                 | 715.03   | 717.17   | 2.15  |
| K           | 794.30                 | 793.11   | 795.49   | 2.38  |
| L           | 881.00                 | 879.68   | 882.32   | 2.64  |
| M           | 977.20                 | 975.73   | 978.67   | 2.93  |
| P           | 1,083.90               | 1,082.27 | 1,085.53 | 3.25  |
| Q           | 1,202.30               | 1,200.50 | 1,204.10 | 3.61  |
| R           | 1,333.50               | 1,331.50 | 1,335.50 | 4.00  |
| S           | 1,479.10               | 1,476.88 | 1,481.32 | 4.44  |


### Received Tones

| Designation | Nominal Frequency | Low        | High     | Width | Guard |
| ----------- | ----------------- | ---        | ----     | ----- | ----- |
| A           | 312.60            | 306.35     | 318.85   | 12.50 | 20.91 |
| B           | 346.70            | 339.77     | 353.63   | 13.87 | 23.27 |
| C           | 384.60            | 376.91     | 392.29   | 15.38 | 25.78 |
| D           | 426.60            | 418.07     | 435.13   | 17.06 | 28.60 |
| E           | 473.20            | 463.74     | 482.66   | 18.93 | 31.64 |
| F           | 524.80            | 514.30     | 535.30   | 20.99 | 35.16 |
| G           | 582.10            | 570.46     | 593.74   | 23.28 | 39.04 |
| H           | 645.70            | 632.79     | 658.61   | 25.83 | 43.16 |
| J           | 716.10            | 701.78     | 730.42   | 28.64 | 47.99 |
| K           | 794.30            | 778.41     | 810.19   | 31.77 | 53.19 |
| L           | 881.00            | 863.38     | 898.62   | 35.24 | 59.04 |
| M           | 977.20            | 957.66     | 996.74   | 39.09 | 65.48 |
| P           | 1,083.90          | 1,062.22   | 1,105.58 | 43.36 | 72.68 |
| Q           | 1,202.30          | 1,178.25   | 1,226.35 | 48.09 | 80.48 |
| R           | 1,333.50          | 1,306.83   | 1,360.17 | 53.34 | 89.35 |
| S           | 1,479.10          | 1,449.52   | 1,508.68 | 59.16 | --    |

### Table of Tone Frequencies and Derivation of the Frequencies

fN = 10^((N-1) x 0.045 + 2). For the first tone, N=12, second N=13, etc.

| Designation | Log Frequency | Frequency (Hz) |
| ----------- | ------------- | -------------- |
| A           | 2.495         | 312.6          |
| B           | 2.540         | 346.7          |
| C           | 2.585         | 384.6          |
| D           | 2.630         | 426.6          |
| E           | 2.675         | 473.2          |
| F           | 2.720         | 524.8          |
| G           | 2.765         | 582.1          |
| H           | 2.810         | 645.7          |
| J           | 2.855         | 716.1          |
| K           | 2.900         | 794.3          |
| L           | 2.945         | 881.0          |
| M           | 2.990         | 977.2          |
| P           | 3.035         | 1083.9         |
| Q           | 3.080         | 1202.3         |
| R           | 3.125         | 1333.5         |
| S           | 3.170         | 1479.1         |

Challenges for SSB Receivers
----------------------------

It is important to note that "real" selcal receivers use AM demodulators to
receive the suppressed carrier (SC) transmissions from the ground stations, and
so for them, the audio tones received will be effectively the same as those
transmitted by the ground stations. The tones are then decoded and used to
either signal the user of the call, or to automatically unmute a separate SSB
receiver.

For hobbyist uses, there is typically only one receiver, and it is a SSB
receiver. This adds additional errors to the received tones, based on offsets
in the tuned frequency and the carrier injection (BFO) frequency. One possible
solution to this problem is to step back from trying to determine the
frequencies of the individual tones and to instead verify that:

1. There are two tones present
2. The difference in frequency between the two tones matches a pair of known
   tones in the alphabet

### Table of Tone Frequency Differences

| Tone      | Frequency | A      | B      | C      | D      | E      | F      | G      | H      | J      | K      | L      | M      | P      | Q      | R      | S      |
| --------- | --------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
|           |           | 312.6  | 346.7  | 384.6  | 426.6  | 473.2  | 524.8  | 582.1  | 645.7  | 716.1  | 794.3  | 881.0  | 977.2  | 1083.9 | 1202.3 | 1333.5 | 1479.1 |
| A         | 312.6     | 0.0    |        |        |        |        |        |        |        |        |        |        |        |        |        |        |        |
| B         | 346.7     | 34.1   | 0.0    |        |        |        |        |        |        |        |        |        |        |        |        |        |        |
| C         | 384.6     | 72.0   | 37.9   | 0.0    |        |        |        |        |        |        |        |        |        |        |        |        |        |
| D         | 426.6     | 114.0  | 79.9   | 42.0   | 0.0    |        |        |        |        |        |        |        |        |        |        |        |        |
| E         | 473.2     | 160.6  | 126.5  | 88.6   | 46.6   | 0.0    |        |        |        |        |        |        |        |        |        |        |        |
| F         | 524.8     | 212.2  | 178.1  | 140.2  | 98.2   | 51.6   | 0.0    |        |        |        |        |        |        |        |        |        |        |
| G         | 582.1     | 269.5  | 235.4  | 197.5  | 155.5  | 108.9  | 57.3   | 0.0    |        |        |        |        |        |        |        |        |        |
| H         | 645.7     | 333.1  | 299.0  | 261.1  | 219.1  | 172.5  | 120.9  | 63.6   | 0.0    |        |        |        |        |        |        |        |        |
| J         | 716.1     | 403.5  | 369.4  | 331.5  | 289.5  | 242.9  | 191.3  | 134.0  | 70.4   | 0.0    |        |        |        |        |        |        |        |
| K         | 794.3     | 481.7  | 447.6  | 409.7  | 367.7  | 321.1  | 269.5  | 212.2  | 148.6  | 78.2   | 0.0    |        |        |        |        |        |        |
| L         | 881.0     | 568.4  | 534.3  | 496.4  | 454.4  | 407.8  | 356.2  | 298.9  | 235.3  | 164.9  | 86.7   | 0.0    |        |        |        |        |        |
| M         | 977.2     | 664.6  | 630.5  | 592.6  | 550.6  | 504.0  | 452.4  | 395.1  | 331.5  | 261.1  | 182.9  | 96.2   | 0.0    |        |        |        |        |
| P         | 1083.9    | 771.3  | 737.2  | 699.3  | 657.3  | 610.7  | 559.1  | 501.8  | 438.2  | 367.8  | 289.6  | 202.9  | 106.7  | 0.0    |        |        |        |
| Q         | 1202.3    | 889.7  | 855.6  | 817.7  | 775.7  | 729.1  | 677.5  | 620.2  | 556.6  | 486.2  | 408.0  | 321.3  | 225.1  | 118.4  | 0.0    |        |        |
| R         | 1333.5    | 1020.9 | 986.8  | 948.9  | 906.9  | 860.3  | 808.7  | 751.4  | 687.8  | 617.4  | 539.2  | 452.5  | 356.3  | 249.6  | 131.2  | 0.0    |        |
| S         | 1479.1    | 1166.5 | 1132.4 | 1094.5 | 1052.5 | 1005.9 | 954.3  | 897.0  | 833.4  | 763.0  | 684.8  | 598.1  | 501.9  | 395.2  | 276.8  | 145.6  | 0.0    |

Signal Processing
-----------------

Detection of the selcal tones is quite similar to DTMF tone detection, and
this has been well documented. There are several approaches available:

1. Bandpass filter bank and energy detectors (i.e. analog implementation approach)
2. Discrete FFT and energy detection in bins containing selcal tones
3. Goertzl algorithm for fast DFT (see <https://en.wikipedia.org/wiki/Goertzel_algorithm>)
4. Chirp-Z transform for DFT (see <https://en.wikipedia.org/wiki/Bluestein%27s_FFT_algorithm>)
5. MUSIC algorithm (see <https://en.wikipedia.org/wiki/Multiple_signal_classification>)
6. ESPRIT algorithm (see <https://en.wikipedia.org/wiki/Estimation_of_signal_parameters_via_rotational_invariance_techniques>)
7. Wavelet transform and convolution (seems highly advanced)
8. Q Transform (handles geometric spacing of tones/bins much better)

The implementation should take into account characteristics of the HF radio medium:

* Often poor signal/noise ratio
* Frequent ionospheric and auroral fading and flutter
* Slight doppler due to relative ionospheric motion

These imply that unlike DTMF decoder implementations, a series of measurements should
be made during the signal and a final decision determined from statistical analysis
of the raw measurements. Based on the highest baseband frequency of approximately
1500 Hz, this means that any audio sampling rate above 4000 samples/second should work
fine. Looking at the post-detection stage, we can see that the gap between the two tone
groups is specified as 200 mS +/- 100 mS, so in the worst case, the gap could be 100 mS.
Following Nyquist and sampling theory, this means that in that 100 mS period, we need to
check for the presence or absence of signal at least twice, or once every 50 mS. The actual
numbers will vary based on audio sampling rates, but for the typical 44100 samples/second
rate of modern sound cards, this leads us to use a block size of 2048 (using a nice round
binary number) and a post-processing sample rate of 2048/44100 or 46.4 mS. This also means
that we need to window this sample size appropriately and choose an algorithm for tone
detection that is "comfortable" with this block size.

After considerable trolling through the Internet, and discarding many approaches
(see above) that are oriented toward detecting _unknown_ tones, it seems that
theoretically, the ideal approach is to use [cross-correlation][5] of the input signal with
_known_ signals to detect their presence, otherwise known as [matched filtering][6].

The figure below shows the cross-correlation between the received SELCAL "JRAE" and each
of the 16 tones in the alphabet. The lines are ordered from tone A on the top to tone
S on the bottom, and 2.5 to 3.0 seconds of time run from left to right.

![16 Channel matched filter](doc/16channel.png "Receving SELCAL JRAE on 16 channel matched filter receiver")

Some care must be taken in selecting the block size, as it is a tradeoff between
integrating more signal power to improve cross-correlation detection, and added
difficulty in detecting the silent period between the tone groups. As mentioned
earlier, presumably for direct detection of the shortest possible silent period,
blocks should be less than 50 mS, but this would result in requiring detection
based on only 15 cycles (312.6 Hz * 0.05 sec) for the lowest frequency tone.

![Cross-correlation demonstration](doc/cross-correlation.png "Demonstration of cross-correlation")

The normal source of sampled audio is the soundcard interface.
After some digging, it seems that PortAudio would be a good choice for an audio interface
API, since it provides both a degree of platform independence and isolates the application
from the various underlying audio frameworks (i.e. ALSA, Pulseaudio, SndKit, etc.).
In general, lower sampling rates are preferred due to the reduced processing load,
as are fixed point DSP implementations versus floating point implementations.

### Pseudocode

    Clear the result buffer
    Clear the tones
    Set state to idle
    Set the threshold to 50%
    While true
        Capture one block of audio (~100 mS)
        Decimate it by 10
        For each tone in the alphabet
            Cross correlate the audio with the tone
            If the correlation is greater than the threshold
                Save the result in the buffer
            Else
                Add the correlation to the threshold and average
        If there are > 800 mS of results in the buffer
            If the last result was silence (no tones)
                For each tone in the alphabet
                    If there is a majority of results in the buffer
                        Then the current tone is detected
                If two tones are detected
                    If the state is idle
                        Set the state to two tones
                        Save the two tones
                    If the state is two tones
                        Return the four tones
                    Clear the result buffer
                    Clear the tones
                    Set the state to idle

References
----------

[^1]: http://www.asri.aero/our-services/selcal/ "Aviation Spectrum Resources Inc. website, retrieved 3, Nov 2013"

[^2]: http://store.aviation-ia.com/cf/store/catalog_detail.cfm?item_id=126 "ARINC Characteristic 714-6-1990, chapter 2; August 15, 1990"

[^3]: https://lra.le.ac.uk/bitstream/2381/7403/3/propagation%20of%20HF%20radio%20waves.pdf "Propagation of HF radio waves over northerly paths: measurements, simulation and systems aspects, Warrington et al"

[^4]: http://onlinelibrary.wiley.com/doi/10.1002/2013RS005264/full "Observations of Doppler and delay spreads on HF signals received over polar cap and trough paths at various stages of the solar cycle, Stocker, A. J., E. M. Warrington, and D. R. Siddle (2013), Radio Sci., 48, 638–645, doi:10.1002/2013RS005264"

[^5]: https://en.wikipedia.org/wiki/Autocorrelation "Autocorrelation"

[^6]: https://en.wikipedia.org/wiki/Matched_filter "Matched filter"
