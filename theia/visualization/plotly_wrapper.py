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
import plotly.graph_objects as go


class PlotlyWidget(go.FigureWidget):
    def __init__(self, data=None, layout=None, frames=None, skip_invalid=False, **kwargs):
        super(go.FigureWidget, self).__init__(data, layout, frames, skip_invalid, **kwargs)

    def show(self, *args, **kwargs):
        """Display the figure.
        """
        import plotly.io as pio

        config = {}
        if 'config' not in kwargs.keys():
            config={'scrollZoom': False,
                    'displayModeBar': False,
                    'editable': False}

        return pio.show(self, *args, config=config, **kwargs)

    def savefig(self, filename, figsize=(None, None), scale=1, transparent=False):
        """Safe the figure as a static image.

        Parameters:
            filename (str): Name of the file to which the image is saved.
            figsize (tuple): Size of figure in pixels.
            scale (float): Scale factor for non-vectorized image formats.
            transparent (bool): Set the background to transparent.
        """
        if transparent:
            plot_color = self.layout['plot_bgcolor']
            paper_color = self.layout['paper_bgcolor']
            self.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                               plot_bgcolor='rgba(0,0,0,0)')
        
        self.write_image(filename, width=figsize[0], height=figsize[1], scale=scale)
        if transparent:
            self.update_layout(plot_bgcolor=plot_color,
                               paper_bgcolor=paper_color)
