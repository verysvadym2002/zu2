import numpy as np


class FuzzySet:
    def __init__(self, name, membership_function):
        self.name = name
        self.membership_function = membership_function

    def membership(self, x):
        return self.membership_function(x)


class LingVariable:
    def __init__(self, name):
        self.name = name
        self.sets = {}

    def add_set(self, fuzzy_set):
        self.sets[fuzzy_set.name] = fuzzy_set

    def fuzzify(self, value):
        memberships = {}
        for name, fuzzy_set in self.sets.items():
            memberships[name] = fuzzy_set.membership(value)

        return memberships


class FuzzyRule:
    def __init__(self, antecedents, consequent):
        self.antecedents = antecedents
        self.consequent = consequent

    def evaluate(self, fuzzified_inputs):
        memberships = [fuzzified_inputs[var][fuzzy_set] for var, fuzzy_set in self.antecedents]
        return min(memberships)


class FuzzySystem:
    def __init__(self):
        self.variables = {}
        self.rules = []
        self.output_variable = None

    def add_variable(self, fuzzy_variable, is_output=False):
        if is_output:
            self.output_variable = fuzzy_variable
        else:
            self.variables[fuzzy_variable.name] = fuzzy_variable

    def add_rule(self, rule):
        self.rules.append(rule)

    def infer(self, inputs):
        fuzzified_inputs = {name: var.fuzzify(inputs[name]) for name, var in self.variables.items()}
        output_sets = {name: [] for name in self.output_variable.sets}
        for rule in self.rules:
            activation = rule.evaluate(fuzzified_inputs)
            output_set_name = rule.consequent[1]
            output_sets[output_set_name].append(activation)

        aggregated_output = {name: max(values) if values else 0 for name, values in output_sets.items()}
        return aggregated_output

    def defuzzify(self, aggregated_output, resolution=1000):
        x = np.linspace(100, 0, resolution)
        max_xi = 0
        max_membership = 0
        for xi in x:
            for set_name, membership_value in aggregated_output.items():
                membership_value_temp = min(self.output_variable.sets[set_name].membership(xi), membership_value)
                if membership_value_temp > max_membership:
                    max_membership = membership_value_temp
                    max_xi = xi

        return max_xi


def triangle(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif a < x < b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)
