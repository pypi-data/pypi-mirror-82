from Classification.DataSet.DataSet cimport DataSet
from Classification.DataSet.DataDefinition cimport DataDefinition


cdef class LaryFilter(FeatureFilter):

    def __init__(self, dataSet: DataSet):
        """
        Constructor that sets the dataSet and all the attributes distributions.

        PARAMETERS
        ----------
        dataSet : DataSet
            DataSet that will bu used.
        """
        super().__init__(dataSet)
        self.attributeDistributions = dataSet.getInstanceList().allAttributesDistribution()

    cpdef removeDiscreteAttributesFromInstance(self, Instance instance, int size):
        """
        The removeDiscreteAttributesFromInstance method takes an Instance as an input, and removes the discrete
        attributes from given instance.

        PARAMETERS
        ----------
        instance : Instance
            Instance to removes attributes from.
        size : int
            Size of the given instance.
        """
        cdef int k, i
        k = 0
        for i in range(size):
            if len(self.attributeDistributions[i]) > 0:
                instance.removeAttribute(k)
            else:
                k = k + 1

    cpdef removeDiscreteAttributesFromDataDefinition(self, int size):
        """
        The removeDiscreteAttributesFromDataDefinition method removes the discrete attributes from dataDefinition.

        PARAMETERS
        ----------
        size : int
            Size of item that attributes will be removed.
        """
        cdef DataDefinition dataDefinition
        cdef int k, i
        dataDefinition = self.dataSet.getDataDefinition()
        k = 0
        for i in range(size):
            if len(self.attributeDistributions[i]) > 0:
                dataDefinition.removeAttribute(k)
            else:
                k = k + 1
