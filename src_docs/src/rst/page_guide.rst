.. index:: pair: page; Guide / Tutorial
.. _doxid-guide:

Guide / Tutorial
===============================================================================

.. _doxid-guide_1guide_installation:

Installation and tests
-------------------------------------------------------------------------------

BRKGA-MP-IPR was developed using >= Python 3.7.2, especially using the new
``enum`` capabilities. The parameters' loading and writing functions may fail
on Python 3.6 or previous versions. However, the main algorithm functions
work fine on Python 3.6, by providing BrkgaParams manually (or implementing
your own parameter loading).

Assuming you have the correct Python version, the installation is pretty
straightforward using Pypi:

.. code-block:: bash

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

BRKGA-MP-IPR also provides a thorough unit testing that aims to harden and make
the code ready for production environments.
You can use builtin
`unittest <https://docs.python.org/3.7/library/unittest.html>`_,
or yet `pytest <https://www.pytest.org>`_
or `Tox <https://tox.readthedocs.io>`_.

.. note::
    The tests take about 10 minutes, mainly because the permutation path relink.

.. warning::
    It is a hard test to test algorithms that use random signals. In
    BRKGA-MP-IPR, the tests are carefully designed to ensure repeatability. For
    that, we use the Mersenne Twister
    `[1] <https://en.wikipedia.org/wiki/Mersenne_Twister>`_
    `[2] <http://dx.doi.org/10.1145/272991.272995>`_ as our standard random
    generator number engine, particularly the `version that comes with
    Python 3.7 <https://docs.python.org/3.7/library/random.html>`_.
    However, it may happen that such engine has slightly different
    implementations across platforms and, therefore, the tests may fail. The
    current version was tested on 64-bit platforms (Mac OS X, GNU/Linux, and
    Windows 10).


.. _doxid-guide_1guide_tldr:

TL;DR
-------------------------------------------------------------------------------

The best way to keep it short is to look in the on examples on `the git repo.
<https://github.com/ceandrade/brkga_mp_ipr_python/tree/master/examples>`_
Let's take a look into
`main_minimal.cpp <https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/main_minimal.py>`_,
which solves the
`Traveling Salesman Problem (TSP) <https://en.wikipedia.org/wiki/Travelling_salesman_problem>`_.
This is a trimmed copy:

.. code-block:: python

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

You can identify the following basic steps:

#. Create a data structure to hold your input data which is passed to the
   decoder function (example
   `tsp_instance.py <https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/tsp_instance.py>`_).
   Note that you may not implement a data/instance class but load all needed
   information directly on your decoder;

#. Create a decoder class. The ``decode()`` method from this class
   translates a chromosome (array of numbers in the interval [0, 1]) to a
   solution for your problem. The decoder must return the solution value or cost
   to be used as fitness by BRKGA (example
   `tsp_decoder.py <https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/tsp_decoder.py>`_).
   Note that the ``decode()`` method must have the following signature:

   .. code-block:: python

        def decode(self, chromosome: BaseChromosome, rewrite: bool) -> float

   where ``BaseChromosome`` is a class inhereted from ``list``. In other words,
   you can tread ``chromosome`` as a simple list of floats;

#. Load the instance and other relevant data, and instantiate the decoder;

#. Read the algorithm parameters using ``load_configuration()`` or create
   a BrkgaParams object by hand;

#. Create a ``BrkgaMpIpr`` algorithm object;

#. Call ``initialize()`` to init the BRKGA state;

#. Call ``evolve()`` to optimize;

#. Call ``get_best_fitness()`` and/or ``get_best_chromosome()`` to
   retrieve the best solution.

`main_minimal.py <https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/main_minimal.py>`_
provides a very minimal example to understand the necessary steps to use the
BRKGA-MP-IPR framework. However,
`main_complete.py <https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/main_complete.py>`_
provides a full-featured code, handy for scientific use, such as
experimentation and paper writing. This code allows fine-grained control of
the optimization, shows several features of BRKGA-MP-IPR such as the resets,
chromosome injection, and others. It also logs
all optimization steps, *creating outputs easy to be parsed.* **You should use
this code for serious business and experimentation.**


.. _doxid-guide_1guide_getting_started:

Getting started
-------------------------------------------------------------------------------

BRKGA-MP-IPR is pretty simple, and you must provide one required **decoder**
object to translate chromosomes to solutions.
In general, such decoder uses the problem information to map a vector of real
numbers in the interval [0,1] to a (valid) solution. In some cases, even
though a valid solution cannot be found, library users apply penalization
factors and push the BRKGA to find valid solutions.

Before you go further, please take a look at the ``examples`` folder in `the
git repo <https://github.com/ceandrade/brkga_mp_ipr_python>`_.
In this guide, we solve the classical `Traveling Salesman Problem
<https://en.wikipedia.org/wiki/Travelling_salesman_problem>`_. Given a set of
cities and the distances between them (full weighted undirect graph), one
must find a minimum-cost tour among all cities, such that each city is
visited only once (i.e., find a Hamiltonian cycle of minimum cost). The
folder has the following structure:

- `tsp_instance.py <https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/tsp_instance.py>`_:
  contains the input data structures and helper functions;

- `tsp_decoder.py <https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/tsp_decoder.py>`_:
  contains the decoder function for TSP;

- `greedy_tour.py <https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/greedy_tour.py>`_:
  simple heuristic that computes a greedy tour;

- `config.conf <https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/config.conf>`_:
  example of parameter settings;

- `main_minimal.py <https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/main_minimal.py>`_:
  minimal code useful to understand and test the framework.
  **You should start here!** Please take a look on this file before continue
  this tutorial;

- `main_complete.py <https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/main_complete.py>`_:
  full-featured code, handy for scientific use, such as
  experimentation and paper writing. This code allows fine-grained control of
  the optimization, shows several features of BRKGA-MP-IPR such as the
  path-relinking calls, resets, chromosome injection, and others. It also logs
  all optimization steps, _creating outputs easy to be parsed._
  **You should use this code for serious business and experimentation;**

- `instances <https://github.com/ceandrade/brkga_mp_ipr_python/tree/master/examples/tsp/instances>`_:
  folder containing some TSP instances for testing.

When you call
`main_minimal.py <https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/main_minimal.py>`_
or
`main_complete.py <https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/main_complete.py>`_:
without arguments, they show the usage. For example, assuming you are using
a terminal:

.. code-block:: bash

    $ python3.7 main_minimal.py
    Usage: python main_minimal.py <seed> <config-file> <num-generations> <tsp-instance-file>

    $ python3.7 main_complete.py
    Usage:
      main_complete.py -c <config_file> -s <seed> -r <stop_rule> -a <stop_arg> -t <max_time> -i <instance_file> [--no_evolution]

.. note::
    `main_complete.py <https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/main_complete.py>`_
    uses the `DocOpt package <https://github.com/docopt/docopt>`_.
    Please, install it before run this script.

So, this is a possible output whe calling ``main_minimal`` :

.. code-block:: bash

    $ python3.7 main_minimal.py 27000001 config.conf 100 instances/brazil58.dat
    Reading data...
    Reading parameters...
    Building BRKGA data and initializing...
    Evolving 100 generations...
    Best cost: 89375.0

For ``main_complete``, the output is more verbose, since we want to capture
as much information as possible to do some statistical analysis. The output
should be something close to this:

.. code-block:: bash

    $ python3.7 main_complete.py -c config.conf -s 2700001 -r Generations -a 100 -t 60 -i instances/brazil58.dat
    ------------------------------------------------------
    > Experiment started at 2019-11-21 18:37:03.023320
    > Instance: instances/brazil58.dat
    > Configuration: config.conf
    > Algorithm Parameters:
    >  -population_size 2000
    >  -elite_percentage 0.3
    >  -mutants_percentage 0.15
    >  -num_elite_parents 2
    >  -total_parents 3
    >  -bias_type LOGINVERSE
    >  -num_independent_populations 3
    >  -pr_number_pairs 0
    >  -pr_minimum_distance 0.15
    >  -pr_type PERMUTATION
    >  -pr_selection BESTSOLUTION
    >  -alpha_block_size 1.0
    >  -pr_percentage 1.0
    >  -exchange_interval 200
    >  -num_exchange_indivuduals 2
    >  -reset_interval 600
    > Seed: 2700001
    > Stop rule: GENERATIONS
    > Stop argument: 100
    > Maximum time (s): 60.0
    ------------------------------------------------------

    [2019-11-21 18:37:03.023403] Reading TSP data...
    Number of nodes: 58

    [2019-11-21 18:37:03.024271] Generating initial tour...
    Initial cost: 30774.0

    [2019-11-21 18:37:03.025056] Building BRKGA data...
    New population size: 580

    [2019-11-21 18:37:03.025311] Initializing BRKGA data...

    [2019-11-21 18:37:03.193528] Warming up...

    [2019-11-21 18:37:04.117741] Evolving...
    * Iteration | Cost | CurrentTime
    * 1 | 30774 | 0.40
    * 74 | 30759 | 30.15
    * 78 | 30721 | 31.77
    * 79 | 30371 | 32.18
    * 81 | 30350 | 32.99
    [2019-11-21 18:37:44.924912] End of optimization

    Total number of iterations: 100
    Last update iteration: 81
    Total optimization time: 40.81
    Last update time: 32.99
    Large number of iterations between improvements: 73

    % Best tour cost: 30350.00
    % Best tour: 41 0 29 12 39 24 8 31 19 52 49 3 17 43 23 57 4 26 42 11 56 22 53 54 1 40 34 9 51 50 46 48 2 47 28 35 16 25 18 5 27 32 13 36 33 45 55 44 14 20 38 10 15 21 7 37 30 6

    Instance,Seed,NumNodes,TotalIterations,TotalTime,LargeOffset,LastUpdateIteration,LastUpdateTime,Cost
    brazil58.dat,2700001,58,100,40.81,73,81,32.99,30350

I hope by now you got your system set up and running. Let's see the essential
details on how to use the BRKGA-MP-IPR.

.. _doxid-guide_1guide_decoder:

First things first: the decoder function
-------------------------------------------------------------------------------

The core of the BRKGA algorithm is the definition of a decoder
function/object. The decoder maps the chromosomes (vectors of real numbers in
the interval [0, 1]) to solutions of the problem. In some sense, a decoder is
similar to a `kernel function from Support Vector Machines
<https://en.wikipedia.org/wiki/Kernel_method>`_ : both functions are used to
project solutions/distances in different spaces.

Here, we have a small difference between the Python/C++ and the Julia
implementations. In the Julia version, you must define a data container
inherit from `AbstractInstance
<https://ceandrade.github.io/brkga_mp_ipr_julia/guide/index.html#First-things-first:-basic-data-structures-and-decoder-function-1>`_,
and a decoder function. The reason you must do that is because structs in
Julia have no methods (but constructors), and the decoder function must take
both chromosome and input data in the call. In Python/C++, we can encapsulate the
input data into the decoder object, resulting in a much more clear API.

The basic form of a decoder should be:

.. code-block:: python

    class Decoder():
        def __init__(self):
            pass

        def decode(self, chromosome: BaseChromosome, rewrite: bool) -> float:
            return 0.0

The decoder **must** contain a **decode()** method that receives a
``BaseChromosome`` reference and an ``boolean``, and returns a float point
number. But before going further, let's talk about the chromosome.


The chromosome or vector of doubles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Note that all long the BRKGA discussion, the chromosome is represented as a
vector of real numbers in the interval [0,1]. Indeed, we could use
straightforward ``list``. However, sometimes is interesting to
keep more information inside the chromosome for further analysis, such as,
other solution metrics that not the main fitness value. For example, in a
scheduling problem, we may choose to keep both makespan and total completion
time metrics. Therefore, we chose to make the chromosome a "generic" data
structure in our design.

File `types.py <https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/brkga_mp_ipr/types.py>`_ shows the
basic represetation of a chromosome:

.. code-block:: python

    class BaseChromosome(list):
        pass


Therefore, the ``BaseChromosome`` is a simple list, and can be tread as so in
your decoder. If this enough for you, you go already and use such a
definition. However, instead to redefine in your own code, **we do recommend
to import and use the definition from** `types.py
<https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/brkga_mp_ipr/types.py>`_
since it is the same definition the main BRKGA-MP-IPR algorithm uses.

However, if you need more information to be tracked during the optimization,
you can redefine the chromosome. First, your definition must complain with
the ``list`` interface. The easiest way to do that is to inherit
from the ``BaseChromosome``. For instance, assume we want to keep track of the
makespan and the total completion time for a scheduling problem. We can do
the following:

.. code-block:: python

    class SchedulingChromosome(BaseChromosome):
        def __init__(self, value):
            super().__init__(value)
            self.makespan = 0.0
            self.total_completion_time = 0.0

Note that when subclassing BaseChromosome, we must define the method
``__init__(self, value)`` and call the parent (``BaseChromosome``)
constructor. We need at least one argument to be passed to ``BaseChromosome``
constructor. Note that the new custom chromosome type must be pass to the
main algorithm constructor (``BrkgaMpIpr.__init__``). Internally,
``BrkgaMpIpr`` builds new chromosomes using
``CustomChromosomeType(<list>)``, where ``<list>`` is a list of floats in the
interval [0, 1].

Back to the decoder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Again, the decoder is the heart of a BRKGA. An easy way to keep the API clean
is to define a decoder that has a reference for the input data. This is a TSP
decoder defined on file `examples/tsp/tsp_decoder.py
<https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/tsp_decoder.py>`_:

.. code-block:: python

    class TSPDecoder():
        def __init__(self, instance: TSPInstance):
            self.instance = instance

        def decode(self, chromosome: BaseChromosome, rewrite: bool) -> float:
            permutation = sorted(
                (key, index) for index, key in enumerate(chromosome)
            )
            cost = self.instance.distance(permutation[0][1], permutation[-1][1])
            for i in range(len(permutation) - 1):
                cost += self.instance.distance(permutation[i][1],
                                               permutation[i + 1][1])
            return cost

Note that ``TSPDecoder`` get a reference to ``TSPInstance`` (from
`examples/tsp/tsp_instance.py
<https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/tsp_instance.py>`_),
that holds the input data. Therefore, ``TSPDecoder`` has direct access to the
data for optimization. This approach also benefits cache efficiency, mainly
when multiple threads are used for decoding, i.e., several threads can use
the same read-only data already in the cache, which speeds up the
optimization.

The decode method also has a ``rewrite`` argument that indicates if the decoder
should rewrite the chromosome, in case of local search / local improvements be
performed during the decoder process. This flag is critical if you intend to
use the Implicit Path Relink (not implemented in Python version yet).
Even though you do not rewrite the chromosome in your decoder, you must provide
such signature for API compatibility.

The decoder must return a ``float`` that is used as the **fitness** to rank
the chromosomes. In general, fitness is the cost/value of the solution, but you
may want to use it to penalize solutions that violate the problem constraints,
for example.

In our TSP example, we have a very simple decoder that generates a permutation
of nodes, and compute the cost of the cycle from that permutation
(note that we don't use the flag ``rewrite`` in that example).

With the instance data and the decoder ready, we can build the BRKGA data
structures and perform the optimization.


.. _doxid-guide_1guide_brkga_object:

Building BRKGA-MP-IPR algorithm object
-------------------------------------------------------------------------------

`BrkgaMpIpr` is the main object that
implements all BRKGA-MP-IPR algorithms such as evolution, path relink, and
other auxiliary procedures.

The first step is to call the algorithm constructor that has the following
signature:

.. code-block:: python

    def __init__(self, decoder: object, sense: Sense, seed: int,
                 chromosome_size: int, params: BrkgaParams,
                 evolutionary_mechanism_on: bool = True,
                 chrmosome_type: type = BaseChromosome)


The first argument is the decoder object that must implement the ``decode()``
method as discussed before. You also must indicate whether you are minimizing
or maximizing through parameter ``BRKGA::Sense``.

A good seed also must be provided for the (pseudo) random number generator
(according to `this paper <http://doi.acm.org/10.1145/1276927.1276928>`_).
BrkgaMpIpr uses the Mersenne Twister engine
`[1] <http://dx.doi.org/10.1145/272991.272995>`_
`[2] <https://en.wikipedia.org/wiki/Mersenne_Twister>`_
from the standard Python library
`[3] <https://docs.python.org/3.7/library/random.html>`_

The ``chromosome_size`` also must be given. It indicates the length of each
chromosome in the population. In general, this size depends on the instance
and how the decoder works. The constructor also takes a ``BrkgaParams``
object that holds several parameters. We will take about that later.

Another common argument is ``evolutionary_mechanism_on`` which is enabled by
default. When disabled, no evolution is performed. The algorithm only decodes
the chromosomes and ranks them. On each generation, all population is replaced
excluding the best chromosome. This flag helps on implementations of simple
multi-start algorithms.

Finally, when using custom chromosomes, the user must provide the its
class/type. As explained before, internally, ``BrkgaMpIpr`` builds new
chromosomes using ``CustomChromosomeType(<list>)``, where ``<list>`` is a
list of floats in the interval [0, 1].

All BRKGA and Path Relink hyper-parameters are stored in a ``BrkgaParams``
object. Such objects can be read and write from plain text files or can be
created by hand by the user. There is also a companion
``ExternalControlParams`` object that stores extra control parameters that
can be used outside the ``BrkgaMpIpr`` to control several aspects of the
optimization. For instance, interval to apply path relink, reset the
population, perform population migration, among others. This is how a
configuration file looks like (see `config.conf
<https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/config.conf>`_
for a commented version):

.. code-block::

    population_size 2000
    elite_percentage 0.30
    mutants_percentage 0.15
    num_elite_parents 2
    total_parents 3
    bias_type LOGINVERSE
    num_independent_populations 3
    pr_number_pairs 0
    pr_minimum_distance 0.15
    pr_type PERMUTATION
    pr_selection BESTSOLUTION
    alpha_block_size 1.0
    pr_percentage 1.0
    exchange_interval 200
    num_exchange_indivuduals 2
    reset_interval 600

To read this file, you can use the function ``load_configuration()``, which
returns a tuple ``(BrkgaParams, ExternalControlParams)``. When reading such
file, the function ignores all blank lines, and lines starting with ``#``. As
commented before, ``BrkgaParams`` contains all hyper-parameters regarding
BRKGA and IPR methods and ``ExternalControlParams`` contains extra control
parameters, and although their presence is required on the config file, they
are not mandatory to the BRKGA-MP-IPR itself.

Let's take a look in the example from `main_minimal.py <https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/main_minimal.py>`_:

.. code-block:: python

    seed = int(sys.argv[1])
    configuration_file = sys.argv[2]
    num_generations = int(sys.argv[3])
    instance_file = sys.argv[4]

    instance = TSPInstance(instance_file)

    brkga_params, _ = load_configuration(configuration_file)

    decoder = TSPDecoder(instance)

    brkga = BrkgaMpIpr(
        decoder=decoder,
        sense=Sense.MINIMIZE,
        seed=seed,
        chromosome_size=instance.num_nodes,
        params=brkga_params
    )

This code gets some arguments from the command line and loads a TSP instance.
After that, it reads the BRKGA parameters from the configuration file. Since in
this example, we only care about the BRKGA parameters, we ignore the control
parameters. We then build the decoder object, and the BRKGA
algorithm. Since we are looking for cycles of minimum cost, we ask for the
algorithm ``MINIMIZE``. The starting seed is also given. Since ``TSPDecode``
considers each chromosome key as a node/city, the length of the chromosome must
be the number of nodes, i.e., ``instance.num_nodes``. Finally, we also pass the
BRKGA parameters.

Now, we have a ``BrkgaMpIpr`` which will be used to call all other functions
during the optimization. Note that we can build several ``BrkgaMpIpr``
objects using different parameters, decoders, or instance data. These
structures can be evolved in parallel and mixed-and-matched at your will.
Each one holds a self-contained BRKGA state including populations, fitness
information, and a state of the random number generator.


.. _doxid-guide_1guide_algo_init:

Initialization and Warm-start solutions
-------------------------------------------------------------------------------

Before starting the optimization, we need to initialize the ``BrkgaMpIpr``
algorithm state using ``BrkgaMpIpr.initialize()`` method. This procedure
initializes the populations and others data structures of the BRKGA. If an
initial population (warm start) is supplied, the initialization method
completes the remaining individuals, if they do not exist. This method also
performs the initial decoding of the chromosomes. Therefore, depending on the
decoder implementation, this can take a while, and you may want to time such
procedure. Assuming that ``brkga`` is our ``BrkgaMpIpr`` object, the syntax
is pretty straightforward:

.. code-block:: python

    brkga.initialize()

.. warning::
  ``initialize()`` must be called before any optimization methods.

Warm-start solutions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One good strategy is to bootstrap the main optimization algorithm with good
solutions from fast heuristics
[`1 <http://dx.doi.org/10.1002/net.21685>`_,
`2 <http://dx.doi.org/10.1016/j.ejor.2017.10.045>`_,
`3 <http://dx.doi.org/10.1016/j.ejor.2017.10.045>`_]
or even from relaxations of integer linear programming models
`[4] <http://dx.doi.org/10.1162/EVCO_a_00138>`_.

To do it, you must set these initial solutions before call ``initialize()``.
Since BrkgaMpIpr does not know the problem structure, you must *encode* the
warm-start solution as chromosomes (vectors in the interval [0, 1]). In other
words, you must do the inverse process that your decoder does. For instance,
this is a piece of code from `main_complete.py
<https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/main_complete.py>`_
showing this process:

.. code-block:: python

    initial_cost, initial_tour = greedy_tour(instance)
    ...

    random.seed(seed)
    keys = sorted([random.random() for _ in range(instance.num_nodes)])

    initial_chromosome = [0] * instance.num_nodes
    for i in range(instance.num_nodes):
        initial_chromosome[initial_tour[i]] = keys[i]

    brkga.set_initial_population([initial_chromosome])

Here, we create one incumbent solution using the greedy heuristic
``greedy_tour()`` `found here
<https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/greedy_tour.py>`_.
It gives us the ``initial_cost`` of the tour represented by the sequence of
nodes ``initial_tour``. In the next lines, we encode ``initial_tour``. First,
we create a vector of sorted random ``keys`` using a local random number
generator. For that, we create the vector ``keys``, and fill up ``keys`` with
random numbers in the interval [0,1]. Once we have the keys, we sort them as
``TSPDecoder.decode()`` does. We then create the ``initial_chromosome``, and
fill it up with ``keys`` according to the nodes' order in ``initial_tour``.
Finally, we call `` BrkgaMpIpr.set_initial_population()`` to assign the
incumbent to the initial population. Note that we enclose the initial
solution inside a vector of chromosomes, since ``set_initial_population()``
may take more than one starting solution. See its signature:

.. code-block:: python

    def set_initial_population(self, chromosomes: List[BaseChromosome]) -> None

Indeed, you can have as much warm-start solutions as you like, limited to the
size of the population. Just remember:

.. warning::
  ``set_initial_population()`` must be called **BEFORE** ``initialize()``.


.. _doxid-guide_1guide_opt:

Optimization time: evolving the population
-------------------------------------------------------------------------------

Once all data is set up, it is time to evolve the population and perform other
operations like path-relinking, shaking, migration, and others. The call is
pretty simple:

.. code-block:: python

    brkga.evolve(num_generations);

``BrkgaMpIpr.evolve()``
evolves all populations for ``num_generations``. If ``num_genertions`` is
omitted, ``evolve()`` evolves only one generation.

For example, in `main_minimal.py
<https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/main_mininal.py>`_,
we just evolve the population for a given number of generations directly and
then extract the best solution cost.

.. code-block:: python

    brkga.evolve(num_generations);
    best_cost = brkga.get_best_fitness()

On `main_complete.py
<https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/main_complete.py>`_
we have fine-grained control on the optimization. There, we have a main loop
that evolves the population one generation at a time and performs several
operations as to hold the best solution, to check whether it is time for path
relink, population reset, among others. The advantage of that code is that we
can track all optimization details, and I do recommend similar style for
experimentation.

.. _doxid-guide_1guide_access_solutions:

Accessing solutions/chromosomes
-------------------------------------------------------------------------------

``BrkgaMpIpr`` offers several mechanisms to access a variaty of data during
the optimization. Most common, we want to access the best chromosome after some
iterations. You can use the companion functions:

.. code-block:: python

    def get_best_fitness(self) -> float

    def get_best_chromosome(self) -> BaseChromosome

``get_best_fitness()``
returns the value/fitness of the best chromosome across all populations.

``get_best_chromosome()`` returns a *deep copy* of the best chromosome across
all populations. You may want to extract an actual solution from such
chromosome, i.e., to apply a decoding function that returns the actual
solution instead only its value.

You may also want to get a reference of specific chromosome for a given
population using ``BrkgaMpIpr.get_chromosome()``.

.. code-block:: python

    def get_chromosome(self, population_index: int, position: int) -> BaseChromosome

For example, you can get the 3rd best chromosome from the 2nd population using

.. code-block:: python

    third_best = brkga.get_chromosome(1, 2)

.. note::
  Just remember that Python is zero-indexed. So, the first population index is 0
  (zero), the second population index is 1 (one), and so forth. The same happens
  for the chromosomes.

Now, suppose you get such chromosome or chromosomes and apply a quick local
search procedure on them. It may be useful to reinsert such new solutions in
the BRKGA population for the next
evolutionary cycles. You can do that using
``BrkgaMpIpr.inject_chromosome()``:

.. code-block:: python

    def inject_chromosome(self, chromosome: BaseChromosome,
                          population_index: int, position: int,
                          fitness: float = math.inf) -> None

Note that the chromosome is put in a specific position of a given population.
If you do not provide the fitness, ``inject_chromosome()`` will decode the
injected chromosome. For example, assuming the ``brkga`` is your
BRKGA-MP-IPR object and ``brkga_params`` is your ``BrkgaParams`` object, the
following code injects the random chromosome ``keys`` into the population #1 in
the last position (``population_size``), i.e., it will replace the worst
solution by a random one:

.. code-block:: python

    random.seed(seed)
    keys = sorted([random.random() for _ in range(instance.num_nodes)])
    brkga.inject_chromosome(keys, 0, brkga_params.population_size)


.. _doxid-guide_1guide_ipr:

Implicit Path Relink
-------------------------------------------------------------------------------

.. note::
    The Implicit Path Relink is not implemented in the Python version yet.


.. _doxid-guide_1guide_shaking_reset:

Shaking and Resetting
-------------------------------------------------------------------------------

Sometimes, BRKGA gets stuck, converging to local maxima/minima, for several
iterations. When such a situation happens, it is a good idea to perturb the
population, or even restart from a new one completely new. BrkgaMpIpr offers
``shake()`` method, an improved variation of the original version
proposed in [this paper](http://dx.doi.org/10.1016/j.eswa.2019.03.007).

.. note::
    Shaking is not implemented in the Python version yet.

Sometimes, even shaking the populations does not help to escape from local
maxima/minima. So, we need a drastic measure, restarting from scratch the role
population. This can be easily accomplished with
``BrkgaMpIpr.reset()``:

.. code-block:: python

    brkga.reset()

.. note::
  When using ``reset()``, all warm-start solutions provided by
  ``set_initial_population()`` are discarded. You may use
  ``inject_chromosome()`` to insert those solutions again.

.. _doxid-guide_1guide_migration:

Multi-population and migration
-------------------------------------------------------------------------------

Multi-population or *island model* was introduced in genetic algorithms in
`this paper
<http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.36.7225>`_. The idea
is to evolve parallel and independent populations and, once a while, exchange
individuals among these populations. In several scenarios, this approach is
very beneficial for optimization.

BRKGA-MP-IPR is implemented using such island idea from the core. If you read
the guide until here, you may notice that several methods take into account
multiple populations. To use multiple populations, you must set
``BrkgaParams.num_independent_populations`` with 2 ou more populations, and
build the BRKGA algorithm from such parameters.

.. note:
    The immigration process is not implemented in the Python version at this
    time.

.. _doxid-guide_1guide_standard_brkga:

Simulating the standard BRKGA
-------------------------------------------------------------------------------

Sometimes, it is a good idea to test how the standard BRKGA algorithm performs
for a problem. You can use BrkgaMpIpr framework to quickly implement and test
a standard BRKGA.

First, you must guarantee that, during the crossover, the algorithm chooses
only one elite individual and only one non-elite individual. This is easily
accomplished setting ``num_elite_parents = 1`` and ``total_parents = 2``. Then,
you must set up a bias function that ranks the elite and no-elite individual
according to the original BRKGA bias parameter :math:`\rho` (rho).

You can use ``BrkgaMpIpr.set_bias_custom_function()``
for that task. The given function receives the index of the chromosome and
returns a ranking for it. Such ranking is used in the roulette method to choose
the individual from which each allele comes to build the new chromosome. Since
we have one two individuals for crossover in the standard BRKGA, the bias
function must return the probability to one or other individual. In the
following code, we do that with a simple ``if...else`` lambda function.

.. code-block:: python

    # Create brkga_params by hand or reading from a file,
    # then set the following by hand.
    brkga_params.num_elite_parents = 1
    brkga_params.total_parents = 2

    rho = 0.75;
    brkga.set_bias_custom_function(lambda x: rho if x == 1 else 1.0 - rho)
    brkga.initialize()

Here, we first set the ``num_elite_parents = 1`` and ``total_parents = 2`` as
explained before. Following, we set a variable ``rho = 0.75``. This is the
:math:`\rho` from standard BRKGA, and you may set it as you wish. Then, we set
the bias function as a very simple lambda function:

.. code-block:: python

    lambda x: rho if x == 1 else 1.0 - rho

So, if the index of the chromosome is 1 (elite individual), it gets a 0.75
rank/probability. If the index is 2 (non-elite individual), the chromosome gets
0.25 rank/probability.

.. note::
  All these operations must be done before calling ``initialize()``.

.. warning::
    Note that we consider the index 1 as the elite individual instead index
    0, and index 2 to the non-elite individual opposed to index 1. The reason
    for this is that, internally, BRKGA always pass ``r > 0`` to the bias
    function to avoid division-by-zero exceptions.


.. _doxid-guide_1guide_parameters:

Reading and writing parameters
-------------------------------------------------------------------------------

Although we can build the BRKGA algorithm data by set up a ``BrkgaParams``
object manually, the easiest way to do so is to read such parameters from a
configuration file. For this, we can use ``read_configuration()`` that reads
a simple plain text file and returns a tuple of ``BrkgaParams`` and
``ExternalControlParams`` objects. For instance,

.. code-block:: python

    brkga_params, control_params = read_configuration ("tuned_conf.txt")

The configuration file must be plain text such that contains pairs of
parameter name and value. This file must list all fields from ``BrkgaParams``
``ExternalControlParams``, even though you do not use each one at this
moment. In `examples folder
<https://github.com/ceandrade/brkga_mp_ipr_python/tree/master/examples/tsp>`_,
we have `config.conf
<https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/config.conf>`_
that looks like this:

.. code-block:: python

    population_size 2000
    elite_percentage 0.30
    mutants_percentage 0.15
    num_elite_parents 2
    total_parents 3
    bias_type LOGINVERSE
    num_independent_populations 3
    pr_number_pairs 0
    pr_minimum_distance 0.15
    pr_type PERMUTATION
    pr_selection BESTSOLUTION
    alpha_block_size 1.0
    pr_percentage 1.0
    exchange_interval 200
    num_exchange_indivuduals 2
    reset_interval 600

It does not matter whether we use lower or upper cases. Blank lines and lines
starting with ``#`` are ignored. The order of the parameters should not matter
either. And, finally, this file should be readble for both C++, Julia,
and Python framework versions.

In some cases, you define some of the parameters at the running time, and you
may want to save them for debug or posterior use. To do so, you can use
``write_configuration()``call upon a ``BrkgaParams`` and
``ExternalControlParams`` objects.

.. code-block:: python

    write_configuration("test.conf", brkga_params, control_params)
    # or
    write_configuration("test.conf", brkga_params, ExternalControlParams())

In the last line, default values are used for ``ExternalControlParams``.

.. note::
  ``write_configuration()`` rewrites the given file. So, watch out to not lose
  previous configurations.


.. _doxid-guide_1guide_tips:

(Probable Valuable) Tips
-------------------------------------------------------------------------------

Algorithm warmup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While in Julia framework version is primordial to do a dry-run to precompile
all functions, in C++ and Python this warmup is not necessary. However,
Python compiles all scripts not previously compiled, and this can take some
time. Therefore, it is a good idea to warm up your code. Another advantage is
the memory location effects of our data (principle of locality), that can be
brought closer to the processor (L2/L3 caches) during the running.
Obliviously, this depends on how you implement and use your data structures.

In `main_complete.py <https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/examples/tsp/main_complete.py>`_,
we have the following piece of code to warmup mainly the decoder and other
functions. Note that we just deep-copy ``brkga``, and then, we may lose
the principle of locality.

.. code-block:: python

    bogus_alg = deepcopy(brkga)
    bogus_alg.evolve(2)
    # TODO (ceandrade): warm up path relink functions.
    # bogus_alg.path_relink(brkga_params.pr_type, brkga_params.pr_selection,
    #              (x, y) -> 1.0, (x, y) -> true, 0, 0.5, 1, 10.0, 1.0)
    bogus_alg.get_best_fitness()
    bogus_alg.get_best_chromosome()
    bogus_alg = None

Complex decoders and timing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some problems require complex decoders while for others, the decoder contains
local search procedures, that can be time-consuming. In general, the decoding
is the most time-expensive component of a BRKGA algorithm, and it may skew some
stopping criteria based on running time. Therefore, if your decoder is
time-consuming, it is a good idea to implement a timer or chronometer kind of
thing inside the decoder.

Testing for stopping time uses several CPU cycles, and you need to be careful
when/where to test it, otherwise, you spend all the optimization time doing
system calls to the clock.

IMHO, the most effective way to do it is to test time at the very end of the
decoding. If the current time is larger than the maximum time allowed, simple
return ``Inf`` or ``-Inf`` according to your optimization direction. In this
way, we make the solution **invalid** since it violates the maximum time
allowed. The BRKGA framework takes care of the rest.

Multi-threading
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

BRKGA multi-threading decoding is not implemented in Python at this time.
