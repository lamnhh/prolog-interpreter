from functools import reduce
from models import Variable, KnowledgeBase


class Term:
    def __init__(self, functor, arguments=None):
        if arguments is None:
            arguments = []
        self.functor = functor
        self.arguments = arguments

    # Returns a map of matching variable bindings
    def match_variable_bindings(self, other_term):

        # If the passed in term is a variable, we bind the variable to our current term and return the result.
        if isinstance(other_term, Variable):
            return other_term.match_variable_bindings(self)

        # If we have a term, we check if the terms are identical and if so, we extract the combined variable bindings.
        if isinstance(other_term, Term):

            # Verify that the functor and argument lengths match.
            if self.functor != other_term.functor or len(self.arguments) != len(other_term.arguments):
                return None

            # Zip the current term and the other term arguments and combine the results into one list.
            # Zip creates a new list filled with tuples containing the matching elements from the 2 argument lists.
            # i.e. zip ([1, 2, 3],[4, 5, 6]) returns [(1, 4), (2, 5), (3, 6)]
            zipped_argument_list = list(zip(self.arguments, other_term.arguments))

            # Get the matched variable bindings list for the matching arguments in our 2 terms and merge them.
            matched_argument_var_bindings = \
                [arguments[0].match_variable_bindings(arguments[1]) for arguments in zipped_argument_list]

            # Merge the combined argument variable bindings and return the result.
            # The reduce function applies a rolling computation to sequential pairs of values in a list.
            # i.e. reduce((lambda x, y: x + y), [1, 2, 3, 4]) returns 10
            return reduce(KnowledgeBase.merge_bindings, [{}] + matched_argument_var_bindings)

    # Take the variable bindings map and return a term with all occurrences of the term variables
    # replaced with the corresponding variable values from our variable bindings map.
    def substitute_variable_bindings(self, variable_bindings):
        return Term( self.functor,
                    [argument.substitute_variable_bindings(variable_bindings) for argument in self.arguments] )

    # Query the database for terms matching this one
    def query(self, database):
        yield from database.query(self)

    # Return a readable representation of our term containing our functor and argument info.
    def __str__(self):
        return str(self.functor) if len(self.arguments) == 0 else str(self.functor) + " ( " + ", ".join(
            str(argument) for argument in self.arguments) + " ) "

    # Use the default string representation
    def __repr__(self):
        return str(self)


# A predefined term used to represent facts as rules.
# i.e. functor(argument1, argument2) for example gets translated to functor(argument1, argument2) :- TRUE
class TRUE(Term):
    def __init__(self, functor="TRUE", arguments=None):
        super(TRUE, self).__init__(functor, arguments)

    # Simply return our truth term since there is nothing to bind
    def substitute_variable_bindings(self, variable_bindings):
        return self

    def query(self, database):
        yield self
