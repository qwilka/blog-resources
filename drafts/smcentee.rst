:author: Stephen McEntee
:email: stephenmce@gmail.com
:institution: Qwilka Limited
:corresponding:
:bibliography: references

:video: https://youtu.be/LgyBPAWDDU8

---------------------------------------------------
pflacs: Faster load cases and parameter studies
---------------------------------------------------

.. class:: abstract

   The engineering design process has a significant computational component
   involving analysis of
   multiple load cases and parameter studies, with the aim of identifying 
   a combination of design parameters that yields an optimal design solution.
   The design process typically involves large numbers
   of parameters and design load cases that must be considered, 
   and design methodolgies are
   traditionally very manual and iterative. 
   Recent developments in computer technologies are leading to
   a growing trend in towards automation in engineering design.
   This article presents ``pflacs``, an open-source Python package that takes
   advantage of Python's flexible dynamic nature and its introspection tools
   to provide an object-orientated framework for automating computational studies.
   ``pflacs`` combines data and Python functions together in an object-orientated
   fashion, and uses a tree data structure that is reflective of the hierarchical 
   structure of many design projects. The author has a background in the subsea
   oil & gas industry, and has applied  ``pflacs`` to automating the  design
   of subsea pipelines.  Although its origins are in engineering design, ``pflacs`` 
   can be used to manage and automate 



.. class:: keywords

   parameter study, computational, engineering, tree

Introduction
------------

.. TODO Outline engineering design process


``pflacs`` is a pure Python module that facilitates parameter studies. 
``pflacs`` is a simple Python tree.
``pflacs`` provides a means of integrating input data with pure Python functions.
``pflacs`` is a tree data structure that operates in a hierarchical workflow that is
reflective of typical engineering project structure.
What differentiates pflacs is the way it uses Python dynamic programming and introspection.
this is a test :cite:`vntree`


Basic usage
----------------------------------

Taking a very simple example to illustrate basic usage, we start by importing the ``pflacs.Premise`` class.
``Premise`` is the fundemental class in ``pflacs``, it is a sub-class of ``vntree.Node`` :cite:`vntree`, 
and hence ``Premise`` instances are nodes in a tree data structure. The purpose of ``Premise`` is to contain
the study parameters (these are the *premise* of the study), and to group together other tree nodes.

.. code-block:: python

	from pflacs import Premise
	base = Premise("Base case",
	            parameters={"a":10, "b":5} )
	print(f"base.a={base.a} base.b={base.b}")

.. This code outputs: 

:code:`base.a=10 base.b=5`

The :code:`parameters` dictionary items are passed to a 
method :code:`Premise.add_param`
that uses a ``pflacs`` descriptor class called :code:`Parameter` to convert the
parameters into attributes of the :code:`Premise` node instance.
 

We would like to add some functionality to our study, so taking a very simple
function:

.. code-block:: python

	def adda(a, b, c=0):
	    print(f"«adda» w/args a={a} b={b}", end="")
	    print(f" c={c}") if c else print()
	    return a + b + c

and using the method :code:`Premise.plugin_func` to plug-in, or patch, the function ``adda`` 
into our study tree nodes, and invoking ``adda`` on instance :code:`base`:

.. code-block:: python

	base.plugin_func(adda)    
	result = base.adda()
	print(f"base.adda() result={result}")

.. This code outputs: 

:code:`«adda» w/args a=10 b=5`

:code:`base.adda() result=15`

The default values for the function arguments can be over-ridden by explicitly
specifying arguments when invoking the plug-in method:

.. code-block:: python

	result = base.adda(b=-3)
	print(f"base.adda(b=-3) result={result}")
	result = base.adda(5, 4.2, -3)
	print(f"base.adda(5,4.2,-3) res={result}")

.. This code outputs: 

:code:`«adda» w/args a=10 b=-3`

:code:`base.adda(b=-3) result=7`

:code:`«adda» w/args a=5 b=4.2 c=-3`

:code:`base.adda(5,4.2,-3) res=6.199999999999999`

To make things a bit more interesting, we will add more functionality:

.. code-block:: python

	def subx(x, y, z=0):
	    print(f"«subx» w/args x={x} y={y}", end="")
	    print(f" z={z}") if z else print()
	    return x - y - z

Inconveniently, the arguments of function ``subx`` do not correspond with the parameter
names in our study, so we need to supply a mapping to indicate how the node attributes
should be applied to ``subx``. We will also introduce a new 
parameter as instance attribute ``base.c``:

.. code-block:: python

	base.plugin_func(subx, argmap={"x":"a",
	       "y":"b", "z":"c"} )
	base.add_param("c", 6.5)
	print("base.subx() =", base.subx() )
	print("base.subx(b=99) =", base.subx(b=99) )

.. This code outputs: 

:code:`«subx» w/args x=10 y=5 z=6.5`

:code:`base.subx() = -1.5`

:code:`«subx» w/args x=10 y=99 z=6.5`

:code:`base.subx(b=99) = -95.5`


