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

"""An exception notifications module"""
import traceback
import ipyvuetify as vue
from IPython.display import display


def exception_widget(exc):
    """Create an exception notification widget.

    Parameters:
        exc (Exception): Input exception.
    """
    tback = traceback.TracebackException.from_exception(exc).format()
    trace_list = [string for string in tback if 'File' in string]
    tback = trace_list[-1].split('\n')[0]
    exc_type = exc.__class__.__name__
    exc_msg = exc.args[0]

    exc_card = vue.Card(children=[vue.CardTitle(class_='headline body-1 font-weight-medium',
                                                primary_title=True,
                                                children=[vue.Icon(children=['warning'],
                                                                   style_='color:#ffffff;'
                                                                          'margin: 0px 5px'
                                                                  ),
                                                          exc_type],
                                                style_='height:50px;'
                                                       'background-color:#DA1E28;'
                                                       'color:#ffffff'
                                               ),
                                  vue.CardSubtitle(children=[exc_msg],
                                                   class_='text--primary body-1 fontweight-medium',
                                                   style_="margin: 10px 0px; color:#212121"
                                                  ),
                                  vue.CardText(children=[tback],
                                               class_='font-weight-medium',
                                               style_="margin: -15px 0px"
                                              )
                                  ],
                        style_='height: auto; min-height: 140px;')
    display(exc_card)
