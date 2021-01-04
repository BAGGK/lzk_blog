from .model import Fitness
from .fitness_context import FitnessContext


class AdapterFactor(object):

    def __new__(cls, instance):
        if isinstance(instance, Fitness):
            return FitnessAdapter(instance)

        return super(AdapterFactor, cls).__new__(cls)


class FitnessAdapter(FitnessContext):

    def __init__(self, fitness_db):
        """

        :type fitness_db: Fitness
        """
        super(FitnessAdapter, self).__init__(fitness_db.weight, fitness_db.date)
