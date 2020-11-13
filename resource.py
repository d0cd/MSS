from enum import Enum


# Define any new resource types here
class ResourceType(Enum):
    CPU = 1
    GPU = 1


class Resource:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Resource class should not be implemented. Create a subclass.")


class ResourcePool:
    pass


