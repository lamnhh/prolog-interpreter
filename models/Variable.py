

# A variable is a type of term. Variables start with an uppercase letter and represent placeholders for actual terms.
class Variable:
    def __init__(self, name):
        self.name = name

    # If the passed in term doesn't represent the same variable, we bind our current variable to the outer term and
    # return the mapped binding.
    def match_variable_bindings(self, other_term):
        bindings = {}

        if self != other_term:
            bindings[self] = other_term

        return bindings

    # Fetch the currently bound variable value for our variable and return the substituted bindings if our
    # variable is mapped. If our variable isn't mapped, we simply return the variable as the substitute.
    def substitute_variable_bindings(self, variable_bindings):
        bound_variable_value = variable_bindings.get(self)

        if bound_variable_value:
            return bound_variable_value.substitute_variable_bindings(variable_bindings)

        return self

    # Return a readable representation of our variable containing the variable name.
    def __str__(self):
        return str(self.name)

    # Use the default string representation.
    def __repr__(self):
        return str(self)
