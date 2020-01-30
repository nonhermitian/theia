###################
Theia documentation
###################

.. toctree::
  :maxdepth: 2
  :hidden:

  API References <apidocs/theia>


.. container:: toggle

    .. container:: header

       **An accordion with a movie**

    .. image:: images/depth_movie.gif

Interactive widgets

.. jupyter-execute::
    :hide-code:

    from qiskit import IBMQ
    from theia.visualization import iplot_error_map

    IBMQ.load_account()

    provider = IBMQ.get_provider(group='open', project='main')
    backend = provider.get_backend('ibmq_vigo')

    iplot_error_map(backend)

.. Hiding - Indices and tables
   :ref:`genindex`
   :ref:`modindex`
   :ref:`search`
