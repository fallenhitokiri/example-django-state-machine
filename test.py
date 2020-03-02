import inspect


class Foo:
    def transition(self):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)

        if calframe[1][3] != "caller1":
            raise Exception("nope")

    def caller1(self):
        self.transition()


def caller2(foo):
    foo.transition()


f = Foo()
print("caller1")
f.caller1()
print("caller2")
caller2(f)
