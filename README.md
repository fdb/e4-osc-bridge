# Empatica E4 - OSC bridge

This Python script receives messages from the Empatica E4 streaming server and forwards them to OSC.

It uses [open-e4-client](https://pypi.org/project/open-e4-client/) and [Python OSC](https://pypi.org/project/python-osc/) to communicate with both the E4 and OSC.

## Setup

- Install Python 3.10 or higher (I suggest using [miniconda](https://docs.conda.io/projects/miniconda/en/latest/)).
- Install dependencies:

```bash
pip install numpy open-e4-client python-osc
```

## Usage

### Recording an E4 event stream

Connect to an E4 Streaming Server, read all events, record them in an event log and forwards them over OSC:

```python
python e4-osc-bridge.py --record event.log --osc_ip 192.168.1.5 --osc_port 9999
```

The osc_ip is optional and will default to `127.0.0.1` (localhost).

### Replaying an E4 event stream

Read events from a recorded log file and forward them over OSC, using the correct timing:

```python
python e4-osc-bridge.py --replay event.log --osc_ip 192.168.1.5 --osc_port 9999
```

### Converting an E4 event stream dump

The E4 also has its own format to save a session as a folder containing `.csv` files. Use the `convert-e4-recording.py` script to turn it into a log file we can use to replay:

```python
python convert-e4-recording.py your-e4-session-directory your-output.log
```

Then replay it:

```python
python e4-osc-bridge.py --replay your-output.log --osc_port 8000
```

### Additional options

To see a list of arguments, run:

```python
python e4-osc-bridge.py --help
```
