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

# result = base.adda()
# print(f"base.adda() result={result}")

# result = base.adda(b=-3)
# print(f"base.adda(b=-3) result={result}")
# result = base.adda(5, 4.2, -3)
# print(f"base.adda(5,4.2,-3) res={result}")


def subx(x, y, z=0):
    """Subtract number y from number x. Optionally also subract z.
    """
    print(f"«subx» w/args x={x} y={y}", end="")
    print(f" z={z}") if z else print()
    return x - y - z

base.plugin_func(subx, argmap={"x":"a",
       "y":"b", "z":"c"} )
base.add_param("c", 6.5)
# print("base.subx() =", base.subx() )
# print("base.subx(b=99) =", base.subx(b=99) )

lc1 = Premise("Load case 1", parent=base,
            parameters={"a":100})
# result = lc1.adda()
# print(f"lc1.adda() result={result}")

from pflacs import Calc
lc1_sub = Calc("LC1 «subx()»", lc1, funcname="subx")
lc1_sub(); print(lc1_sub._subx)
#print(f"lc1_sub() result={lc1_sub._subx}")

lc1_add = Calc("LC1 «adda()»", lc1, funcname="adda", 
              argmap={"return":"adda_res"})
lc1_add(); print(lc1_add.adda_res)
df = lc1_add.to_dataframe(); print(df)

lc2 = base.add_child( lc1.copy() )
lc2.name = "Load case 2"
lc2.a = 200
lc2_sub = lc2.get_child_by_name("LC1 «subx()»")
lc2_sub.name = "LC2 «subx()»"
lc2_add = lc2.get_child_by_name("LC1 «adda()»")
lc2_add.name = "LC2 «adda()»"


def multk(k:"a", l:"b", m:"c" = 1) -> "mult_res":
    return k * l * m
base.plugin_func(multk)
result = base.multk()
print(f"{base.a} * {base.b} * {base.c} = {result}")

lc3_mul = Calc("LC3 «multk()»", base, funcname="multk")
import numpy as np
lc3_mul.b = np.linspace(0,10,3)
lc3_mul()
lc3_mul.to_dataframe()
# print(f"{lc3_mul.a}*{lc3_mul.b}*{lc3_mul.c}={lc3_mul.mult_res}")

for _n in base:
    if type(_n) == Calc:
        _n()

base.savefile("simple_study.pflacs")

for node in base:
    if type(node) == Calc:
        node.to_hdf5()

