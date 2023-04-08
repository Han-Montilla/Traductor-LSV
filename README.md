### Initial Setup
1. Create python virtual enviorment with [conda](https://docs.conda.io/en/latest/miniconda.html) `conda create -n lsv python=3.9`
2. Activate virtual enviorment: `conda activate lsv`
3. For GPU support:
	`conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0`
1. Upgrade `pip`: `pip install --upgrade pip`
2. Install local dependencies: `pip install "tensorflow<2.11" opencv-python mediapipe scikit-learn ipykernel tensorflowjs`