# 🛰️ python-gps-receiver
This project implements a software-defined GPS L1 receiver in Python. It focuses on the full signal processing chain required to extract navigation messages from raw I/Q samples using standard GPS signal structure and modulation.

## 📦 Features
- Reads raw I/Q data from `.dat` file
- Signal spectrum visualization
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
<br/>

---

### Input data

Sample data can be downloaded from [gnss-sdr](https://github.com/gnss-sdr/gnss-sdr) project page on [SourceForge](https://sourceforge.net/projects/gnss-sdr/files/data/). Alternatively, use this `wget` command in your terminal:<br/>
```bash
wget https://sourceforge.net/projects/gnss-sdr/files/data/2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN.tar.gz
```
If the estimated download time is too long, you can also download the data using Google Colab and then copy it to your Google Drive after mounting the drive in Colab Notebook.

Then unpack the archive:
```bash
tar -zxvf 2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN.tar.gz
```