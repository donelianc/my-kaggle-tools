"""Build base model and train it."""

from typing import Tuple
from yaml import safe_load

from pandas import read_feather, read_csv

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_selector as selector

from sklearn.impute import SimpleImputer

from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler, StandardScaler

from src.features.build_features import *


class BaseModel:
    """Base model class."""

    def __init__(self) -> None:
        self.config = None

        self.data = None

        self.features_in = None
        self.target = None
        self.team = None

        self.base_pipeline = None

    def read_config(self, path: str) -> dict:
        """Read config file and return dict."""

        self.config = safe_load(open(path, "r", encoding="utf-8"))
        return self.config

    def get_data(self) -> Tuple[list, str]:
        """Read data from model config and return features and target"""

        assert (
            self.config is not None
        ), "Model has not been configured yet. Run read_config() first."

        self.data = read_feather("../" + self.config["paths"]["data"])
        self.data.set_index(self.config["data"]["index"], inplace=True)

        model_features = read_csv("../" + self.config["paths"]["dtypes"])

        self.features_in = [
            feature for feature in model_features.column.tolist() if feature != "id"
        ]
        self.team = self.config["model"]["team"]
        self.target = f"team_{self.team}_scoring_within_10sec"

        return self.features_in, self.target

    def build_base_pipeline(self) -> None:
        """Build model pipeline."""

        assert (
            self.config is not None
        ), "Model has not been configured yet. Run read_config() first."

        player_pipe_meta = dict()
        for feature in self.config["model"]["features"]["player"]:

            if feature == "demolished":
                player_pipe_meta[feature] = {
                    "transformer": PlayerDemolished(),
                    "columns": selector("p[0-5]"),
                }

            if feature == "velocity":
                player_velocity_pipe = Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="constant", fill_value=0.0)),
                        ("scaler", MinMaxScaler()),
                    ]
                )
                player_pipe_meta[feature] = {
                    "transformer": player_velocity_pipe,
                    "columns": selector("p[0-5]_vel_"),
                }

            if feature == "speed":
                player_speed_pipe = Pipeline(
                    steps=[
                        ("speed", PlayerSpeed()),
                        ("imputer", SimpleImputer(strategy="constant", fill_value=0.0)),
                        ("scaler", StandardScaler()),
                    ]
                )
                player_pipe_meta[feature] = {
                    "transformer": player_speed_pipe,
                    "columns": selector("p[0-5]_vel_]"),
                }

            if feature == "position":
                player_position_pipe = Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="constant", fill_value=0.0)),
                        ("scaler", MinMaxScaler()),
                    ]
                )
                player_pipe_meta[feature] = {
                    "transformer": player_position_pipe,
                    "columns": selector("p[0-5]_pos_"),
                }

        player_trans = ColumnTransformer(
            transformers=[
                (name, pipe["transformer"], pipe["columns"])
                for name, pipe in player_pipe_meta.items()
            ],
        )

        ball_pipe_meta = dict()
        for feature in self.config["model"]["features"]["ball"]:

            if feature == "velocity":
                ball_velocity_pipe = Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="constant", fill_value=0.0)),
                        ("scaler", MaxAbsScaler()),
                    ]
                )
                ball_pipe_meta[feature] = {
                    "transformer": ball_velocity_pipe,
                    "columns": selector("ball_vel_"),
                }

            if feature == "speed":
                ball_speed_pipe = Pipeline(
                    steps=[
                        ("speed", BallSpeed()),
                        ("scaler", StandardScaler()),
                    ]
                )
                ball_pipe_meta[feature] = {
                    "transformer": ball_speed_pipe,
                    "columns": selector("ball_vel_]"),
                }

            if feature == "position":
                ball_position_pipe = Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="constant", fill_value=0.0)),
                        ("scaler", MinMaxScaler()),
                    ]
                )
                ball_pipe_meta[feature] = {
                    "transformer": ball_position_pipe,
                    "columns": selector("ball_pos_"),
                }

            if feature == "distance_to_goal_posts":
                distance_to_goal_posts_pipe = Pipeline(
                    steps=[
                        (
                            "distance",
                            DistanceBallGoalPosts(
                                posts=[
                                    self.config["data"]["goal_post1"],
                                    self.config["data"]["goal_post2"],
                                ]
                            ),
                        ),
                        ("scaler", MinMaxScaler()),
                    ]
                )
                ball_pipe_meta[feature] = {
                    "transformer": distance_to_goal_posts_pipe,
                    "columns": selector("ball_pos_"),
                }

        ball_trans = ColumnTransformer(
            transformers=[
                (name, pipe["transformer"], pipe["columns"])
                for name, pipe in ball_pipe_meta.items()
            ],
        )

        timer_pipe_meta = dict()
        for feature in self.config["model"]["features"]["timer"]:

            if feature == "timer":
                timer_pipe = Pipeline(
                    steps=[
                        (
                            "timer",
                            FunctionTransformer(abs, feature_names_out="one-to-one"),
                        ),
                        ("scaler", MaxAbsScaler()),
                    ]
                )
                timer_pipe_meta[feature] = {
                    "transformer": timer_pipe,
                    "columns": selector("boost[0-5]_timer"),
                }

        timer_trans = ColumnTransformer(
            transformers=[
                (name, pipe["transformer"], pipe["columns"])
                for name, pipe in timer_pipe_meta.items()
            ],
        )

        booster_pipe_meta = dict()
        for feature in self.config["model"]["features"]["booster"]:

            if feature == "booster":
                booster_pipe = Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="constant", fill_value=0.0)),
                        ("scaler", MaxAbsScaler()),
                    ]
                )
                booster_pipe_meta[feature] = {
                    "transformer": booster_pipe,
                    "columns": selector("p[0-5]_boost"),
                }

        booster_trans = ColumnTransformer(
            transformers=[
                (name, pipe["transformer"], pipe["columns"])
                for name, pipe in booster_pipe_meta.items()
            ],
        )

        team_pipe_meta = dict()
        for feature in self.config["model"]["features"]["team"]:

            if feature == "centroid":
                team_pipe = Pipeline(
                    steps=[
                        ("team_centroid", TeamCentroid()),
                        ("scaler", StandardScaler()),
                    ]
                )
                team_pipe_meta[feature] = {
                    "transformer": team_pipe,
                    "columns": selector("p[0-5]_pos_"),
                }

        team_trans = ColumnTransformer(
            transformers=[
                (name, pipe["transformer"], pipe["columns"])
                for name, pipe in team_pipe_meta.items()
            ],
        )

        processor_pipe = FeatureUnion(
            transformer_list=[
                ("player", player_trans),
                ("ball", ball_trans),
                ("timer", timer_trans),
                ("booster", booster_trans),
                ("team", team_trans),
            ],
        )

        self.base_pipeline = Pipeline(
            steps=[
                ("preprocessor", processor_pipe),
            ]
        )
