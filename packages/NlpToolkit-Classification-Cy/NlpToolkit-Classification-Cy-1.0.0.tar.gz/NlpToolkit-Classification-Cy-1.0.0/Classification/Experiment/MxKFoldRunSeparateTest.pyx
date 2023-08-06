from Sampling.KFoldCrossValidation cimport KFoldCrossValidation
from Classification.Experiment.Experiment cimport Experiment
from Classification.Experiment.KFoldRunSeparateTest cimport KFoldRunSeparateTest
from Classification.InstanceList.Partition cimport Partition
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Performance.ExperimentPerformance cimport ExperimentPerformance


cdef class MxKFoldRunSeparateTest(KFoldRunSeparateTest):

    cdef int M

    def __init__(self, M: int, K: int):
        """
        Constructor for KFoldRunSeparateTest class. Basically sets K parameter of the K-fold cross-validation and M for
        the number of times.

        PARAMETERS
        ----------
        M : int
            number of cross-validation times.
        K : int
            K of the K-fold cross-validation.
        """
        super().__init__(K)
        self.M = M

    cpdef ExperimentPerformance execute(self, Experiment experiment):
        """
        Execute the MxKFold run with separate test set with the given classifier on the given data set using the given
        parameters.

        PARAMETERS
        ----------
        experiment : Experiment
            Experiment to be run.

        RETURNS
        -------
        ExperimentPerformance
            An ExperimentPerformance instance.
        """
        cdef ExperimentPerformance result
        cdef InstanceList instanceList
        cdef Partition partition
        cdef int j
        cdef KFoldCrossValidation crossValidation
        result = ExperimentPerformance()
        instanceList = experiment.getDataSet().getInstanceList()
        partition = Partition(instanceList, 0.25, experiment.getParameter().getSeed(), True)
        for j in range(self.M):
            crossValidation = KFoldCrossValidation(partition.get(1).getInstances(), self.K, experiment.getParameter().
                                                   getSeed())
            self.runExperimentSeparate(experiment.getClassifier(), experiment.getParameter(), result, crossValidation,
                               partition.get(0))
        return result
