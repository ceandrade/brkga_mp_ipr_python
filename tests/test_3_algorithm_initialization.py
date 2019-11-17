"""
test_algorithm_initialization.py: Tests constructor and initialization methods.

(c) Copyright 2019, Carlos Eduardo de Andrade. All Rights Reserved.

This code is released under LICENSE.md.

Created on:  Nov 08, 2019 by ceandrade
Last update: Nov 13, 2019 by ceandrade

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

    def test_constructor(self):
        """
        Tests BrkgaParams constructor.
        """

        ########################
        # Test regular/correct building.
        #######################

        param_values = deepcopy(self.default_param_values)
        brkga = BrkgaMpIpr(**param_values)

        self.assertEqual(brkga.elite_size, 3)
        self.assertEqual(brkga.num_mutants, 1)

        brkga_params = param_values["params"]
        self.assertEqual(len(brkga._parents_ordered), brkga_params.total_parents)

        local_rng = Random(param_values["seed"])
        # Same warm up that the one in the constructor.
        for _ in range(1000):
            local_rng.random()
        self.assertEqual(brkga._rng.getstate(), local_rng.getstate())

        self.assertEqual(brkga._ChromosomeType, BaseChromosome)

        ########################
        # Test multi-start building.
        ########################

        param_values["evolutionary_mechanism_on"] = False
        param_values["params"].population_size = 10
        brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(brkga.elite_size, 1)
        self.assertEqual(brkga.num_mutants, 9)

        ########################
        # Test bias functions.
        ########################

        param_values = deepcopy(self.default_param_values)
        param_values["params"].bias_type = BiasFunctionType.LOGINVERSE
        brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(brkga.params.bias_type, BiasFunctionType.LOGINVERSE)
        self.assertAlmostEqual(brkga._bias_function(1), 1.4426950408889634)
        self.assertAlmostEqual(brkga._bias_function(2), 0.9102392266268375)
        self.assertAlmostEqual(brkga._bias_function(3), 0.721347520444481)

        param_values["params"].bias_type = BiasFunctionType.LINEAR
        brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(brkga.params.bias_type, BiasFunctionType.LINEAR)
        self.assertAlmostEqual(brkga._bias_function(1), 1.0)
        self.assertAlmostEqual(brkga._bias_function(2), 0.5)
        self.assertAlmostEqual(brkga._bias_function(3), 0.333333333333)

        param_values["params"].bias_type = BiasFunctionType.QUADRATIC
        brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(brkga.params.bias_type, BiasFunctionType.QUADRATIC)
        self.assertAlmostEqual(brkga._bias_function(1), 1.0)
        self.assertAlmostEqual(brkga._bias_function(2), 0.25)
        self.assertAlmostEqual(brkga._bias_function(3), 0.111111111111)

        param_values["params"].bias_type = BiasFunctionType.CUBIC
        brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(brkga.params.bias_type, BiasFunctionType.CUBIC)
        self.assertAlmostEqual(brkga._bias_function(1), 1.0)
        self.assertAlmostEqual(brkga._bias_function(2), 0.125)
        self.assertAlmostEqual(brkga._bias_function(3), 0.037037037037037035)

        param_values["params"].bias_type = BiasFunctionType.EXPONENTIAL
        brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(brkga.params.bias_type, BiasFunctionType.EXPONENTIAL)
        self.assertAlmostEqual(brkga._bias_function(1), 0.36787944117144233)
        self.assertAlmostEqual(brkga._bias_function(2), 0.1353352832366127)
        self.assertAlmostEqual(brkga._bias_function(3), 0.049787068367863944)

        param_values["params"].bias_type = BiasFunctionType.CONSTANT
        brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(brkga.params.bias_type, BiasFunctionType.CONSTANT)
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
                         "Chromosome size must be larger than zero: 0")

        param_values["chromosome_size"] = -10
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "Chromosome size must be larger than zero: -10")

        # Population size
        param_values = deepcopy(self.default_param_values)
        param_values["params"].population_size = 0
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "Population size size must be larger than zero: 0")

        param_values["params"].population_size = -10
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "Population size size must be larger than zero: -10")

        # Elite size
        param_values = deepcopy(self.default_param_values)
        param_values["params"].elite_percentage = 0.0
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "Elite set size less then one: 0")

        param_values["params"].elite_percentage = -1.0
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "Elite set size less then one: -10")

        param_values["params"].elite_percentage = 0.3
        param_values["params"].population_size = 2
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "Elite set size less then one: 0")

        param_values["params"].elite_percentage = 1.1
        param_values["params"].population_size = 10
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "Elite set size (11) greater than population size (10)")

        # Mutant size
        param_values = deepcopy(self.default_param_values)
        param_values["params"].mutants_percentage = 0.0
        brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(brkga.num_mutants, 0)

        param_values["params"].mutants_percentage = -1.0
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "Mutant set size less then zero: -10")

        param_values["params"].mutants_percentage = 1.1
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "Mutant set size (11) greater than population size (10)")

        # Elite + Mutant size.
        param_values = deepcopy(self.default_param_values)
        param_values["params"].elite_percentage = 0.6
        param_values["params"].mutants_percentage = 0.6
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "Elite set size (6) + mutant set size (6) greater "
                         "than population size (10)")

        # Elite parents for mating.
        param_values = deepcopy(self.default_param_values)
        param_values["params"].num_elite_parents = 0
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "Number of elite parents must be at least 1: 0")

        param_values["params"].num_elite_parents = 1
        param_values["params"].total_parents = 1
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "Total parents must be at least 2: 1")

        param_values["params"].num_elite_parents = 2
        param_values["params"].total_parents = 2
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "Number of elite parents (2) is greater than or "
                         "equal to total_parents (2)")

        param_values["params"].num_elite_parents = 3
        param_values["params"].total_parents = 2
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "Number of elite parents (3) is greater than or "
                         "equal to total_parents (2)")

        brkga_params = param_values["params"]
        brkga_params.num_elite_parents = \
            1 + int(brkga_params.population_size * brkga_params.elite_percentage)
        brkga_params.total_parents = 1 + brkga_params.num_elite_parents
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "Number of elite parents (4) is greater than elite set (3)")

        # Number of independent populations.
        param_values = deepcopy(self.default_param_values)
        param_values["params"].num_independent_populations = 0
        with self.assertRaises(ValueError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "Number of parallel populations must be larger than zero: 0")

        # TODO: enable the following when IPR methods be implemented.
        # # alpha_block_size.
        # param_values = deepcopy(self.default_param_values)
        # param_values["params"].alpha_block_size = 0
        # with self.assertRaises(ValueError) as context:
        #     brkga = BrkgaMpIpr(**param_values)
        # self.assertEqual(str(context.exception).strip(),
        #                  "Alpha block size must be larger than zero: 0")

        # # Percentage / path size.
        # param_values = deepcopy(self.default_param_values)
        # param_values["params"].pr_percentage = 0.0
        # with self.assertRaises(ValueError) as context:
        #     brkga = BrkgaMpIpr(**param_values)
        # self.assertEqual(str(context.exception).strip(),
        #                  "Percentage / path size must be in (0, 1]: 0.0")

        # param_values["params"].pr_percentage = 1.001
        # with self.assertRaises(ValueError) as context:
        #     brkga = BrkgaMpIpr(**param_values)
        # self.assertEqual(str(context.exception).strip(),
        #                  "Percentage / path size must be in (0, 1]: 1.001")

        # Invalid decoder object.
        param_values = deepcopy(self.default_param_values)
        param_values["decoder"] = None
        with self.assertRaises(TypeError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "The given decoder (<class 'NoneType'>) has no 'decode()' method")

        param_values["decoder"] = lambda x: sum(x)
        with self.assertRaises(TypeError) as context:
            brkga = BrkgaMpIpr(**param_values)
        self.assertEqual(str(context.exception).strip(),
                         "The given decoder (<class 'function'>) has no 'decode()' method")

    ###########################################################################

    def test_generate_chromosome(self):
        """
        Tests generate_chromosome() method.
        """

        param_values = deepcopy(self.default_param_values)
        brkga = BrkgaMpIpr(**param_values)

        local_rng = Random(param_values["seed"])
        # Same warm up that the one in the constructor.
        for _ in range(1000):
            local_rng.random()
        self.assertEqual(brkga._rng.getstate(), local_rng.getstate())

        size = param_values["chromosome_size"]
        standard = BaseChromosome([local_rng.random() for _ in range(size)])
        new_chr = brkga.generate_chromosome(size)
        self.assertEqual(len(new_chr), size)
        self.assertEqual(new_chr, standard)

        size = 1000
        standard = BaseChromosome([local_rng.random() for _ in range(size)])
        new_chr = brkga.generate_chromosome(size)
        self.assertEqual(len(new_chr), size)
        self.assertEqual(new_chr, standard)

    ###########################################################################

    def test_fill_chromosome(self):
        """
        Tests fill_chromosome() method.
        """

        param_values = deepcopy(self.default_param_values)
        brkga = BrkgaMpIpr(**param_values)

        local_rng = Random(param_values["seed"])
        # Same warm up that the one in the constructor.
        for _ in range(1000):
            local_rng.random()
        self.assertEqual(brkga._rng.getstate(), local_rng.getstate())

        size = param_values["chromosome_size"]
        chromosome = BaseChromosome([0.0 for _ in range(size)])
        old_chrmosome = deepcopy(chromosome)

        brkga.fill_chromosome(chromosome)

        local_chr = BaseChromosome([local_rng.random() for _ in range(size)])
        self.assertEqual(len(chromosome), len(old_chrmosome))
        self.assertNotEqual(chromosome, old_chrmosome)
        self.assertEqual(chromosome, local_chr)

        size = 1000
        chromosome = BaseChromosome([0.0 for _ in range(size)])
        old_chrmosome = deepcopy(chromosome)

        brkga.fill_chromosome(chromosome)

        local_chr = BaseChromosome([local_rng.random() for _ in range(size)])
        self.assertEqual(len(chromosome), len(old_chrmosome))
        self.assertNotEqual(chromosome, old_chrmosome)
        self.assertEqual(chromosome, local_chr)

    ###########################################################################

    def test_set_initial_population(self):
        """
        Tests set_initial_population() method.
        """

        param_values = deepcopy(self.default_param_values)
        param_values["chromosome_size"] = 3
        param_values["params"].num_independent_populations = 2
        brkga = BrkgaMpIpr(**param_values)

        local_rng = Random(param_values["seed"])

        chromosomes = [
            BaseChromosome() for _ in range(brkga.params.population_size + 1)
        ]
        with self.assertRaises(ValueError) as context:
            brkga.set_initial_population(chromosomes)
        self.assertEqual(str(context.exception).strip(),
                         "Number of given chromosomes (11) is large than "
                         "the population size (10)")

        chromosomes = [
            BaseChromosome([local_rng.random() for _ in
                            range(param_values["chromosome_size"] + 1)])
        ]
        with self.assertRaises(ValueError) as context:
            brkga.set_initial_population(chromosomes)
        self.assertEqual(str(context.exception).strip(),
                         "Error on setting initial population: chromosome 0 "
                         "does not have the required dimension "
                         "(actual size: 4, required size: 3)")

        chromosomes = [
            BaseChromosome([local_rng.random() for _ in
                            range(param_values["chromosome_size"] - 1)])
        ]
        with self.assertRaises(ValueError) as context:
            brkga.set_initial_population(chromosomes)
        self.assertEqual(str(context.exception).strip(),
                         "Error on setting initial population: chromosome 0 "
                         "does not have the required dimension "
                         "(actual size: 2, required size: 3)")

        chromosomes = [
            BaseChromosome([local_rng.random() for _ in
                            range(param_values["chromosome_size"] + 1)]),
            BaseChromosome([local_rng.random() for _ in
                            range(param_values["chromosome_size"])]),
            BaseChromosome([local_rng.random() for _ in
                            range(param_values["chromosome_size"])])
        ]
        with self.assertRaises(ValueError) as context:
            brkga.set_initial_population(chromosomes)
        self.assertEqual(str(context.exception).strip(),
                         "Error on setting initial population: chromosome 0 "
                         "does not have the required dimension "
                         "(actual size: 4, required size: 3)")

        chromosomes = [
            BaseChromosome([local_rng.random() for _ in
                            range(param_values["chromosome_size"])]),
            BaseChromosome([local_rng.random() for _ in
                            range(param_values["chromosome_size"] + 1)]),
            BaseChromosome([local_rng.random() for _ in
                            range(param_values["chromosome_size"])])
        ]
        with self.assertRaises(ValueError) as context:
            brkga.set_initial_population(chromosomes)
        self.assertEqual(str(context.exception).strip(),
                         "Error on setting initial population: chromosome 1 "
                         "does not have the required dimension "
                         "(actual size: 4, required size: 3)")

        chromosomes = [
            BaseChromosome([local_rng.random() for _ in
                            range(param_values["chromosome_size"])]),
            BaseChromosome([local_rng.random() for _ in
                            range(param_values["chromosome_size"])]),
            BaseChromosome([local_rng.random() for _ in
                            range(param_values["chromosome_size"] + 1)])
        ]
        with self.assertRaises(ValueError) as context:
            brkga.set_initial_population(chromosomes)
        self.assertEqual(str(context.exception).strip(),
                         "Error on setting initial population: chromosome 2 "
                         "does not have the required dimension "
                         "(actual size: 4, required size: 3)")

        chromosomes = [BaseChromosome([local_rng.random() for _ in
                                      range(param_values["chromosome_size"])])]
        brkga.set_initial_population(chromosomes)

        self.assertEqual(brkga._current_populations[0].chromosomes[0], chromosomes[0])
        self.assertIsNot(brkga._current_populations[0].chromosomes[0], chromosomes[0])

        chromosomes[0] = BaseChromosome([0.1111, 0.2222, 0.3333])
        self.assertNotEqual(brkga._current_populations[0].chromosomes[0], chromosomes[0])

        chromosomes = [
            BaseChromosome([local_rng.random() for _ in
                            range(param_values["chromosome_size"])]),
            BaseChromosome([local_rng.random() for _ in
                            range(param_values["chromosome_size"])]),
            BaseChromosome([local_rng.random() for _ in
                            range(param_values["chromosome_size"])])
        ]
        brkga.set_initial_population(chromosomes)

        self.assertEqual(len(brkga._current_populations[0].chromosomes),
                         len(chromosomes))
        self.assertEqual(brkga._current_populations[0].chromosomes, chromosomes)
        self.assertIsNot(brkga._current_populations[0].chromosomes, chromosomes)

        self.assertEqual(brkga._initial_population, True)

    ###########################################################################

    def test_set_bias_custom_function(self):
        """
        Tests set_bias_custom_function() method.
        """

        param_values = deepcopy(self.default_param_values)
        param_values["params"].population_size = 100
        param_values["params"].total_parents = 10
        brkga = BrkgaMpIpr(**param_values)

        # After build, brkga_params function is never CUSTOM
        self.assertNotEqual(brkga.params.bias_type, BiasFunctionType.CUSTOM)

        with self.assertRaises(ValueError) as context:
            brkga.set_bias_custom_function(lambda x: -x)
        self.assertEqual(str(context.exception).strip(),
                         "Bias function must be positive non-increasing")

        with self.assertRaises(ValueError) as context:
            brkga.set_bias_custom_function(lambda x: x)
        self.assertEqual(str(context.exception).strip(),
                         "Bias function is not a non-increasing function")

        with self.assertRaises(ValueError) as context:
            brkga.set_bias_custom_function(lambda x: x + 1)
        self.assertEqual(str(context.exception).strip(),
                         "Bias function is not a non-increasing function")

        with self.assertRaises(ValueError) as context:
            brkga.set_bias_custom_function(lambda x: math.log1p(x))
        self.assertEqual(str(context.exception).strip(),
                         "Bias function is not a non-increasing function")

        brkga.set_bias_custom_function(lambda x:  1.0 / math.log1p(x))
        self.assertAlmostEqual(brkga._total_bias_weight, 6.554970525044798)

        # After 2nd call to set_bias_custom_function, brkga_params function
        # is always CUSTOM
        self.assertEqual(brkga.params.bias_type, BiasFunctionType.CUSTOM)

        brkga.set_bias_custom_function(lambda x: 1.0 / x)
        self.assertAlmostEqual(brkga._total_bias_weight, 2.9289682539682538)
        self.assertEqual(brkga.params.bias_type, BiasFunctionType.CUSTOM)

        brkga.set_bias_custom_function(lambda x: x ** -2.0)
        self.assertAlmostEqual(brkga._total_bias_weight, 1.5497677311665408)
        self.assertEqual(brkga.params.bias_type, BiasFunctionType.CUSTOM)

        brkga.set_bias_custom_function(lambda x: x ** -3.0)
        self.assertAlmostEqual(brkga._total_bias_weight, 1.197531985674193)
        self.assertEqual(brkga.params.bias_type, BiasFunctionType.CUSTOM)

        brkga.set_bias_custom_function(lambda x: math.exp(-x))
        self.assertAlmostEqual(brkga._total_bias_weight, 0.5819502851677112)
        self.assertEqual(brkga.params.bias_type, BiasFunctionType.CUSTOM)

        # This is a constance function.
        brkga.set_bias_custom_function(lambda _: 1.0 / brkga.params.total_parents)
        self.assertAlmostEqual(brkga._total_bias_weight, 0.9999999999999999)
        self.assertEqual(brkga.params.bias_type, BiasFunctionType.CUSTOM)

        brkga.set_bias_custom_function(lambda x: 0.6325 / math.sqrt(x))
        self.assertAlmostEqual(brkga._total_bias_weight, 3.175781171302612)
        self.assertEqual(brkga.params.bias_type, BiasFunctionType.CUSTOM)

        #############################################
        # Constant functions test for standard BRKGA
        #############################################

        param_values = deepcopy(self.default_param_values)
        param_values["params"].num_elite_parents = 1
        param_values["params"].total_parents = 2
        brkga = BrkgaMpIpr(**param_values)

        rho = 0.5
        brkga.set_bias_custom_function(lambda x: rho if x == 1 else 1.0 - rho)
        self.assertAlmostEqual(brkga._total_bias_weight, 1.0)
        self.assertAlmostEqual(brkga._bias_function(1), 0.5)
        self.assertAlmostEqual(brkga._bias_function(2), 0.5)

        rho = 0.75
        brkga.set_bias_custom_function(lambda x: rho if x == 1 else 1.0 - rho)
        self.assertAlmostEqual(brkga._total_bias_weight, 1.0)
        self.assertAlmostEqual(brkga._bias_function(1), 0.75)
        self.assertAlmostEqual(brkga._bias_function(2), 0.25)

        rho = 0.9
        brkga.set_bias_custom_function(lambda x: rho if x == 1 else 1.0 - rho)
        self.assertAlmostEqual(brkga._total_bias_weight, 1.0)
        self.assertAlmostEqual(brkga._bias_function(1), 0.9)
        self.assertAlmostEqual(brkga._bias_function(2), 0.1)

    ###########################################################################

    def test_initialize(self):
        """
        Tests initialize() method.
        """

        # Double initialization.
        param_values = deepcopy(self.default_param_values)
        brkga = BrkgaMpIpr(**param_values)

        # 1st initialization.
        brkga.initialize()
        with self.assertRaises(RuntimeError) as context:
            # 2nd initialization.
            brkga.initialize()
        self.assertEqual(str(context.exception).strip(),
                         "The algorithm is already initialized. "
                         "Please call 'reset()' instead.")

        # Custom function is not defined.
        filename = os.path.join(CONFIG_DIR, "custom_bias_function.conf")
        brkga_params, _ = load_configuration(filename)

        param_values = deepcopy(self.default_param_values)
        param_values["params"] = brkga_params
        brkga = BrkgaMpIpr(**param_values)

        with self.assertRaises(ValueError) as context:
            brkga.initialize()
        self.assertEqual(str(context.exception).strip(),
                         "The bias function is not defined. Call "
                         "set_bias_custom_function() before call initialize().")

        ########################
        # Test without warmstart
        ########################

        param_values = deepcopy(self.default_param_values)
        param_values["sense"] = Sense.MAXIMIZE
        params = param_values["params"]
        brkga = BrkgaMpIpr(**param_values)
        brkga.initialize()

        self.assertTrue(brkga._initialized,
                        "Flag 'brkga._initialized' is supposed to be 'True'")
        self.assertFalse(brkga._reset_phase,
                        "Flag 'brkga._reset_phase' is supposed to be 'False'")

        self.assertEqual(len(brkga._current_populations),
                         params.num_independent_populations)
        self.assertEqual(len(brkga._previous_populations),
                         params.num_independent_populations)

        for i in range(params.num_independent_populations):
            self.assertEqual(len(brkga._current_populations[i].chromosomes),
                             params.population_size)
            self.assertEqual(len(brkga._current_populations[i].fitness),
                             params.population_size)
            self.assertEqual(len(brkga._previous_populations[i].chromosomes),
                             params.population_size)
            self.assertEqual(len(brkga._previous_populations[i].fitness),
                             params.population_size)

            self.assertEqual(brkga._current_populations[i].chromosomes,
                             brkga._previous_populations[i].chromosomes)

            self.assertIsNot(brkga._current_populations[i].chromosomes,
                             brkga._previous_populations[i].chromosomes)

            correct_order = True
            for j in range(1, brkga.params.population_size):
                correct_order &= \
                    brkga._current_populations[i].fitness[j - 1][0] >= \
                    brkga._current_populations[i].fitness[j][0]
            # end for
            self.assertTrue(correct_order, "incorrect chromosome order")
        # end for

        param_values = deepcopy(self.default_param_values)
        param_values["sense"] = Sense.MINIMIZE
        params = param_values["params"]
        brkga = BrkgaMpIpr(**param_values)
        brkga.initialize()

        for i in range(params.num_independent_populations):
            correct_order = True
            for j in range(1, brkga.params.population_size):
                correct_order &= \
                    brkga._current_populations[i].fitness[j - 1][0] <= \
                    brkga._current_populations[i].fitness[j][0]
            # end for
            self.assertTrue(correct_order, "incorrect chromosome order")
        # end for

        ########################
        # Test with warmstart
        ########################

        local_rng = Random(param_values["seed"])
        chromosomes = [
            BaseChromosome([local_rng.random() for _ in
                            range(param_values["chromosome_size"])]),
            BaseChromosome([local_rng.random() for _ in
                            range(param_values["chromosome_size"])]),
            BaseChromosome([local_rng.random() for _ in
                            range(param_values["chromosome_size"])])
        ]

        param_values = deepcopy(self.default_param_values)
        param_values["sense"] = Sense.MINIMIZE
        params = param_values["params"]
        brkga = BrkgaMpIpr(**param_values)
        brkga.set_initial_population(chromosomes)
        brkga.initialize()

        for i in range(params.num_independent_populations):
            self.assertEqual(len(brkga._current_populations[i].chromosomes),
                             params.population_size)
            self.assertEqual(len(brkga._current_populations[i].fitness),
                             params.population_size)
            self.assertEqual(len(brkga._previous_populations[i].chromosomes),
                             params.population_size)
            self.assertEqual(len(brkga._previous_populations[i].fitness),
                             params.population_size)

            self.assertEqual(brkga._current_populations[i].chromosomes,
                             brkga._previous_populations[i].chromosomes)

            self.assertIsNot(brkga._current_populations[i].chromosomes,
                             brkga._previous_populations[i].chromosomes)
        # end for

        old_chr = deepcopy(chromosomes[0])
        param_values["decoder"].decode(chromosomes[0], rewrite=True)
        self.assertNotEqual(chromosomes[0], old_chr)
        self.assertEqual(brkga._current_populations[0].chromosomes[0],
                         chromosomes[0])

        # Create a local chromosome and applied the decoder on it.
        local_rng = Random(param_values["seed"])
        for _ in range(1000):
            local_rng.random()
        local_chr = BaseChromosome([
            local_rng.random() for _ in range(param_values["chromosome_size"])
        ])
        param_values["decoder"].decode(local_chr, rewrite=True)

        # 4th chromosome must be the 1st generated one due to the warmstart.
        self.assertEqual(brkga._current_populations[0].chromosomes[3],
                         local_chr)

        ########################
        # Test reset phase
        ########################

        param_values = deepcopy(self.default_param_values)
        params = param_values["params"]
        brkga = BrkgaMpIpr(**param_values)
        brkga.initialize()

        # Create a local RNG and advance it until the same state as the
        # internal BRKGA RNG after initialization.
        local_rng = Random(param_values["seed"])
        skip = 1000 + params.num_independent_populations * \
               params.population_size * brkga.chromosome_size
        for _ in range(skip):
            local_rng.random()

        self.assertEqual(brkga._rng.getstate(), local_rng.getstate())

        brkga._reset_phase = True
        brkga.initialize()

        # Create a local chromosome and applied the decoder on it.
        local_chr = BaseChromosome([
            local_rng.random() for _ in range(param_values["chromosome_size"])
        ])
        param_values["decoder"].decode(local_chr, rewrite=True)

        self.assertEqual(brkga._current_populations[0].chromosomes[0],
                         local_chr)

###############################################################################

if __name__ == "__main__":
    unittest.main()
