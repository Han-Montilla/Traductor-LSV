# Realtime VSL Translator

// TODO: add description

## Initial Setup

1. Clone this repo `git clone https://github.com/Han-Montilla/Traductor-LSV`
2. Update submodule dependencies `git submodule update --init`
3. Install virtual enviorment package `pip install virtualenv`
4. Create virtual enviorment `python -m venv .env` and activate it:
	- on windows `.env\Scripts\activate.bat`
	- on mac/linux `source .env/bin/activate`
6. Install python dependencies `pip install -r requirements.txt`

## Capturing & Labeling

> *If you already have a dataset to train on simply skip the first step

1. Capture images by running `scripts/capture.py` script
2. Partition your test (~10%), train (~80%) and validation (~10%) images into their respective folder within the `workspace/images` directory
3. Download a use [labelimg](https://github.com/heartexlabs/labelImg) to generate the corresponding XML for every image