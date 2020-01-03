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

_CURRENT_WARNING = None

def warning_widget(msg, duration=5):
    """Makes a warning snackbar.

    Only one snackbar is allowed at a time, so only
    one warning is displayed at a time.  Older warnings
    will be closed early if a new one is requested.

    Properties:
        msg (str): The warning string.
        duration (int): Duration of snackbar in seconds.
    """
    global _CURRENT_WARNING  #pylint: disable=global-statement
    if _CURRENT_WARNING:
        _CURRENT_WARNING.value = False
        _CURRENT_WARNING.close()

    snack_button = vue.Btn(text=True, children=['close'],
                           style_='color:#212121')

    snack_icon = vue.Icon(children=['info'], style_='color:#212121; margin: 5px')

    snack = vue.Snackbar(right=True, bottom=True, value=True,
                         timeout=duration*1000, color='#F1C21B',
                         children=[snack_icon, msg, snack_button],
                         style_='color:#212121')

    #pylint: disable=unused-argument
    def on_click(widget, event, data):
        snack.value = False

    snack_button.on_event('click', on_click)

    _CURRENT_WARNING = snack

    display(snack)
