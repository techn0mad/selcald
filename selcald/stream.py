"""Inspired by http://stackoverflow.com/questions/24974032/reading-realtime
-audio-data-into-numpy-array."""
from __future__ import print_function
import pyaudio
import numpy
import scipy.io.wavefile as wav

RATE = 16000
RECORD_SECONDS = 2.5
CHUNKSIZE = 1024

# initialize portaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNKSIZE)

frames = []  # A python-list of chunks(numpy.ndarray)
for _ in range(0, int(RATE / CHUNKSIZE * RECORD_SECONDS)):
    data = stream.read(CHUNKSIZE)
    frames.append(numpy.fromstring(data, dtype=numpy.int16))

# Convert the list of numpy-arrays into a 1D array (column-wise)
numpydata = numpy.hstack(frames)

# close stream
stream.stop_stream()
stream.close()
p.terminate()

wav.write('out.wav', RATE, numpydata)
