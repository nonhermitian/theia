# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""A Warnings snackbar module"""
import ipyvuetify as vue
from IPython.display import display

INFO_COLOR = '#154890'
SUCCESS_COLOR = '#008C5B'
WARNING_COLOR = '#EB8921'
ERROR_COLOR = '#AA0114'

def message_widget(msg, kind='warning'):
    """Makes a warning snackbar.

    Only one snackbar is allowed at a time, so only
    one warning is displayed at a time.  Older warnings
    will be closed early if a new one is requested.

    Properties:
        msg (str): The warning string.
        kind (str): Kind of message ('info', 'success', 'warning', or 'error').
    """
    if kind == 'info':
        color = INFO_COLOR
        icon = 'info'
    elif kind == 'success':
        color = SUCCESS_COLOR
        icon = 'info'
    elif kind == 'warning':
        color = WARNING_COLOR
        icon = 'warning'
    elif kind == 'error':
        color = ERROR_COLOR
        icon = 'error'
    else:
        raise ValueError('Invalid input kind for message.')
    
    msg_html = vue.Html(tag='div',
                        children=[msg],
                        style_='font-weight: light; font-size: 14px;'
                                'margin: 0px 5px 0px 0px')

    children = [msg_html]

    msg_widget = vue.Alert(children=children,
                           outlined=False,
                           dense=True,
                           elevation=0,
                           text=True,
                           type=kind,
                           border="left",
                           style_='margin: 0px')

    display(msg_widget)
