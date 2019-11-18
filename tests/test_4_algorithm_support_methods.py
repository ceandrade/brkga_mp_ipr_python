"""
test_algorithm_support_methods.py: Tests the support methods.

(c) Copyright 2019, Carlos Eduardo de Andrade. All Rights Reserved.

This code is released under LICENSE.md.

Created on:  Nov 08, 2019 by ceandrade
Last update: Nov 18, 2019 by ceandrade

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

from copy import deepcopy
import math
from random import Random
import unittest

from brkga_mp_ipr.algorithm import BrkgaMpIpr
from brkga_mp_ipr.enums import *
from brkga_mp_ipr.types import BaseChromosome, BrkgaParams
from brkga_mp_ipr.types_io import load_configuration

from tests.instance import Instance
from tests.decoders import SumDecode, RankDecode
from tests.paths_constants import *

class Test(unittest.TestCase):
    """
    Test units for types.
    """

    ###########################################################################

    def setUp(self):
        """
        Sets up some configurations.
        """

        Test.maxDiff = None

        self.chromosome_size = 100

        self.default_brkga_params = BrkgaParams()
        self.default_brkga_params.population_size = 10
        self.default_brkga_params.elite_percentage = 0.3
        self.default_brkga_params.mutants_percentage = 0.1
        self.default_brkga_params.num_elite_parents = 1
        self.default_brkga_params.total_parents = 2
        self.default_brkga_params.bias_type = BiasFunctionType.LOGINVERSE
        self.default_brkga_params.num_independent_populations = 3
        self.default_brkga_params.pr_number_pairs = 0
        self.default_brkga_params.pr_minimum_distance = 0.0
        self.default_brkga_params.pr_type = PathRelinkingType.DIRECT
        self.default_brkga_params.pr_selection = PathRelinkingSelection.BESTSOLUTION
        self.default_brkga_params.alpha_block_size = 1.0
        self.default_brkga_params.pr_percentage = 1.0

        self.instance = Instance(self.chromosome_size)
        self.sum_decoder = SumDecode(self.instance)
        self.rank_decoder = RankDecode(self.instance)

        self.default_param_values = {
            "decoder": self.sum_decoder,
            "sense": Sense.MAXIMIZE,
            "seed": 98747382473209,
            "chromosome_size": self.chromosome_size,
            "params": self.default_brkga_params,
            "evolutionary_mechanism_on": True,
            "chrmosome_type": BaseChromosome
        }

    ###########################################################################

    def test_get_best_fitness(self):
        """
        Tests get_best_fitness() method.
        """

        param_values = deepcopy(self.default_param_values)
        param_values["sense"] = Sense.MAXIMIZE
        param_values["seed"] = 12323
        param_values["chromosome_size"] = self.chromosome_size
        param_values["params"].population_size = 500
        param_values["params"].num_independent_populations = 3

        params = param_values["params"]
        brkga = BrkgaMpIpr(**param_values)

        # Not initialized
        with self.assertRaises(RuntimeError) as context:
            brkga.get_best_fitness()
        self.assertEqual(str(context.exception).strip(),
                         "The algorithm hasn't been initialized. "
                         "Call 'initialize()' before 'get_best_fitness()'")

        brkga.initialize()

        ########################
        # Test for maximization
        ########################

        local_rng = Random(param_values["seed"])
        for _ in range(1000):
            local_rng.random()

        num_individuals = params.population_size * \
                          params.num_independent_populations

        best_value = -math.inf
        for _ in range(num_individuals):
            local_chr = BaseChromosome([
                local_rng.random() for _ in range(param_values["chromosome_size"])
            ])
            best_value = max(
                best_value, self.sum_decoder.decode(local_chr, True)
            )

        # Assert the both generators are in the same state.
        self.assertEqual(brkga._rng.getstate(), local_rng.getstate())

        # Test the actual value.
        self.assertAlmostEqual(brkga.get_best_fitness(), best_value)

        ########################
        # Test for minimization
        ########################

        param_values["sense"] = Sense.MINIMIZE
        brkga = BrkgaMpIpr(**param_values)
        brkga.initialize()

        local_rng = Random(param_values["seed"])
        for _ in range(1000):
            local_rng.random()

        num_individuals = params.population_size * \
                          params.num_independent_populations

        best_value = math.inf
        for _ in range(num_individuals):
            local_chr = BaseChromosome([
                local_rng.random() for _ in range(param_values["chromosome_size"])
            ])
            best_value = min(
                best_value, self.sum_decoder.decode(local_chr, True)
            )

        # Assert the both generators are in the same state.
        self.assertEqual(brkga._rng.getstate(), local_rng.getstate())

        # Test the actual value.
        self.assertAlmostEqual(brkga.get_best_fitness(), best_value)

    ###########################################################################

    def test_get_best_chromosome(self):
        """
        Tests get_best_chromosome() method.
        """

        param_values = deepcopy(self.default_param_values)
        param_values["sense"] = Sense.MAXIMIZE
        param_values["seed"] = 12323
        param_values["chromosome_size"] = self.chromosome_size
        param_values["params"].population_size = 500
        param_values["params"].num_independent_populations = 3

        params = param_values["params"]
        brkga = BrkgaMpIpr(**param_values)

        # Not initialized
        with self.assertRaises(RuntimeError) as context:
            brkga.get_best_chromosome()
        self.assertEqual(str(context.exception).strip(),
                         "The algorithm hasn't been initialized. "
                         "Call 'initialize()' before 'get_best_chromosome()'")

        brkga.initialize()

        ########################
        # Test for maximization
        ########################

        local_rng = Random(param_values["seed"])
        for _ in range(1000):
            local_rng.random()

        num_individuals = params.population_size * \
                          params.num_independent_populations

        best_value = -math.inf
        best_chr = None
        for _ in range(num_individuals):
            local_chr = BaseChromosome([
                local_rng.random() for _ in range(param_values["chromosome_size"])
            ])
            value = self.sum_decoder.decode(local_chr, True)
            if best_value < value:
                best_value = value
                best_chr = local_chr
        # end for

        # Assert the both generators are in the same state.
        self.assertEqual(brkga._rng.getstate(), local_rng.getstate())

        # Test the actual value.
        self.assertEqual(brkga.get_best_chromosome(), best_chr)

        ########################
        # Test for minimization
        ########################

        param_values["sense"] = Sense.MINIMIZE
        brkga = BrkgaMpIpr(**param_values)
        brkga.initialize()

        local_rng = Random(param_values["seed"])
        for _ in range(1000):
            local_rng.random()

        num_individuals = params.population_size * \
                          params.num_independent_populations

        best_value = math.inf
        best_chr = None
        for _ in range(num_individuals):
            local_chr = BaseChromosome([
                local_rng.random() for _ in range(param_values["chromosome_size"])
            ])
            value = self.sum_decoder.decode(local_chr, True)
            if best_value > value:
                best_value = value
                best_chr = local_chr
        # end for

        # Assert the both generators are in the same state.
        self.assertEqual(brkga._rng.getstate(), local_rng.getstate())

        # Test the actual value.
        self.assertEqual(brkga.get_best_chromosome(), best_chr)

    ###########################################################################

    def test_get_chromosome(self):
        """
        Tests get_chromosome() method.
        """

        param_values = deepcopy(self.default_param_values)
        param_values["params"].num_independent_populations = 3
        params = param_values["params"]
        brkga = BrkgaMpIpr(**param_values)

        # Not initialized
        with self.assertRaises(RuntimeError) as context:
            brkga.get_chromosome(0, 0)
        self.assertEqual(str(context.exception).strip(),
                         "The algorithm hasn't been initialized. "
                         "Call 'initialize()' before 'get_chromosome()'")

        brkga.initialize()

        # Test invalid population indices.
        population_index = -1
        position = 0
        with self.assertRaises(ValueError) as context:
            brkga.get_chromosome(population_index, position)
        self.assertEqual(str(context.exception).strip(),
                         "Population must be in [0, 2]: -1")

        population_index = brkga.params.num_independent_populations
        position = 0
        with self.assertRaises(ValueError) as context:
            brkga.get_chromosome(population_index, position)
        self.assertEqual(str(context.exception).strip(),
                         "Population must be in [0, 2]: 3")

        # Test invalid chrmosome indices.
        population_index = 0
        position = -1
        with self.assertRaises(ValueError) as context:
            brkga.get_chromosome(population_index, position)
        self.assertEqual(str(context.exception).strip(),
                         "Chromosome position must be in [0, 9]: -1")

        population_index = 0
        position = brkga.params.population_size
        with self.assertRaises(ValueError) as context:
            brkga.get_chromosome(population_index, position)
        self.assertEqual(str(context.exception).strip(),
                         "Chromosome position must be in [0, 9]: 10")

        # Test if the chromosome matches.

        # Create a local RNG and advance it until the same state as the
        # internal BRKGA RNG after initialization.
        local_rng = Random(param_values["seed"])
        skip = 1000
        for _ in range(skip):
            local_rng.random()

        # Now, we create the populations, decode them, and sort the
        # individuals according to their fitness, reproducing initialize()
        # basically.
        local_populations = []
        for _ in range(brkga.params.num_independent_populations):
            population = []
            for _ in range(brkga.params.population_size):
                local_chr = BaseChromosome([
                    local_rng.random() for _ in range(param_values["chromosome_size"])
                ])

                fitness = brkga._decoder.decode(local_chr, True)
                population.append((fitness, local_chr))
            # end for
            population.sort(reverse=(brkga.opt_sense == Sense.MAXIMIZE))
            local_populations.append(population)
        # end for

        # Assert the both generators are in the same state.
        self.assertEqual(brkga._rng.getstate(), local_rng.getstate())

        population_index = 0
        position = 0
        copy_chr = brkga.get_chromosome(population_index, position)
        self.assertEqual(copy_chr, local_populations[population_index][position][1])
        self.assertIsNot(copy_chr, local_populations[population_index][position][1])

        population_index = 1
        position = 1
        copy_chr = brkga.get_chromosome(population_index, position)
        self.assertEqual(copy_chr, local_populations[population_index][position][1])
        self.assertIsNot(copy_chr, local_populations[population_index][position][1])

        population_index = brkga.params.num_independent_populations - 1
        position = brkga.params.population_size - 1
        copy_chr = brkga.get_chromosome(population_index, position)
        self.assertEqual(copy_chr, local_populations[population_index][position][1])
        self.assertIsNot(copy_chr, local_populations[population_index][position][1])

    ###########################################################################

    def test_get_current_population(self):
        """
        Tests get_current_population() method.
        """

        param_values = deepcopy(self.default_param_values)
        param_values["params"].num_independent_populations = 3
        params = param_values["params"]
        brkga = BrkgaMpIpr(**param_values)

        # Not initialized
        with self.assertRaises(RuntimeError) as context:
            brkga.get_current_population()
        self.assertEqual(str(context.exception).strip(),
                         "The algorithm hasn't been initialized. "
                         "Call 'initialize()' before 'get_current_population()'")

        brkga.initialize()

         # Test invalid population indices.
        population_index = -1
        with self.assertRaises(ValueError) as context:
            brkga.get_current_population(population_index)
        self.assertEqual(str(context.exception).strip(),
                         "Population must be in [0, 2]: -1")

        population_index = brkga.params.num_independent_populations
        with self.assertRaises(ValueError) as context:
            brkga.get_current_population(population_index)
        self.assertEqual(str(context.exception).strip(),
                         "Population must be in [0, 2]: 3")

        # Test if it is returning the right population.
        for i in range(params.num_independent_populations):
            self.assertIs(brkga.get_current_population(i),
                          brkga._current_populations[i])

###############################################################################

if __name__ == "__main__":
    unittest.main()
