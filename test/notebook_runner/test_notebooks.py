# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2018.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Jupyter notebook test runner."""

import os
import unittest

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from qiskit.test import QiskitTestCase


# Timeout (in seconds) for a single notebook.
TIMEOUT = 1000
# Jupyter kernel to execute the notebook in.
JUPYTER_KERNEL = 'python3'


class TestJupyter(QiskitTestCase):
    """Notebooks test case."""
    def setUp(self):
        self.execution_path = os.path.join(os.path.dirname( __file__ ), '..')

    def _execute_notebook(self, filename):
        # Create the preprocessor.
        execute_preprocessor = ExecutePreprocessor(timeout=TIMEOUT,
                                                   kernel_name=JUPYTER_KERNEL)

        # Read the notebook.
        with open(filename) as file_:
            notebook = nbformat.read(file_, as_version=4)

        # Run the notebook into the folder containing the `qiskit/` module.
        execute_preprocessor.preprocess(notebook)

    def test_jupyter_jobs_pbars(self):
        """Test Jupyter progress bars and job status functionality"""
        self._execute_notebook(self.execution_path+'/notebooks/test_pbar_status.ipynb')

    def test_backend_tools(self):
        """Test Jupyter backend tools."""
        self._execute_notebook(self.execution_path+'/notebooks/test_pbar_status.ipynb'),
                               
if __name__ == '__main__':
    unittest.main(verbosity=2)
