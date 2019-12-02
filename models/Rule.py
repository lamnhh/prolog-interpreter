

# Rules are used to define relationships between facts and other rules.They allow us to make conditional statements
# about our world. Let's say we want to say that all humans are mortal. We can do so using the rule below:
# mortal(X) :- human(X)
class Rule:
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    # Return a readable representation of our rule containing our rule head and tail info.
    def __str__(self):
        return str(self.head) + ' :- ' + str(self.tail)

    # Use the default string representation
    def __repr__(self):
        return str(self)