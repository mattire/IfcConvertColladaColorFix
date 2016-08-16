
from abc import abstractmethod


class LineManagerBase(object):
    """Abstract base class for ifc file line manager"""
    def __init__(self):
        pass

    @abstractmethod
    def getElementNewMaterial(self, elemId, oldType):
        raise NotImplementedError('derived classes should implement this')


