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
import threading
import time
import ipyvuetify as vue
from IPython.display import display

_CURRENT_WARNING = None


INFO_COLOR = '#154890'
SUCCESS_COLOR = '#008C5B'
WARNING_COLOR = '#EB8921'


def _close_snack(snack, duration):
    """Closes a snackbar after the specified duration.
    """
    time.sleep(duration)
    snack.close()

def message_widget(msg, kind='info', warning_kind=None, duration=5):
    """Makes a warning snackbar.

    Only one snackbar is allowed at a time, so only
    one warning is displayed at a time.  Older warnings
    will be closed early if a new one is requested.

    Properties:
        msg (str): The warning string.
        kind (str): Kind of message ('info', 'success', or 'warning').
        warning_kind (type): A warning type, e.g. ValueError.
        duration (int): Duration of snackbar in seconds.
    """
    global _CURRENT_WARNING  #pylint: disable=global-statement
    if _CURRENT_WARNING:
        _CURRENT_WARNING.value = False
        _CURRENT_WARNING.close()
        _CURRENT_WARNING = None

    if kind == 'info':
        color = INFO_COLOR
        font_color = '#FFFFFF'
        icon = 'info'
    elif kind == 'success':
        color = SUCCESS_COLOR
        font_color = '#FFFFFF'
        icon = 'info'
    elif kind == 'warning':
        color = WARNING_COLOR
        font_color = '#212121'
        icon = 'warning'
    else:
        raise ValueError('Invalid input kind for message.')

    snack_button = vue.Btn(text=True, children=['close'],
                           style_='color:{}'.format(font_color))

    snack_icon = vue.Icon(children=['{}'.format(icon)],
                          style_='color:{}; margin: 5px'.format(font_color))

    if warning_kind:
        warn_type_widget = vue.Html(tag='div',
                                    children=[warning_kind.__name__+ ': '],
                                    style_='font-weight: bold; color:{}; '
                                           'margin: 0px 5px 0px 0px'.format(font_color))

        children = [snack_icon, warn_type_widget, msg, snack_button]
    else:
        children = [snack_icon, msg, snack_button]

    snack = vue.Snackbar(right=True, bottom=True, value=True,
                         timeout=duration*1000, color=color,
                         children=children,
                         style_='color:{}'.format(font_color))

    #pylint: disable=unused-argument
    def on_click(widget, event, data):
        snack.value = False
        snack.close()

    snack_button.on_event('click', on_click)

    _CURRENT_WARNING = snack
    display(snack)
    # We need to close the snack via a thread otherwise if a
    # notebook is closed and then reopened (while still active)
    # the last snackbar will get rerendered upon loading of the
    # notebook javascript.
    thread = threading.Thread(target=_close_snack,
                              args=(snack, duration))
    thread.start()
