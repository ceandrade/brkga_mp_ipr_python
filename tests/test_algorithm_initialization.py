"""
test_algorithm_initialization.py: Tests constructor and initialization methods.

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

from copy import deepcopy
import math
from random import Random
import unittest

from brkga_mp_ipr.algorithm import BrkgaMpIpr
from brkga_mp_ipr.enums import *
from brkga_mp_ipr.types import BaseChromosome, BrkgaParams

###############################################################################

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

        self.default_param_values = {
            "decoder": None,
            "sense": Sense.MAXIMIZE,
            "seed": 2700001,
            "chromosome_size": 100,
            "params": self.default_brkga_params,
            "evolutionary_mechanism_on": True,
            "chrmosome_type": BaseChromosome
        }

    ###########################################################################

    def test_constructor(self):
        """
        Tests BrkgaParams constructor.
        """

        ########################
        # Test regular/correct building.
        #######################

        param_values = deepcopy(self.default_param_values)
        brkga = BrkgaMpIpr(**param_values)

        self.assertEqual(brkga.ELITE_SIZE, 3)
        self.assertEqual(brkga.NUM_MUTANTS, 1)

        brkga_params = param_values["params"]
        self.assertEqual(len(brkga._shuffled_individuals), brkga_params.population_size)
        self.assertEqual(len(brkga._parents_ordered), brkga_params.total_parents)

        local_rng = Random(param_values["seed"])
        # Same warm up that the one in the constructor.
        for _ in range(1000):
            local_rng.random()
        self.assertEqual(brkga._rng.getstate(), local_rng.getstate())

        self.assertEqual(brkga._ChrmosomeType, BaseChromosome)

        ########################
        # Test multi-start building.
        ########################

        param_values["evolutionary_mechanism_on"] = False
        param_values["params"].population_size = 10
        brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(brkga.ELITE_SIZE, 1)
        self.assertEqual(brkga.NUM_MUTANTS, 9)

        ########################
        # Test bias functions.
        ########################

        param_values = deepcopy(self.default_param_values)
        param_values["params"].bias_type = BiasFunctionType.LOGINVERSE
        brkga = BrkgaMpIpr(**param_values)
        self.assertAlmostEqual(brkga._bias_function(1), 1.4426950408889634)
        self.assertAlmostEqual(brkga._bias_function(2), 0.9102392266268375)
        self.assertAlmostEqual(brkga._bias_function(3), 0.721347520444481)

        param_values["params"].bias_type = BiasFunctionType.LINEAR
        brkga = BrkgaMpIpr(**param_values)
        self.assertAlmostEqual(brkga._bias_function(1), 1.0)
        self.assertAlmostEqual(brkga._bias_function(2), 0.5)
        self.assertAlmostEqual(brkga._bias_function(3), 0.333333333333)

        param_values["params"].bias_type = BiasFunctionType.QUADRATIC
        brkga = BrkgaMpIpr(**param_values)
        self.assertAlmostEqual(brkga._bias_function(1), 1.0)
        self.assertAlmostEqual(brkga._bias_function(2), 0.25)
        self.assertAlmostEqual(brkga._bias_function(3), 0.111111111111)

        param_values["params"].bias_type = BiasFunctionType.CUBIC
        brkga = BrkgaMpIpr(**param_values)
        self.assertAlmostEqual(brkga._bias_function(1), 1.0)
        self.assertAlmostEqual(brkga._bias_function(2), 0.125)
        self.assertAlmostEqual(brkga._bias_function(3), 0.037037037037037035)

        param_values["params"].bias_type = BiasFunctionType.EXPONENTIAL
        brkga = BrkgaMpIpr(**param_values)
        self.assertAlmostEqual(brkga._bias_function(1), 0.36787944117144233)
        self.assertAlmostEqual(brkga._bias_function(2), 0.1353352832366127)
        self.assertAlmostEqual(brkga._bias_function(3), 0.049787068367863944)

        param_values["params"].bias_type = BiasFunctionType.CONSTANT
        brkga = BrkgaMpIpr(**param_values)
        self.assertAlmostEqual(brkga._bias_function(1), 0.5)
        self.assertAlmostEqual(brkga._bias_function(2), 0.5)
        self.assertAlmostEqual(brkga._bias_function(3), 0.5)

        ########################
        # Test exceptions.
        ########################

        # Chromosome size
        param_values = deepcopy(self.default_param_values)
        param_values["chromosome_size"] = 0
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "chromosome size must be larger than zero: 0")

        param_values["chromosome_size"] = -10
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "chromosome size must be larger than zero: -10")

        # Population size
        param_values = deepcopy(self.default_param_values)
        param_values["params"].population_size = 0
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "population_size size must be larger than zero: 0")

        param_values["params"].population_size = -10
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "population_size size must be larger than zero: -10")

        # Elite size
        param_values = deepcopy(self.default_param_values)
        param_values["params"].elite_percentage = 0.0
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "elite-set size less then one: 0")

        param_values["params"].elite_percentage = -1.0
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "elite-set size less then one: -10")

        param_values["params"].elite_percentage = 0.3
        param_values["params"].population_size = 2
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "elite-set size less then one: 0")

        param_values["params"].elite_percentage = 1.1
        param_values["params"].population_size = 10
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "elite-set size (11) greater than population size (10)")

        # Mutant size
        param_values = deepcopy(self.default_param_values)
        param_values["params"].mutants_percentage = 0.0
        brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(brkga.NUM_MUTANTS, 0)

        param_values["params"].mutants_percentage = -1.0
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "mutant-set size less then zero: -10")

        param_values["params"].mutants_percentage = 1.1
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "mutant-set size (11) greater than population size (10)")

        # Elite + Mutant size.
        param_values = deepcopy(self.default_param_values)
        param_values["params"].elite_percentage = 0.6
        param_values["params"].mutants_percentage = 0.6
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "elite-set size (6) + mutant-set size (6) greater "
                         "than population size (10)")

        # Elite parents for mating.
        param_values = deepcopy(self.default_param_values)
        param_values["params"].num_elite_parents = 0
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "num_elite_parents must be at least 1: 0")

        param_values["params"].num_elite_parents = 1
        param_values["params"].total_parents = 1
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "total_parents must be at least 2: 1")

        param_values["params"].num_elite_parents = 2
        param_values["params"].total_parents = 2
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "num_elite_parents (2) is greater than or equal to "
                         "total_parents (2)")

        param_values["params"].num_elite_parents = 3
        param_values["params"].total_parents = 2
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "num_elite_parents (3) is greater than or equal to "
                         "total_parents (2)")

        brkga_params = param_values["params"]
        brkga_params.num_elite_parents = \
            1 + int(brkga_params.population_size * brkga_params.elite_percentage)
        brkga_params.total_parents = 1 + brkga_params.num_elite_parents
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "num_elite_parents (4) is greater than elite set (3)")

        # Number of independent populations.
        param_values = deepcopy(self.default_param_values)
        param_values["params"].num_independent_populations = 0
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "number of parallel populations must be larger than zero: 0")

        # TODO: enable the following when IPR methods be implemented.
        # # alpha_block_size.
        # param_values = deepcopy(self.default_param_values)
        # param_values["params"].alpha_block_size = 0
        # with self.assertRaises(ValueError) as context:
        #     brkga = BrkgaMpIpr(**param_values)
        # self.assertEqual(str(context.exception).strip(),
        #                  "alpha_block_size must be larger than zero: 0")

        # # Percentage / path size.
        # param_values = deepcopy(self.default_param_values)
        # param_values["params"].pr_percentage = 0.0
        # with self.assertRaises(ValueError) as context:
        #     brkga = BrkgaMpIpr(**param_values)
        # self.assertEqual(str(context.exception).strip(),
        #                  "percentage / path size must be in (0, 1]: 0.0")

        # param_values["params"].pr_percentage = 1.001
        # with self.assertRaises(ValueError) as context:
        #     brkga = BrkgaMpIpr(**param_values)
        # self.assertEqual(str(context.exception).strip(),
        #                  "percentage / path size must be in (0, 1]: 1.001")


    # ###########################################################################

    # def test_set_initial_population(self):
    #     """
    #     Tests set_initial_population() method.
    #     """

    #     brkga = BRKGA_MP_IPR()
    #     self.assertRaises(NotImplementedError, brkga.set_initial_population, [])

    ###########################################################################

    def test_set_bias_custom_function(self):
        """
        Tests set_bias_custom_function() method.
        """

        param_values = deepcopy(self.default_param_values)
        param_values["params"].population_size = 100
        param_values["params"].total_parents = 10
        brkga = BrkgaMpIpr(**param_values)

        # TODO: enable this after finish the constructor.
        # After build, brkga_params function is never CUSTOM
        # @test brkga_data.params.bias_type != CUSTOM

        with self.assertRaises(ValueError) as context:
            brkga.set_bias_custom_function(lambda x: -x)
        self.assertEqual(str(context.exception).strip(),
                         "bias_function must be positive non-increasing")

        with self.assertRaises(ValueError) as context:
            brkga.set_bias_custom_function(lambda x: x)
        self.assertEqual(str(context.exception).strip(),
                         "bias_function is not a non-increasing function")

        with self.assertRaises(ValueError) as context:
            brkga.set_bias_custom_function(lambda x: x + 1)
        self.assertEqual(str(context.exception).strip(),
                         "bias_function is not a non-increasing function")

        with self.assertRaises(ValueError) as context:
            brkga.set_bias_custom_function(lambda x: math.log1p(x))
        self.assertEqual(str(context.exception).strip(),
                         "bias_function is not a non-increasing function")

        brkga.set_bias_custom_function(lambda x:  1.0 / math.log1p(x))
        self.assertAlmostEqual(brkga._total_bias_weight, 6.554970525044798)

        # After 2nd call to set_bias_custom_function, brkga_params function
        # is always CUSTOM
        self.assertEqual(brkga.PARAMS.bias_type, BiasFunctionType.CUSTOM)

        brkga.set_bias_custom_function(lambda x:  1.0 / x)
        self.assertAlmostEqual(brkga._total_bias_weight, 2.9289682539682538)
        self.assertEqual(brkga.PARAMS.bias_type, BiasFunctionType.CUSTOM)

        brkga.set_bias_custom_function(lambda x:  x ** -2.0)
        self.assertAlmostEqual(brkga._total_bias_weight, 1.5497677311665408)
        self.assertEqual(brkga.PARAMS.bias_type, BiasFunctionType.CUSTOM)

        brkga.set_bias_custom_function(lambda x:  x ** -3.0)
        self.assertAlmostEqual(brkga._total_bias_weight, 1.197531985674193)
        self.assertEqual(brkga.PARAMS.bias_type, BiasFunctionType.CUSTOM)

        brkga.set_bias_custom_function(lambda x:  math.exp(-x))
        self.assertAlmostEqual(brkga._total_bias_weight, 0.5819502851677112)
        self.assertEqual(brkga.PARAMS.bias_type, BiasFunctionType.CUSTOM)

        # This is a constance function.
        brkga.set_bias_custom_function(lambda _:  1.0 / brkga.PARAMS.total_parents)
        self.assertAlmostEqual(brkga._total_bias_weight, 0.9999999999999999)
        self.assertEqual(brkga.PARAMS.bias_type, BiasFunctionType.CUSTOM)

        brkga.set_bias_custom_function(lambda x:  0.6325 / math.sqrt(x))
        self.assertAlmostEqual(brkga._total_bias_weight, 3.175781171302612)
        self.assertEqual(brkga.PARAMS.bias_type, BiasFunctionType.CUSTOM)


    # ###########################################################################

    # def test_initialize(self):
    #     """
    #     Tests initialize() method.
    #     """

    #     brkga = BRKGA_MP_IPR()
    #     self.assertRaises(NotImplementedError, brkga.initialize)


###############################################################################

if __name__ == "__main__":
    unittest.main()
