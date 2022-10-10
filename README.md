my-kaggle-tools
==============================

Personal tools to compite in Kaggle competitions. Individual competitions are stored in the `./competitions` directory.

Environment Setup for Competitions 
------------

Since each competition has its own environment, it is recommended to use a virtual environment for each competition. The following steps will setup a virtual environment for a competition.

I'm using `conda` to manage my virtual environments. If you are using `conda`, you can use the following commands to setup a virtual environment for a competition.

```bash
cd ./competitions/<competition-name>
conda env create -f conda_<platform>.yml
```

I work mainly on Linux but sometimes I can switch to MacOS. I'll try to keep the `conda_<platform>.yml` files up to date for both platforms (if needed).

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── competitions       <- Individual Kaggle competitions are stored here.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Champion models from competions
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
