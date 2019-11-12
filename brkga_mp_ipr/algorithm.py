"""
algorithm.py: Definition of BRKGA-MP-API methods and algorithms.

(c) Copyright 2019, Carlos Eduardo de Andrade. All Rights Reserved.

This code is released under LICENSE.md.

Created on:  Nov 08, 2019 by ceandrade
Last update: Nov 09, 2019 by ceandrade

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

import copy
import math
from random import Random
from typing import List, Callable

from brkga_mp_ipr.enums import *
from brkga_mp_ipr.types import *

###############################################################################

class BrkgaMpIpr:
    """
    This class represents a Multi-Parent Biased Random-key Genetic Algorithm
    with Implicit Path Relinking (BRKGA-MP-IPR).

    **Main capabilities**

    **Evolutionary process**

    In the BRKGA-MP-IPR, we keep a population of chromosomes divided between
    the elite and the non-elite group. During the mating, multiple parents
    are chosen from the elite group and the non-elite group. They are sorted
    either on no-decreasing order for minimization or non-increasing order to
    maximization problems. Given this order, a bias function is applied to
    the rank of each chromosome, resulting in weight for each one. Using a
    roulette method based on the weights, the chromosomes are combined using
    a biased crossover.

    This code also implements the island model, where multiple populations
    can be evolved in parallel, and migration between individuals between
    the islands are performed using ``exchange_elite()`` method.

    This code requires a `Decoder` object capable to map a chromosome to a
    solution for the specific problem, and return a value to be used as
    fitness to the decoded chromosome. The decoder must have the method

    .. code-block:: python

        def decode(self, chromosome: BaseChromosome, rewrite: bool = False) -> float:

    where ``chromosome`` is an ``BaseChromosome`` object of representing a
    solution and `rewrite` is a boolean indicating that if the decode should
    rewrite the chromosome in case it implements local searches and modifies
    the initial solution decoded from the chromosome.

    Note that ``BaseChromosome`` is a simple list of floats and can be
    manipulated as so. However, wrapping such a list into a new class allows
    the user to customize the chromosome, adding new functionalities as
    needed. Please, see ``BaseChromosome`` for more details.

    Attributes:
        params (BrkgaParams): The BRKGA and IPR hyper-parameters.

        opt_sense (Sense): Indicates whether we are maximizing or minimizing.

        chromosome_size (positive int): Number of genes in the chromosome.

        elite_size (positive int): Number of elite items in the population.

        num_mutants (positive int): Number of mutants introduced at each
            generation into the population.

        evolutionary_mechanism_on (bool): If false, no evolution is performed
            but only chromosome decoding. Very useful to emulate a
            multi-start algorithm.
    """

    def __init__(self, decoder: object, sense: Sense, seed: int,
                 chromosome_size: int, params: BrkgaParams,
                 evolutionary_mechanism_on: bool = True,
                 chrmosome_type: type = BaseChromosome):

        ###################
        # Initial BRKGA Hyper-parameters assignmet.
        ###################

        self.params = copy.deepcopy(params)
        self.opt_sense = sense
        self.chromosome_size = chromosome_size
        self.evolutionary_mechanism_on = evolutionary_mechanism_on

        if evolutionary_mechanism_on:
            self.elite_size = int(params.elite_percentage *
                                  params.population_size)
            self.num_mutants = int(params.mutants_percentage *
                                   params.population_size)
        else:
            self.elite_size = 1
            self.num_mutants = params.population_size - 1

        ###################
        # Error checking
        ###################

        if chromosome_size < 1:
            raise ValueError(f"Chromosome size must be larger than "
                             f"zero: {chromosome_size}")
        elif params.population_size < 1:
            raise ValueError(f"Population size size must be larger than "
                             f"zero: {params.population_size}")
        elif self.elite_size < 1:
            raise ValueError(f"Elite set size less then one: "
                             f"{self.elite_size}")
        elif self.elite_size > params.population_size:
            raise ValueError(f"Elite set size ({self.elite_size}) greater than "
                             f"population size ({params.population_size})")
        elif self.num_mutants < 0:
            raise ValueError(f"Mutant set size less then zero: "
                             f"{self.num_mutants}")
        elif self.num_mutants > params.population_size:
            raise ValueError(f"Mutant set size ({self.num_mutants}) greater "
                             f"than population size ({params.population_size})")
        elif (self.elite_size + self.num_mutants) > params.population_size:
            raise ValueError(f"Elite set size ({self.elite_size}) + "
                             f"mutant set size ({self.num_mutants}) greater "
                             f"than population size ({params.population_size})")
        elif params.num_elite_parents < 1:
            raise ValueError(f"Number of elite parents must be at least 1: "
                             f"{params.num_elite_parents}")
        elif params.total_parents < 2:
            raise ValueError(f"Total parents must be at least 2: "
                             f"{params.total_parents}")
        elif params.num_elite_parents >= params.total_parents:
            raise ValueError(f"Number of elite parents ({params.num_elite_parents}) "
                             f"is greater than or equal to total_parents "
                             f"({params.total_parents})")
        elif params.num_elite_parents > self.elite_size:
            raise ValueError(f"Number of elite parents ({params.num_elite_parents}) "
                             f"is greater than elite set ({self.elite_size})")
        elif params.num_independent_populations < 1:
            raise ValueError(f"Number of parallel populations must be larger "
                             f"than zero: {params.num_independent_populations}")
        # TODO: enable the following when IPR methods be implemented.
        # elif params.alpha_block_size <= 0.0:
        #     raise ValueError(f"Alpha block size must be larger than zero: "
        #                      f"{params.alpha_block_size}")
        # elif params.pr_percentage <= 0.0 or params.pr_percentage > 1.0:
        #     raise ValueError(f"Percentage / path size must be in (0, 1]: "
        #                      f"{params.pr_percentage}")

        elif not hasattr(decoder, "decode"):
            raise TypeError(f"The given decoder ({type(decoder)}) "
                            f"has no 'decode()' method")

        ###################
        # Engines
        ###################

        self._decoder = decoder
        """Problem-dependent Decoder."""

        self._rng = Random(seed)
        """Mersenne twister random number generator."""

        for _ in range(1000):
            self._rng.random()

        ###################
        # Algorithm data
        ###################

        self._ChrmosomeType = chrmosome_type
        """This is the class/type for the chromosomes."""

        self._previous_populations = [
            Population() for _ in range(params.num_independent_populations)
        ]
        """Previous populations."""

        self._current_populations = [
            Population() for _ in range(params.num_independent_populations)
        ]
        """Current populations."""

        self._bias_function = None
        """The bias function."""

        self._total_bias_weight = 0.0
        """Holds the sum of the results of each raking given a bias function.
           This value is needed to normalization."""

        self._shuffled_individuals = [0] * params.population_size
        """Used to shuffled individual/chromosome indices during the mate."""

        self._parents_ordered = [0] * params.total_parents
        """Defines the order of parents during the mating."""

        self._initial_population = False
        """Indicates if a initial population is set."""

        self._initialized = False
        """Indicates if the algorithm was proper initialized."""

        self._reset_phase = False
        """Indicates if the algorithm have been reset."""

        self._pr_start_time = None
        """Holds the start time for a call of the path relink procedure."""

        # Sets the bias function.
        if params.bias_type == BiasFunctionType.LOGINVERSE:
            self.set_bias_custom_function(lambda r: 1.0 / math.log1p(r))
            self.params.bias_type = BiasFunctionType.LOGINVERSE

        elif params.bias_type == BiasFunctionType.LINEAR:
            self.set_bias_custom_function(lambda r: 1.0 / r)
            self.params.bias_type = BiasFunctionType.LINEAR

        elif params.bias_type == BiasFunctionType.QUADRATIC:
            self.set_bias_custom_function(lambda r: r ** -2.0)
            self.params.bias_type = BiasFunctionType.QUADRATIC

        elif params.bias_type == BiasFunctionType.CUBIC:
            self.set_bias_custom_function(lambda r: r ** -3.0)
            self.params.bias_type = BiasFunctionType.CUBIC

        elif params.bias_type == BiasFunctionType.EXPONENTIAL:
            self.set_bias_custom_function(lambda r: math.exp(-r))
            self.params.bias_type = BiasFunctionType.EXPONENTIAL

        elif params.bias_type == BiasFunctionType.CONSTANT:
            self.set_bias_custom_function(lambda _: 1.0 / params.total_parents)
            self.params.bias_type = BiasFunctionType.CONSTANT

    ###########################################################################
    # Initialization methods
    ###########################################################################

    def set_initial_population(self, chromosomes: List[BaseChromosome]) -> None:
        """
        Sets initial individuals into the poulation to work as warm-starters.
        Such individuals can be obtained from solutions of external
        procedures such as fast heuristics, other methaheuristics, or even
        relaxations from a mixed integer programming model that models the
        problem.

        All given solutions are assigned to one population only. Therefore, the
        maximum number of solutions is the size of the populations.

        Args:
            chromosomes (list of BaseChromosome): a set of individuals or
                solutions encoded as BaseChromosomes.

        Raises:
            ``ValueError``: if the number of given chromosomes is larger than
                the population size; if the sizes of the given chromosomes do
                not match with the required chromosome size.
        """

        if len(chromosomes) > self.params.population_size:
            raise ValueError(
                f"Number of given chromosomes ({len(chromosomes)}) is large "
                f"than the population size ({self.params.population_size})"
            )

        self._current_populations = [
            Population() for _ in range(self.params.num_independent_populations)
        ]

        for i, chromosome in enumerate(chromosomes):
            if len(chromosome) != self.chromosome_size:
                raise ValueError(
                    f"Error on setting initial population: chromosome {i} "
                    f"does not have the required dimension (actual size: "
                    f"{len(chromosome)}, required size: {self.chromosome_size})"
                )
            self._current_populations[0].chromosomes\
                .append(BaseChromosome(chromosome))

        self._initial_population = True

    ###########################################################################

    def set_bias_custom_function(self, bias_function: Callable[[int], float]) \
            -> None:
        """
        Sets a new bias function to be used to rank the chromosomes during
        the mating. **It must be a positive non-increasing function** returning
        a ``float``, i.e., :math:`f : \\mathbb{N}^+ \\to \\mathbb{R}^+` such
        that :math:`f(i) \\ge 0`
        and :math:`f(i) \\ge f(i+1)` for :math:`i \\in [1..total\_parents]`.
        For instance, the following sets an inverse quadratic function:

        .. code-block:: python

            brkga = BRKGA_MP_IPR(...)
            brkga.set_bias_custom_function(lambda x : 1.0 / (x * x))

        Args:
            bias_function: A positive non-increasing function.

        Raises:
            ``ValueError``: In case the function is not a non-increasing
                positive function.
        """

        bias_values = [
            x for x in map(bias_function,
                           range(1, self.params.total_parents + 1))
        ]

        if any(map(lambda x: x < 0.0, bias_values)):
            raise ValueError(f"Bias function must be positive non-increasing")

        for i, value in enumerate(bias_values[1:]):
            if value > bias_values[i]:
                raise ValueError(f"Bias function is not a non-increasing "
                                 "function")

        self.params.bias_type = BiasFunctionType.CUSTOM
        self._bias_function = bias_function
        self._total_bias_weight = sum(bias_values)

    ###########################################################################

    def initialize(self, true_init: bool = True) -> None:
        """
        Initializes the populations and others data structures of the BRKGA.
        If an initial population is supplied, this method completes the
        remaining individuals, if they do not exist.

        Warning:
            THIS METHOD MUST BE CALLED BEFORE ANY OPTIMIZATION METHODS.

        This method also performs the initial decoding of the chromosomes.
        Therefore, depending on the decoder implementation, this can take a
        while, and the user may want to time such procedure in his/her
        experiments.
        """

        raise NotImplementedError

    ###########################################################################
    # Population manipulation methods
    ###########################################################################

    def exchange_elite(self, num_immigrants: int) -> None:
        raise NotImplementedError

    ###########################################################################

    def reset(self) -> None:
        raise NotImplementedError

    ###########################################################################

    def shake(self, intensity: int, shaking_type: ShakingType,
              population_index: int = math.inf) -> None:
        raise NotImplementedError

    ###########################################################################

    def inject_chromosome(self, chromosome: BaseChromosome,
                          population_index: int, position: int,
                          fitness: float = math.inf) -> None:
        raise NotImplementedError

    ###########################################################################
    # Support methods
    ###########################################################################

    # TODO: fix return annotation to population.
    def get_current_population(self, population_index: int = 0) -> None:
        raise NotImplementedError

    ###########################################################################

    def get_best_chromosome(self) -> BaseChromosome:
        raise NotImplementedError

    ###########################################################################

    def get_best_fitness(self) -> float:
        raise NotImplementedError

    ###########################################################################

    def get_chromosome(self, population_index: int, position: int) \
            -> BaseChromosome:
        raise NotImplementedError

    ###########################################################################
    # Optimization (evolutionary / Path-relink) methods
    ###########################################################################

    def evolve(self, generations: int = 1) -> None:
        raise NotImplementedError

    ###########################################################################

    def path_relink(self, pr_type: PathRelinkingType,
                    pr_selection: PathRelinkingSelection, dist: callable,
                    number_pairs: int, minimum_distance: float,
                    block_size: int = 1, max_time: int = 0,
                    percentage: int = 1.0) -> PathRelinkingResult:
        raise NotImplementedError

    ###########################################################################
    # Core internal/private evolutionary methods
    ###########################################################################

    # TODO: fix the argments' type
    # def _evolution(curr: Population, next:Population) -> None
    def _evolution(self, curr, next) -> None:
        raise NotImplementedError

    ###########################################################################
    # Core internal/private path-relink methods
    ###########################################################################

    def _direct_path_relink(
            self, chr1: BaseChromosome, chr2: BaseChromosome, dist: callable,
            best_found: tuple, block_size: int, max_time: int,
            percentage: float) -> None:
        raise NotImplementedError

    ###########################################################################

    def _permutation_based_path_relink(
            self, chr1: BaseChromosome, chr2: BaseChromosome, dist: callable,
            best_found: tuple, block_size: int, max_time: int,
            percentage: float) -> None:
        raise NotImplementedError
