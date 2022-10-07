Tabular Playground Series - Oct 2022
==============================

This may be one of the most challenging Tabular Playground competitions to date! It just so happens that one of Kaggle's software engineers is an avid Rocket League player and he's assembled a dataset of Rocket League gameplay for this month's TPS.

This month's challenge is to predict the probability of each team scoring within the next 10 seconds of the game given a snapshot from a Rocket League match. Sounds awesome, right?

Well, it's not that simple. The training data is fairly large; trying to read and model it in a single go might pose some challenges. The purpose of this month's competition is for you to explore ways you can take a big dataset and make it manageable within the time and resources you have. For most people, typical brute force approaches aren't going to work well.

- Can you scale down the dataset?
- Can you use, e.g., online learning methods that allow you to train from the data one row at a time? (FTLR is a great place to start if you're not familiar with online learning! e.g., this notebook)
- Can you figure out a nice set of features to reduce the dataset down to?

In addition to that challenge, while your predictions must be made pointwise, the training data is made up of timeseries—maybe you can use that temporal information to improve your model? This competition also has plenty of opportunity for data visualizations. Let's see some pretty graphs!

So, share your ideas about tackling this beast of a dataset and have a great time!

Acknowledgments
------------

This competition includes Rocket League data and images from the [Rocket League Community Tournament Assets](https://epicgames.ent.box.com/s/z14m4isqko9ifumy12e1o4sdy72wyzyz/folder/154490878719).

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
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
