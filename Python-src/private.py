


class PrivateAttr:
    def __init__(self):
        #print("PrivateAttr.__init__")  
        pass
    def __get__(self, instance, owner):
        #print("GET PrivateAttr.__get__")
        #print(instance, owner, owner.__name__)
        # value = getattr(instance, self.name, None)
        print("GET accessed by:", owner.__name__)
        if owner.__name__ in self.classname:
            value = instance.__dict__[self.name]
            return value
        else:
            raise TypeError("Cannot get PRIVATE attribute «%s»" % self.name)

    def __set__(self, instance, value):
        #print("SET PrivateAttr.__set__")
        #print(instance, value, instance.__class__.__name__)
        #setattr(instance, self.name, value)
        #object.__setattr__(instance, self.name, value)
        # if instance.__class__.__name__ == self.classname:
        #     instance.__dict__[self.name] = value
        # else:
        #     #raise TypeError("Cannot set PRIVATE attribute «%s»" % self.name)
        #     pass
        instance.__dict__[self.name] = value
        if instance.__class__.__name__ != self.classname:
            self.classname.append(instance.__class__.__name__)
    def __delete__(self, instance):
        #print("PrivateAttr.__delete__")
        #print(instance)
        pass
    def __set_name__(self, owner, name):
        #print("PrivateAttr.__set_name__")
        #print(owner, name)
        self.name = name
        self.classname = [owner.__name__]


class MyBase:
    private1 = PrivateAttr()
    private2 = PrivateAttr()
    def __init__(self):
        self.public = "«this is a public attribute»"
        self.private1 = "«MyBase PRIVATE attribute 1»"
        self.private2 = "«MyBase PRIVATE attribute 2»"


class MySub(MyBase):
    def __init__(self, value):
        super().__init__() 
        self.private2 = value



if __name__=="__main__":
    b = MyBase()
    c = MySub(10)
