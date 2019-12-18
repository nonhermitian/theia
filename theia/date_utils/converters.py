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

import datetime

def utc_to_local(utc_str):
    """Takes a string representing UTC time and
    converts it to the local time.

    Parameters:
        utc_str (str): Input UTC time string.

    Returns:
        str: Input time expressed in local timezone.
    """
    utc_dt = datetime.datetime.strptime(utc_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    utc_dt = utc_dt.replace(tzinfo=datetime.timezone.utc)
    local_tz = datetime.datetime.now().astimezone().tzinfo
    local_tz_name = local_tz.tzname(None)
    local_dt = utc_dt.astimezone(local_tz)
    return local_dt.strftime("%Y-%m-%dT%H:%M:%S {}".format(local_tz_name))
