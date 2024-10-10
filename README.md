# Setup StepuP

This repo contains scripts to setup the StepuP project on a new machine.

## Installation
To clone the repository and install the necessary packages using Poetry, follow these steps:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/stepup_setup_jw.git
    cd stepup_setup_jw
    ```

2. **Install Poetry:**
    If you don't have Poetry installed, you can install it by following the instructions [here](https://python-poetry.org/docs/#installation).

3. **Install dependencies:**
    ```sh
    poetry install
    ```

This will set up a virtual environment and install all the dependencies specified in the `pyproject.toml` file.

Additinaly software you ahve to have installed or SDKs which are needed:

**DelSys (EMG)**
- [Trigno control unit](https://delsys.com/support/software/)

**Qualisys (Motion Capture)**
- [Qualisys Python SDK](https://qualisys.github.io/qualisys_python_sdk/index.html)
- [Qualisys Track Manager](https://www.qualisys.com/software/qtm/) with [enabled real-time straming](https://www.qualisys.com/video-tutorials/how-to-use-real-time-streaming-with-qtm/)

**mbt (EEG)**
- mbtStreamer

**LabRecorder (LSL-recording)**
- [LabRecorder](https://github.com/labstreaminglayer/App-LabRecorder/releases)

## Run the scripts
To run the scripts, you can use the following command:

**EMG to LSL:**
```sh
poetry run python -m delsys2lsl.py
```

**Qualisys to LSL:**
```sh
poetry run python -m qualisys2lsl.py
```

## Record data
Simply open the lab recorder and start the recording. The data will be saved in the specified folder.

## Authors
[Julius Welzel](mailto:j.welzel@neurologie.uni-kiel.de%20?subject=StepuP%20setup)
