from blog.global_class.base_input import BaseInput
from .fitness_context import FitnessContext


class DBInput(BaseInput):

    def save(self):
        data: FitnessContext = self.data

        Fitness(weight=data.weight, date=data.date).save()
