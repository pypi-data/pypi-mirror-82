# OkHound module

A python wrapper for the "Ok Hound" phrase spotter.


## Install

1. Install the header files for the Python C API, **python-dev** / **python-devel**;

2. Run `pip install okhound`


## Example script

```python
import okhound
import pyaudio


CHUNKSIZE = 1024

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=CHUNKSIZE)

okhound.setThreshold(0.4)

while True:
	try:
		audio = stream.read(CHUNKSIZE)
	except IOError:
		print("Skipped frame")
		continue

	phraseSpotted = okhound.processSamples(audio)
	if phraseSpotted: break


print("'Ok Hound' spotted! Sensitivity: {0}".format(okhound.getThreshold()))
```


## Run example script

1. Install PortAudio development tools, **portaudio19-dev** / **libportaudio-devel**;

2. Install pyaudio module, `pip install pyaudio`;

3. Run example_pyaudio.py script, `python example_pyaudio.py`.
