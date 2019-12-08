from functools import reduce
from models import Variable, KnowledgeBase


class Term:
    def __init__(self, functor, arguments=None):
        if arguments is None:
            arguments = []
        self.functor = functor
        self.arguments = arguments

    def match_variable_bindings(self, other_term):
        if isinstance(other_term, Variable):
            # If the other_term is a Variable, match them using Variable.match_variable_bindings()
            return other_term.match_variable_bindings(self)

        if isinstance(other_term, Term):
            # Verify if the two terms has identical functors and number of arguments.
            if self.functor != other_term.functor or len(self.arguments) != len(other_term.arguments):
                return None

            # Zip the argument lists of the two terms.
            # zipped_argument_list will have shape (num_args, 2).
            # where zipped_argument_list[i][0] is the i-th argument of self,
            # and   zipped_argument_list[i][1] is the i-th argument of other_term.
            # These two are to be matched together.
            zipped_argument_list = list(zip(self.arguments, other_term.arguments))

            # Get the matched variable bindings list for the matching arguments in our 2 terms and merge them.
            matched_argument_var_bindings = [
                arguments[0].match_variable_bindings(arguments[1])
                for arguments in zipped_argument_list
            ]

            # Merge all the variable bindings
            return reduce(KnowledgeBase.merge_bindings, [{}] + matched_argument_var_bindings)

    def substitute_variable_bindings(self, variable_bindings):
        return Term(self.functor, [
            argument.substitute_variable_bindings(variable_bindings)
            for argument in self.arguments
        ])

    def query(self, database):
        yield from database.query(self)

    def __str__(self):
        if len(self.arguments) == 0:
            return str(self.functor)
        args = ", ".join(str(argument) for argument in self.arguments)
        return str(self.functor) + " ( " + args + " ) "

    def __repr__(self):
        return str(self)


class TRUE(Term):
    def __init__(self, functor="TRUE", arguments=None):
        super(TRUE, self).__init__(functor, arguments)

    def substitute_variable_bindings(self, variable_bindings):
        return self

    def query(self, database):
        yield self
