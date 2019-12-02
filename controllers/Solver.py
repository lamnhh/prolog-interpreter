from collections import defaultdict
from controllers.Parser import Parser
from models import KnowledgeBase, Variable


class Solver:
    # Parse the rules text and initialize the database we plan to use to query our rules.
    def __init__ (self, knowledge_base):
        self.rules = Parser(knowledge_base).parse_rules()
        self.database = KnowledgeBase(self.rules)

    # Parse the query text and use our database rules to search for matching query solutions.
    def solve(self, query_text):

        query = Parser(query_text).parse_query()

        query_variable_map = {}
        variables_in_query = False

        # Find any variables within the query and return a map containing the variable name to actual
        # Prolog variable mapping we can later use to query our database.
        for argument in query.arguments:
            if isinstance(argument, Variable):
                variables_in_query = True
                query_variable_map[argument.name] = argument

        # Return a generator which iterates over the terms matching our query
        matching_query_terms = [item for item in self.database.query(query)]

        if matching_query_terms:
            if query_variable_map:

                # If our query has variables and we have matching query terms/items, we iterate over the query items
                # and our list of query variables and construct a map containing the matching variable names
                # and their values
                solutions_map = defaultdict(list)
                for matching_query_term in matching_query_terms:
                    matching_variable_bindings = query.match_variable_bindings(matching_query_term)

                    # Iterate over the query variables and bind them to the matched database bindings
                    for variable_name, variable in query_variable_map.items():
                        solutions_map[variable_name].append(matching_variable_bindings.get(variable))

                ans = ""
                for i in range(len(next(iter(solutions_map.values())))):
                    for x, y in solutions_map.items():
                        ans = ans + ("%s = %s\n" % (x, y[i]))
                    ans = ans + "\n"
                return ans.strip()

            else:
                # If we have matching query items / terms but no variables in our query, we simply return true
                # to indicate that our query did match our goal. Otherwise, we return None
                return True if not variables_in_query else None
        else:
            # If we have no variables in our query, it means our goal had no matches, so we return False.
            # Otherwise we simply return None to show no variable bindings were found.
            return False if not variables_in_query else None

