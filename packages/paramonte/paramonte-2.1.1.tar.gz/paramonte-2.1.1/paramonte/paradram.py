####################################################################################################################################
####################################################################################################################################
####
####   ParaMonte: plain powerful parallel Monte Carlo library.
####
####   Copyright (C) 2012-present, The Computational Data Science Lab
####
####   This file is part of the ParaMonte library.
####
####   ParaMonte is free software: you can redistribute it and/or modify it
####   under the terms of the GNU Lesser General Public License as published
####   by the Free Software Foundation, version 3 of the License.
####
####   ParaMonte is distributed in the hope that it will be useful,
####   but WITHOUT ANY WARRANTY; without even the implied warranty of
####   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
####   GNU Lesser General Public License for more details.
####
####   You should have received a copy of the GNU Lesser General Public License
####   along with the ParaMonte library. If not, see,
####
####       https://github.com/cdslaborg/paramonte/blob/master/LICENSE
####
####   ACKNOWLEDGMENT
####
####   As per the ParaMonte library license agreement terms,
####   if you use any parts of this library for any purposes,
####   we ask you to acknowledge the use of the ParaMonte library
####   in your work (education/research/industry/development/...)
####   by citing the ParaMonte library as described on this page:
####
####       https://github.com/cdslaborg/paramonte/blob/master/ACKNOWLEDGMENT.md
####
####################################################################################################################################
####################################################################################################################################

import os
import sys
import numpy as np
import typing as tp

fileAbsDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(fileAbsDir)

from _SpecBase import _SpecBase, _genOutputFileName
from _SpecMCMC import _SpecMCMC
from _SpecDRAM import _SpecDRAM
from _pmutils import _FrozenClass
from _ParaDRAMChain import _ParaDRAMChain
import _paramonte as _pm

import ctypes as _ct

####################################################################################################################################
#### ParaDRAM class
####################################################################################################################################

class ParaDRAM:
    """
    |
    This is the **ParaDRAM** class for generating instances of the **serial** and **parallel**
    **Delayed-Rejection Adaptive Metropolis-Hastings Markov Chain Monte Carlo**
    sampler of the ParaMonte library.

        All ParaDRAM class attributes (input arguments to the ParaDRAM constructor)
        are optional and all attributes can be also set after a ParaDRAM instance
        is returned by the constructor.

        Once you set the optional attributes to your desired values,
        call the ParaDRAM sampler via the object's method ``runSampler()``.

        .. _example-serial-usage:

        **Example serial usage**

        Copy and paste the following code enclosed between the
        two comment lines in your python/ipython/jupyter session
        (make sure the indentations of the pasted lines comply with Python rules):

        .. code-block:: python
            :linenos:

            ##################################
            import paramonte as pm
            import numpy as np
            def getLogFunc(point):
                # return the log of the standard multivariate
                # Normal density function with ndim dimensions
                return -0.5 * np.sum( np.double( point )**2 )
            pmpd = pm.ParaDRAM()
            pmpd.runSampler ( ndim = 4                  # number of dimensions of the objective function
                            , getLogFunc = getLogFunc   # the objective function
                            )
            ##################################

        where,

            ndim
                represents the number of dimensions of the domain of
                the user's objective function ``getLogFunc(point)`` and,

            getLogFunc(point)
                represents the user's objective function to be sampled,
                which must take a single input argument ``point`` of type
                numpy-float64 array of length ``ndim`` and must return the
                natural logarithm of the objective function.

        .. _example-parallel-usage:

        **Example parallel usage**

        Copy and paste the following code enclosed between the
        two comment lines in your python/ipython/jupyter session
        (make sure the indentations of the pasted lines comply with Python rules):

        .. code-block:: python
            :linenos:

            ##################################
            with open("main.py", "w") as file:
                file.write  ('''
            import paramonte as pm
            import numpy as np
            def getLogFunc(point):
                # return the log of the standard multivariate
                # Normal density function with ndim dimensions
                return -0.5 * np.sum( np.double( point )**2 )
            pmpd = pm.ParaDRAM()
            pmpd.mpiEnabled = True
            pmpd.runSampler ( ndim = 4                  # number of dimensions of the objective function
                            , getLogFunc = getLogFunc   # the objective function
                            )
            ''')
            ##################################

        where,

            ndim
                represents the number of dimensions of the domain of
                the user's objective function ``getLogFunc(point)`` and,

            getLogFunc(point)
                represents the user's objective function that is to be sampled.
                This function must take a single input argument ``point`` of type
                numpy-float64 array of length ndim and must return the natural
                logarithm of the objective function.

            mpiEnabled
                is a logical (boolean) indicator that, if ``True``, will
                cause the ParaDRAM simulation to run in parallel
                on the requested number of processors.
                The default value is ``False``.

        The above will generate a Parallel-ParaDRAM-simulation Python script in the current working
        directory of Python. Note the only difference between the serial and parallel simulation
        scripts: the extra line ``pmpd.mpiEnabled = True`` which tell the ParaMonte library to run
        the simulation in parallel.

        Assuming that you already have an MPI runtime library installed on your system (see below),
        you can now execute this Python script file ``main.py`` in parallel in two ways:

        1.  from inside ipython or jupyter, type the following,

            .. code-block:: bash

                !mpiexec -n 3 python main.py

        2.  outside of Python environment,
            from within a Bash shell (on Linux or Mac) or,
            from within an Anaconda command prompt on Windows,
            type the following,

            .. code-block:: bash

                mpiexec -n 3 python main.py

        **Note:**

        On Windows platform, if you are using the Intel MPI library,
        we recommend that you also specify the extra flag -localonly,

        .. code-block:: bash

            mpiexec -localonly -n 3 python main.py

        This will cause the simulations to run in parallel only on a single node,
        but more importantly, it will also prevent the use of Hydra service and
        the requirement for its registration. If you are not on a Windows cluster,
        (e.g., you are using your personal device), then we highly recommend
        specifying this flag.


        In all cases in the above, the script ``main.py`` will run on 3 processors.
        Feel free to change the number of processors to any number desired. But do
        not request more than the available number of physical cores on your system.

        **Tips on parallel usage**

        For up-to-date detailed instructions on how to run simulations in parallel visit:

            https://www.cdslab.org/paramonte

        You can also use the following commands on the Python command-line,

        .. code-block:: python
            :linenos:

            ##################################
            import paramonte as pm
            pm.verify() # verify the existence of parallel simulation prerequisites 
            ##################################

        to obtain specific information on how to run a parallel simulation,
        in particular, in relation to your current installation of ParaMonte.
        In general, for parallel simulations:

        0.  Ensure you need and will get a speedup by running the ParaDRAM sampler
            in parallel. Typically, if a single evaluation of the objective function
            takes much longer than a few milliseconds, your simulation may then
            benefit from the parallel run.

        1.  Ensure you have an MPI library installed, preferably, the Intel MPI
            runtime libraries. An MPI library should be automatically installed
            on your system with ParaMonte. If needed, you can download the Intel
            MPI library from their website and install it.

        2.  Ensure the ParaDRAM object property ``mpiEnabled`` is ``True``
            (the default is ``False``).

        3.  Before running the parallel simulation, in particular, on Windows systems,
            you may need to define the necessary MPI environmental variables on your system.
            To get information on how to define the variables, use the paramonte modules's
            function, ``verify()``, as described in the above.

        4.  Call your main Python code from a Python-aware mpiexec-aware command-line via,

            .. code-block:: bash

                mpi_launcher -n num_process python name_of_yor_python_code.py

            where,

            1.  "mpi_launcher" is the name of the MPI launcher
                of the MPI runtime library that you have installed.
                For example, the Intel MPI library's launcher is named mpiexec,
                also recognized by Microsoft, MPICH, and OpenMPI.
                Note that on supercomputers, the MPI launcher is usually
                something other than ``mpiexec``, for example:
                ``ibrun``, ``mpirun``, ...

            2.  "num_process" represents the number of cores
                on which you want to run the program. Replace this
                with the an integer number, like, 3 (meaning 3 cores).

                Do not assign more processes than the available number of
                physical cores on your device/cluster. Assigning more cores
                than physically available on your system will only slow down
                your simulation.

        Once the above script is saved in the file ``main.py``, open a Python-aware and
        MPI-aware command prompt to run the simulation in parallel via the MPI launcher,

        .. code-block:: bash

            mpiexec -n 3 python main.py

        This will execute the Python script main.py on three processes (images).
        Keep in mind that on Windows systems you may need to define MPI environmental
        variables before a parallel simulation, as descibed in the above.

        **ParaDRAM Class Attributes**

        See also:

            https://www.cdslab.org/paramonte/notes/usage/paradram/specifications/

        All input specifications (attributes) of a ParaDRAM simulation are optional.
        However, it is recomended that you provide as much information as possible
        about the specific ParaDRAM simulation and the objective function to be sampled
        via ParaDRAM simulation specifications.

        The ParaDRAM simulation specifications have lengthy comprehensive descriptions
        that appear in full in the output report file of every ParaDRAM simulation.

        The best way to learn about individual ParaDRAM simulation attributes
        is to a run a minimal serial simulation with the following Python script,

        .. code-block:: python
            :linenos:

            ##################################
            from paramonte import ParaDRAM
            pmpd = ParaDRAM()
            pmpd.outputFileName = "./test"
            def getLogFunc(point): return -sum(point**2)
            pmpd.runSampler( ndim = 1, getLogFunc = getLogFunc )
            ##################################

        Running this code will generate a set of simulation output files (in the current
        working directory of Python) that begin with the prefix ``test_process_1``. Among
        these, the file ``test_process_1_report.txt`` contains the full description of all
        input specifications of the ParaDRAM simulation as well as other information
        about the simulation results and statistics.

    ---------------------------------------------------------------------------
    """

    def __init__( self
                # ParaMonte variables
                , sampleSize                            : tp.Optional[int]                                      = None
                , randomSeed                            : tp.Optional[int]                                      = None
                , description                           : tp.Optional[str]                                      = None
                , outputFileName                        : tp.Optional[str]                                      = None
                , outputDelimiter                       : tp.Optional[str]                                      = None
                , chainFileFormat                       : tp.Optional[str]                                      = None
                , variableNameList                      : tp.Optional[tp.List[str]]                             = None
                , restartFileFormat                     : tp.Optional[str]                                      = None
                , outputColumnWidth                     : tp.Optional[int]                                      = None
                , outputRealPrecision                   : tp.Optional[int]                                      = None
                , silentModeRequested                   : tp.Optional[bool]                                     = None
                , domainLowerLimitVec                   : tp.Optional[tp.List[float]]                           = None
                , domainUpperLimitVec                   : tp.Optional[tp.List[float]]                           = None
                , parallelizationModel                  : tp.Optional[str]                                      = None
                , progressReportPeriod                  : tp.Optional[int]                                      = None
                , targetAcceptanceRate                  : tp.Optional[float]                                    = None
                , mpiFinalizeRequested                  : tp.Optional[bool]                                     = None
                , maxNumDomainCheckToWarn               : tp.Optional[int]                                      = None
                , maxNumDomainCheckToStop               : tp.Optional[int]                                      = None
                # ParaMCMC variables
                , chainSize                             : tp.Optional[int]                                      = None
                , scaleFactor                           : tp.Optional[float]                                    = None
                , startPointVec                         : tp.Optional[tp.List[float]]                           = None
                , proposalModel                         : tp.Optional[str]                                      = None
                , proposalStartCovMat                   : tp.Optional[tp.Union[np.mat,tp.List[tp.List[float]]]] = None
                , proposalStartCorMat                   : tp.Optional[tp.Union[np.mat,tp.List[tp.List[float]]]] = None
                , proposalStartStdVec                   : tp.Optional[tp.Union[np.mat,tp.List[float]]]          = None
                , sampleRefinementCount                 : tp.Optional[int]                                      = None
                , sampleRefinementMethod                : tp.Optional[str]                                      = None
                , randomStartPointRequested             : tp.Optional[bool]                                     = None
                , randomStartPointDomainLowerLimitVec   : tp.Optional[tp.List[float]]                           = None
                , randomStartPointDomainUpperLimitVec   : tp.Optional[tp.List[float]]                           = None
                # ParaDRAM variables
                , adaptiveUpdateCount                   : tp.Optional[int]                                      = None
                , adaptiveUpdatePeriod                  : tp.Optional[int]                                      = None
                , greedyAdaptationCount                 : tp.Optional[int]                                      = None
                , delayedRejectionCount                 : tp.Optional[int]                                      = None
                , burninAdaptationMeasure               : tp.Optional[float]                                    = None
                , delayedRejectionScaleFactorVec        : tp.Optional[tp.Union[np.mat,tp.List[float]]]          = None
                ):
        """
        The constructor for ParaDRAM class.
        All input parameters are optional and all class attributes
        can be changed after the object construction.

            **Parameters**

                The list of input parameters to
                the constructor is extensive. See the
                help information for ParaDRAM class: help(ParaDRAM)

        """

        # ParaMonte specifications

        self.spec = _FrozenClass()

        # ParaMonte variables
        self.spec.sampleSize                           = sampleSize
        self.spec.randomSeed                           = randomSeed
        self.spec.description                          = description
        self.spec.outputFileName                       = outputFileName
        self.spec.outputDelimiter                      = outputDelimiter
        self.spec.chainFileFormat                      = chainFileFormat
        self.spec.variableNameList                     = variableNameList
        self.spec.restartFileFormat                    = restartFileFormat
        self.spec.outputColumnWidth                    = outputColumnWidth
        self.spec.outputRealPrecision                  = outputRealPrecision
        self.spec.silentModeRequested                  = silentModeRequested
        self.spec.domainLowerLimitVec                  = domainLowerLimitVec
        self.spec.domainUpperLimitVec                  = domainUpperLimitVec
        self.spec.parallelizationModel                 = parallelizationModel
        self.spec.progressReportPeriod                 = progressReportPeriod
        self.spec.targetAcceptanceRate                 = targetAcceptanceRate
        self.spec.mpiFinalizeRequested                 = mpiFinalizeRequested
        self.spec.maxNumDomainCheckToWarn              = maxNumDomainCheckToWarn
        self.spec.maxNumDomainCheckToStop              = maxNumDomainCheckToStop
        # ParaMCMC variables
        self.spec.chainSize                            = chainSize
        self.spec.scaleFactor                          = scaleFactor
        self.spec.startPointVec                        = startPointVec
        self.spec.proposalModel                        = proposalModel
        self.spec.proposalStartCovMat                  = proposalStartCovMat
        self.spec.proposalStartCorMat                  = proposalStartCorMat
        self.spec.proposalStartStdVec                  = proposalStartStdVec
        self.spec.sampleRefinementCount                = sampleRefinementCount
        self.spec.sampleRefinementMethod               = sampleRefinementMethod
        self.spec.randomStartPointRequested            = randomStartPointRequested
        self.spec.randomStartPointDomainLowerLimitVec  = randomStartPointDomainLowerLimitVec
        self.spec.randomStartPointDomainUpperLimitVec  = randomStartPointDomainUpperLimitVec
        # ParaDRAM variables
        self.spec.adaptiveUpdateCount                  = adaptiveUpdateCount
        self.spec.adaptiveUpdatePeriod                 = adaptiveUpdatePeriod
        self.spec.greedyAdaptationCount                = greedyAdaptationCount
        self.spec.delayedRejectionCount                = delayedRejectionCount
        self.spec.burninAdaptationMeasure              = burninAdaptationMeasure
        self.spec.delayedRejectionScaleFactorVec       = delayedRejectionScaleFactorVec

        self.spec._freeze()

        self.mpiEnabled = False
        self._mpiDisabled = not self.mpiEnabled

    ################################################################################################################################

    def _getInputFile(self,inputFile): #,mpiEnabled):

        if inputFile is None:

            ############################################################################################################################
            #### begin namelist generation from arguments
            ############################################################################################################################

            SpecBase = _SpecBase()
            SpecMCMC = _SpecMCMC()
            SpecDRAM = _SpecDRAM()
            nameListParaDRAM = ""

            # setup outputFileName if it is None

            from _SpecBase import _genOutputFileName
            if self.spec.outputFileName is None:
                self.spec.outputFileName = os.path.join( os.getcwd() , _genOutputFileName(_pm.names.paradram) )
            else:
                #if not os.path.isabs(self.spec.outputFileName):
                    #headTailList = os.path.split(self.spec.outputFileName)
                    #if headTailList[1]=="":
                    #self.spec.outputFileName = SpecBase.outputFileName(self.spec.outputFileName)
                    if self.spec.outputFileName[-1] == "\\" or self.spec.outputFileName[-1] == "/":
                        self.spec.outputFileName = os.path.join( os.path.abspath( self.spec.outputFileName ) , _genOutputFileName(_pm.names.paradram) )

            # ParaMonte variables

            if   self.spec.sampleSize                            is not None: nameListParaDRAM += SpecBase.sampleSize                            (self.spec.sampleSize                         )
            if   self.spec.randomSeed                            is not None: nameListParaDRAM += SpecBase.randomSeed                            (self.spec.randomSeed                         )
            if   self.spec.description                           is not None: nameListParaDRAM += SpecBase.description                           (self.spec.description                        )
            if   self.spec.outputFileName                        is not None: nameListParaDRAM += SpecBase.outputFileName                        (self.spec.outputFileName                     )
            if   self.spec.outputDelimiter                       is not None: nameListParaDRAM += SpecBase.outputDelimiter                       (self.spec.outputDelimiter                    )
            if   self.spec.chainFileFormat                       is not None: nameListParaDRAM += SpecBase.chainFileFormat                       (self.spec.chainFileFormat                    )
            if   self.spec.variableNameList                      is not None: nameListParaDRAM += SpecBase.variableNameList                      (self.spec.variableNameList                   )
            if   self.spec.restartFileFormat                     is not None: nameListParaDRAM += SpecBase.restartFileFormat                     (self.spec.restartFileFormat                  )
            if   self.spec.outputColumnWidth                     is not None: nameListParaDRAM += SpecBase.outputColumnWidth                     (self.spec.outputColumnWidth                  )
            if   self.spec.outputRealPrecision                   is not None: nameListParaDRAM += SpecBase.outputRealPrecision                   (self.spec.outputRealPrecision                )
            if   self.spec.silentModeRequested                   is not None: nameListParaDRAM += SpecBase.silentModeRequested                   (self.spec.silentModeRequested                )
            if   self.spec.domainLowerLimitVec                   is not None: nameListParaDRAM += SpecBase.domainLowerLimitVec                   (self.spec.domainLowerLimitVec                )
            if   self.spec.domainUpperLimitVec                   is not None: nameListParaDRAM += SpecBase.domainUpperLimitVec                   (self.spec.domainUpperLimitVec                )
            if   self.spec.parallelizationModel                  is not None: nameListParaDRAM += SpecBase.parallelizationModel                  (self.spec.parallelizationModel               )
            if   self.spec.progressReportPeriod                  is not None: nameListParaDRAM += SpecBase.progressReportPeriod                  (self.spec.progressReportPeriod               )
            if   self.spec.targetAcceptanceRate                  is not None: nameListParaDRAM += SpecBase.targetAcceptanceRate                  (self.spec.targetAcceptanceRate               )
            if   self.spec.mpiFinalizeRequested                  is not None: nameListParaDRAM += SpecBase.mpiFinalizeRequested                  (self.spec.mpiFinalizeRequested               )
            if   self.spec.maxNumDomainCheckToWarn               is not None: nameListParaDRAM += SpecBase.maxNumDomainCheckToWarn               (self.spec.maxNumDomainCheckToWarn            )
            if   self.spec.maxNumDomainCheckToStop               is not None: nameListParaDRAM += SpecBase.maxNumDomainCheckToStop               (self.spec.maxNumDomainCheckToStop            )
            # ParaMCMC variables
            if   self.spec.chainSize                             is not None: nameListParaDRAM += SpecMCMC.chainSize                             (self.spec.chainSize                          )
            if   self.spec.scaleFactor                           is not None: nameListParaDRAM += SpecMCMC.scaleFactor                           (self.spec.scaleFactor                        )
            if   self.spec.startPointVec                         is not None: nameListParaDRAM += SpecMCMC.startPointVec                         (self.spec.startPointVec                      )
            if   self.spec.proposalModel                         is not None: nameListParaDRAM += SpecMCMC.proposalModel                         (self.spec.proposalModel                      )
            if   self.spec.proposalStartCovMat                   is not None: nameListParaDRAM += SpecMCMC.proposalStartCovMat                   (self.spec.proposalStartCovMat                )
            if   self.spec.proposalStartCorMat                   is not None: nameListParaDRAM += SpecMCMC.proposalStartCorMat                   (self.spec.proposalStartCorMat                )
            if   self.spec.proposalStartStdVec                   is not None: nameListParaDRAM += SpecMCMC.proposalStartStdVec                   (self.spec.proposalStartStdVec                )
            if   self.spec.sampleRefinementCount                 is not None: nameListParaDRAM += SpecMCMC.sampleRefinementCount                 (self.spec.sampleRefinementCount              )
            if   self.spec.sampleRefinementMethod                is not None: nameListParaDRAM += SpecMCMC.sampleRefinementMethod                (self.spec.sampleRefinementMethod             )
            if   self.spec.randomStartPointRequested             is not None: nameListParaDRAM += SpecMCMC.randomStartPointRequested             (self.spec.randomStartPointRequested          )
            if   self.spec.randomStartPointDomainLowerLimitVec   is not None: nameListParaDRAM += SpecMCMC.randomStartPointDomainLowerLimitVec   (self.spec.randomStartPointDomainLowerLimitVec)
            if   self.spec.randomStartPointDomainUpperLimitVec   is not None: nameListParaDRAM += SpecMCMC.randomStartPointDomainUpperLimitVec   (self.spec.randomStartPointDomainUpperLimitVec)
            # ParaDRAM variables
            if   self.spec.adaptiveUpdateCount                   is not None: nameListParaDRAM += SpecDRAM.adaptiveUpdateCount                   (self.spec.adaptiveUpdateCount                )
            if   self.spec.adaptiveUpdatePeriod                  is not None: nameListParaDRAM += SpecDRAM.adaptiveUpdatePeriod                  (self.spec.adaptiveUpdatePeriod               )
            if   self.spec.greedyAdaptationCount                 is not None: nameListParaDRAM += SpecDRAM.greedyAdaptationCount                 (self.spec.greedyAdaptationCount              )
            if   self.spec.delayedRejectionCount                 is not None: nameListParaDRAM += SpecDRAM.delayedRejectionCount                 (self.spec.delayedRejectionCount              )
            if   self.spec.burninAdaptationMeasure               is not None: nameListParaDRAM += SpecDRAM.burninAdaptationMeasure               (self.spec.burninAdaptationMeasure            )
            if   self.spec.delayedRejectionScaleFactorVec        is not None: nameListParaDRAM += SpecDRAM.delayedRejectionScaleFactorVec        (self.spec.delayedRejectionScaleFactorVec     )

            nameListParaDRAM = "&ParaDRAM " + nameListParaDRAM + SpecBase.interfaceType() + "/"

            ############################################################################################################################
            #### end namelist generation from arguments
            ############################################################################################################################

            inputFileVec_pntr = nameListParaDRAM.encode("utf-8")                # create byte-object from the internal input file

        else:

            if not self.mpiEnabled:
                _pm.warn( msg = "Input namelist file is given by the user. \n"
                                + "All simulation specifications will be read from the input file."
                        , methodName = _pm.names.paradram
                        , marginTop = 1
                        , marginBot = 1
                        )

            inputFileVec_pntr = inputFile.encode("utf-8")                       # create byte-object from the external input file

        inputFileLen = len(inputFileVec_pntr) # byte-object length
       #inputFileLen_pntr = _ct.byref( _ct.c_size_t( len(inputFileVec_pntr) ) ) # pointer to byte-object length
        inputFileVec_pntr = _ct.c_char_p( inputFileVec_pntr )                   # pointer to byte-object

        return inputFileVec_pntr, inputFileLen #_pntr

    ################################################################################################################################

    def runSampler  ( self
                    , ndim          : int
                    , getLogFunc    : tp.Callable[[tp.List[float]], float]
                    , buildMode     : tp.Optional[str]     = "release"
                    , mpiEnabled    : tp.Optional[bool]    = None
                    , inputFile     : tp.Optional[str]     = None
                    ) -> None:
        """

        Run ParaDRAM sampler and return nothing.

            **Parameters**

                ndim
                    integer representing the number of dimensions of the
                    domain of the user's objective function ``getLogFunc(point)``.
                    It must be a positive integer.

                getLogFunc(point)
                    represents the user's objective function to be sampled,
                    which must take a single input argument ``point`` of type
                    numpy-float64 array of length ``ndim`` and must return the
                    natural logarithm of the objective function.

                buildMode
                    optional string argument with default value "release".
                    possible choices are:

                        "debug"
                            to be used for identifying sources of bug
                            and causes of code crash.

                        "release"
                            to be used in all other normal scenarios
                            for maximum runtime efficiency.

                mpiEnabled
                    optional logical (boolean) indicator which is None by default.
                    If it is set to True, it will cause the ParaDRAM simulation
                    to run in parallel on the requested number of processors.
                    If it is not provided, its value will taken from the
                    ``mpiEnabled`` property of the sampler object.
                    See ParaDRAM class information on how
                    to run a simulation in parallel.

                inputFile
                    optional string input representing the path to
                    an external input namelist of simulation specifications.

                        **Warning**

                        **Use this optional argument with caution and only if
                        you know what you are doing. Specifying this option
                        will cause paradram to ignore all other paradram
                        simulation specifications set by the user via
                        paradram instance attributes.**

            **Returns**

                None

        """

        if not isinstance(ndim,int) or ndim<1:
            _pm.abort   ( msg   = "The input argument ndim must be a positive integer,\n"
                                + "representing the number of dimensions of the domain of\n"
                                + "the user's objective function getLogFunc().\n"
                                + "You have entered ndim = " + str(ndim)
                        , methodName = _pm.names.paradram
                        , marginTop = 1
                        , marginBot = 1
                        )

        if not callable(getLogFunc):
            _pm.abort   ( msg   = "The input argument getLogFunc must be a callable function.\n"
                                + "It represents the user's objective function to be sampled,\n"
                                + "which must take a single input argument of type numpy\n"
                                + "float64 array of length ndim and must return the\n"
                                + "natural logarithm of the objective function."
                        , methodName = _pm.names.paradram
                        , marginTop = 1
                        , marginBot = 1
                        )

        errorOccurred = not isinstance(buildMode,str)
        if not errorOccurred: errorOccurred = buildMode.split("-")[0] not in ["release","testing","debug"]
        if errorOccurred:
            _pm.abort   ( msg   = "The input argument buildMode must be of type str.\n"
                                + "It is an optional string argument with default value \"release\"\n."
                                + "possible choices are:\n"
                                + "    \"debug\":\n"
                                + "        to be used for identifying sources of bug\n"
                                + "        and causes of code crash.\n"
                                + "    \"release\":\n"
                                + "        to be used in all other normal scenarios\n"
                                + "        for maximum runtime efficiency.\n"
                                + "You have entered buildMode = " + str(buildMode)
                        , methodName = _pm.names.paradram
                        , marginTop = 1
                        , marginBot = 1
                        )

        if mpiEnabled is not None:
            if isinstance(mpiEnabled,bool):
                self.mpiEnabled = mpiEnabled
            else:
                _pm.abort   ( msg   = "The input argument `mpiEnabled` must be of type bool.\n"
                                    + "It is an optional logical (boolean) indicator which is False by default.\n"
                                    + "If it is set to True, it will cause the ParaDRAM simulation\n"
                                    + "to run in parallel on the requested number of processors.\n"
                                    + "See ParaDRAM class information on how to run a simulation in parallel.\n"
                                    + "You have entered mpiEnabled = " + str(mpiEnabled)
                            , methodName = _pm.names.paradram
                            , marginTop = 1
                            , marginBot = 1
                            )
        self._mpiDisabled = not self.mpiEnabled

        if inputFile is not None and not isinstance(inputFile,str):
            _pm.abort   ( msg   = "The input argument `inputFile` must be of type str.\n"
                                + "It is an optional string input representing the path to\n"
                                + "an external input namelist of simulation specifications.\n"
                                + "USE THIS OPTIONAL ARGUMENT WITH CAUTION AND\n"
                                + "ONLY IF YOU KNOW WHAT YOU ARE DOING.\n"
                                + "Specifying this option will cause ParaDRAM to ignore\n"
                                + "all other paraDRAM simulation specifications set by\n"
                                + "the user via ParaDRAM instance attributes.\n"
                                + "You have entered inputFile = " + str(inputFile)
                        , methodName = _pm.names.paradram
                        , marginTop = 1
                        , marginBot = 1
                        )

        def getLogFunc2arg(ndim,point):
            PointVec = np.array(point[0:ndim])
            return getLogFunc(PointVec)

        self._runSampler( ndim
                        , getLogFunc2arg
                        , buildMode
                        , mpiEnabled
                        , inputFile
                        )

    ################################################################################################################################

    def _runSampler ( self
                    , ndim          : int
                    , getLogFuncRaw : tp.Callable[[int,tp.List[float]], float]
                    , buildMode     : tp.Optional[str]     = "release"
                    , mpiEnabled    : tp.Optional[bool]    = False
                    , inputFile     : tp.Optional[str]     = None
                    ) -> None:
        """

        Run ParaDRAM sampler and return nothing. This method is identical to
        the ``runSampler()`` method, except that the input ``point`` parameter to
        the user-provided input objective function ``getLogFuncRaw(ndim,point)`` is
        a C-style raw pointer. This requires the user to guarantee that ``point`` will 
        be always used with array bounds in their implementation of the objective function. 
        The use of ``_runSampler()`` in place of ``runSampler()`` leads to a slight 
        performance gain in the simulations.

            **Example serial usage**

            Copy and paste the following code enclosed between the
            two comment lines in your python/ipython/jupyter session
            (make sure the indentations of the pasted lines comply with Python rules):

            .. code-block:: python
                :linenos:

                ##################################
                import paramonte as pm
                import numpy as np
                def getLogFuncRaw(ndim,point):
                    # return the log of the standard multivariate
                    # Normal density function with ndim dimensions
                    return -0.5 * np.sum( np.double( point[0:ndim] )**2 )
                pmpd = pm.ParaDRAM()
                pmpd._runSampler( ndim = 4                      # length of point
                                , getLogFuncRaw = getLogFuncRaw # the objective function
                                )
                ##################################

            where,

                ndim
                    represents the number of dimensions of the domain of
                    the user's objective function ``getLogFuncRaw(ndim, point)`` and,

                getLogFuncRaw(ndim, point)
                    represents the user's objective function to be sampled,
                    where,

                        ndim
                            is a 32-bit integer, representing the number of
                            dimensions of the domain of the user-provided
                            objective function.
                        point
                            is a C-style array-pointer of length ``ndim``
                            and type float64. Note that the bounds of
                            ``point`` must be always specified wherever
                            it is used within the objective function.

                    On output, it must return the natural logarithm of
                    the objective function.

            **Parameters**

                All input parameters have the same meaning as the parameters
                of ``runSampler()``. The only difference is in the input
                parameters to the objective function ``getLogFuncRaw``.

            **Returns**

                None

        """

        errorOccurred = not isinstance(ndim,int)
        if not errorOccurred: errorOccurred = ndim < 1
        if errorOccurred:
            _pm.abort   ( msg   = "The input argument ndim must be a positive integer,\n"
                                + "representing the number of dimensions of the domain of\n"
                                + "the user's objective function getLogFuncRaw().\n"
                                + "You have entered ndim = " + str(ndim)
                        , methodName = _pm.names.paradram
                        , marginTop = 1
                        , marginBot = 1
                        )

        if not callable(getLogFuncRaw):
            _pm.abort   ( msg   = "The input argument getLogFuncRaw must be a callable function.\n"
                                + "It represents the user's objective function to be sampled,\n"
                                + "which must take an input integer ndim representing the number of\n"
                                + "dimensions of the domain of the objective function to be samples and,\n"
                                + "a second input argument of type numpy float64 array of length ndim.\n"
                                + "On return it must return the natural logarithm of the objective function."
                        , methodName = _pm.names.paradram
                        , marginTop = 1
                        , marginBot = 1
                        )

        stype = None
        dummyList = None
        errorOccurred = True
        if isinstance(buildMode,str):
            errorOccurred = False
            if "-" in buildMode:
                dummyList = buildMode.split("-")
                buildMode = dummyList[0] # build type
                stype = dummyList[1] # compiler suite

        if not errorOccurred: errorOccurred = buildMode not in ["release","testing","debug"]
        if not errorOccurred and stype is not None: errorOccurred = not (stype=="gnu" or stype=="intel")
        if errorOccurred:
            if dummyList is not None: buildMode = "-".join(dummyList)
            _pm.abort   ( msg   = "The input argument buildMode must be of type str.\n"
                                + "It is an optional string argument with default value \"release\"\n."
                                + "possible choices are:\n"
                                + "    \"debug\":\n"
                                + "        to be used for identifying sources of bug\n"
                                + "        and causes of code crash.\n"
                                + "    \"release\":\n"
                                + "        to be used in all other normal scenarios\n"
                                + "        for maximum runtime efficiency.\n"
                                + "You have entered buildMode = " + str(buildMode)
                        , methodName = _pm.names.paradram
                        , marginTop = 1
                        , marginBot = 1
                        )

        if mpiEnabled is not None:
            if isinstance(mpiEnabled,bool):
                self.mpiEnabled = mpiEnabled
            else:
                _pm.abort   ( msg   = "The input argument mpiEnabled must be of type bool.\n"
                                    + "It is an optional logical (boolean) indicator which is False by default.\n"
                                    + "If it is set to True, it will cause the ParaDRAM simulation\n"
                                    + "to run in parallel on the requested number of processors.\n"
                                    + "See ParaDRAM class information on how to run a simulation in parallel.\n"
                                    + "You have entered mpiEnabled = " + str(mpiEnabled)
                            , methodName = _pm.names.paradram
                            , marginTop = 1
                            , marginBot = 1
                            )
        self._mpiDisabled = not self.mpiEnabled

        if inputFile is not None and not isinstance(inputFile,str):
            _pm.abort   ( msg   = "The input argument `inputFile` must be of type str.\n"
                                + "It is an optional string input representing the path to\n"
                                + "an external input namelist of simulation specifications.\n"
                                + "USE THIS OPTIONAL ARGUMENT WITH CAUTION AND\n"
                                + "ONLY IF YOU KNOW WHAT YOU ARE DOING.\n"
                                + "Specifying this option will cause ParaDRAM to ignore\n"
                                + "all other paraDRAM simulation specifications set by\n"
                                + "the user via ParaDRAM instance attributes.\n"
                                + "You have entered inputFile = " + str(inputFile)
                        , methodName = _pm.names.paradram
                        , marginTop = 1
                        , marginBot = 1
                        )

        inputFileVec_pntr, inputFileLen = self._getInputFile(inputFile) #,mpiEnabled)

        #platform = sys.platform.lower()
        #isWin32 = True if platform=="win32" else False
        #isLinux = True if platform=="linux" else False
        #isMacOS = True if platform=="darwin" else False

        if self.mpiEnabled:
            parallelism = "_mpi"
        else:
            parallelism = ""
            _pm.note( msg   = "Running the ParaDRAM sampler in serial mode...\n"
                            + "To run the ParaDRAM sampler in parallel mode visit: cdslab.org/pm\n"
                            + "If you are using Jupyter notebook, check the Jupyter's terminal window\n"
                            + "for realtime simulation progress and report."
                    , methodName = _pm.names.paradram
                    , marginTop = 1
                    , marginBot = 1
                    )

        #if len(sys.argv)>1:
        #    if sys.argv[1]=="p":
        #        _pm.note( msg = Running sampler in parallel mode...
        #                , methodName = _pm.names.paradram
        #                )
        #        print("\nRunning sampler in parallel mode...\n")
        #        libName += "_mpi"
        #else:
        #    print("\nRunning ParaMonte sampler in serial mode...\n")
        #try:
        #    from mpi4py import MPI
        #    comm = MPI.COMM_WORLD
        #    libName += "_mpi"
        #    if comm.size==1:
        #        print("\nRunning ParaMonte sampler in serial mode...\n")
        #        if MPI.Is_initialized():
        #            print("Hello")
        #            MPI.Finalize()
        #    elif comm.rank==0:
        #        print("\nRunning ParaMonte sampler in parallel mode on {} processes...\n".format(comm.size))
        #        comm.barrier()
        #except ImportError:
        #    print("\nImportError occurred...\n")
        #    print("\nRunning ParaMonte sampler in serial mode...\n")

        sys.stdout.flush()

        # setup env

        if _pm.platform.isWin32:

            if "PATH" in os.environ:
                os.environ["PATH"] = fileAbsDir + os.pathsep + os.environ["PATH"]
            else:
                os.environ["PATH"] = fileAbsDir

            mpiFound = False
            pathList = os.environ["PATH"].split(";")
            for path in pathList:
                pathLower = path.lower().replace("\\","")
                if ("mpiintel64bin" in pathLower):
                    #mpiFound = True
                    #bldMode = buildMode
                    #if bldMode=="testing": bldMode = "release"
                    mpiPath = os.path.join(path,"release")
                    os.environ["PATH"] = mpiPath + os.pathsep + os.environ["PATH"]
                    libfabricPath = os.path.join(os.path.dirname(path),"libfabric","bin")
                    os.environ["PATH"] = libfabricPath + os.pathsep + os.environ["PATH"]
                    break

        else:

            if "LD_LIBRARY_PATH" not in os.environ:
                os.environ["LD_LIBRARY_PATH"] = "."
                if self._mpiDisabled:
                    _pm.warn( msg   = "LD_LIBRARY_PATH environmental variable is not defined in your Python session.\n"
                                    + "Consider running the following command in your Bash shell before running Python.\n"
                                    + "and using ParaMonte library:\n\n"
                                    + "    export LD_LIBRARY_PATH=."
                            , methodName = _pm.names.paradram
                            , marginTop = 1
                            , marginBot = 1
                            )
            libdir = "/usr/lib"
            if os.path.isdir(libdir):
                os.environ["LD_LIBRARY_PATH"]  = libdir + os.pathsep + os.environ["LD_LIBRARY_PATH"]
            libdir = "/usr/local/lib"
            if os.path.isdir(libdir):
                os.environ["LD_LIBRARY_PATH"]  = libdir + os.pathsep + os.environ["LD_LIBRARY_PATH"]
            libdir = "/usr/lib64"
            if os.path.isdir(libdir):
                os.environ["LD_LIBRARY_PATH"]  = libdir + os.pathsep + os.environ["LD_LIBRARY_PATH"]
            libdir = "/usr/local/lib64"
            if os.path.isdir(libdir):
                os.environ["LD_LIBRARY_PATH"]  = libdir + os.pathsep + os.environ["LD_LIBRARY_PATH"]
            os.environ["LD_LIBRARY_PATH"]  = fileAbsDir + os.pathsep + os.environ["LD_LIBRARY_PATH"]

            from _pmreqs import getLocalInstallDir
            localInstallDir = getLocalInstallDir()

            if localInstallDir.gnu.root is not None:
                for object in os.scandir(localInstallDir.gnu.root):
                    if object.is_dir() and ("lib" in object.name):
                        os.environ["LD_LIBRARY_PATH"] = object.path + os.pathsep + os.environ["LD_LIBRARY_PATH"]

            if localInstallDir.mpi.root is not None:
                if localInstallDir.mpi.bin is not None: os.environ["PATH"] = localInstallDir.mpi.bin + os.pathsep + os.environ["PATH"]
                for object in os.scandir(localInstallDir.mpi.root):
                    if object.is_dir() and ("lib" in object.name):
                        os.environ["LD_LIBRARY_PATH"] = object.path + os.pathsep + os.environ["LD_LIBRARY_PATH"]
                if localInstallDir.mpi.lib is not None: os.environ["LD_LIBRARY_PATH"] = localInstallDir.mpi.lib + os.pathsep + os.environ["LD_LIBRARY_PATH"]

        # import ParaMonte dll define result (None) AND argument (pointer to a c function) type

        from ctypes.util import find_library

        #fileAbsDir = os.path.dirname(os.path.abspath(__file__))

        buildModeList = ["release","testing","debug"]
        buildModeList.pop(buildModeList.index(buildMode))
        buildModeList.insert(0,buildMode)
        pmcsList = ["intel","gnu"]
        if stype is not None:
            pmcsList.pop(pmcsList.index(stype))
            pmcsList.insert(0,stype)

        libNameSuffix = parallelism +   { "windows" : ".dll"
                                        , "cygwin"  : ".dll"
                                        , "darwin"  : ".dylib"
                                        , "linux"   : ".so"
                                        }.get(_pm.platform.osname, ".so")

        libPath = None
        libFound = False
        libNamePrefix = "libparamonte_python_" + _pm.platform.osname.lower() + "_" + _pm.platform.arch + "_";
        for buildMode in buildModeList:

            for pmcs in pmcsList:

                libName = libNamePrefix + pmcs + "_" + buildMode + "_dynamic_heap" + libNameSuffix;
                libPath = find_library(libName)
                if libPath==None: libPath = os.path.join( fileAbsDir, libName )

                libFound = os.path.isfile(libPath)
                if libFound: break

            if libFound: # check if lib file exists
                break
            #else:
            #    if self._mpiDisabled:
            #        _pm.warn( msg   = "ParaMonte dynamic library for the requested build mode " + buildMode + " not found.\n"
            #                        + "Searching for ParaMonte dynamic library in other build modes..."
            #                , methodName = _pm.names.paradram
            #                , marginTop = 1
            #                , marginBot = 1
            #                )
            #    #libName = libName.replace(buildMode,mode)
            #    #buildMode = mode

        if not libFound:
            from _pmreqs import buildInstructionNote
            _pm.abort( msg  = "Exhausted all possible ParaMonte dynamic library search \n"
                            + "names but could not find any compatible library. \n"
                            #+ "Last search:\n\n"
                            #+ "    " + libPath + "\n\n"
                            + "It appears your ParaMonte Python interface is missing \n"
                            + "the dynamic libraries. Please report this issue at: \n\n"
                            + "    https://github.com/cdslaborg/paramonte/issues\n\n"
                            + "Visit https://www.cdslab.org/pm for instructions \n"
                            + "to build ParaMonte object files on your system."
                            + buildInstructionNote
                    , methodName = _pm.names.paradram
                    , marginTop = 1
                    , marginBot = 1
                    )

        # define ctypes wrapper function, with the proper result and argument types
        _getLogFuncRaw_proc = _ct.CFUNCTYPE ( _ct.c_double                  # function result
                                           #, _ct.POINTER(_ct.c_int32)      # ndim
                                            , _ct.c_int32                   # ndim
                                            , _ct.POINTER(_ct.c_double)     # point
                                            )
        getLogFuncRaw_pntr = _getLogFuncRaw_proc(getLogFuncRaw)

        try:

            pmdll = _ct.CDLL(libPath)

        except Exception as e:

            import logging
            logger = logging.Logger("catch_all")
            logger.error(e, exc_info=True)

            from _pmreqs import buildInstructionNote
            _pm.abort( msg  = "Failed to load the required ParaMonte shared library (DLL).\n"
                            + "This is either due to the incompatibility of the DLL with your\n"
                            + "platform or due to missing some required dependent libraries.\n"
                            + "In either case, you can likely resolve this error by building.\n"
                            + "the required ParaMonte shared libraries on your system.\n\n"
                            + "Visit https://www.cdslab.org/pm for instructions \n"
                            + "to build ParaMonte library on your system.\n\n"
                            + "Please report this issue at: \n\n"
                            + "    https://github.com/cdslaborg/paramonte/issues\n\n"
                            + buildInstructionNote
                    , methodName = _pm.names.paradram
                    , marginTop = 1
                    , marginBot = 1
                    )

        pmdll.runParaDRAM.restype = _ct.c_int32
        #pmdll.runParaDRAM.restype = None
        #pmdll.runParaDRAM.argtypes =    [ _ct.POINTER(_ct.c_int32)     # ndim
        pmdll.runParaDRAM.argtypes =    [ _ct.c_int32                   # ndim
                                        , _getLogFuncRaw_proc           # procedure
                                        , _ct.POINTER(_ct.c_char)       # inputFile byte object
                                        , _ct.c_int32                   # lenInpuFile
                                       #, _ct.POINTER(_ct.c_size_t)     # lenInpuFile
                                        , ]

        #def getLogFuncRawWrapper(ndim_pntr,point): return getLogFuncRaw(ndim[0],point)

        # construct procedure pointer
        #def getLogFuncRawWrapper(ndim,point): return getLogFuncRaw(np.array(point[0:ndim]))
        #getLogFuncRaw_pntr = _getLogFuncRaw_proc(getLogFuncRawWrapper)

        # construct ndim pointer
        #ndim_pntr = _ct.byref(_ct.c_int32(ndim))

        # call ParaMonte
        #pmdll.runParaDRAM   ( ndim_pntr
        #pmdll.runParaDRAM   ( _ct.c_int32(ndim)
        errFlag = pmdll.runParaDRAM ( _ct.c_int32(ndim)
                                    , getLogFuncRaw_pntr
                                    , inputFileVec_pntr
                                    , _ct.c_int32(inputFileLen)
                                   #, inputFileLen_pntr
                                    )
        if errFlag!=0:
            msg = "."
            if isinstance(self.spec.outputFileName, str): 
                msg = ":\n\n" + "    " + self.spec.outputFileName + "_report.txt"
            _pm.abort   ( msg   = "The simulation failed. For more information, checkout the \n"
                                + "contents of the output report file (if any has been generated)"
                                + msg
                        , methodName = _pm.names.paradram
                        , marginTop = 1
                        , marginBot = 1
                        )
       #def isLoaded(libPath):
       #    abslibPath =
       #    return os.system("lsof -p {} | grep {} > /dev/null".format( os.getpid(), os.path.abspath(libPath) )) == 0

        def dlclose(libdll): libdll.dlclose(libdll._handle)

        if _pm.platform.isWin32:
            handle = _ct.windll.kernel32.LoadLibraryA(libPath)
            _ct.windll.kernel32.FreeLibrary(handle)
        else:
           #while isLoaded(libPath):
           #    dlclose(pmdll._handle)
            try:
                import _ctypes
                _ctypes.dlclose(pmdll._handle)
            except:
                if self._mpiDisabled:
                    _pm.warn( msg   = "Failed to properly close the ParaMonte dynamic library file\n"
                                    + "This should not cause any major problems, unless you intend to\n"
                                    + "run a new ParaMonte simulation, in which case, you may want to\n"
                                    + "exit and re-enter your Python environment."
                            , methodName = _pm.names.paradram
                            , marginTop = 1
                            , marginBot = 1
                            )

        if self._mpiDisabled:
            _pm.note( msg   = "To read the generated output files sample or chain files, try the following:\n\n"
                            + "    pmpd.readSample()      # to read the final i.i.d. sample from the output sample file. \n"
                            + "    pmpd.readChain()       # to read the uniquely-accepted points from the output chain file. \n"
                            + "    pmpd.readMarkovChain() # to read the Markov Chain. NOT recommended for extremely-large chains.\n\n"
                            + "Replace 'pmpd' with the name you are using for your ParaDRAM object.\n"
                            + "For more information and examples on the usage, visit:\n\n"
                            + "    https://www.cdslab.org/paramonte/"
                    , methodName = _pm.names.paradram
                    , marginTop = 1
                    , marginBot = 1
                    )

        return None

    ################################################################################################################################
    #### ParaDRAM postprocessing
    ################################################################################################################################

    def readChain   ( self
                    , file          : tp.Optional[str] = None
                    , delimiter     : tp.Optional[str] = None
                    , parseContents : tp.Optional[bool] = True
                    , renabled      : tp.Optional[bool] = False
                    ) -> tp.List[_ParaDRAMChain] :
        """

        Return a list of the contents of a set of ParaDRAM output
        chain files whose names begin the user-provided input file.
        This method is to be only used for postprocessing of the output
        chain file(s) of an already finished ParaDRAM simulation.
        It is not meant to be called by all processes in parallel mode,
        although it is possible.

            **Parameters**

                file
                    A string representing the path to the chain file with
                    the default value of None.
                    The path only needs to uniquely identify the simulation
                    to which the chain file belongs. For example, specifying
                    "./mydir/mysim" as input will lead to a search for a file
                    that begins with "mysim" and ends with "_chain.txt"
                    inside the directory "./mydir/". If there are multiple
                    files with such name, then all of them will be read
                    and returned as a list.
                    If this input argument is not provided by the user, the
                    value of the object attribute outputFileName
                    will be used instead. At least one of the two mentioned
                    routes must provide the path to the chain file otherwise,
                    this method will break by calling ``sys.exit()``.

                delimiter
                    Optional input string representing the delimiter used in the
                    output chain file. If it is not provided as input argument,
                    the value of the corresponding object attribute outputDelimiter
                    will be used instead. If none of the two are available,
                    the default comma delimiter "," will be assumed and used.

                parseContents
                    If set to True, the contents of the file will be parsed and
                    stored in a component of the object named ``contents``.
                    The default value is ``True``.

                renabled
                    If set to False, the contents of the file(s) will be stored as a
                    list in a (new) component of the ParaDRAM object named ``chainList``
                    and ``None`` will be the return value of the method.
                    If set to True, the reverse will done.
                    The default value is ``False``.

            **Returns**

                a list of objects, each of which has the following properties:

                    file
                        full absolute path to the chain file.

                    delimiter
                        the delimiter used in the chain file.

                    ndim
                        number of dimensions of the domain of the objective function
                        from which the chain has been drawn.

                    count
                        the number of unique (weighted) points in the chain file.
                        This is essentially the number of rows in the chain file
                        minus one (representing the header line).

                    df
                        the contents of the chain file in the form of
                        a pandas-library DataFrame (hence called ``df``).

                    dynamic attributes:
                        corresponding to each column in the chain file, a property
                        with the same name as the column header is also created
                        for the object which contains the data stored in that column
                        of the chain file.

                If ``renabled = True``, the list of objects will be returned as the
                return value of the method. Otherwise, the list will be stored in a
                component of the ParaDRAM object named ``chainList``.

        """

        if file is None:
            if self.spec.outputFileName is None:
                _pm.abort   ( msg   = "'file' is neither given as input nor set as a ParaDRAM object property.\n"
                                    + "This information is essential, otherwise how could the output files be found?\n"
                                    + "All that is needed is the unique name (including path) of the simulation name shared\n"
                                    + "among its output files or simply, the path to the chain file."
                            , methodName = _pm.names.paradram
                            , marginTop = 1
                            , marginBot = 1
                            )
            else:
                file = self.spec.outputFileName

        if delimiter is None:
            if self.spec.outputDelimiter is None:
                delimiter   = ","
                if self._mpiDisabled:
                    _pm.warn( msg   = "delimiter is neither given as input nor set as a ParaDRAM object property.\n"
                                    + "This information is essential for successful reading of the requested chain file(s).\n"
                                    + "Proceeding with the default assumption of comma-delimited chain file contents..."
                            , methodName = _pm.names.paradram
                            , marginTop = 1
                            , marginBot = 1
                            )
            else:
                delimiter = self.spec.outputDelimiter

        FileList = _pm.utils.getFileList(file,"chain",_pm.names.paradram,self._mpiDisabled)

        chainList = []
        for file in FileList:

            file = os.path.abspath(file)
            if self._mpiDisabled:
                _pm.note( msg = "processing file: " + file
                        , methodName = _pm.names.paradram
                        , marginTop = 0
                        , marginBot = 0
                        )

            Chain = _ParaDRAMChain  ( file = file
                                    , delimiter = delimiter
                                    , parseContents = parseContents
                                    , mpiDisabled = self._mpiDisabled
                                    )
            chainList.append(Chain)

        if renabled:
            print("\n")
            return chainList
        else:
            if self._mpiDisabled:
                self.chainList = chainList
                _pm.note( msg   = "The processed chain file(s) are now stored as a Python list in \n"
                                + "the new component \"chainList\" of the ParaDRAM-instance object.\n"
                                + "For example, to access the contents of the first (or the only) chain file, try:\n\n"
                                + "    pmpd.chainList[0].df\n\n"
                                + "To access plots, try:\n\n"
                                + "    pmpd.chainList[0].plot.<PRESS TAB TO SEE THE LIST OF PLOTS>\n\n"
                                + "Replace 'pmpd' with the name you are using for your ParaDRAM object.\n"
                                + "For more information and examples on the usage, visit:\n\n"
                                + "    https://www.cdslab.org/paramonte/"
                        , methodName = _pm.names.paradram
                        , marginTop = 1
                        , marginBot = 1
                        )


    ################################################################################################################################

    def readMarkovChain ( self
                        , file          : tp.Optional[str] = None
                        , delimiter     : tp.Optional[str] = None
                        , parseContents : tp.Optional[bool] = True
                        , renabled      : tp.Optional[bool] = False
                        ) -> tp.List[_ParaDRAMChain] :
        """

        .. py:method:: readMarkovChain(self, file = None, delimiter = None, parseContents = True, renabled = False)

        Return a list of the unweighted (Markov-chain) contents of a set of
        ParaDRAM output chain files, whose names begin the user-provided
        input variable 'file'. This method is to be only used for postprocessing
        of the output chain file(s) of an already finished ParaDRAM simulation.
        It is not meant to be called by all processes in parallel mode,
        although it is possible.

            **Parameters**

                file
                    A string representing the path to the chain file with
                    the default value of None.
                    The path only needs to uniquely identify the simulation
                    to which the chain file belongs. For example, specifying
                    "./mydir/mysim" as input will lead to a search for a file
                    that begins with "mysim" and ends with "_chain.txt"
                    inside the directory "./mydir/". If there are multiple
                    files with such name, then all of them will be read
                    and returned as a list.
                    If this input argument is not provided by the user, the
                    value of the object attribute outputFileName
                    will be used instead. At least one of the two mentioned
                    routes must provide the path to the chain file otherwise,
                    this method will break by calling ``sys.exit()``.

                delimiter
                    Optional input string representing the delimiter used in the
                    output chain file. If it is not provided as input argument,
                    the value of the corresponding object attribute outputDelimiter
                    will be used instead. If none of the two are available,
                    the default comma delimiter "," will be assumed and used.

                parseContents
                    If set to True, the contents of the file will be parsed and
                    stored in a component of the object named ``contents``.
                    The default value is ``True``.

                renabled
                    If set to False, the contents of the file(s) will be stored as a
                    list in a (new) component of the ParaDRAM object named ``markovChainList``
                    and ``None`` will be the return value of the method.
                    If set to True, the reverse will done.
                    The default value is ``False``.

            **Returns**

                a list of objects, each of which has the following properties:

                    file
                        full absolute path to the chain file.

                    delimiter
                        the delimiter used in the chain file.

                    ndim
                        number of dimensions of the domain of the objective function
                        from which the chain has been drawn.

                    count
                        the number of unique (weighted) points in the chain file.
                        This is essentially the number of rows in the chain file
                        minus one (representing the header line).

                    df
                        the unweighted (Markovian) contents of the chain file in the
                        form of a pandas-library DataFrame (hence called ``df``).

                    dynamic attributes:
                        corresponding to each column in the chain file, a property
                        with the same name as the column header is also created
                        for the object which contains the data stored in that column
                        of the chain file.

                If ``renabled = True``, the list of objects will be returned as the
                return value of the method. Otherwise, the list will be stored in a
                component of the ParaDRAM object named ``markovChainList``.

        """

        if file is None:
            if self.spec.outputFileName is None:
                _pm.abort   ( msg   = "'file' is neither given as input nor set as a ParaDRAM object property.\n"
                                    + "This information is essential, otherwise how could the output files be found?\n"
                                    + "All that is needed is the unique name (including path) of the simulation name shared\n"
                                    + "among its output files or simply, the path to the chain file."
                            , methodName = _pm.names.paradram
                            , marginTop = 1
                            , marginBot = 1
                            )
            else:
                file = self.spec.outputFileName

        if delimiter is None:
            if self.spec.outputDelimiter is None:
                delimiter   = ","
                if self._mpiDisabled:
                    _pm.warn( msg   = "delimiter is neither given as input nor set as a ParaDRAM object property.\n"
                                    + "This information is essential for successful reading of the requested chain file(s).\n"
                                    + "Proceeding with the default assumption of comma-delimited chain file contents..."
                            , methodName = _pm.names.paradram
                            , marginTop = 1
                            , marginBot = 1
                            )
            else:
                delimiter = self.spec.outputDelimiter

        FileList = _pm.utils.getFileList(file,"chain",_pm.names.paradram,self._mpiDisabled)

        markovChainList = []
        for file in FileList:

            file = os.path.abspath(file)
            if self._mpiDisabled:
                _pm.note( msg = "processing file: " + file
                        , methodName = _pm.names.paradram
                        , marginTop = 0
                        , marginBot = 0
                        )

            Chain = _ParaDRAMChain  ( file = file
                                    , delimiter = delimiter
                                    , parseContents = parseContents
                                    , markovChainRequested = True
                                    , mpiDisabled = self._mpiDisabled
                                    )
            markovChainList.append(Chain)

        if renabled:
            print("\n")
            return markovChainList
        else:
            if self._mpiDisabled:
                self.markovChainList = markovChainList
                _pm.note( msg   = "The processed Markov chain file(s) are now stored as a Python list in \n"
                                + "the new component \"markovChainList\" of the ParaDRAM-instance object.\n"
                                + "For example, to access the contents of the first (or the only) Markov chain, try:\n\n"
                                + "    pmpd.markovChainList[0].df\n\n"
                                + "To access plots, try:\n\n"
                                + "    pmpd.markovChainList[0].plot.<PRESS TAB TO SEE THE LIST OF PLOTS>\n\n"
                                + "Replace 'pmpd' with the name you are using for your ParaDRAM object.\n"
                                + "For more information and examples on the usage, visit:\n\n"
                                + "    https://www.cdslab.org/paramonte/"
                        , methodName = _pm.names.paradram
                        , marginTop = 1
                        , marginBot = 1
                        )

    ################################################################################################################################

    def readSample  ( self
                    , file          : tp.Optional[str]  = None
                    , delimiter     : tp.Optional[str]  = None
                    , parseContents : tp.Optional[bool] = True
                    , renabled      : tp.Optional[bool] = False
                    ) -> tp.List[_ParaDRAMChain] :
        """


        Return a list of the contents of a set of ParaDRAM output
        sample files whose names contain the user-provided input file.
        This method is to be only used for postprocessing of the output
        sample file(s) of an already finished ParaDRAM simulation.
        It is not meant to be called by all processes in parallel mode,
        although it is possible.

            **Parameters**

                file
                    A string representing the path to the sample file with
                    the default value of None.
                    The path only needs to uniquely identify the simulation
                    to which the sample file belongs. For example, specifying
                    "./mydir/mysim" as input will lead to a search for a file
                    that begins with "mysim" and ends with "_sample.txt"
                    inside the directory "./mydir/". If there are multiple
                    files with such name, then all of them will be read
                    and returned as a list.
                    If this input argument is not provided by the user, the
                    value of the object attribute outputFileName
                    will be used instead. At least one of the two mentioned
                    routes must provide the path to the sample file otherwise,
                    this method will break by calling ``sys.exit()``.

                delimiter
                    Optional input string representing the delimiter used in the
                    output sample file. If it is not provided as input argument,
                    the value of the corresponding object attribute outputDelimiter
                    will be used instead. If none of the two are available,
                    the default comma delimiter "," will be assumed and used.

                parseContents
                    If set to True, the contents of the file will be parsed and
                    stored in a component of the object named ``contents``.
                    The default value is ``True``.

                renabled
                    If set to False, the contents of the file(s) will be stored as a
                    list in a (new) component of the ParaDRAM object named ``sampleList``
                    and ``None`` will be the return value of the method.
                    If set to True, the reverse will done.
                    The default value is ``False``.

            **Returns**

                a list of objects, each of which has the following properties:

                    file
                        full absolute path to the sample file.

                    delimiter
                        the delimiter used in the sample file.

                    ndim
                        number of dimensions of the domain of the objective function
                        from which the sample has been drawn.

                    count
                        number of sampled points in the sample file.

                    df
                        the contents of the sample file in the form of
                        a pandas-library DataFrame (hence called ``df``).

                    dynamic attributes:
                        corresponding to each column in the sample file, a property
                        with the same name as the column header is also created
                        for the object which contains the data stored in that column
                        of the sample file.

                If ``renabled = True``, the list of objects will be returned as the
                return value of the method. Otherwise, the list will be stored in a
                component of the ParaDRAM object named ``sampleList``.

        """

        if file is None:
            if self.spec.outputFileName is None:
                _pm.abort   ( msg   = "'file' is neither given as input nor set as a ParaDRAM object property.\n"
                                    + "This information is essential, otherwise how could the output files be found?\n"
                                    + "All that is needed is the unique name (including path) of the simulation name shared\n"
                                    + "among its output files or simply, the path to the sample file."
                            , methodName = _pm.names.paradram
                            )
            else:
                file = self.spec.outputFileName

        if delimiter is None:
            if self.spec.outputDelimiter is None:
                delimiter   = ","
                if self._mpiDisabled:
                    _pm.warn( msg   = "delimiter is neither given as input nor set as a ParaDRAM object property.\n"
                                    + "This information is essential for successful reading of the requested sample file(s).\n"
                                    + "Proceeding with the default assumption of comma-delimited sample file contents..."
                            , methodName = _pm.names.paradram
                            , marginTop = 1
                            , marginBot = 1
                            )
            else:
                delimiter = self.spec.outputDelimiter

        FileList = _pm.utils.getFileList(file,"sample",_pm.names.paradram,self._mpiDisabled)

        sampleList = []
        for file in FileList:

            file = os.path.abspath(file)
            if self._mpiDisabled:
                _pm.note( msg = "processing file: " + file
                        , methodName = _pm.names.paradram
                        , marginTop = 0
                        , marginBot = 0
                        )

            Sample = _ParaDRAMChain ( file = file
                                    , delimiter = delimiter
                                    , parseContents = parseContents
                                    , mpiDisabled = self._mpiDisabled
                                    )
            sampleList.append(Sample)

        if renabled:
            print("\n")
            return sampleList
        else:
            if self._mpiDisabled:
                self.sampleList = sampleList
                _pm.note( msg   = "The processed sample file(s) are now stored as a Python list in \n"
                                + "the new component \"sampleList\" of the ParaDRAM-instance object.\n"
                                + "For example, to access the contents of the first (or the only) sample file, try:\n\n"
                                + "    pmpd.sampleList[0].df\n\n"
                                + "To access plots, try:\n\n"
                                + "    pmpd.sampleList[0].plot.<PRESS TAB TO SEE THE LIST OF PLOTS>\n\n"
                                + "Replace 'pmpd' with the name you are using for your ParaDRAM object.\n"
                                + "For more information and examples on the usage, visit:\n\n"
                                + "    https://www.cdslab.org/paramonte/"
                        , methodName = _pm.names.paradram
                        , marginTop = 1
                        , marginBot = 1
                        )

    ################################################################################################################################

__all__ = [ "ParaDRAM" ]