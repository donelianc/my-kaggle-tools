"""Feature engineering and feature creation."""

from pandas.core.frame import DataFrame
from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.utils.validation import check_is_fitted
from sklearn.utils.validation import _generate_get_feature_names_out


class PlayerDemolished(BaseEstimator, TransformerMixin):
    """Create a feature that indicates whether a player was demolished."""

    def __init__(self):
        self.player_features = None
        self.feature_names_out = None
        self._n_features_out = 6

    def fit(self, X, y=None):
        """
        Fit the transformer on data

        Parameters
        ----------
        data : pandas.DataFrame
            The data to fit the transformer on data
        y : pandas.Series, default=None
            The target variable

        Returns
        -------
        self
        """
        columns = X.columns
        self.player_features = columns[columns.str.startswith(r"p[0-5]_")].to_list()
        self.feature_names_out = [f"p{i}_demolished" for i in range(6)]
        return self

    def transform(self, X):
        """
        Transform the X. This method is called by the pipeline.
        Identify the player that was demolished and create a feature.

        Parameters
        ----------
        data : pandas.DataFrame
            The data to transform

        Returns
        -------
        pandas.DataFrame
            The transformed data
        """

        X_copy = X.copy()
        for i in range(6):
            X_copy[self.feature_names_out[i]] = (
                X_copy[self.player_features].isna().all(axis=1).astype(int)
            )
        return X_copy[self.feature_names_out]

    # TODO: Improve this method
    def get_feature_names_out(self, input_features=None):
        """Get output feature names for transformation.

        Parameters
        ----------
        input_features : array-like of str or None, default=None
            Only used to validate feature names with the names seen in :meth:`fit`.

        Returns
        -------
        feature_names_out : ndarray of str objects
            Transformed feature names.
        """
        check_is_fitted(self, "_n_features_out")
        return _generate_get_feature_names_out(
            self, self._n_features_out, input_features=input_features
        )


# TODO: Another implementation (using FunctionTransformer) can be found here:
# https://github.com/scikit-learn/scikit-learn/discussions/23992
class DistanceBallGoalPosts(BaseEstimator, TransformerMixin):
    """Create a feature that indicates the distance between the ball and the goal posts."""

    def __init__(self, posts):
        self.posts = posts
        self.ball_position = None
        self.feature_names_out = None
        self._n_features_out = 2

    def fit(self, X, y=None):
        """
        Fit the transformer on data

        Parameters
        ----------
        data : pandas.DataFrame
            The data to fit the transformer on data
        target : pandas.Series, default=None
            The target variable

        Returns
        -------
        self
        """

        self.ball_position = ["ball_pos_x", "ball_pos_y", "ball_pos_z"]
        self.feature_names_out = [
            f"ball_distance_to_post{i}" for i in range(1, len(self.posts) + 1)
        ]

        return self

    def transform(self, X):
        """
        Transform the X. This method is called by the pipeline.
        Calculate the distance between the ball and the goal posts.

        Parameters
        ----------
        data : pandas.DataFrame
            The data to transform

        Returns
        -------
        pandas.DataFrame
            The transformed data
        """

        X_copy = X.copy()
        for i, post in enumerate(self.posts):
            X_copy[self.feature_names_out[i]] = (
                X_copy[self.ball_position].sub(post).pow(2).sum(axis=1).pow(0.5)
            )
        return X_copy[self.feature_names_out]

    def get_feature_names_out(self, input_features=None):
        """Get output feature names for transformation.

        Parameters
        ----------
        input_features : array-like of str or None, default=None
            Only used to validate feature names with the names seen in :meth:`fit`.

        Returns
        -------
        feature_names_out : ndarray of str objects
            Transformed feature names.
        """
        check_is_fitted(self, "_n_features_out")
        return _generate_get_feature_names_out(
            self, self._n_features_out, input_features=input_features
        )


class BallSpeed(BaseEstimator, TransformerMixin):
    """Create a feature that indicates the speed of the ball."""

    def __init__(self):
        self.ball_velocity = None
        self.feature_names_out = None
        self._n_features_out = 1

    def fit(self, X, y=None):
        """
        Fit the transformer on data
        """
        self.feature_names_out = ["ball_speed"]
        return self

    def transform(self, X: DataFrame):
        """
        Transform the X. This method is called by the pipeline.
        Calculate the speed of the ball.
        """
        X_copy = X.copy()     
        ball_velocity = ["ball_vel_x", "ball_vel_y", "ball_vel_z"]   
        X_copy[self.feature_names_out[0]] = X_copy[ball_velocity].pow(2).sum(axis=1).pow(0.5)
        return X_copy[self.feature_names_out]

    def get_feature_names_out(self, input_features=None):
        """Get output feature names for transformation.

        Parameters
        ----------
        input_features : array-like of str or None, default=None
            Only used to validate feature names with the names seen in :meth:`fit`.

        Returns
        -------
        feature_names_out : ndarray of str objects
            Transformed feature names.
        """
        check_is_fitted(self, "_n_features_out")
        return _generate_get_feature_names_out(
            self, self._n_features_out, input_features=input_features
        )


class PlayerSpeed(BaseEstimator, TransformerMixin):
    """Create a feature that indicates the speed of the players."""

    def __init__(self):
        self.feature_names_out = None
        self._n_features_out = 6

    def fit(self, X, y=None):
        """
        Fit the transformer on data
        """
        self.feature_names_out = [f"p{i}_speed" for i in range(6)]
        return self

    def transform(self, X):
        """
        Transform the X. This method is called by the pipeline.
        Calculate the speed of the players.

        Parameters
        ----------
        data : pandas.DataFrame
            The data to transform

        Returns
        -------
        pandas.DataFrame
            The transformed data
        """
        X_copy = X.copy()

        for i in range(6):
            velocity_vector = [v for v in X_copy.columns if v.startswith(f"p{i}")]
            X_copy[self.feature_names_out[i]] = X_copy[velocity_vector].pow(2).sum(axis=1).pow(0.5)

        return X_copy[self.feature_names_out]

    def get_feature_names_out(self, input_features=None):
        """Get output feature names for transformation.

        Parameters
        ----------
        input_features : array-like of str or None, default=None
            Only used to validate feature names with the names seen in :meth:`fit`.

        Returns
        -------
        feature_names_out : ndarray of str objects
            Transformed feature names.
        """
        check_is_fitted(self, "_n_features_out")
        return _generate_get_feature_names_out(
            self, self._n_features_out, input_features=input_features
        )


class TeamCentroid(BaseEstimator, TransformerMixin):
    """Create a feature that indicates the centroid of the team."""

    def __init__(self):
        self.feature_names_out = None
        self._n_features_out = 2

    def fit(self, X, y=None):
        """
        Fit the transformer on data
        """
        team_A_centroids = [f"team_A_centroid_{axis}" for axis in ["x", "y"]]
        team_B_centroids = [f"team_B_centroid_{axis}" for axis in ["x", "y"]]
        self.feature_names_out = team_A_centroids + team_B_centroids
        return self

    def transform(self, X):
        """
        Transform the X. This method is called by the pipeline.
        Calculate the centroid of the team.

        Parameters
        ----------
        data : pandas.DataFrame
            The data to transform

        Returns
        -------
        pandas.DataFrame
            The transformed data
        """
        X_copy = X.copy()
        for team in ["A", "B"]:
            if team == "A":
                xpositions = X_copy.columns[
                    X_copy.columns.str.contains(r"p[0-2]_pos_x")
                ]
                ypositions = X_copy.columns[
                    X_copy.columns.str.contains(r"p[0-2]_pos_y")
                ]
            elif team == "B":
                xpositions = X_copy.columns[
                    X_copy.columns.str.contains(r"p[3-5]_pos_x")
                ]
                ypositions = X_copy.columns[
                    X_copy.columns.str.contains(r"p[3-5]_pos_y")
                ]

            X_copy[f"team_{team}_centroid_x"] = X_copy[xpositions].fillna(0).mean(axis=1)
            X_copy[f"team_{team}_centroid_y"] = X_copy[ypositions].fillna(0).mean(axis=1)

        return X_copy[self.feature_names_out]

    def get_feature_names_out(self, input_features=None):
        """Get output feature names for transformation.

        Parameters
        ----------
        input_features : array-like of str or None, default=None
            Only used to validate feature names with the names seen in :meth:`fit`.

        Returns
        -------
        feature_names_out : ndarray of str objects
            Transformed feature names.
        """
        check_is_fitted(self, "_n_features_out")
        return _generate_get_feature_names_out(
            self, self._n_features_out, input_features=input_features
        )
