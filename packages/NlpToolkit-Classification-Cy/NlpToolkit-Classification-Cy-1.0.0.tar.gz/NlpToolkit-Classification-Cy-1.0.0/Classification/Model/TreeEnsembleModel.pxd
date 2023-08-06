from Classification.Model.Model cimport Model


cdef class TreeEnsembleModel(Model):

    cdef list __forest
