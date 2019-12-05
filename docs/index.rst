###################
Theia documentation
###################

.. jupyter-execute::

   from qiskit import IBMQ
   import qiskit.tools.jupyter

   provider = IBMQ.load_account()
   backend = provider.get_backend('ibmq_vigo')
   backend

.. toctree::
  :maxdepth: 2
  :hidden:

  API References <apidocs/theia>

.. Hiding - Indices and tables
   :ref:`genindex`
   :ref:`modindex`
   :ref:`search`
