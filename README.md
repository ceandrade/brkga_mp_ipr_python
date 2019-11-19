<div align="center">
  <img src="https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/docs/src/assets/logo_name_300.png">
</div>

BRKGA-MP-IPR - Python version
================================================================================

[![Build Status](https://travis-ci.org/ceandrade/brkga_mp_ipr_python.svg?branch=master)](https://travis-ci.org/ceandrade/brkga_mp_ipr_python)

[![Coverage Status](https://coveralls.io/repos/ceandrade/brkga_mp_ipr_python/badge.svg?branch=master&service=github)](https://coveralls.io/github/ceandrade/brkga_mp_ipr_python?branch=master)

[![codecov.io](http://codecov.io/github/ceandrade/brkga_mp_ipr_python/coverage.svg?branch=master)](http://codecov.io/github/ceandrade/brkga_mp_ipr_python?branch=master)

BRKGA-MP-IPR provides a _very easy-to-use_ framework for the
Multi-Parent Biased Random-Key Genetic Algorithm with Implict Path Relink
(**BRKGA-MP-IPR**). Assuming that your have a _decoder_ to your problem,
we can setup, run, and extract the value of the best solution in less than
5 commands (obvisiously, you may need few other lines fo code to do a proper
test).

This Python version is very flexible and suitable for prototyping. However,
it is not as fast as the
[C++ version](https://github.com/ceandrade/brkga_mp_ipr_cpp) or the
[Julia version](https://github.com/ceandrade/brkga_mp_ipr_julia).
Moreover, due to Python Interpreter limitations (see
https://wiki.python.org/moin/GlobalInterpreterLock), real multithread is
not possible, defeating the BRKGA's capability of parallel decoding, which
speeds up the optimization by large paces.

If Python is not suitable to you, we may find useful the
[C++ version](https://github.com/ceandrade/brkga_mp_ipr_cpp) or the
[Julia version](https://github.com/ceandrade/brkga_mp_ipr_julia) of this
framework. At this moment, we have no plans to implement the BRKGA-MP-IPR in
other languages such as Java or C#. But if you want to do so, you are must
welcome. But please, keep the API as close as possible to the C++ API (or
Julia API in case you decide go C), and use the best coding and documentation
practices of your chosen language/framework.

If you are not familiar with how BRKGA works, take a look on
[Standard BRKGA](http://dx.doi.org/10.1007/s10732-010-9143-1) and
[Multi-Parent BRKGA](http://dx.doi.org/xxx).
In the future, we will provide a _Prime on BRKGA-MP_
section.

Dependencies
--------------------------------------------------------------------------------

BRKGA-MP-IPR was developed using Python 3.7, especially using the new `enum`
capabilities. The parameters' loading and writing functions may fail on
Python 3.6 or previous versions. However, the main algorithm functions work
fine on Python 3.6, by providing BrkgaParams manually (or implementing your
own parameter loading).

Install
--------------------------------------------------------------------------------

TODO

Short usage (TL;DR)
--------------------------------------------------------------------------------

The best way to keep it short is to look in the
[`examples`](https://github.com/ceandrade/brkga_mp_ipr_python/tree/master/examples/tsp) folder
on [the git repo.](https://github.com/ceandrade/brkga_mp_ipr_python)
Let's take a look into
[`main_minimal.py`](https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/main_minimal.py),
copied (and trimmed) below:

```python
import sys

from brkga_mp_ipr.enums import Sense
from brkga_mp_ipr.types_io import load_configuration
from brkga_mp_ipr.algorithm import BrkgaMpIpr

from tsp_instance import TSPInstance
from tsp_decoder import TSPDecoder

def main() -> None:
    if len(sys.argv) < 4:
        print("Usage: python main_minimal.py <seed> <config-file> "
              "<num-generations> <tsp-instance-file>")
        sys.exit(1)

    seed = int(sys.argv[1])
    configuration_file = sys.argv[2]
    num_generations = int(sys.argv[3])
    instance_file = sys.argv[4]

    instance = TSPInstance(instance_file)

    decoder = TSPDecoder(instance)

    brkga_params, _ = load_configuration(configuration_file)

    brkga = BrkgaMpIpr(
        decoder=decoder,
        sense=Sense.MINIMIZE,
        seed=seed,
        chromosome_size=instance.num_nodes,
        params=brkga_params
    )

    brkga.initialize()

    brkga.evolve(num_generations)

    best_cost = brkga.get_best_fitness()
    print(f"Best cost: {best_cost}")

if __name__ == "__main__":
    main()
```

You can identify the following basic steps:

1. Create a data structure to hold your input data which is passed to the
   decoder function (example
   [`tsp_instance.py`](https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/tsp_instance.py)).
   Note that you may not implement a data/instance class but load all needed
   information directly on your decoder;

2. Create a decoder class. The `decode()` method from this class
   translates a chromosome (array of numbers in the interval [0, 1]) to a
   solution for your problem. The decoder must return the solution value or cost
   to be used as fitness by BRKGA (example
   [`tsp_decoder.py`](https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/tsp_decoder.py)).
   Note that the `decode()` method must have the following signature:

   ```python
   def decode(self, chromosome: BaseChromosome, rewrite: bool) -> float
   ```

   where `BaseChromosome` is a class inhereted from ``list``. In other words,
   you can tread ``chromosome`` as a simple list of floats;

3. Load the instance and other relevant data, and instantiate the decoder;

4. Read the algorithm parameters using ``load_configuration()`` or create
   a BrkgaParams object by hand;

5. Create a ``BrkgaMpIpr`` algorithm object;

6. Call `initialize()` to init the BRKGA state;

7. Call `evolve()` to optimize;

8. Call `get_best_fitness()` and/or `get_best_chromosome()` to
   retrieve the best solution.

[`main_minimal.py`](https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/main_minimal.py)
provides a very minimal example to understand the necessary steps to use the
BRKGA-MP-IPR framework. However,
[`main_complete.py`](https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/main_complete.py)
provides a full-featured code, handy for scientific use, such as
experimentation and paper writing. This code allows fine-grained control of
the optimization, shows several features of BRKGA-MP-IPR such as the resets,
chromosome injection, and others. It also logs
all optimization steps, _creating outputs easy to be parsed._ **You should use
this code for serious business and experimentation.**

Tutorial (complete)
--------------------------------------------------------------------------------

The tutorial is a working-in-progress yet. Meanwhile, the reader can use
the [C++ tutorial](https://ceandrade.github.io/brkga_mp_ipr_cpp) or
the [Julia tutorial](https://ceandrade.github.io/brkga_mp_ipr_julia)
since the APIs are very similar each other.

License and Citing
--------------------------------------------------------------------------------

BRKGA-MP-IPR uses a permissive BSD-like license and it can be used as it
pleases you. And since this framework is also part of an academic effort, we
kindly ask you to remember to cite the originating paper of this work.
Indeed, Clause 4 estipulates that "all publications, softwares, or any other
materials mentioning features or use of this software and/or the data used to
test it must cite explicitly the following article":

> C.E. Andrade. R.F. Toso, J.F. Gonçalves, M.G.C. Resende. The Multi-Parent
> Biased Random-key Genetic Algorithm with Implicit Path Relinking. _European
> Journal of Operational Research_, volume XX, issue X, pages xx-xx, 2019.
> DOI [to be determined](http://dx.doi.org/xxx)

Contributing
--------------------------------------------------------------------------------

[Contribution guidelines for this project](CONTRIBUTING.md)
