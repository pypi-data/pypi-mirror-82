from Classification.Instance.Instance cimport Instance
from Classification.Model.Model cimport Model


cdef class RandomModel(Model):

    cdef list __classLabels

    cpdef str predict(self, Instance instance)
