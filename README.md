[![ZnTrack](https://img.shields.io/badge/Powered%20by-ZnTrack-%23007CB0)](https://zntrack.readthedocs.io/en/latest/)
[![zincware](https://img.shields.io/badge/Powered%20by-zincware-darkcyan)](https://github.com/zincware)
# 2024_ZnTrack_Workshop
## Setup a Python environment 
```bash
conda create -n spp2363  -c conda-forge python=3.11
conda activate spp2363
pip install -r requirements.txt
```

## Setup DVC remote

```bash
export AWS_ACCESS_KEY_ID='myid'
export AWS_SECRET_ACCESS_KEY='mysecret'
```

## Run the Experiment
1. Switch to a feature branch
```bash
git checkout -b <branch-name>
```
2. Adapt the `main.py`
3. Run the experiment
```bash
python main.py
```
4. Commit and push your results
```
git add .
git commit -m "<experiment description>"
git push --set-upstream origin <branch-name>
# or simply git push
dvc push
```
5. Start new experiment at 1. or 2.
