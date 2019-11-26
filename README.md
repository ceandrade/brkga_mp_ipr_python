<div align="center">
  <img src="https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/src_docs/src/assets/logo_name_300.png">
</div>

BRKGA-MP-IPR - Python version
================================================================================

<table>
<tr>
  <td>Build Status</td>
  <td>
    <a href="https://travis-ci.org/ceandrade/brkga_mp_ipr_python">
    <img src="https://travis-ci.org/ceandrade/brkga_mp_ipr_python.svg?branch=master" alt="Build Status" />
    </a>
  </td>
</tr>
<tr>
  <td>Coverage Status</td>
  <td>
    <a href="https://coveralls.io/github/ceandrade/brkga_mp_ipr_python?branch=master">
    <img src='https://coveralls.io/repos/github/ceandrade/brkga_mp_ipr_python/badge.svg?branch=master' alt='Coverage Status' /></a>
  </td>
</tr>
<tr>
  <td>codecov.io</td>
  <td>
    <a href="http://codecov.io/github/ceandrade/brkga_mp_ipr_python?branch=master">
    <img src="http://codecov.io/github/ceandrade/brkga_mp_ipr_python/coverage.svg?branch=master" alt="codecov.io" />
    </a>
  </td>
</tr>
<tr>
  <td>Documentation</td>
  <td>
    <a href="https://ceandrade.github.io/brkga_mp_ipr_python">
    <img src="https://img.shields.io/badge/Tutorial-API-blue.svg" alt="Documentation" />
    </a>
  </td>
</tr>
<tr>
  <td>License</td>
  <td>
    <a href="https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/LICENSE.md">
    <img src="https://img.shields.io/badge/license-BSD--like-blue" alt="License" />
    </a>
  </td>
</tr>
</table>

BRKGA-MP-IPR provides a _very easy-to-use_ framework for the
Multi-Parent Biased Random-Key Genetic Algorithm with Implict Path Relink
(**BRKGA-MP-IPR**). Assuming that your have a _decoder_ to your problem,
we can setup, run, and extract the value of the best solution in less than
5 commands (obvisiously, you may need few other lines fo code to do a proper
test).

This Python version is very flexible and suitable for prototyping. However,
it is not as fast as the
[**C++ version**](https://github.com/ceandrade/brkga_mp_ipr_cpp) or the
[**Julia version**](https://github.com/ceandrade/brkga_mp_ipr_julia).
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

- [**C++ version**](https://github.com/ceandrade/brkga_mp_ipr_cpp)
- [**Julia version**](https://github.com/ceandrade/brkga_mp_ipr_julia)

If you are not familiar with how BRKGA works, take a look on
[Standard BRKGA](http://dx.doi.org/10.1007/s10732-010-9143-1) and
[Multi-Parent BRKGA](http://dx.doi.org/xxx).
In the future, we will provide a _Prime on BRKGA-MP_
section.

:computer: Installation and tests
--------------------------------------------------------------------------------

BRKGA-MP-IPR was developed using >= Python 3.7.2, especially using the new
`enum` capabilities. The parameters' loading and writing functions may fail
on Python 3.6 or previous versions. However, the main algorithm functions
work fine on Python 3.6, by providing BrkgaParams manually (or implementing
your own parameter loading).

Assuming you have the correct Python version, the installation is pretty
straightforward using Pypi:

```
$ pip3.7 search brkga
brkga-mp-ipr (0.9)  - The Multi-Parent Biased Random-Key Genetic Algorithm with Implict Path Relink

$ pip3.7 install brkga-mp-ipr
Collecting brkga-mp-ipr
...
Installing collected packages: brkga-mp-ipr
Successfully installed brkga-mp-ipr-0.9

$ python3.7
Python 3.7.5 (default, Oct 19 2019, 01:20:12)
Type "help", "copyright", "credits" or "license" for more information.
>>> from brkga_mp_ipr.types_io import load_configuration
>>> from brkga_mp_ipr.algorithm import BrkgaMpIpr
>>> BrkgaMpIpr
<class 'brkga_mp_ipr.algorithm.BrkgaMpIpr'>
>>> load_configuration
<function load_configuration at 0x10620e320>
>>> help(load_configuration)
Help on function load_configuration in module brkga_mp_ipr.types_io:

load_configuration(configuration_file: str) -> (<class 'brkga_mp_ipr.types.BrkgaParams'>, <class 'brkga_mp_ipr.types.ExternalControlParams'>)
    Loads the parameters from `configuration_file` returning them as a tuple.

    Args:
        configuration_file (str): plain text file containing the configuration.

    Returns:
        A tuple containing a `BrkgaParams` and a `ExternalControlParams` object.

    Raises:
        IsADirectoryError: If `configuration_file` is a folder.

        FileNotFoundError: If `configuration_file` does not exist.

        LoadError: In cases of missing data or bad-formatted data.
```

BRKGA-MP-IPR also provides a thorough unit testing that aims to harden and make
the code ready for production environments.
You can use builtin
[unittest](https://docs.python.org/3.7/library/unittest.html),
or yet [pytest](https://www.pytest.org)
or [Tox](https://tox.readthedocs.io).

> :information_source: **NOTE:**
    The tests take about 10 minutes, mainly because the permutation path relink.

> :warning: **Warning**:
    It is a hard test to test algorithms that use random signals. In
    BRKGA-MP-IPR, the tests are carefully designed to ensure repeatability. For
    that, we use the Mersenne Twister
    [[1]](https://en.wikipedia.org/wiki/Mersenne_Twister)
    [[2]](http://dx.doi.org/10.1145/272991.272995) as our standard random
    generator number engine, particularly the [version that comes with
    Python 3.7](https://docs.python.org/3.7/library/random.html).
    However, it may happen that such engine has slightly different
    implementations across platforms and, therefore, the tests may fail. The
    current version was tested on 64-bit platforms (Mac OS X, GNU/Linux, and
    Windows 10).

:zap: Usage - TL;DR
--------------------------------------------------------------------------------

The best way to keep it short is to look in the
[`examples`](https://github.com/ceandrade/brkga_mp_ipr_python/tree/master/examples/tsp) folder
on [the git repo.](https://github.com/ceandrade/brkga_mp_ipr_python)
Let's take a look into
[`main_minimal.py`](https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/main_minimal.py),
which solves the
[Traveling Salesman Problem (TSP)](https://en.wikipedia.org/wiki/Travelling_salesman_problem).
This is a trimmed copy:

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

:books: Tutorial and full documentation
--------------------------------------------------------------------------------

Check out the complete tutorial and API documentation:
https://ceandrade.github.io/brkga_mp_ipr_python

:black_nib: License and Citing
--------------------------------------------------------------------------------

BRKGA-MP-IPR uses a permissive BSD-like license and it can be used as it
pleases you. And since this framework is also part of an academic effort, we
kindly ask you to remember to cite the originating paper of this work.
Indeed, Clause 4 estipulates that "all publications, softwares, or any other
materials mentioning features or use of this software (as a whole package or
any parts of it) and/or the data used to test it must cite the following
article explicitly:":

> C.E. Andrade. R.F. Toso, J.F. Gonçalves, M.G.C. Resende. The Multi-Parent
> Biased Random-key Genetic Algorithm with Implicit Path Relinking. _European
> Jornal of Operational Research_, To appear, 2019.
> DOI https://doi.org/10.1016/j.ejor.2019.11.037

[Check it out the full license.](https://github.com/ceandrade/brkga_mp_ipr_julia/blob/master/LICENSE.md)

:construction_worker: TODO
--------------------------------------------------------------------------------

Coding side:

- Implement the remaining population manipulation methods and tests
  (short term);

- Implement the path relinking methods and tests (long term).

CI and tests side:

- Configure Travis-Ci correctly, such that we can run tests on Mac OSX and
  Windows too.

Documentation side:

- Create a comprehensive tutorial as we did for C++ and Julia versions.

:pencil2: Contributing
--------------------------------------------------------------------------------

[Contribution guidelines for this project](CONTRIBUTING.md)

