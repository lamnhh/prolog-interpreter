from models import Term, KnowledgeBase


class Conjunction(Term):
    def __init__(self, arguments=None):
        super().__init__("", arguments)

    def query(self, knowledge_base):
        def find_solutions(this, kb, argument_index, variable_bindings):
            if argument_index >= len(this.arguments):
                yield this.substitute_variable_bindings(variable_bindings)
            else:
                current_term = this.arguments[argument_index]
                for item in kb.query(current_term.substitute_variable_bindings(variable_bindings)):
                    combined_variable_bindings = KnowledgeBase.merge_bindings(
                        current_term.match_variable_bindings(item),
                        variable_bindings
                    )

                    if combined_variable_bindings is not None:
                        yield from find_solutions(this, kb, argument_index + 1, combined_variable_bindings)

        yield from find_solutions(self, knowledge_base, 0, {})

    def substitute_variable_bindings(self, variable_bindings):
        return Conjunction([argument.substitute_variable_bindings(variable_bindings) for argument in self.arguments])

    def __str__(self):
        return ", ".join(str(argument) for argument in self.arguments)

    def __repr__(self):
        return str(self)
