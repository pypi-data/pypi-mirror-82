from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.DecisionTree.DecisionNode cimport DecisionNode
from Classification.Model.ValidatedModel cimport ValidatedModel


cdef class DecisionTree(ValidatedModel):

    cdef DecisionNode __root

    cpdef pruneNode(self, DecisionNode node, InstanceList pruneSet)
    cpdef prune(self, InstanceList pruneSet)
