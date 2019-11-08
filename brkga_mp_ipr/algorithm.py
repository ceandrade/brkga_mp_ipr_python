"""
algorithm.py: Definition of BRKGA-MP-API methods and algorithms.

(c) Copyright 2019, Carlos Eduardo de Andrade. All Rights Reserved.

This code is released under LICENSE.md.

Created on:  Nov 08, 2019 by ceandrade
Last update: Nov 08, 2019 by ceandrade

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

import math

from brkga_mp_ipr.enums import *
from brkga_mp_ipr.types import *

###############################################################################

class BRKGA_MP_IPR:

    def __init__(self):
        pass

    ###########################################################################
    # Initialization methods
    ###########################################################################

    def set_initial_population(self, chromosomes: list) -> None:
        raise NotImplementedError

    ###########################################################################

    def set_bias_custom_function(self, func: callable) -> None:
        raise NotImplementedError

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
            number_pairs: int, minimum_distance: float, block_size: int = 1,
            max_time: int = 0, percentage: int = 1.0) -> PathRelinkingResult:
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

    def _direct_path_relink(self, chr1: BaseChromosome, chr2: BaseChromosome,
                            dist: callable, best_found: tuple, block_size: int,
                            max_time: int, percentage: float) -> None:
        raise NotImplementedError

    ###########################################################################

    def _permutation_based_path_relink(self, chr1: BaseChromosome,
            chr2: BaseChromosome, dist: callable, best_found: tuple,
            block_size: int, max_time: int, percentage: float) -> None:
        raise NotImplementedError
