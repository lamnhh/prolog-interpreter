from collections import defaultdict
from controllers.Parser import Parser
from models import KnowledgeBase, Variable


class Solver:
    def __init__(self, knowledge_base):
        self.rules = Parser(knowledge_base).parse_rules()
        self.knowledge_base = KnowledgeBase(self.rules)

    def solve(self, query_text):
        query = Parser(query_text).parse_query()

        query_variable_map = {}
        variables_in_query = False

        # Map all variables to actual variables
        for argument in query.arguments:
            if isinstance(argument, Variable):
                variables_in_query = True
                query_variable_map[argument.name] = argument

        matching_query_terms = [item for item in self.knowledge_base.query(query)]

        if matching_query_terms:
            if query_variable_map:
                solutions_map = defaultdict(list)
                for matching_query_term in matching_query_terms:
                    matching_variable_bindings = query.match_variable_bindings(matching_query_term)
                    for variable_name, variable in query_variable_map.items():
                        solutions_map[variable_name].append(matching_variable_bindings.get(variable))

                ans = ""
                for i in range(len(next(iter(solutions_map.values())))):
                    for x, y in solutions_map.items():
                        ans = ans + ("%s = %s\n" % (x, y[i]))
                    ans = ans + "\n"
                return ans.strip()
            else:
                # All terms are matched, but there is no variable in the query.
                # The result should be True, which means the query is correct.
                # This happens for cases like "mother(a, b)."
                return True
        else:
            # Some terms cannot be matched.
            # If there are variables in the query, it means the query has no solution => None.
            # If there is no variable, it means the query is incorrect => False.
            return False if not variables_in_query else None

