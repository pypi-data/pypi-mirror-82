# -*- coding: utf-8 -*-

from ..init_fig import init_fig
from .plot_A_3D import plot_A_3D
from ...definitions import config_dict
from numpy import meshgrid, max as np_max


def plot_A_surf(
    data,
    is_deg=True,
    t_max=None,
    a_max=400,
    z_min=None,
    z_max=None,
    is_norm=False,
    unit="SI",
    colormap=None,
    save_path=None,
    fig=None,
    subplot_index=None,
):
    """Plots the isosurface of a field in 3D

    Parameters
    ----------
    data : Data
        a Data object
    is_deg : bool
        boolean indicating if the angle must be converted to degrees
    t_max : float
        maximum value of the time for the x axis
    a_max : float
        maximum value of the angle for the y axis
    z_min : float
        minimum value of the amplitude for the z axis
    z_max : float
        maximum value of the amplitude for the z axis
    is_norm : bool
        boolean indicating if the field must be normalized
    unit : str
        unit in which to plot the field
    colormap : colormap object
        colormap prescribed by user
    save_path : str
        path and name of the png file to save
    fig : Matplotlib.figure.Figure
        existing figure to use if None create a new one
    """

    # Set plot
    is_show_fig = True if fig is None else False
    (fig, axes, patch_leg, label_leg) = init_fig(fig, shape="rectangle")
    title = data.name + " as a function of time and space"
    if colormap is None:
        colormap = config_dict["PLOT"]["COLOR_DICT"]["COLOR_MAP"]
    xlabel = "Time [s]"
    if is_deg:
        ylabel = "Angle [°]"
    else:
        ylabel = "Angle [rad]"
    if unit == "SI":
        unit = data.unit
    if is_norm:
        zlabel = r"$\frac{" + data.symbol + "}{" + data.symbol + "_0}\, [" + unit + "]$"
    else:
        zlabel = r"$" + data.symbol + "\, [" + unit + "]$"

    # Extract the field
    if is_deg:
        results = data.get_along("time", "angle{°}", unit=unit, is_norm=is_norm)
    else:
        results = data.get_along("time", "angle{°}", unit=unit, is_norm=is_norm)

    angle = results["angle"]
    time = results["time"]
    Ydata = results[data.symbol]

    if is_deg and round(np_max(angle) / 6) % 5 == 0:
        yticks = [i * round(np_max(angle) / 6) for i in range(7)]
    else:
        yticks = None

    angle_map, time_map = meshgrid(angle, time)

    if t_max is None:
        t_max = np_max(time)

    if z_max is None:
        z_max = np_max(Ydata)

    if z_min is None:
        z_min = -z_max

    # Plot the original graph
    plot_A_3D(
        time_map,
        angle_map,
        Ydata,
        fig=fig,
        colormap=colormap,
        x_min=0,
        x_max=t_max,
        y_min=0,
        y_max=a_max,
        z_min=z_min,
        z_max=z_max,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        zlabel=zlabel,
        yticks=yticks,
        type="surf",
        save_path=save_path,
        subplot_index=subplot_index,
    )

    if is_show_fig:
        fig.show()
