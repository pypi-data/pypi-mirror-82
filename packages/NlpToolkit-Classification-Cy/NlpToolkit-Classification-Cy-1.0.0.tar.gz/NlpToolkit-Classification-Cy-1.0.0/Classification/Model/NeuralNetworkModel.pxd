from Math.Matrix cimport Matrix
from Math.Vector cimport Vector
from Classification.Instance.Instance cimport Instance
from Classification.Model.ValidatedModel cimport ValidatedModel


cdef class NeuralNetworkModel(ValidatedModel):

    cdef list classLabels
    cdef int K, d
    cdef Vector x, y, r

    cpdef calculateOutput(self)
    cpdef Matrix allocateLayerWeights(self, int row, int column, int seed)
    cpdef Vector normalizeOutput(self, Vector o)
    cpdef createInputVector(self, Instance instance)
    cpdef Vector calculateHidden(self, Vector input, Matrix weights)
    cpdef Vector calculateOneMinusHidden(self, Vector hidden)
    cpdef calculateForwardSingleHiddenLayer(self, Matrix W, Matrix V)
    cpdef Vector calculateRMinusY(self, Instance instance, Vector inputVector, Matrix weights)
    cpdef str predictWithCompositeInstance(self, list possibleClassLabels)
    cpdef str predict(self, Instance instance)
