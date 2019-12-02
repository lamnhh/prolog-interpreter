import re
from models import Conjunction, Variable, Term, Rule
from models.Term import TRUE


REGEX_TOKEN = "[A-Za-z0-9_]+|:\-|[()\.,]"
REGEX_ATOM_NAME = "^[A-Za-z0-9_]+$"
REGEX_VAR = "^[A-Z_][A-Za-z0-9_]*$"
REGEX_COMMENT = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|%[^\r\n]*$)"


class Parser:
    def __init__(self, input_text):
        self.tokens = Parser.get_token_list(input_text)
        self.token_iterator = iter(self.tokens)
        self.current = None
        self.scope = None
        self.finished = False
        self.next()

    @staticmethod
    def remove_comments(input_text):
        regex = re.compile(REGEX_COMMENT, re.MULTILINE | re.DOTALL)

        def remove_comment(match):
            if match.group(2) is not None:
                return ""
            return match.group(1)
        return regex.sub(remove_comment, input_text)

    @staticmethod
    def get_token_list(input_text):
        iterator = re.finditer(REGEX_TOKEN, Parser.remove_comments(input_text))
        return [token.group() for token in iterator]

    def next(self):
        try:
            self.current = next(self.token_iterator)
            self.finished = self.token_iterator.__length_hint__() <= 0
        except StopIteration:
            self.finished = True

    def parse_atom(self):
        name = self.current
        if re.match(REGEX_ATOM_NAME, name) is None:
            raise Exception("Invalid Atom Name: " + str(name))
        self.next()
        return name

    def parse_term(self):
        if self.current == "(":
            self.next()
            argument_list = []
            while self.current != ")":
                argument_list.append(self.parse_term())
                if self.current not in (",", ")"):
                    raise Exception("Expected , or ) in term but got " + str(self.current))
                if self.current == ",":
                    self.next()
            self.next()
            return Conjunction(argument_list)

        functor = self.parse_atom()
        if re.match(REGEX_VAR, functor) is not None:
            if functor == "_":
                return Variable("_")
            var = self.scope.get(functor)
            if var is None:
                self.scope[functor] = Variable(functor)
                var = self.scope[functor]
            return var

        if self.current != "(":
            return Term(functor)

        self.next()

        argument_list = []
        while self.current != ")":
            argument_list.append(self.parse_term())
            if self.current not in (",", ")"):
                raise Exception("Expected , or ) in term but got " + str(self.current))
            if self.current == ",":
                self.next()

        self.next()
        return Term(functor, argument_list)

    def parse_rule(self):
        head = self.parse_term()
        if self.current == ".":
            self.next()
            return Rule(head, TRUE())

        if self.current != ":-":
            raise Exception("Expected :- in rule but got " + str(self.current))

        self.next()
        argument_list = []
        while self.current != ".":
            argument_list.append(self.parse_term())
            if self.current not in (",", "."):
                raise Exception("Expected , or . in rule but got " + str(self.current))
            if self.current == ",":
                self.next()
        self.next()

        tail = argument_list[0] if len(argument_list) == 1 else Conjunction(argument_list)
        return Rule(head, tail)

    def parse_query(self):
        self.scope = {}
        return self.parse_term()

    def parse_rules(self):
        rules = []
        while not self.finished:
            self.scope = {}
            rules.append(self.parse_rule())
        return rules
