from Classification.Instance.CompositeInstance cimport CompositeInstance
from Classification.InstanceList.InstanceList cimport InstanceList


cdef class DummyModel(Model):

    def __init__(self, trainSet: InstanceList):
        """
        Constructor which sets the distribution using the given InstanceList.

        PARAMETERS
        ----------
        trainSet : InstanceList
            InstanceList which is used to get the class distribution.
        """
        self.distribution = trainSet.classDistribution()

    cpdef str predict(self, Instance instance):
        """
        The predict method takes an Instance as an input and returns the entry of distribution which has the maximum
        value.

        PARAMETERS
        ----------
        instance : Instance
            Instance to make prediction.

        RETURNS
        -------
        str
            The entry of distribution which has the maximum value.
        """
        cdef list possibleClassLabels
        if isinstance(instance, CompositeInstance):
            possibleClassLabels = instance.getPossibleClassLabels()
            return self.distribution.getMaxItemIncludeTheseOnly(possibleClassLabels)
        else:
            return self.distribution.getMaxItem()
