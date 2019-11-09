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

from brkga_mp_ipr.enums import *
from brkga_mp_ipr.types import *

###############################################################################

class BrkgaMpIpr:

    def __init__(self, decoder: object, sense: Sense, seed: int,
                 chromosome_size: int, params: BrkgaParams,
                 evolutionary_mechanism_on: bool = True,
                 chrmosome_type: type = BaseChromosome):

        ###################
        # Initial BRKGA Hyper-parameters assignmet.
        ###################

        self.PARAMS = copy.deepcopy(params)
        self.OPT_SENSE = sense
        self.CHROMOSOME_SIZE = chromosome_size
        self.EVOLUTIONARY_MECHANISM_ON = evolutionary_mechanism_on

        if evolutionary_mechanism_on:
            self.ELITE_SIZE = int(params.elite_percentage *
                                  params.population_size)
            self.NUM_MUTANTS = int(params.mutants_percentage *
                                   params.population_size)
        else:
            self.ELITE_SIZE = 1
            self.NUM_MUTANTS = params.population_size - 1

        ###################
        # Error checking
        ###################

        if chromosome_size < 1:
            raise ValueError(f"chromosome size must be larger than "
                             f"zero: {chromosome_size}")
        elif params.population_size < 1:
            raise ValueError(f"population_size size must be larger than "
                             f"zero: {params.population_size}")
        elif self.ELITE_SIZE < 1:
            raise ValueError(f"elite-set size less then one: "
                             f"{self.ELITE_SIZE}")
        elif self.ELITE_SIZE > params.population_size:
            raise ValueError(f"elite-set size ({self.ELITE_SIZE}) greater than "
                             f"population size ({params.population_size})")
        elif self.NUM_MUTANTS < 0:
            raise ValueError(f"mutant-set size less then zero: "
                             f"{self.NUM_MUTANTS}")
        elif self.NUM_MUTANTS > params.population_size:
            raise ValueError(f"mutant-set size ({self.NUM_MUTANTS}) greater "
                             f"than population size ({params.population_size})")
        elif (self.ELITE_SIZE + self.NUM_MUTANTS) > params.population_size:
            raise ValueError(f"elite-set size ({self.ELITE_SIZE}) + "
                             f"mutant-set size ({self.NUM_MUTANTS}) greater "
                             f"than population size ({params.population_size})")
        elif params.num_elite_parents < 1:
            raise ValueError(f"num_elite_parents must be at least 1: "
                             f"{params.num_elite_parents}")
        elif params.total_parents < 2:
            raise ValueError(f"total_parents must be at least 2: "
                             f"{params.total_parents}")
        elif params.num_elite_parents >= params.total_parents:
            raise ValueError(f"num_elite_parents ({params.num_elite_parents}) "
                             f"is greater than or equal to total_parents "
                             f"({params.total_parents})")
        elif params.num_elite_parents > self.ELITE_SIZE:
            raise ValueError(f"num_elite_parents ({params.num_elite_parents}) "
                             f"is greater than elite set ({self.ELITE_SIZE})")
        elif params.num_independent_populations < 1:
            raise ValueError(f"number of parallel populations must be larger "
                             f"than zero: {params.num_independent_populations}")
        # TODO: enable the following when IPR methods be implemented.
        # elif params.alpha_block_size <= 0.0:
        #     raise ValueError(f"alpha_block_size must be larger than zero: "
        #                      f"{params.alpha_block_size}")
        # elif params.pr_percentage <= 0.0 or params.pr_percentage > 1.0:
        #     raise ValueError(f"percentage / path size must be in (0, 1]: "
        #                      f"{params.pr_percentage}")

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

        elif params.bias_type == BiasFunctionType.LINEAR:
            self.set_bias_custom_function(lambda r: 1.0 / r)

        elif params.bias_type == BiasFunctionType.QUADRATIC:
            self.set_bias_custom_function(lambda r: r ** -2.0)

        elif params.bias_type == BiasFunctionType.CUBIC:
            self.set_bias_custom_function(lambda r: r ** -3.0)

        elif params.bias_type == BiasFunctionType.EXPONENTIAL:
            self.set_bias_custom_function(lambda r: math.exp(-r))

        elif params.bias_type == BiasFunctionType.CONSTANT:
            self.set_bias_custom_function(lambda _: 1.0 / params.total_parents)

    ###########################################################################
    # Initialization methods
    ###########################################################################

    def set_initial_population(self, chromosomes: list) -> None:
        raise NotImplementedError

    ###########################################################################

    def set_bias_custom_function(self, bias_function: callable) -> None:
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
            ``ArgumentError``: In case the function is not a non-increasing
                positive function.
        """

        bias_values = [
            x for x in map(bias_function,
                           range(1, self.PARAMS.total_parents + 1))
        ]

        if any(map(lambda x: x < 0.0, bias_values)):
            raise ValueError(f"bias_function must be positive non-increasing")

        for i, value in enumerate(bias_values[1:]):
            if value > bias_values[i]:
                raise ValueError(f"bias_function is not a non-increasing "
                                 "function")

        if bias_function:
            self.PARAMS.bias_type = BiasFunctionType.CUSTOM

        self._bias_function = bias_function
        self._total_bias_weight = sum(bias_values)

    ###########################################################################

    def initialize(self, true_init: bool = True) -> None:
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
    # Core helper methods
    ###########################################################################

    def better_than(self, a1: float, a2: float) -> bool:
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
