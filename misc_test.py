class Proxy:

    def __init__(self, referent: object):
        self.referent = referent
        self.__repr__ = self.referent.__repr__

    def __getattr__(self, name):
        if name not in self.__dict__:
            if name in self.referent.__dict__:
                referent = self.referent
                self.__dict__.update(referent.__dict__)
                self.__class__ = referent.__class__
                # self.__getattribute__ = referent.__getattribute__
                return getattr(self.referent, name)
        return super().__getattribute__(name)


class Test:

    def __init__(self):
        self.x = 1
        self.y = 2


item = Test()
item2 = Proxy(item)

# print(item)
print(item2)
# print(type(item))
print(type(item2))
print(item2.x)
# print(type(item))
print(type(item2))
assert type(item2) is Test  # This confuses the poor type checker
print(item2.y)
print(type(item2) is Test)
print(isinstance(item2, Test))
