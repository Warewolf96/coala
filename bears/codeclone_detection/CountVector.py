class CountVector:
    def __init__(self, name, conditions=None, weightings=None):
        """
        Creates a new count vector.

        :param name:       The name of the variable in the original code.
        :param conditions: The counting conditions as list of function objects,
                           each shall return true when getting data indicating
                           that this occurrence should be counted.
        :param weightings: Optional factors to weight counting conditions.
                           Defaults to 1 for all conditions.
        """
        self.name = name
        self.conditions = conditions if conditions is not None else []
        self.count_vector = [0 for elem in self.conditions]
        self.weightings = weightings
        if self.weightings is None:
            self.weightings = [1 for elem in self.conditions]

        assert len(self.count_vector) is len(self.weightings)

    def count_reference(self, *args, **kwargs):
        """
        Counts the reference to the variable under the conditions held in this
        object.

        Any arguments or kwarguments will be passed to all conditions.
        """
        for i in range(len(self.conditions)):
            if self.conditions[i](*args, **kwargs):
                self.count_vector[i] += self.weightings[i]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.count_vector)

    def __len__(self):
        return len(self.count_vector)

    def __iter__(self):
        return iter(self.count_vector)

    def difference(self, other):
        """
        Calculates a normalized difference. This value can be used to indicate
        the similarity of the associated variables, while 0 means no
        difference, i.e. the count vectors are identical, and 1 means maximum
        difference, i.e. they are not similar at all.

        :param other: The CountVector to calculate the difference to.
        :return:      A difference value in [0, 1].
        """
        assert isinstance(other, CountVector)
        assert len(other) == len(self)

        maxabs = sum(max(x, y)**2 for x, y in zip(self, other))
        if maxabs == 0:
            return 0

        return sum((x-y)**2 for x, y in zip(self, other))/maxabs