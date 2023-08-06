from Classification.DistanceMetric.DistanceMetric cimport DistanceMetric
from Classification.Instance.Instance cimport Instance
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.GaussianModel cimport GaussianModel


cdef class KMeansModel(GaussianModel):

    cdef InstanceList __classMeans
    cdef DistanceMetric __distanceMetric

    cpdef double calculateMetric(self, Instance instance, str Ci)

