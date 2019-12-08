

# The database object is an object which contains a list of our declared rules. It's used to query our data for
# items matching a goal. It also contains the helper function used to merge variable bindings.
class KnowledgeBase:
    def __init__(self, rules):
        self.rules = rules

    # Return a generator that iterates over all of the terms matching the given goal.
    def query(self, goal):
        for index, rule in enumerate(self.rules):

            # We obtain the map containing our shared rule head and goal variable bindings, and process the
            # matching results if there are any to process.
            matching_head_var_bindings = rule.head.match_variable_bindings(goal)

            if matching_head_var_bindings is not None:
                matched_head_item = rule.head.substitute_variable_bindings(matching_head_var_bindings)
                matched_tail_item = rule.tail.substitute_variable_bindings(matching_head_var_bindings)

                # Query the database for the substituted tail items matching our rules
                for matching_item in matched_tail_item.query(self):

                    # Fetch the map containing our variable bindings matching the tail of our rule.
                    matching_tail_var_bindings = matched_tail_item.match_variable_bindings(matching_item)

                    # We return a generator yielding head terms with the substituted variable bindings replaced
                    # with the bindings found by querying our tail.
                    yield matched_head_item.substitute_variable_bindings(matching_tail_var_bindings)

    # This function takes two variable binding maps and returns a combined bindings map if there are no conflicts.
    # If any of the bound variables are present in both bindings maps but the terms they are bound to do not match,
    # merge_bindings returns None.
    @staticmethod
    def merge_bindings(first_bindings_map, second_bindings_map):
        if (first_bindings_map is None) or (second_bindings_map is None):
            return None

        merged_bindings = {}

        # Process our first bindings map and add the variable bindings to our merged map
        for variable, value in first_bindings_map.items():
            merged_bindings[variable] = value

        # Process our second bindings map and verify that the bindings contain in this map align with the bindings
        # from our first binding map. If any variable bindings do not align, we return None. Otherwise, we process
        # any matching items and continue iterating through our binding map adding each binding to our merged map.
        for variable, value in second_bindings_map.items():

            if variable in merged_bindings:

                existing_variable_binding = merged_bindings[variable]
                shared_bindings = existing_variable_binding.match_variable_bindings(value)

                # If we have shared bindings, we add them to our existing map
                if shared_bindings is not None:
                    for var, val in shared_bindings.items():
                        merged_bindings[var] = val

                # If the shared bindings don't match, we have a conflict and we return None
                else:
                    return None

            else:
                merged_bindings[variable] = value

        return merged_bindings

    # Return a readable representation of our database containing a list of our rules.
    def __str__(self):
        return ".\n".join(str(rule) for rule in self.rules)

    # Use the default string representation
    def __repr__(self):
        return str(self)
