###############################################################################
# types.py: Definitions of internal data structures and external API.
#
# (c) Copyright 2019, Carlos Eduardo de Andrade. All Rights Reserved.
#
# This code is released under LICENSE.md.
#
# Created on:  Nov 05, 2019 by ceandrade
# Last update: Nov 08, 2019 by ceandrade
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

from __future__ import annotations
import copy

from brkga_mp_ipr.enums import BiasFunctionType, PathRelinkingType, \
    PathRelinkingSelection

###############################################################################

class BrkgaParams:
    """
    Represents the BRKGA and IPR hyper-parameters.

    Attributes:
        ** BRKGA Hyper-parameters **

        population_size (int): Number of elements in the population [> 0].

        elite_percentage (float): Percentage of individuals to become the
            elite set (0, 1].

        mutants_percentage (float): Percentage of mutants to be inserted in
            the population.

        num_elite_parents (int): Number of elite parents for mating [> 0].

        total_parents (int): Number of total parents for mating [> 0].

        bias_type (BiasFunction): Type of bias that will be used.

        num_independent_populations (int): Number of independent parallel
            populations.

        **Path Relinking parameters**

        pr_number_pairs (int): Number of pairs of chromosomes to be tested
            to path relinking.

        pr_minimum_distance (float): Mininum distance between chromosomes
            selected to path-relinking.

        pr_type (PathRelinkingType): Path relinking type.
        pr_selection (PathRelinkingSelection): Individual selection to
            path-relinking.

        alpha_block_size (float): Defines the block size based on the size of
            the population.

        pr_percentage (float): Percentage / path size to be computed.
            Value in (0, 1].
    """

    def __init__(self):
        """
        Initializes a BrkgaParams object.
        """
        self.population_size = 0
        self.elite_percentage = 0.0
        self.mutants_percentage = 0.0
        self.num_elite_parents = 0
        self.total_parents = 0
        self.bias_type = BiasFunctionType.CONSTANT
        self.num_independent_populations = 0
        self.pr_number_pairs = 0
        self.pr_minimum_distance = 0.0
        self.pr_type = PathRelinkingType.DIRECT
        self.pr_selection = PathRelinkingSelection.BESTSOLUTION
        self.alpha_block_size = 0.0
        self.pr_percentage = 0.0

###############################################################################

class ExternalControlParams:
    """
    Represents additional control parameters that can be used outside this
    framework.

    Attributes:
        exchange_interval (int):  Interval at which elite chromosomes are
            exchanged (0 means no exchange) [> 0].

        num_exchange_indivuduals (int): Number of elite chromosomes exchanged
            from each population [> 0].

        reset_interval (int): Interval at which the populations are reset
            (0 means no reset) [> 0].
    """

    def __init__(self, exchange_interval: int = 0,
                 num_exchange_indivuduals: int = 0,
                 reset_interval: int = 0):
        """
        Initializes a ExternalControlParams object.
        """
        self.exchange_interval = exchange_interval
        self.num_exchange_indivuduals = num_exchange_indivuduals
        self.reset_interval = reset_interval

###############################################################################

class BaseChromosome(list):
    """
    This class represents a chromosome using a vector in the unitary
    hypercube, i.e., :math:`v \\in [0,1]^n` where :math:`n` is the size of the
    array (dimensions of the hypercube).

    Note that this base class is a simple list of float numbers and can be
    used in the algorithm directly. However, in some cases, the user wants
    additional capabilities in the Chromosome class, such as extra data and
    so. For instance, in the example below, the chromosome also keeps the
    makespan and total completion time for a scheduling problem:

    .. code-block:: python

        class SchedulingChromosome(BaseChromosome):
            def __init__(self, value):
                super().__init__(value)
                self.makespan = 0.0
                self.total_completion_time = 0.0

    Note that when subclassing BaseChromosome, we must define the method
    ``__init__(self, value)`` and call the parent (``BaseChromosome``)
    constructor. We need at least one argument to be passed to
    ``BaseChromosome`` constructor.
    """

###############################################################################

class Population():
    """
    Encapsulates a population of chromosomes. Note that this struct is **NOT**
    meant to be used externally of this unit.

    Attributes:
        chromosomes (List[BaseChromosome]): Population of chromosomes.

        fitness (List[Tuple[float, int]]): Fitness of a each chromosome.
            Each pair represents the fitness and the chromosome index.
    """

    def __init__(self, other_population: Population = None):
        """
        Initializes a new population. If ``other_population`` is not ``None``,
        we copy it.

        Args:
            other_population (Population): The population to be copied.
        """

        self.chromosomes = list()
        self.fitness = list()

        if other_population is not None:
            self.chromosomes = copy.deepcopy(other_population.chromosomes)
            self.fitness = copy.deepcopy(other_population.fitness)
