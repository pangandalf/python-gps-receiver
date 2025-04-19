# 🛰️ Python GPS receiver

This project implements a software-defined GPS L1 receiver in Python. It covers the full signal processing chain required to extract navigation messages from raw real-valued samples, based on the standard GPS signal structure and BPSK modulation.

## 📦 Features
- Reads raw real-valued data from `.dat` file (`int16` format)
- Signal spectrum visualization (optional)
- Satellite acquisition using correlation techniques
- Carrier and code tracking loop (DLL + PLL)
- Digital demodulation (BPSK)
- Navigation message decoding

## 🚀 Quick Start

### Requirements
- `Python3.7` or higher
- `pip3`
- `numpy`
- `scipy`
- `matplotlib` (optional, for plotting)

Install dependencies:
```bash
pip3 install -r requirements.txt
```

### Input data
To test the receiver, you will need raw sample data recorded from a GPS L1 signal. This receiver processes only the real (in-phase) component of the signal – not complex I/Q data. Make sure the file contains signed 16-bit integers (int16) representing real-valued samples.

If you don't have your own recordings, you can use public datasets as a starting point and extract only the real part if needed. Sample data can be downloaded e.g. from [gnss-sdr](https://github.com/gnss-sdr/gnss-sdr) project page on [SourceForge](https://sourceforge.net/projects/gnss-sdr/files/data/). Alternatively (on Linux or WSL), use this `wget` command in your terminal:
```bash
wget https://sourceforge.net/projects/gnss-sdr/files/data/2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN.tar.gz
```
> Note: If the estimated download time is too long, you can also download the data using Google Colab and then copy it to your Google Drive after mounting the drive in Colab Notebook.

Then unpack the archive:
```bash
tar -zxvf 2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN.tar.gz
```

Finally, run the script to extract only the real component of the signal:
```python
python3 prepare_data.py
```

## ▶️ Usage
In the `main.py` file, adjust the sampling frequency `fs` to match your input data. A default value of 4 MHz is provided for compatibility with the [gnss-sdr](https://github.com/gnss-sdr/gnss-sdr) dataset. You can also enable or disable plotting by setting the `plot` boolean variable. Then run:
```python
python3 main.py
```

## 📈 Output
### 1. Signal spectrum visualization
![Signal spectrum](screenshots/spectrum.png)
### 2. Correlation surface received in the signal acquisition phase
![Correlation surface](screenshots/correlation_surface.png)
### 3. Carrier frequency tracking
![Carrier tracking](screenshots/carrier_frequency.png)
### 4. Code-phase offset correction over time
![Code-phase offset](screenshots/dll_nco.png)
### 5. BPSK constellation diagram
![Constellation](screenshots/constellation_diagram.png)
### 6. BPSK symbols
![BPSK symbols](screenshots/bpsk_symbols.png)

## 📄 Decoding results
> Note: Values are raw binary fields decoded from the NAV message, without applying scaling factors from ICD-GPS-200.
```plaintext
----------------- Acquisition results -----------------
  1) Detected satellite PRN ID: 1
  2) Doppler offset: 7000.0
  3) Code-phase offset: 3988

----------------- Satelite number: 12 -----------------
                     (Subframe 5)
  1) Eccentricity: 9361
  2) Almanac reference time: 144
  3) Orbital inclination: 6870
  4) Rate of right ascension: 690
  5) Root of semi major axis: 6222754
  6) Longitude of ascension node: 6754408
  7) Argument of perigee: 16245516
  8) Mean anomaly at reference time: 5461369
  9) Clock bias: 133
  10) Clock drift: 1

----------------- Satelite number: 13 -----------------
                     (Subframe 5)
  1) Eccentricity: 10777
  2) Almanac reference time: 111
  3) Orbital inclination: 58976
  4) Rate of right ascension: 691
  5) Root of semi major axis: 6222393
  6) Longitude of ascension node: 4614217
  7) Argument of perigee: 11235851
  8) Mean anomaly at reference time: 3973047
  9) Clock bias: 1910
  10) Clock drift: 0

----------------- Satelite number: 14 -----------------
                     (Subframe 5)
  1) Eccentricity: 14148
  2) Almanac reference time: 111
  3) Orbital inclination: 60194
  4) Rate of right ascension: 64837
  5) Root of semi major axis: 6222489
  6) Longitude of ascension node: 12240192
  7) Argument of perigee: 11360731
  8) Mean anomaly at reference time: 3638923
  9) Clock bias: 232
  10) Clock drift: 0

----------------- Satelite number: 15 -----------------
                     (Subframe 5)
  1) Eccentricity: 11286
  2) Almanac reference time: 111
  3) Orbital inclination: 219
  4) Rate of right ascension: 64801
  5) Root of semi major axis: 6222491
  6) Longitude of ascension node: 4274620
  7) Argument of perigee: 439308
  8) Mean anomaly at reference time: 11761330
  9) Clock bias: 119
  10) Clock drift: 2047
```
