=============
Release Notes
=============

Below are the notes from all libEnsemble releases.

Release 0.7.1
-------------

:Date: Oct 15, 2020

Dependencies:

* ``psutils`` is now a required dependency. (#478 #491)

API additions:

* Executor updates:

 * Addition of a zero-resource worker option for persistent gens (does not allocate nodes to gen). (#500)
 * Multiple applications can be registered to the Executor (and submitted) by name. (#498)
 * Wait function added to Tasks. (#499)

* Gen directories can now be created with options analogous to those for sim dirs. (#349 / #489)

Other changes:

* Improve comms efficiency (Repack fields when NumPy version 1.15+). (#511)
* Fix multiprocessing error on macOS/Python3.8 (Use 'fork' instead of 'spawn'). (#502 / #503)

Updates to example functions:

* Allow APOSMM to trigger ensemble exit when condition reached. (#507)
* Improvement in how persistent APOSMM shuts down subprocesses (preventing PETSc MPI-abort). (#478)

Documentation:

* APOSMM Tutorial added. (#468)
* Writing guide for user functions added to docs (e.g., creating sim_f, gen_f, alloc_f). (#510)
* Addition of posters and presentations section to docs (inc. Jupyter notebooks/binder links). (#492 #497)

:Note:

* Tested platforms include Linux, MacOS, Theta (Cray XC40/Cobalt), Summit (IBM Power9/LSF), Bebop (Cray CS400/Slurm), and Bridges (HPE system at PSC).
* Cori (Cray XC40/Slurm) was not tested with release code due to system issues.
* Tested Python versions: (Cpython) 3.5, 3.6, 3.7, 3.8.

:Known issues:

* We currently recommended running in Central mode on Bridges as distributed runs are experiencing hangs.
* OpenMPI does not work with direct MPI job launches in mpi4py comms mode, since it does not support nested MPI launches
  (Either use local mode or Balsam job controller).
* See known issues section in the documentation for more issues.

Release 0.7.0
-------------

:Date: May 22, 2020

Breaking API changes:

* `Job_controller`/`Job` renamed to `Executor`/`Task` and ``launch`` function to ``submit``. (#285)
* Executors/Resources/Utils moved into sub-packages. ``utils`` now in package ``tools``. (#285)
* sim/gen/alloc support functions moved into ``tools`` sub-package. (#285)
* Restructuring of `sim` directory creation with ``libE_specs`` configuration options.
  E.g: When ``sim_input_dir`` is given, directories for each `sim` are created. (#267)
* User can supply a file called ``node_list`` (replaces ``worker_list``). (#455)

API additions:

* Added gen_funcs.rc configuration framework with option to select APOSMM Optimizers for import. (#444)
* Provide ``alloc_specs`` defaults via `alloc_funcs.defaults` module. (#325)
* Added ``extra_args`` option to the Executor submit function to allow addition of arbitrary MPI runner options. (#445)
* Added ``custom_info`` argument to MPI Executor to allow overriding of detected settings. (#448)
* Added ``libE_specs`` option to disable log files. (#368)

Other changes:

* Added libEnsemble Conda package, hosted on conda-forge.
* Bugfix: Intermittent failures with repeated libE calls under `mpi4py` comms.
  Every libE call now uses its own duplicate of provided communicator and closes out. (#373/#387)
* More accurate timing in `libE_stats.txt`. (#318)
* Addition of new post-processing scripts.

Updates to example functions:

* Persistent APOSMM is now the recommended APOSMM (`aposmm.py` renamed to `old_aposmm.py`). (#435)
* New alloc/gen func: Finite difference parameters with noise estimation.  (#350)
* New example gen func: Tasmanian UQ generator.  (#351)
* New example gen func: Deap/NSGA2 generator.  (#407)
* New example gen func to interface with VTMOP.
* New example sim func: Borehole. (#367)
* New example use-case: WarpX/APOSMM. (#425)

:Note:

* Tested platforms include Linux, MacOS, Theta (Cray XC40/Cobalt), Summit (IBM Power9/LSF), Bebop (Cray CS400/Slurm), Cori (Cray XC40/Slurm), and Bridges (HPE system at PSC).
* Tested Python versions: (Cpython) 3.5, 3.6, 3.7, 3.8.

:Known issues:

* We currently recommended running in Central mode on Bridges as distributed runs are experiencing hangs.
* See known issues section in the documentation for more issues.

Release 0.6.0
-------------

:Date: December 4, 2019

API changes:

* sim/gen/alloc_specs options that do not directly involve these routines are moved to libE_specs (see docs). (#266, #269)
* sim/gen/alloc_specs now require user-defined attributes to be added under the ``'user'`` field (see docs and examples). (#266, #269)
* Addition of a utils module to help users create calling scripts. Includes an argument parser and utility functions. (#308)
* check_inputs() function is moved to the utils module. (#308)
* The libE_specs option ``nprocesses`` has been changed to ``nworkers``. (#235)

New example functions:

* Addition of a persistent APOSMM generator function. (#217)

Other changes:

* Overhaul of documentation, including HPC platform guides and a new pdf structure. (inc. #232, #282)
* Addition of OpenMP threading and GPU support to forces test. (#250)
* Balsam job_controller now tested on Travis. (#47)

:Note:

* Tested platforms include Linux, MacOS, Theta (Cray XC40/Cobalt), Summit (IBM Power9/LSF), Bebop (Cray CS400/Slurm), and Cori (Cray XC40/Slurm).
* Tested Python versions: (Cpython) 3.5, 3.6, 3.7

:Known issues:

* These are unchanged from v0.5.0.
* A known issues section has now been added to the documentation.

Release 0.5.2
-------------

:Date: August 19, 2019

* Code has been restructured to meet xSDK package policies for interoperable ECP software (version 0.5.0). #208
* The use of MPI.COMM_WORLD has been removed. Uses a duplicate of COMM_WORLD if no communicator passed (any process not in communicator returns with an exit code of 3). #108
* All output from libEnsemble goes via logger. MANAGER_WARNING level added. This level and above are echoed to stderr by default. API option to change echo level.
* Simulation directories are created only during sim_f calls are suffixed by _worker. #146
* New user function libE.check_inputs() can be used to check valid configuration of inputs. Can be called in serial or under MPI (see libE API). #65
* Installation option has been added to install dependencies used in tests ``pip install libensemble[extras]``.
* A profiling option has been added to sim_specs. #170
* Results comparison scripts have been included for convenience.

:Note:

* Tested platforms include Linux, MacOS (**New**), Theta (Cray XC40/Cobalt), Summit (IBM Power9/LSF), and Bebop (Cray CS400/Slurm).
* Tested Python versions: (Cpython) 3.5, 3.6, 3.7
* **Note** Support has been removed for Python 3.4 since it is officially retired. Also NumPy has removed support.

:Known issues:

* These are unchanged from v0.5.0.

Release 0.5.1
-------------

:Date: July 11, 2019

* Fixed LSF resource detection for large jobs on LSF systems (e.g., Summit). #184
* Added support for macOS. #182
* Improved the documentation (including addition of beginner's tutorial and FAQ).

:Note:

* Tested platforms include Local Linux, Theta (Cray XC40/Cobalt), Summit (IBM Power9/LSF), and Bebop (Cray CS400/Slurm).
* Tested Python versions: (Cpython) 3.4, 3.5, 3.6, 3.7.

:Known issues:

* These are unchanged from v0.5.0.

Release 0.5.0
-------------

:Date: May 22, 2019

* Added local (multiprocessing) and TCP options for manager/worker communications, in addition to mpi4py. (#42).

 * Example: libEnsemble can be run on MOM/launch nodes (e.g., those of ALCF/Theta & OLCF/Summit) and can remotely detect compute resources.
 * Example: libEnsemble can be run on a system without MPI.
 * Example: libEnsemble can be run with a local manager and remote TCP workers.

* Added support for Summit/LSF scheduler in job controller.
* MPI job controller detects and retries launches on failure; adding resilience. (#143)
* Job controller supports option to extract/print job times in libE_stats.txt. (#136)
* Default logging level changed to INFO. (#164)
* Logging interface added, which allows user to change logging level and file. (#110)
* All worker logging and calculation stats are routed through manager.
* libEnsemble can be run without a gen_func, for example, when using a previously computed random sample. (#122)
* Aborts dump persis_info with the history.

:Note:

* **This version no longer supports Python 2.**
* Tested platforms include Local Linux, Theta (Cray XC40/Cobalt), Summit (IBM Power9/LSF), and Bebop (Cray CS400/Slurm).

:Known issues:

* OpenMPI does not work with direct MPI job launches in mpi4py comms mode, since it does not support nested MPI launches
  (Either use local mode or Balsam job controller).
* Local comms mode (multiprocessing) may fail if MPI is initialized before forking processors. This is thought to be responsible for issues combining with PETSc.
* Remote detection of logical cores via LSB_HOSTS (e.g., Summit) returns number of physical cores since SMT info not available.
* TCP mode does not support (1) more than one libEnsemble call in a given script or (2) the auto-resources option to the job controller.

Release 0.4.1
-------------

:Date: February 20, 2019

* Logging no longer uses root logger (also added option to change libEnsemble log level). (#105)
* Added wait_on_run option for job controller launch to block until jobs have started. (#111)
* persis_info can be passed to sim as well as gen functions. (#112)
* Postprocessing scripts added to create performance/utilization graphs. (#102)
* New scaling test added (not part of current CI test suite). (#114)

Release 0.4.0
-------------

:Date: November 7, 2018

* Separated job controller classes into different modules including a base class (API change).
* Added central_mode run option to distributed type (MPI) job_controllers (API addition). (#93)
* Made poll and kill job methods (API change).
* In job_controller, set_kill_mode is removed and replaced by a wait argument for a hard kill (API change).
* Removed register module - incorporated into job_controller (API change).
* APOSMM has improved asynchronicity when batch mode is false (with new example). (#96)
* Manager errors (instead of hangs) when alloc_f or gen_f don't return work when all workers are idle. (#95)

:Known issues:

* OpenMPI is not supported with direct MPI launches since nested MPI launches are not supported.

Release 0.3.0
-------------

:Date: September 7, 2018

* Issues with killing jobs have been fixed. (#21)
* Fixed job_controller manager_poll to work with multiple jobs. (#62)
* API change: persis_info now included as an argument to libE and is returned from libE instead of gen_info
* Gen funcs: aposmm_logic module renamed to aposmm.
* New example gen and allocation functions.
* Updated Balsam launch script (with new Balsam workflow).
* History is dumped to file on manager or worker exception and MPI aborted (with exit code 1). (#46)
* Default logging level changed to DEBUG and redirected to file ensemble.log.
* Added directory of standalone tests (comms, job kills, and nested MPI launches).
* Improved and speeded up unit tests. (#68)
* Considerable documentation enhancements.

:Known issues:

* OpenMPI is not supported with direct MPI launches since nested MPI launches are not supported.

Release 0.2.0
-------------

:Date: June 29, 2018

* Added job_controller interface (for portable user scripts).
* Added support for using the Balsam job manager. Enables portability and dynamic scheduling.
* Added autodetection of system resources.
* Scalability testing: Ensemble performed with 1023 workers on Theta (Cray XC40) using Balsam.
* Tested MPI libraries: MPICH and Intel MPI.

:Known issues:

* Killing MPI jobs does not work correctly on some systems (including Cray XC40 and CS400). In these cases, libEnsemble continues, but processes remain running.
* OpenMPI does not work correctly with direct launches (and has not been tested with Balsam).

Release 0.1.0
-------------

:Date: November 30, 2017

* Initial release.
