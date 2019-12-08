class Variable:
    def __init__(self, name):
        self.name = name

    def match_variable_bindings(self, other_term):
        bindings = {}
        if self != other_term:
            bindings[self] = other_term
        return bindings

    def substitute_variable_bindings(self, variable_bindings):
        bound_variable_value = variable_bindings.get(self)
        if bound_variable_value:
            return bound_variable_value.substitute_variable_bindings(variable_bindings)
        return self

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self)
