Pyrameters
====

Pyrameters is a package for programmatically interacting with hierarchical parameter inputs for scientific software. It is currently targeted at the [Deal.II PRM format](https://www.dealii.org/developer/doxygen/deal.II/classParameterHandler.html).

## Usage

This package can be installed from the PyPi package manager

    pip install pyrameters

Using it is a matter of importing the `pyrameters` module, and creating a `PRM` object.

```
from pyrameters import PRM

with open('input.prm','r') as input:
    prm = PRM(input.read())

if prm['Dimension'] == 2:
    prm.set('/Model geometry/Hypercube/Length', 100)
else:
    prm.get('/Model geometry/Hypercube/Length', 10)

print(prm)
```

An empty `PRM` object can also be created without providing an input file.

```
from pyrameters import PRM

prm = PRM()

prm['Dimension'] = 3
prm['Output directory'] = 'results'
prm.add_subsection('Postprocess')
prm['Postprocess']['Output frequency'] = 10
prm.set('/Postprocess/Visualization/Format','vtu')

print(prm)
```

Which would output parameters to the terminal in valid `PRM` format:

>set Dimension = 3  
  set Output directory = results
>
>subsection Postprocess  
&nbsp;&nbsp;set Output frequency = 10  
>
>&nbsp;&nbsp;subsection Visuzliation  
&nbsp;&nbsp;&nbsp;&nbsp;set Format = vtu  
&nbsp;&nbsp;end  
end
