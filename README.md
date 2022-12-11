# Realtime VSL Translator

// TODO: add description

## Initial Setup

1. Clone this repo `git clone https://github.com/Han-Montilla/Traductor-LSV.git`
2. Install virtual enviorment package `pip install virtualenv`
3. Create virtual enviorment `python -m venv .env` and activate it:
	- on windows `.env\Scripts\activate.bat`
	- on mac/linux `source .env/Scripts/activate`
4.  If prompted, upgrade pip `python -m pip install --upgrade pip`
5. Run the following commands (in order)
	1. `pip install tensorflow --upgrade`
	2. `pip install ipykernel opencv-python labelImg matplotlib pytz pycocotools Cython wget pyyaml tensorflow-gpu tensorflow-addons`
	3. `python -m ipykernel install --user --name=.env`
	4. Optionally, install your linter of choice
6. If you'd like to use your GPU for training, follow [tensorflows](https://www.tensorflow.org/install) guide
7. Open the `main.ipynb` notebook to get started.

## Dataset prep & Labeling

> *If you already have a dataset to train on skip the first and second step*

1. In the `Definitions` section there is a `SIGNS` array, edit this too choose which signs to capture
2. Head over to the `Capturing` section to begin capturing images using a webcam
3. Partition your test (~10%), train (~80%) and validation (~10%) images into their respective folder within the `workspace/images` directory
4. Run `labelimg`  or the cell in the `Labeling` section to start [labelimg](https://github.com/heartexlabs/labelImg).  Label all your images with the correct class. Make sure the bounding boxes are as tight as possible.

> if labelimg throws an error about incomplatable types  replace the `.env/Lib/site-packages/labelImg/labelImg.py` with `backups/labelimg/labelImg.py` and the `.env/Lib/site-packages/libs/canvas.py` with `backups/labelimg/canvas.py`

## Training

1. Choose which model to use (for transfer learning) on tensorflows official [model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md)
2. Update the `Definitions` section's `PRETRAINED_MODEL_NAME` and `PRETRAINED_MODEL_URL` variables to match your choice. Optionally change `MODEL_NAME` variable to change the generate model folder name
3. 