###############################################################################
# algorithm.py: Definition of BRKGA-MP-API methods and algorithms.
#
# (c) Copyright 2022, Carlos Eduardo de Andrade. All Rights Reserved.
#
# This code is released under LICENSE.md.
#
# Created on:  Nov 08, 2019 by ceandrade
# Last update: May 18, 2022 by ceandrade
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###############################################################################

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

        def decode(self, chromosome: BaseChromosome, rewrite: bool) -> float:

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

        if chromosome_size < 2:
            raise ValueError(f"Chromosome size must be larger than "
                             f"one, current {chromosome_size}")
        elif params.population_size < 1:
            raise ValueError(f"Population size size must be larger than "
                             f"zero, current {params.population_size}")
        elif self.elite_size < 1:
            raise ValueError(f"Elite set size less then one, current "
                             f"{self.elite_size}")
        elif self.elite_size > params.population_size:
            raise ValueError(f"Elite set size ({self.elite_size}) greater than "
                             f"population size ({params.population_size})")
        elif self.num_mutants < 0:
            raise ValueError(f"Mutant set size less then zero, current "
                             f"{self.num_mutants}")
        elif self.num_mutants > params.population_size:
            raise ValueError(f"Mutant set size ({self.num_mutants}) greater "
                             f"than population size ({params.population_size})")
        elif (self.elite_size + self.num_mutants) > params.population_size:
            raise ValueError(f"Elite set size ({self.elite_size}) + "
                             f"mutant set size ({self.num_mutants}) greater "
                             f"than population size ({params.population_size})")
        elif params.num_elite_parents < 1:
            raise ValueError(f"Number of elite parents must be at least 1, "
                             f"current {params.num_elite_parents}")
        elif params.total_parents < 2:
            raise ValueError(f"Total parents must be at least 2, current "
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
                             f"than zero, current {params.num_independent_populations}")
        # TODO (ceandrade): enable the following when IPR methods be implemented.
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

        self._ChromosomeType = chrmosome_type
        """(type BaseChromosome) This is the class/type for the chromosomes."""

        self._current_populations = []
        """(List[Population]) Current populations."""

        self._previous_populations = []
        """(List[Population]) Previous populations."""

        self._bias_function = None
        """(Callable[[int], float]) The bias function."""

        self._total_bias_weight = 0.0
        """(float) Holds the sum of the results of each raking given a bias
           function. This value is needed to normalization."""

        # self._shuffled_individuals = [0] * params.population_size
        # """Used to shuffled individual/chromosome indices during the mate."""

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

    def initialize(self) -> None:
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

        Raises:
            ``RuntimeError``: If the algorith has been initialized before
                and it is not a ``reset()`` call.

            ``ValueError``: If the bias functions is not set.
        """

        if self._initialized and not self._reset_phase:
            raise RuntimeError("The algorithm is already initialized. "
                               "Please call 'reset()' instead.")

        if self._bias_function is None:
            raise ValueError("The bias function is not defined. "
                             "Call set_bias_custom_function() before call "
                             "initialize().")

        # If we have warmstaters, complete the population if necessary.
        # Note that it is done only in the true initialization.
        pop_start = 0
        if self._current_populations and not self._reset_phase:
            population = self._current_populations[0]
            for _ in range(len(population.chromosomes),
                               self.params.population_size):
                new_chr = self.generate_chromosome(self.chromosome_size)
                population.chromosomes.append(new_chr)

            population.fitness = [
                (0.0, 0) for _ in range(self.params.population_size)
            ]
            pop_start = 1

        elif not self._current_populations:
            self._current_populations = [
                Population()
                for _ in range(self.params.num_independent_populations)
            ]
            self._previous_populations = [
                Population()
                for _ in range(self.params.num_independent_populations)
            ]
        # end if

        # Build the remaining populations and associated data structures.
        for i in range(pop_start, self.params.num_independent_populations):
            # If no reset, allocate memory.
            if not self._reset_phase:
                population = self._current_populations[i]
                for _ in range(self.params.population_size):
                    population.chromosomes.append(
                        self.generate_chromosome(self.chromosome_size)
                    )
                # end for
                population.fitness = [
                    (0.0, 0) for _ in range(self.params.population_size)
                ]
            else:
                for chromosome in self._current_populations[i].chromosomes:
                    self.fill_chromosome(chromosome)
            # end if
        # end for

        # Perform initial decoding. It may take a while.
        # NOTE (ceandrade): This loop can be / should be parallelized since
        # each decoding is independent. Please, take a look at the C++ and
        # Julia versions, where we use OpenMP and Julia threads for that task.
        # In Python, due to restrictions to the Python interpreter, this may
        # not be possible, from a pure Python implementation perspective.
        for population in self._current_populations:
            for i, chromosome in enumerate(population.chromosomes):
                value = self._decoder.decode(chromosome=chromosome,
                                             rewrite=True)
                population.fitness[i] = (value, i)
            population.fitness.sort(reverse=(self.opt_sense == Sense.MAXIMIZE))
        # end for

        # Copy the data to previous populations.
        # **NOTE:** (ceandrade) During reset phase, copying item by item maybe
        # faster than deepcoping (which allocates new memory).
        self._previous_populations = copy.deepcopy(self._current_populations)
        self._initialized = True
        self._reset_phase = False

    ###########################################################################
    # Population manipulation methods
    ###########################################################################

    def exchange_elite(self, num_immigrants: int) -> None:
        """
        :todo: to be implemented.
        """
        raise NotImplementedError

    ###########################################################################

    def reset(self) -> None:
        """
        Resets all populations with brand new keys. All warm-start solutions
        provided by ``set_initial_population()`` are discarded. You may
        use ``inject_chromosome()`` to insert those solutions again.

        Raises:
            ``RuntimeError``: If the algorith has been initialized before.
        """

        if not self._initialized:
            raise RuntimeError("The algorithm hasn't been initialized. "
                               "Call 'initialize()' before 'reset()'")
        self._reset_phase = True
        self.initialize()

    ###########################################################################

    def shake(self, intensity: int, shaking_type: ShakingType,
              population_index: int = math.inf) -> None:
        """
        :todo: to be implemented.
        """
        raise NotImplementedError

    ###########################################################################

    def inject_chromosome(self, chromosome: BaseChromosome,
                          population_index: int, position: int,
                          fitness: float = math.inf) -> None:
        """
        :todo: to be implemented.
        """
        raise NotImplementedError

    ###########################################################################
    # Support methods
    ###########################################################################

    def get_best_fitness(self) -> float:
        """
        Returns the fitness/value of the best individual found so far among
        all populations.

        Raises:
            ``RuntimeError``: If the algorith has been initialized before.
        """

        if not self._initialized:
            raise RuntimeError("The algorithm hasn't been initialized. Call "
                               "'initialize()' before 'get_best_fitness()'")

        best = self._current_populations[0].fitness[0][0]
        for i in range(1, self.params.num_independent_populations):
            if (self._current_populations[i].fitness[0][0] < best) == \
               (self.opt_sense == Sense.MINIMIZE):
                best = self._current_populations[i].fitness[0][0]
        return best

    ###########################################################################

    def get_best_chromosome(self) -> BaseChromosome:
        """
        Returns a deep copy of the best individual found so far among all
        populations.

        Raises:
            ``RuntimeError``: If the algorith has been initialized before.
        """

        if not self._initialized:
            raise RuntimeError("The algorithm hasn't been initialized. Call "
                               "'initialize()' before 'get_best_chromosome()'")

        best_value, idx = self._current_populations[0].fitness[0]
        best_individual = self._current_populations[0].chromosomes[idx]
        for i in range(1, self.params.num_independent_populations):
            value, idx = self._current_populations[i].fitness[0]
            if (value < best_value) == (self.opt_sense == Sense.MINIMIZE):
                best_value = value
                best_individual = self._current_populations[i].chromosomes[idx]

        return copy.deepcopy(best_individual)

    ###########################################################################

    def get_chromosome(self, population_index: int, position: int) \
            -> BaseChromosome:
        """
        Returns a deep copy of the chromosome ranked at ``position``
        in the population ``population_index``.

        Args:
            population_index (positive int): the population from where
                fetch the chromosome.

            position (positive int): position the chromosome position,
                ordered by fitness. The best chromosome is located in
                position 0.

        Raises:
            ``RuntimeError``: If the algorith has been initialized before.

            ``ValueError``: either if ``population_index < 0`` or
                ``population_index >= num_independent_populations``.

            ``ValueError``: either if when ``position < 0`` or
                ``position >= population_size``.
        """

        if not self._initialized:
            raise RuntimeError("The algorithm hasn't been initialized. Call "
                               "'initialize()' before 'get_chromosome()'")

        if population_index < 0 or \
           population_index >= self.params.num_independent_populations:
            raise ValueError(
                f"Population must be in "
                f"[0, {self.params.num_independent_populations - 1}]: "
                f"{population_index}")

        if position < 0 or position >= self.params.population_size:
            raise ValueError(
                f"Chromosome position must be in "
                f"[0, {self.params.population_size - 1}]: "
                f"{position}")

        pop = self._current_populations[population_index]
        return copy.deepcopy(pop.chromosomes[pop.fitness[position][1]])

    ###########################################################################

    def get_current_population(self, population_index: int = 0) -> None:
        """
        Returns a reference for population ``population_index``.

        Warning:
            IT IS NOT ADIVISED TO CHANGE THE POPULATION DIRECTLY, since such
            changes can result in undefined behavior.

        Args:
            population_index (positive int): the index for the population.

        Raises:
            ``RuntimeError``: If the algorith has been initialized before.

            ``ValueError``: either if ``population_index < 0`` or
                ``population_index >= num_independent_populations``.
        """

        if not self._initialized:
            raise RuntimeError("The algorithm hasn't been initialized. "
                               "Call 'initialize()' before "
                               "'get_current_population()'")

        if population_index < 0 or \
           population_index >= self.params.num_independent_populations:
            raise ValueError(
                f"Population must be in "
                f"[0, {self.params.num_independent_populations - 1}]: "
                f"{population_index}")

        return self._current_populations[population_index]

    ###########################################################################
    # Optimization (evolutionary / Path-relink) methods
    ###########################################################################

    def evolve(self, num_generations: int = 1) -> None:
        """
        Evolves all populations for ``generations``.

        Args:
            num_generations (positive int): the number of generations to be
                evolved.

        Raises:
            ``RuntimeError``: If the algorith has been initialized before.

            ``ValueError``: either if ``population_index < 0`` or
                ``population_index >= num_independent_populations``.
        """

        if not self._initialized:
            raise RuntimeError("The algorithm hasn't been initialized. "
                                "Call 'initialize()' before "
                                "'evolve()'")
        if num_generations < 1:
            raise ValueError(f"Number of generations must be large than one. "
                             f"Given {num_generations}")

        for _ in range(num_generations):
            for pop_idx in range(self.params.num_independent_populations):
                self.evolve_population(pop_idx)

    ###########################################################################

    def evolve_population(self, population_index: int) -> None:
        """
        Evolves the population ``population_index`` to the next generation.

        Note:
            Although this method allows us to evolve populations
            independently, and therefore, provide nice flexibility, the
            generation of each population can be unsyched. We must proceed
            with care when using this function instead of ``evolve()``.

        Args:
            population_index (positive int): the index for the population to
                be evolved.

        Raises:
            ``RuntimeError``: If the algorith has been initialized before.

            ``ValueError``: either if ``population_index < 0`` or
                ``population_index >= num_independent_populations``.
        """

        if not self._initialized:
            raise RuntimeError("The algorithm hasn't been initialized. "
                                "Call 'initialize()' before "
                                "'evolve_population()'")

        if population_index < 0 or \
           population_index >= self.params.num_independent_populations:
            raise ValueError(
                f"Population must be in "
                f"[0, {self.params.num_independent_populations - 1}]: "
                f"{population_index}")

        # Make names shorter.
        curr_pop = self._current_populations[population_index]
        next_pop = self._previous_populations[population_index]

        # Which index we start to replace individuals.
        replace_idx = self.params.population_size - self.num_mutants

        # First, we copy the elite chromosomes to the next generation.
        for i in range(self.elite_size):
            next_pop.chromosomes[i][:] = curr_pop.chromosomes[curr_pop.fitness[i][1]][:]
            next_pop.fitness[i] = (curr_pop.fitness[i][0], i)

        # Then, we mate/crossover 'pop_size - elite_size - num_mutants' pairs.
        for chr_idx in range(self.elite_size, replace_idx):
            # First, we shuffled the elite set and non-elite set indices,
            # then we take the elite and non-elite parents. Note that we cannot
            # shuffled both sets together, otherwise we would mix elite
            # and non-elite individuals.
            elite_indices = list(range(self.elite_size))
            self._rng.shuffle(elite_indices)
            non_elite_indices = list(range(self.elite_size, replace_idx))
            self._rng.shuffle(non_elite_indices)
            shuffled_individuals = elite_indices + non_elite_indices

            # Take the elite parents.
            for i in range(self.params.num_elite_parents):
                self._parents_ordered[i] = \
                    curr_pop.fitness[shuffled_individuals[i]]

            # Take the non-elite parents.
            for i in range(self.params.total_parents -
                           self.params.num_elite_parents):
                self._parents_ordered[i + self.params.num_elite_parents] = \
                    curr_pop.fitness[shuffled_individuals[i + self.elite_size]]

            self._parents_ordered.sort(reverse=(self.opt_sense ==
                                                Sense.MAXIMIZE))

            # Performs the mate.
            for allele in range(self.chromosome_size):
                # Roullete method.
                parent = 0
                cumulative_probability = 0.0
                toss = self._rng.random()
                while cumulative_probability < toss:
                    # Start parent from 1 because the bias function.
                    parent += 1
                    cumulative_probability += \
                        self._bias_function(parent) / self._total_bias_weight

                # Decrement parent to the right index.
                parent -= 1
                next_pop.chromosomes[chr_idx][allele] = curr_pop\
                    .chromosomes[self._parents_ordered[parent][1]][allele]
            # end for mate.
        # end for crossover.

        # To finish, we fill up the remaining spots with mutants.
        for chr_idx in range(self.params.population_size - self.num_mutants,
                             self.params.population_size):
            self.fill_chromosome(next_pop.chromosomes[chr_idx])

        # Perform the decoding on the offpring and mutants.
        # NOTE (ceandrade): This loop can be / should be parallelized since
        # each decoding is independent. Please, take a look at the C++ and
        # Julia versions, where we use OpenMP and Julia threads for that task.
        # In Python, due to restrictions to the Python interpreter, this may
        # not be possible, from a pure Python implementation perspective.
        for i in range(self.elite_size, self.params.population_size):
            value = self._decoder.decode(chromosome=next_pop.chromosomes[i],
                                         rewrite=True)
            next_pop.fitness[i] = (value, i)

        next_pop.fitness.sort(reverse=(self.opt_sense == Sense.MAXIMIZE))

        # Swap populations.
        self._previous_populations[population_index], \
        self._current_populations[population_index] = \
            self._current_populations[population_index], \
            self._previous_populations[population_index]

    ###########################################################################

    def path_relink(self, pr_type: PathRelinkingType,
                    pr_selection: PathRelinkingSelection, dist: callable,
                    number_pairs: int, minimum_distance: float,
                    block_size: int = 1, max_time: int = 0,
                    percentage: int = 1.0) -> PathRelinkingResult:
        """
        :todo: to be implemented.
        """
        raise NotImplementedError

    ###########################################################################
    # Helper methods
    ###########################################################################

    def generate_chromosome(self, chromosome_size: int) -> BaseChromosome:
        """
        Generates a new chromosome with the given size. The new chromosome is
        an object of class ``self._ChromosomeType`` (which should be a
        ``BaseChromosome`` derivative), given in the constructor. If the
        chromosome type is not given in the constructor, ``BaseChromosome`` is
        used instead. Please, see the documentation of both the
        ``BaseChromosome`` and the constructor for more details.

        Args:
            chromosome_size (positive int): The size of the chromosome.
        """
        return self._ChromosomeType([
            self._rng.random() for _ in range(chromosome_size)
        ])

    ###########################################################################

    def fill_chromosome(self, chromosome: BaseChromosome) -> None:
        """
        Fills a given chromosome with random keys, using the pre-allocated
        memory.

        Args:
            chromosome (BaseChromosome): The chromosome to be filled.
        """
        for i in range(len(chromosome)):
            chromosome[i] = self._rng.random()

    ###########################################################################
    # Core internal/private path-relink methods
    ###########################################################################

    def _direct_path_relink(
            self, chr1: BaseChromosome, chr2: BaseChromosome, dist: callable,
            best_found: tuple, block_size: int, max_time: int,
            percentage: float) -> None:
        """
        :todo: to be implemented.
        """
        raise NotImplementedError

    ###########################################################################

    def _permutation_based_path_relink(
            self, chr1: BaseChromosome, chr2: BaseChromosome, dist: callable,
            best_found: tuple, block_size: int, max_time: int,
            percentage: float) -> None:
        """
        :todo: to be implemented.
        """
        raise NotImplementedError
