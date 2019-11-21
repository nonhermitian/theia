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

"""Interactive jobs display"""

import datetime
import plotly.graph_objects as go
from ..date_utils.converters import utc_to_local
from .plotly_wrapper import PlotlyFigure


MONTH_NAMES = {1: 'Jan.',
               2: 'Feb.',
               3: 'Mar.',
               4: 'Apr.',
               5: 'May',
               6: 'June',
               7: 'July',
               8: 'Aug.',
               9: 'Sept.',
               10: 'Oct.',
               11: 'Nov.',
               12: 'Dec.'
               }

def job_summary(backend):
    """Interactive jobs summary for a backend.
    Args:
        backend (BaseBackend): A backend instance.

    Returns:
        PlotlyFigureWrapper:
            A figure for the rendered histogram.
    """
    now = datetime.datetime.now()
    past_year_date = now - datetime.timedelta(days=365)
    date_filter = {'creationDate': {'gt': past_year_date.isoformat()}}
    jobs = backend.jobs(limit=None, db_filter=date_filter)

    num_jobs = len(jobs)
    main_str = "<b>Total Jobs</b><br>{}".format(num_jobs)
    jobs_dates = {}

    for job in jobs:
        _date = utc_to_local(job.creation_date())
        _year = _date[:4]
        if _year not in jobs_dates.keys():
            jobs_dates[_year] = {}

        _month = _date[5:7]
        if _month not in jobs_dates[_year].keys():
            jobs_dates[_year][_month] = {}

        _day = _date[8:10]
        if _day not in jobs_dates[_year][_month].keys():
            jobs_dates[_year][_month][_day] = 0

        jobs_dates[_year][_month][_day] += 1

    labels = [main_str]
    parents = [""]
    values = [num_jobs]

    for yr_key, yr_dict in jobs_dates.items():
        # Do the months
        for key, val in yr_dict.items():
            total_jobs_month = sum(val.values())
            # Set the label to the year
            month_label = "{mon} {yr}".format(mon=MONTH_NAMES[int(key)],
                                              yr=yr_key)
            labels.append(month_label)
            # Set the parents to the main str
            parents.append(main_str)
            # Add to the total jobs in that year to values
            values.append(total_jobs_month)

            #Do the days
            for day_num, day_jobs in val.items():
                _day_num = day_num
                if _day_num[0] == '0':
                    _day_num = _day_num[1:]

                if _day_num[-1] == '1':
                    if _day_num[0] != '1':
                        _day_num = _day_num+'st'
                    else:
                        _day_num = _day_num+'th'
                elif _day_num[-1] == '2':
                    if _day_num[0] != '1':
                        _day_num = _day_num+'nd'
                    else:
                        _day_num = _day_num+'th'
                elif _day_num[-1] == '3':
                    if _day_num[0] != '1':
                        _day_num = _day_num+'rd'
                    else:
                        _day_num = _day_num+'th'
                else:
                    _day_num = _day_num+'th'

                labels.append(_day_num)
                parents.append(month_label)
                values.append(day_jobs)

    colors = ['#003f5c', '#ffa600', '#374c80', '#ff764a',
              '#7a5195', '#ef5675', '#bc5090']

    num_colors = len(colors)

    wedge_str = "<b>{label}</b><br><b>{value} Jobs</b>"

    hover_text = [None]+[wedge_str.format(label=labels[kk],
                                          value=values[kk]) for kk in range(1, len(labels))]

    wedge_colors = ["#FFFFFF"]+[colors[kk % num_colors]for kk in range(len(parents)-1)]

    fig = go.Figure(go.Sunburst(labels=labels,
                                parents=parents,
                                values=values,
                                branchvalues="total",
                                textfont=dict(size=18),
                                outsidetextfont=dict(size=24),
                                maxdepth=2,
                                hoverinfo="text",
                                hovertext=hover_text,
                                marker=dict(colors=wedge_colors),
                                )
                    )
    return PlotlyFigure(fig)
