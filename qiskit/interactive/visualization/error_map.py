# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
# pylint: disable=invalid-name

"""Interactive error map for devices"""

import math
import numpy as np
import seaborn as sns
import matplotlib as mpl
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .plotly_wrapper import PlotlyFigure
from .colormaps import HELIX_LIGHT, HELIX_DARK


def iplot_error_map(backend, figsize=(700, 500),
                    show_title=True,
                    remove_badcal_edges=True,
                    background_color='white'):
    """Plots the gate map of a device.

    Parameters:
        backend (BaseBackend): A backend instance.
        figsize (tuple): Figure size in pixels.
        show_title (bool): Show figure title.
        remove_badcal_edges (bool): Remove bad CX gate calibration
                                    data.
        background_color (str): Set the background color to 'white'
                                or 'black'.

    Returns:
        PlotlyFigure: The output figure.

    Raises:
        ValueError: Invalid color selection.
        TypeError: If tried to pass a simulator.
    """
    if background_color == 'white':
        color_map = sns.cubehelix_palette(reverse=True, as_cmap=True)
        text_color = '#000000'
        plotly_cmap = HELIX_LIGHT
    elif background_color == 'black':
        color_map = sns.cubehelix_palette(dark=0.25, light=0.97,
                                          reverse=True, as_cmap=True)
        text_color = '#FFFFFF'
        plotly_cmap = HELIX_DARK
    else:
        raise ValueError('Invalid background_color selection.')

    if backend.configuration().simulator:
        raise TypeError('Requires a device backend, not simulator.')

    mpl_data = {}

    mpl_data[20] = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4],
                    [1, 0], [1, 1], [1, 2], [1, 3], [1, 4],
                    [2, 0], [2, 1], [2, 2], [2, 3], [2, 4],
                    [3, 0], [3, 1], [3, 2], [3, 3], [3, 4]]

    mpl_data[14] = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4],
                    [0, 5], [0, 6], [1, 7], [1, 6], [1, 5],
                    [1, 4], [1, 3], [1, 2], [1, 1]]

    mpl_data[16] = [[1, 0], [0, 0], [0, 1], [0, 2], [0, 3],
                    [0, 4], [0, 5], [0, 6], [0, 7], [1, 7],
                    [1, 6], [1, 5], [1, 4], [1, 3], [1, 2], [1, 1]]

    mpl_data[5] = [[1, 0], [0, 1], [1, 1], [1, 2], [2, 1]]

    mpl_data[53] = [[0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
                    [1, 2], [1, 6],
                    [2, 0], [2, 1], [2, 2], [2, 3], [2, 4],
                    [2, 5], [2, 6], [2, 7], [2, 8],
                    [3, 0], [3, 4], [3, 8],
                    [4, 0], [4, 1], [4, 2], [4, 3], [4, 4],
                    [4, 5], [4, 6], [4, 7], [4, 8],
                    [5, 2], [5, 6],
                    [6, 0], [6, 1], [6, 2], [6, 3], [6, 4],
                    [6, 5], [6, 6], [6, 7], [6, 8],
                    [7, 0], [7, 4], [7, 8],
                    [8, 0], [8, 1], [8, 2], [8, 3], [8, 4],
                    [8, 5], [8, 6], [8, 7], [8, 8],
                    [9, 2], [9, 6]]

    config = backend.configuration()
    n_qubits = config.n_qubits
    cmap = config.coupling_map

    props = backend.properties().to_dict()

    t1s = []
    t2s = []
    for qubit_props in props['qubits']:
        count = 0
        for item in qubit_props:
            if item['name'] == 'T1':
                t1s.append(item['value'])
                count += 1
            elif item['name'] == 'T2':
                t2s.append(item['value'])
                count += 1
            if count == 2:
                break

    # U2 error rates
    single_gate_errors = [0]*n_qubits
    for gate in props['gates']:
        if gate['gate'] == 'u2':
            _qubit = gate['qubits'][0]
            single_gate_errors[_qubit] = gate['parameters'][0]['value']

    # Convert to percent
    single_gate_errors = 100 * np.asarray(single_gate_errors)
    avg_1q_err = np.mean(single_gate_errors)
    max_1q_err = max(single_gate_errors)

    single_norm = mpl.colors.Normalize(
        vmin=min(single_gate_errors), vmax=max_1q_err)

    q_colors = [mpl.colors.rgb2hex(color_map(single_norm(err))) for err in single_gate_errors]

    cx_errors = []
    for line in cmap:
        for item in props['gates']:
            if item['qubits'] == line:
                cx_errors.append(item['parameters'][0]['value'])
                break
        else:
            continue

    # Convert to percent
    cx_errors = 100 * np.asarray(cx_errors)

    # remove bad cx edges
    if remove_badcal_edges:
        cx_idx = np.where(cx_errors != 100.0)[0]
    else:
        cx_idx = np.arange(len(cx_errors))

    avg_cx_err = np.mean(cx_errors[cx_idx])

    cx_norm = mpl.colors.Normalize(
        vmin=min(cx_errors[cx_idx]), vmax=max(cx_errors[cx_idx]))

    line_colors = []
    for err in cx_errors:
        if err != 100.0 or not remove_badcal_edges:
            line_colors.append(mpl.colors.rgb2hex(color_map(cx_norm(err))))
        else:
            line_colors.append("#ff0000")

    # Measurement errors
    read_err = []

    for qubit in range(n_qubits):
        for item in props['qubits'][qubit]:
            if item['name'] == 'readout_error':
                read_err.append(item['value'])

    read_err = 100 * np.asarray(read_err)
    avg_read_err = np.mean(read_err)
    max_read_err = np.max(read_err)

    if n_qubits < 10:
        num_left = n_qubits
        num_right = 0
    else:
        num_left = math.ceil(n_qubits / 2)
        num_right = n_qubits - num_left

    if n_qubits in mpl_data.keys():
        grid_data = mpl_data[n_qubits]
    else:
        fig = go.Figure()
        fig.update_layout(showlegend=False,
                          plot_bgcolor=background_color,
                          paper_bgcolor=background_color,
                          width=figsize[0], height=figsize[1],
                          margin=dict(t=60, l=0, r=0, b=0)
                         )
        out = PlotlyFigure(fig)
        return out

    x_max = max([d[1] for d in grid_data])
    y_max = max([d[0] for d in grid_data])
    max_dim = max(x_max, y_max)

    qubit_size = 32
    font_size = 14
    offset = 0
    if y_max / max_dim < 0.33:
        qubit_size = 24
        font_size = 10
        offset = 1

    if n_qubits > 5:
        right_meas_title = "Readout Error (%)"
    else:
        right_meas_title = None

    fig = make_subplots(rows=2, cols=11, row_heights=[0.95, 0.05],
                        vertical_spacing=0.15,
                        specs=[[{"colspan": 2}, None, {"colspan": 6},
                                None, None, None,
                                None, None, {"colspan": 2},
                                None, None],
                               [{"colspan": 4}, None, None,
                                None, None, None,
                                {"colspan": 4}, None, None,
                                None, None]],
                        subplot_titles=("Readout Error (%)", None, right_meas_title,
                                        "Hadamard Error Rate [Avg. {}%]".format(
                                            np.round(avg_1q_err, 3)),
                                        "CNOT Error Rate [Avg. {}%]".format(
                                            np.round(avg_cx_err, 3)))
                       )

    # Add lines for couplings
    for ind, edge in enumerate(cmap):
        is_symmetric = False
        if edge[::-1] in cmap:
            is_symmetric = True
        y_start = grid_data[edge[0]][0] + offset
        x_start = grid_data[edge[0]][1]
        y_end = grid_data[edge[1]][0] + offset
        x_end = grid_data[edge[1]][1]

        if is_symmetric:
            if y_start == y_end:
                x_end = (x_end - x_start) / 2 + x_start
                x_mid = x_end
                y_mid = y_start

            elif x_start == x_end:
                y_end = (y_end - y_start) / 2 + y_start
                x_mid = x_start
                y_mid = y_end

            else:
                x_end = (x_end - x_start) / 2 + x_start
                y_end = (y_end - y_start) / 2 + y_start
                x_mid = x_end
                y_mid = y_end
        else:
            if y_start == y_end:
                x_mid = (x_end - x_start) / 2 + x_start
                y_mid = y_end

            elif x_start == x_end:
                x_mid = x_end
                y_mid = (y_end - y_start) / 2 + y_start

            else:
                x_mid = (x_end - x_start) / 2 + x_start
                y_mid = (y_end - y_start) / 2 + y_start

        fig.append_trace(
            go.Scatter(x=[x_start, x_mid, x_end],
                       y=[-y_start, -y_mid, -y_end],
                       mode="lines",
                       line=dict(width=6,
                                 color=line_colors[ind]
                                ),
                       hoverinfo='text',
                       hovertext='CX<sub>err</sub>{B}_{A} = {err} %'.format(
                           A=edge[0], B=edge[1], err=np.round(cx_errors[ind], 3))
                      ), row=1, col=3)

    # Add the qubits themselves
    qubit_text = []
    qubit_str = "<b>Qubit {}</b><br>H<sub>err</sub> = {} %"
    qubit_str += "<br>T1 = {} \u03BCs<br>T2 = {} \u03BCs"
    for kk in range(n_qubits):
        qubit_text.append(qubit_str.format(kk,
                                           np.round(single_gate_errors[kk], 3),
                                           np.round(t1s[kk], 2),
                                           np.round(t2s[kk], 2)))

    if n_qubits > 50:
        qubit_size = 20
        font_size = 9


    qtext_color = []
    for ii in range(n_qubits):
        if background_color == 'black':
            if single_gate_errors[ii] > 0.8*max_1q_err:
                qtext_color.append('black')
            else:
                qtext_color.append('white')
        else:
            qtext_color.append('white')

    fig.append_trace(go.Scatter(
        x=[d[1] for d in grid_data],
        y=[-d[0]-offset for d in grid_data],
        mode="markers+text",
        marker=go.scatter.Marker(size=qubit_size,
                                 color=q_colors,
                                 opacity=1),
        text=[str(ii) for ii in range(n_qubits)],
        textposition="middle center",
        textfont=dict(size=font_size, color=qtext_color),
        hoverinfo="text",
        hovertext=qubit_text), row=1, col=3)

    fig.update_xaxes(row=1, col=3, visible=False)
    _range = None
    if offset:
        _range = [-3.5, 0.5]
    fig.update_yaxes(row=1,
                     col=3,
                     visible=False,
                     range=_range)

    # H error rate colorbar
    fig.append_trace(go.Heatmap(z=[np.linspace(min(single_gate_errors),
                                               max(single_gate_errors), 100),
                                   np.linspace(min(single_gate_errors),
                                               max(single_gate_errors), 100)],
                                colorscale=plotly_cmap,
                                showscale=False,
                                hoverinfo='none'), row=2, col=1)

    fig.update_yaxes(row=2,
                     col=1,
                     visible=False)

    fig.update_xaxes(row=2,
                     col=1,
                     tickvals=[0, 49, 99],
                     ticktext=[np.round(min(single_gate_errors), 3),
                               np.round(max(single_gate_errors)- min(single_gate_errors), 3),
                               np.round(max(single_gate_errors), 3)])

    # CX error rate colorbar
    fig.append_trace(go.Heatmap(z=[np.linspace(min(cx_errors),
                                               max(cx_errors), 100),
                                   np.linspace(min(cx_errors),
                                               max(cx_errors), 100)],
                                colorscale=plotly_cmap,
                                showscale=False,
                                hoverinfo='none'), row=2, col=7)

    fig.update_yaxes(row=2, col=7, visible=False)

    fig.update_xaxes(row=2, col=7,
                     tickvals=[0, 49, 99],
                     ticktext=[np.round(min(cx_errors[cx_idx]), 3),
                               np.round(max(cx_errors[cx_idx])-min(cx_errors[cx_idx]), 3),
                               np.round(max(cx_errors[cx_idx]), 3)])

    hover_text = "<b>Qubit {}</b><br>M<sub>err</sub> = {} %"
    # Add the left side meas errors
    for kk in range(num_left-1, -1, -1):
        fig.append_trace(go.Bar(x=[read_err[kk]], y=[kk],
                                orientation='h',
                                marker=dict(color='#DDBBBA'),
                                hoverinfo="text",
                                hovertext=[hover_text.format(kk,
                                                             np.round(read_err[kk], 3)
                                                             )]
                               ),
                         row=1, col=1)

    fig.append_trace(go.Scatter(x=[avg_read_err, avg_read_err],
                                y=[-0.25, num_left-1+0.25],
                                mode='lines',
                                hoverinfo='none',
                                line=dict(color=text_color,
                                          width=2,
                                          dash='dot')), row=1, col=1)

    fig.update_yaxes(row=1, col=1,
                     tickvals=list(range(num_left)),
                     autorange="reversed")

    fig.update_xaxes(row=1, col=1,
                     range=[0, 1.1*max_read_err],
                     tickvals=[0, np.round(avg_read_err, 2),
                               np.round(max_read_err, 2)],
                     showline=True, linewidth=1, linecolor=text_color,
                     tickcolor=text_color,
                     ticks="outside",
                     showgrid=False,
                     zeroline=False)

    # Add the right side meas errors, if any
    if num_right:
        for kk in range(n_qubits-1, num_left-1, -1):
            fig.append_trace(go.Bar(x=[-read_err[kk]],
                                    y=[kk],
                                    orientation='h',
                                    marker=dict(color='#DDBBBA'),
                                    hoverinfo="text",
                                    hovertext=[hover_text.format(kk,
                                                                 np.round(read_err[kk], 3))]
                                   ), row=1, col=9)

        fig.append_trace(go.Scatter(x=[-avg_read_err, -avg_read_err],
                                    y=[num_left-0.25, n_qubits-1+0.25],
                                    mode='lines',
                                    hoverinfo='none',
                                    line=dict(color=text_color,
                                              width=2,
                                              dash='dot')
                                    ), row=1, col=9)

        fig.update_yaxes(row=1,
                         col=9,
                         tickvals=list(range(n_qubits-1, num_left-1, -1)),
                         side='right',
                         autorange="reversed",
                         )

        fig.update_xaxes(row=1,
                         col=9,
                         range=[-1.1*max_read_err, 0],
                         tickvals=[0, -np.round(avg_read_err, 2), -np.round(max_read_err, 2)],
                         ticktext=[0, np.round(avg_read_err, 2), np.round(max_read_err, 2)],
                         showline=True, linewidth=1, linecolor=text_color,
                         tickcolor=text_color,
                         ticks="outside",
                         showgrid=False,
                         zeroline=False)

    # Makes the subplot titles smaller than the 16pt default
    for ann in fig['layout']['annotations']:
        ann['font'] = dict(size=13)

    title_text = "{} Error Map".format(backend.name()) if show_title else ''
    fig.update_layout(showlegend=False,
                      plot_bgcolor=background_color,
                      paper_bgcolor=background_color,
                      width=figsize[0], height=figsize[1],
                      title=dict(text=title_text, x=0.452),
                      title_font_size=20,
                      font=dict(color=text_color),
                      margin=dict(t=60, l=0, r=0, b=0)
                     )

    return PlotlyFigure(fig)
