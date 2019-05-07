class Parent(object):
    def override(self):
        print("Parent override()")
    def implicit(self):
        print("Parent implicit()")
    def altered(self):
        print("Parent altered()")

class Child(Parent):
    def override(self):
        print("Child override()")
    def altered(self):
        print("Child, before parent altered()")
        super(Child, self).altered()
        print("Child, after Parent altered()")

dad = Parent()
son = Child()
dad.implicit()
son.implicit()
dad.override()
son.override()
dad.altered()
son.altered()

class Other():
    def override(self):
        print("Other override()")
    def implicit(self):
        print("Other implicit()")
    def altered(self):
        print("Other altered()")

class Child():
    def __init__(self):
        self.other = Other()
    def implicit(self):
        self.other.implicit()
    def override(self):
        print("Child override()")
    def altered(self):
        print("Child, before other altered()")
        self.other.altered()
        print("Child, after other altered()")

son = Child()
son.implicit()
son.override()
son.altered()