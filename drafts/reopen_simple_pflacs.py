from pflacs import Premise, Calc


def adda(a, b, c=0):
    """Add number b to number a. Optionally also add c.
    """
    print(f"«adda» w/args a={a} b={b}", end="")
    print(f" c={c}") if c else print()
    return a + b + c


def subx(x, y, z=0):
    """Subtract number y from number x. Optionally also subract z.
    """
    print(f"«subx» w/args x={x} y={y}", end="")
    print(f" z={z}") if z else print()
    return x - y - z


def multk(k:"a", l:"b", m:"c" = 1) -> "mult_res":
    return k * l * m

root = Premise.openfile("simple_study.pflacs")

print(root.to_texttree())
