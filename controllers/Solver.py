from collections import defaultdict
from controllers.Parser import Parser
from models import KnowledgeBase, Variable


class Solver:
    def __init__(self, knowledge_base_raw):
        self.knowledge_base = KnowledgeBase(Parser(knowledge_base_raw).parse_rules())

    def solve(self, query_raw):
        query = Parser(query_raw).parse_query()

        map_name_var = {}
        var_exists = False

        # Map all variables to actual variables
        for argument in query.arguments:
            if isinstance(argument, Variable):
                var_exists = True
                map_name_var[argument.name] = argument

        matching_query_terms = [item for item in self.knowledge_base.query(query)]

        if matching_query_terms:
            if map_name_var:
                solutions_map = defaultdict(list)
                for matching_query_term in matching_query_terms:
                    matching_variable_bindings = query.match_variable_bindings(matching_query_term)
                    for variable_name, variable in map_name_var.items():
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
            return False if not var_exists else None

