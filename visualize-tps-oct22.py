# %% [code]
"""Visualize field, players positions and animate matches."""

from typing import Tuple

import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from matplotlib.path import Path
from matplotlib.patches import PathPatch, Wedge
from matplotlib import rc

rc("animation", html="jshtml")


def draw_rocket_league_field(
    field_fig: matplotlib.figure.Figure, field_ax: matplotlib.axes.SubplotBase
) -> Tuple[matplotlib.figure.Figure, matplotlib.axes.SubplotBase]:
    """
    Draws the rocket league playfield for Kaggle TPS Oct., 2022.

    Author: Sergey Saharovskiy
    Source: https://www.kaggle.com/code/sergiosaharovskiy/tps-oct-2022-viz-players-positions-animated/notebook

    :param field_fig: Figure to draw on
    :param field_ax: Axes to draw on
    :return matplotlib.figure.Figure, matplotlib.axes._subplots.AxesSubplot:
    """

    # Draws two field rectangles ('Player Field Border', 'Ball Field Border').
    center = (0, 0)

    codes_pl = [Path.MOVETO] + [Path.LINETO] * 3 + [Path.CLOSEPOLY]
    vertices_pl = [
        (-120, -82.5),
        (120, -82.5),
        (120, 82.5),
        (-120, 82.5),
        center,
    ]  # inversed x, y.

    codes_ball = [Path.MOVETO] + [Path.LINETO] * 3 + [Path.CLOSEPOLY]
    vertices_ball = [
        (-104.3125, -80.8125),
        (104.3125, -80.8125),
        (104.3125, 80.6875),
        (-104.3125, 80.6875),
        center,
    ]  # inversed x, y.

    path_pl = Path(vertices_pl, codes_pl)
    path_ball = Path(vertices_ball, codes_ball)

    pathpatch_pl = PathPatch(
        path_pl,
        facecolor="#676C40",
        edgecolor="#516EA7",
        linewidth=2,
        label="Player Field Border",
    )
    pathpatch_ball = PathPatch(
        path_ball,
        facecolor="none",
        edgecolor="yellow",
        linewidth=1,
        label="Ball Field Border",
    )

    # Draws the center outer and inner circles.
    center_outer_circle = patches.CirclePolygon(
        center, 20, color="white", fill=False, alpha=0.7
    )

    theta1, theta2 = 90, 90 + 180
    center_half_inner_circle_blue = Wedge(
        center, 10, theta1, theta2, fc="#516EA7", alpha=0.6
    )
    center_half_inner_circle_orange = Wedge(
        center, 10, theta2, theta1, fc="#C57E31", alpha=0.6
    )

    field_ax.add_patch(pathpatch_pl)

    # Draws the dark green stripes.
    for i in range(6):
        dgreen_stripe = patches.Rectangle(
            (-110 + i * 40, -80), 20, 160, color="#565B39"
        )
        field_ax.add_patch(dgreen_stripe)

    # Draws the white corner triangles.
    corners = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
    for corner in corners:
        coor_x, coor_y = corner[0], corner[1]
        corner_triangle = patches.Polygon(
            [
                (121 * coor_x, 85 * coor_y),
                (105 * coor_x, 85 * coor_y),
                (121 * coor_x, 55 * coor_y),
            ],
            40,
            color="white",
        )
        field_ax.add_patch(corner_triangle)

    # Draws the blue and orange outer goalie boxes.
    for i, color in enumerate(["#617A95", "#8D5C2C"]):
        goal_outer_box = patches.Rectangle(
            (-120 + i * 200, -50), 40, 100, color=color, alpha=0.7, ec="white"
        )
        field_ax.add_patch(goal_outer_box)

    # Draws the blue and orange inner goalie boxes.
    for i in range(2):
        goal_inner_box = patches.Rectangle(
            (-120 + i * 230, -25), 10, 50, color="none", ec="white"
        )
        field_ax.add_patch(goal_inner_box)

    # Draws center white cross.
    plt.plot([-70, 70], [0, 0], color="white", alpha=0.7)
    plt.plot([0, 0], [-80.5, 80.5], color="white", alpha=0.7)

    # Adds the patches from above drawings.
    field_ax.add_patch(pathpatch_ball)
    field_ax.add_patch(center_outer_circle)
    field_ax.add_patch(center_half_inner_circle_blue)
    field_ax.add_patch(center_half_inner_circle_orange)

    # Adds the title, legend and removes x, y-axis with the respective ticks.
    for pos in ["top", "bottom", "left", "right"]:
        field_ax.spines[pos].set_visible(False)

    field_ax.get_xaxis().set_visible(False)
    field_ax.get_yaxis().set_visible(False)
    field_ax.set_title("Playfield")

    plt.legend(
        handles=[pathpatch_pl, pathpatch_ball],
        facecolor="#676C40",
        labelcolor="white",
        loc="upper right",
        bbox_to_anchor=(0.964, 1.05),
    )

    return field_fig, field_ax


def draw_rocket_league_position(
    data: pd.DataFrame,
    meta: dict,
    field: Tuple[matplotlib.figure.Figure, matplotlib.axes.SubplotBase],
) -> Tuple[matplotlib.figure.Figure, matplotlib.axes.SubplotBase]:
    """
    Draws the starting positions or the consequtive frames of
    the specified game_num, event_id and event_time (optional).

    Author: Sergey Saharovskiy
    Source: https://www.kaggle.com/code/sergiosaharovskiy/tps-oct-2022-viz-players-positions-animated/notebook

    :param data: pd.DataFrame with the data containing the positions of players and ball in 2 dimensions.
    :param meta: dict with the meta position: game_num, event_id, event_time.
    :param field: Tuple[matplotlib.figure.Figure, matplotlib.axes.SubplotBase] with matplotlib figure and axes.
    :return: Tuple[matplotlib.figure.Figure, matplotlib.axes.SubplotBase] with matplotlib figure and axes.
    """

    game_num = meta["game_num"]
    event_id = meta["event_id"]
    event_time = meta["event_time"]

    field_fig, field_ax = field[0], field[1]
    match_fig, match_ax = draw_rocket_league_field(field_fig, field_ax)

    player_positions_y = data.columns[
        data.columns.str.contains("(^[p0-9_]+)([pos_]+x)")
    ]
    player_positions_x = data.columns[
        data.columns.str.contains("(^[p0-9_]+)([pos_]+y)")
    ]

    ball_positions_y = "ball_pos_x"
    ball_positions_x = "ball_pos_y"

    if event_time:
        game = data.query(
            f"game_num == {game_num} and event_id == {event_id} and event_time == {event_time}"
        )
        title = f"game #{game_num} event_id {event_id} event_time {event_time:.2f}"
    else:
        game = data.query(f"game_num == {game_num} and event_id == {event_id}")
        title = f"game #{game_num} event_id {event_id}"

    x_coordinates_ball = pd.melt(
        game,
        id_vars=["game_num", "event_time"],
        value_vars=ball_positions_x,
        var_name="ball_pos_x",
        value_name="X",
    )
    y_coordinates_ball = pd.melt(
        game,
        id_vars=["game_num", "event_time"],
        value_vars=ball_positions_y,
        var_name="ball_pos_y",
        value_name="Y",
    )
    x_coordinates_pl = pd.melt(
        game,
        id_vars=["game_num", "event_time"],
        value_vars=player_positions_x,
        var_name="player_pos_x",
        value_name="X",
    )
    y_coordinates_pl = pd.melt(
        game,
        id_vars=["game_num", "event_time"],
        value_vars=player_positions_y,
        var_name="player_pos_y",
        value_name="Y",
    )

    game_ball = pd.concat([x_coordinates_ball, y_coordinates_ball["Y"]], axis=1)[
        ["game_num", "event_time", "X", "Y"]
    ]
    game_pl = pd.concat([x_coordinates_pl, y_coordinates_pl["Y"]], axis=1)[
        ["game_num", "event_time", "player_pos_x", "X", "Y"]
    ]
    game_pl["player"] = game_pl.player_pos_x.str.extract("([0-9])+")

    sns.scatterplot(
        data=game_pl.iloc[: int(game_pl.shape[0] / 2), :],
        x="X",
        y="Y",
        ax=match_ax,
        marker="o",
        s=45,
        hue="player",
        palette="Blues_r",
    )
    sns.scatterplot(
        data=game_pl.iloc[-int(game_pl.shape[0] / 2) :, :],
        x="X",
        y="Y",
        ax=match_ax,
        marker="o",
        s=45,
        hue="player",
        palette="Oranges_r",
    )

    sns.scatterplot(
        data=game_ball,
        x="X",
        y="Y",
        ax=match_ax,
        color="red",
        marker="*",
        s=150,
        label="Ball",
    )
    match_ax.legend(
        facecolor="#676C40",
        labelcolor="white",
        loc="upper right",
        bbox_to_anchor=(1.2, 1.04),
    )
    plt.title(title)

    return match_fig, match_ax


def draw_rocket_league_ball(
    data: pd.DataFrame,
    meta: dict,
    field: Tuple[matplotlib.figure.Figure, matplotlib.axes.SubplotBase],
) -> Tuple[matplotlib.figure.Figure, matplotlib.axes.SubplotBase]:
    """
    Draws ball position in 2 dimensions for an specific 
    game_num, event_id and event_time (optional).

    Author: Sergey Saharovskiy
    Source: https://www.kaggle.com/code/sergiosaharovskiy/tps-oct-2022-viz-players-positions-animated/notebook

    :param data: pd.DataFrame with the data containing the positions of players and ball in 2 dimensions.
    :param meta: dict with the meta position: game_num, event_id, event_time.
    :param field: Tuple[matplotlib.figure.Figure, matplotlib.axes.SubplotBase] with matplotlib figure and axes.
    :return: Tuple[matplotlib.figure.Figure, matplotlib.axes.SubplotBase] with matplotlib figure and axes.
    """

    game_num = meta["game_num"]
    event_id = meta["event_id"]
    event_time = meta["event_time"]

    field_fig, field_ax = field[0], field[1]
    match_fig, match_ax = draw_rocket_league_field(field_fig, field_ax)

    ball_positions_y = "ball_pos_x"
    ball_positions_x = "ball_pos_y"

    if event_time:
        game = data.query(
            f"game_num == {game_num} and event_id == {event_id} and event_time == {event_time}"
        )
        title = f"game #{game_num} event_id {event_id} event_time {event_time:.2f}"
    
    else:    
        if event_id:
            game = data.query(f"game_num == {game_num} and event_id == {event_id}")
            title = f"game #{game_num} event_id {event_id}"
        
        else:
            if game_num:
                game = data.query(f"game_num == {game_num}")
                title = f"game #{game_num}"
            
            else:
                game = data
                title = ""

    x_coordinates_ball = pd.melt(
        game,
        # id_vars=["game_num", "event_time"],
        value_vars=ball_positions_x,
        var_name="ball_pos_x",
        value_name="X",
    )
    y_coordinates_ball = pd.melt(
        game,
        # id_vars=["game_num", "event_time"],
        value_vars=ball_positions_y,
        var_name="ball_pos_y",
        value_name="Y",
    )
    vel_coordinates_ball = pd.melt(
        game,
        # id_vars=["game_num", "event_time"],
        value_vars="ball_vel_scalar",
        var_name="velocity",
        value_name="V",
    )

    game_ball = pd.concat([
        x_coordinates_ball["X"], 
        y_coordinates_ball["Y"], 
        vel_coordinates_ball["V"]
        ], axis=1)[
        ["X", "Y", "V"]
    ]

    sns.scatterplot(
        data=game_ball,
        x="X",
        y="Y",
        ax=match_ax,
        size="V",
        sizes=(10, 50),
        hue="V",
        palette="coolwarm",
        label="Avg Ball Position\n(10s before score)",
        alpha=0.75,
    )
    match_ax.legend(
        facecolor="#676C40",
        labelcolor="white",
        loc="upper right",
        bbox_to_anchor=(1.2, 1.04),
    )
    plt.title(title)

    return match_fig, match_ax
