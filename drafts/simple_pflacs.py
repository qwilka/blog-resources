from pflacs import Premise
base = Premise("Base case",
            parameters={"a":10,"b":5})
#print(f"base.a={base.a} base.b={base.b}")


def adda(a, b, c=0):
    """Add number b to number a. Optionally also add c.
    """
    print(f"«adda» w/args a={a} b={b}", end="")
    print(f" c={c}") if c else print()
    return a + b + c

base.plugin_func(adda)    

result = base.adda()
print(f"base.adda() result={result}")

result = base.adda(b=-3)
print(f"base.adda(b=-3) result={result}")
result = base.adda(5, 4.2, -3)
print(f"base.adda(5,4.2,-3) res={result}")


def subx(x, y, z=0):
    """Subtract number y from number x. Optionally also subract z.
    """
    print(f"«subx» w/args x={x} y={y}", end="")
    print(f" z={z}") if z else print()
    return x - y - z

base.plugin_func(subx, argmap={"x":"a",
       "y":"b", "z":"c"} )
base.add_param("c", 6.5)
print("base.subx() =", base.subx() )
print("base.subx(b=99) =", base.subx(b=99) )
