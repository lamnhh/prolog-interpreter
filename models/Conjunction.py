from models import Term, KnowledgeBase


# A conjunction is a logical operator that connects two terms. A conjunction between the two terms will result in
# the expression evaluating to true only if both terms evaluate to true. As an example, we could state that a teacher
# teaches another student if the student lectures a course and the student studies the course using the rule below:
# teaches(Teacher, Student) :- lectures(Teacher, Course), studies(Student, Course).
class Conjunction(Term):
    def __init__(self, arguments=None):
        super().__init__("", arguments)

    # Return a generator that iterates over all of the conjunction terms which match the database rules.
    def query(self, database):
        # Return a generator which iterates over all of the database solutions matching our rules
        def find_solutions(this, kb, argument_index, variable_bindings):

            # If there are no more arguments to match, we return the substituted variable bindings for our
            # entire conjunction
            if argument_index >= len(this.arguments):
                yield this.substitute_variable_bindings(variable_bindings)
            else:
                # There are more arguments to process, so we process the argument at our current index
                current_term = this.arguments[argument_index]

                # Find all of the database items matching our current variable bindings, and if we have matching
                # items, keep searching the database by iterating over our next conjunction arguments
                for item in kb.query(current_term.substitute_variable_bindings(variable_bindings)):

                    combined_variable_bindings = \
                        KnowledgeBase.merge_bindings(current_term.match_variable_bindings(item), variable_bindings)

                    if combined_variable_bindings is not None:
                        yield from find_solutions(this, kb, argument_index + 1, combined_variable_bindings);

        # Find all of the conjunction solutions matching our database rules. As a note, the yield from expression is
        # a form of generator delegation used to recursively process all of the items matching our rules.
        yield from find_solutions( self,  database, 0, {})

    # Take the variable bindings map and return a conjunction with all occurrences of the variables present in our
    # current conjunction terms replaced with a list of terms containing the substituted variable bindings from our
    # variable bindings map.
    def substitute_variable_bindings(self, variable_bindings):
        return Conjunction([argument.substitute_variable_bindings(variable_bindings) for argument in self.arguments])

    # Return a readable representation of our conjunction containing a list of its arguments / terms.
    def __str__(self):
        return ", ".join(str(argument) for argument in self.arguments)

    # Use the default string representation
    def __repr__(self):
        return str(self)
