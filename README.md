
conda create --name [YOUR_ENV_NAME] python=3.9

nvidia-smi

conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0 ipykernel

pip install --upgrade pip

pip install tensorflow opencv-python mediapipe scikit-learn


export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/