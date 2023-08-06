APOSMM
-----------------

Asynchronously Parallel Optimization Solver for finding Multiple Minima
(APOSMM) coordinates concurrent local optimization runs in order to identify
many local minima.

Configuring APOSMM
^^^^^^^^^^^^^^^^^^

By default, APOSMM will import several optimizers which require
external packages and MPI. To import only the optimization packages you are using,
add the following lines in that calling script, before importing APOSMM::

    import libensemble.gen_funcs
    libensemble.gen_funcs.rc.aposmm_optimizers = <optimizers>

Where ``optimizers`` is a string (or list of strings) from the available options:

``'petsc'``, ``'nlopt'``, ``'dfols'``, ``'scipy'``, ``'external'``

To see the optimization algorithms supported, see `LocalOptInterfacer`_.

.. seealso::

    :doc:`Persistent APOSMM Tutorial<../tutorials/aposmm_tutorial>`

Persistent APOSMM
^^^^^^^^^^^^^^^^^

.. automodule:: persistent_aposmm
  :members:
  :undoc-members:

LocalOptInterfacer
^^^^^^^^^^^^^^^^^^
.. automodule:: aposmm_localopt_support
  :members:
  :undoc-members:
