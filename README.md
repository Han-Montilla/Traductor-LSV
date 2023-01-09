
FOR TRAINING:
`conda create --name [YOUR_ENV_NAME] python=3.9`
`conda activate [YOUR_ENV_NAME]`
`nvidia-smi`
`conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0 ipykernel`
`export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/`
`pip install --upgrade pip`
`pip install tensorflow opencv-python mediapipe scikit-learn`

FOR DETECTING:
`pip install virtualenv`
`python -m venv .env`
`source .env/Scripts/activate` or `.env\Scripts\activate.bat`
`python -m pip install --upgrade pip`
`pip install tensorflow opencv-python mediapipe scikit-learn ipykernel`
