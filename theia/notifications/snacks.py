# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
# pylint: disable=unused-argument

"""A collection of Snack bars"""
import IPython
import ipyvuetify as vue


def job_snackbar(job):
    """Makes a snackbar indicating the job has finished and its status.
    """
    job_id = job.job_id()
    status = job.status()
    if status.name == 'DONE':
        stat = 'successful'
        snack_color = '#34BC6E'
    elif status.name == 'ERROR':
        stat = 'errored'
        snack_color = '#DC267F'
    elif status.name == 'CANCELLED':
        stat = 'cancelled'
        snack_color = '#FFB000'
    else:
        return None

    snack_button = vue.Btn(text=True, children=['close'])

    snack_str = 'Job %s %s' % (job_id, stat)
    snack = vue.Snackbar(right=True, bottom=True, value=True,
                         timeout=5000, color=snack_color,
                         children=[snack_str, snack_button])

    def on_click(widget, event, data):
        snack.value = False

    snack_button.on_event('click', on_click)
    IPython.display.display(snack)
