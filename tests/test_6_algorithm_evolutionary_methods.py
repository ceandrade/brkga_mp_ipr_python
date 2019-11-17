"""
test_algorithm_evolutionary_methods.py: Tests the evolutionary methods.

(c) Copyright 2019, Carlos Eduardo de Andrade. All Rights Reserved.

This code is released under LICENSE.md.

Created on:  Nov 08, 2019 by ceandrade
Last update: Nov 15, 2019 by ceandrade

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
from random import Random
from time import time
import dill as pickle
import math
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
    Test units for evolutionary methods.
    """

    ###########################################################################

    def setUp(self):
        """
        Sets up some configurations.
        """

        Test.maxDiff = None

        # For travis-ci output.
        self.start_time = time()

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

    def test_evolve_population0(self):
        """
        Tests evolve_population() method.
        """

        param_values = deepcopy(self.default_param_values)
        brkga_params = param_values["params"]
        brkga_params.num_independent_populations = 3
        brkga_params.num_elite_parents = 1
        brkga_params.total_parents = 2
        brkga = BrkgaMpIpr(**param_values)

        # Not initialized
        with self.assertRaises(RuntimeError) as context:
            brkga.evolve_population(0)
        self.assertEqual(str(context.exception).strip(),
                         "The algorithm hasn't been initialized. "
                         "Call 'initialize()' before 'evolve_population()'")

        brkga.initialize()

         # Test invalid population indices.
        population_index = -1
        with self.assertRaises(ValueError) as context:
            brkga.evolve_population(population_index)
        self.assertEqual(str(context.exception).strip(),
                         "Population must be in [0, 2]: -1")

        population_index = brkga.params.num_independent_populations
        with self.assertRaises(ValueError) as context:
            brkga.evolve_population(population_index)
        self.assertEqual(str(context.exception).strip(),
                         "Population must be in [0, 2]: 3")

        # Save previous and current populations locally
        current = deepcopy(brkga._current_populations)
        previous = deepcopy(brkga._previous_populations)

        ########################
        # Test if algorithm swaps the populations correctly
        ########################

        for i in range(brkga_params.num_independent_populations):
            brkga.evolve_population(i)

            # Internal current and previous generation must be different.
            self.assertNotEqual(brkga._current_populations[i].chromosomes,
                                brkga._previous_populations[i].chromosomes)

            # The current the from this generation is equal to the previous
            # of the next generation.
            self.assertEqual(current[i].chromosomes,
                             brkga._previous_populations[i].chromosomes)
            self.assertEqual(current[i].fitness,
                             brkga._previous_populations[i].fitness)

            # The previous of this generation is lost. Just make sure that
            # the internal swap gets the new generation, not the current one.
            self.assertNotEqual(previous[i].chromosomes,
                                brkga._current_populations[i].chromosomes)
            self.assertNotEqual(previous[i].fitness,
                                brkga._current_populations[i].fitness)
        # end for
        print(f"Elapsed time: {time() - self.start_time :.2f}")

    ###########################################################################

    def test_evolve_population1(self):
        """
        Tests evolve_population() method.
        """
        ########################
        # Test the evolutionary mechanism
        ########################
        # **NOTE:** this test may fail with the random number generation
        # changes. In such case, we have to figure out how to make this test
        # better.
        ########################
        # Data 1

        with open(os.path.join(STATE_DIR, "state1.pickle"), "rb") as hd:
            brkga = pickle.load(hd)

        with open(os.path.join(SOLUTION_DIR, "best_solution1.pickle"), "rb") as hd:
            results = pickle.load(hd)

        brkga.evolve_population(0)
        self.assertEqual(brkga.get_best_fitness(), results["fitness1"])
        self.assertEqual(brkga.get_best_chromosome(), results["chromosome1"])
        print(f"Elapsed time: {time() - self.start_time :.2f}")

        brkga.evolve_population(0)
        self.assertEqual(brkga.get_best_fitness(), results["fitness2"])
        self.assertEqual(brkga.get_best_chromosome(), results["chromosome2"])
        print(f"Elapsed time: {time() - self.start_time :.2f}")

        for _ in range(100):
            brkga.evolve_population(0)
        self.assertEqual(brkga.get_best_fitness(), results["fitness102"])
        self.assertEqual(brkga.get_best_chromosome(), results["chromosome102"])
        print(f"Elapsed time: {time() - self.start_time :.2f}")

    ###########################################################################

    def test_evolve_population2(self):
        """
        Tests evolve_population() method.
        """
        ########################
        # Test the evolutionary mechanism
        ########################
        # **NOTE:** this test may fail with the random number generation
        # changes. In such case, we have to figure out how to make this test
        # better.
        ########################
        # Data 2

        with open(os.path.join(STATE_DIR, "state2.pickle"), "rb") as hd:
            brkga = pickle.load(hd)

        with open(os.path.join(SOLUTION_DIR, "best_solution2.pickle"), "rb") as hd:
            results = pickle.load(hd)

        brkga.evolve_population(0)
        self.assertEqual(brkga.get_best_fitness(), results["fitness1"])
        self.assertEqual(brkga.get_best_chromosome(), results["chromosome1"])
        print(f"Elapsed time: {time() - self.start_time :.2f}")

        brkga.evolve_population(1)
        self.assertEqual(brkga.get_best_fitness(), results["fitness2"])
        self.assertEqual(brkga.get_best_chromosome(), results["chromosome2"])
        print(f"Elapsed time: {time() - self.start_time :.2f}")

        for _ in range(100):
            brkga.evolve_population(0)
            brkga.evolve_population(1)
        self.assertEqual(brkga.get_best_fitness(), results["fitness102"])
        self.assertEqual(brkga.get_best_chromosome(), results["chromosome102"])
        print(f"Elapsed time: {time() - self.start_time :.2f}")

    ###########################################################################

    def test_evolve_population3(self):
        """
        Tests evolve_population() method.
        """
        ########################
        # Test the evolutionary mechanism
        ########################
        # **NOTE:** this test may fail with the random number generation
        # changes. In such case, we have to figure out how to make this test
        # better.
        ########################
        # Data 3

        with open(os.path.join(STATE_DIR, "state3.pickle"), "rb") as hd:
            brkga = pickle.load(hd)

        with open(os.path.join(SOLUTION_DIR, "best_solution3.pickle"), "rb") as hd:
            results = pickle.load(hd)

        for i in range(brkga.params.num_independent_populations):
            brkga.evolve_population(i)

        self.assertEqual(brkga.get_best_fitness(), results["fitness1"])
        self.assertEqual(brkga.get_best_chromosome(), results["chromosome1"])

        for i in range(brkga.params.num_independent_populations):
            brkga.evolve_population(i)
        self.assertEqual(brkga.get_best_fitness(), results["fitness2"])
        self.assertEqual(brkga.get_best_chromosome(), results["chromosome2"])
        print(f"Elapsed time: {time() - self.start_time :.2f}")

        for _ in range(100):
            for i in range(brkga.params.num_independent_populations):
                brkga.evolve_population(i)
        self.assertEqual(brkga.get_best_fitness(), results["fitness102"])
        self.assertEqual(brkga.get_best_chromosome(), results["chromosome102"])
        print(f"Elapsed time: {time() - self.start_time :.2f}")

    ###########################################################################

    def test_evolve_population4(self):
        """
        Tests evolve_population() method.
        """
        ########################
        # Test the evolutionary mechanism
        ########################
        # **NOTE:** this test may fail with the random number generation
        # changes. In such case, we have to figure out how to make this test
        # better.
        ########################
        # Data 4 (traditional BRKGA)

        with open(os.path.join(STATE_DIR, "state4.pickle"), "rb") as hd:
            brkga = pickle.load(hd)

        with open(os.path.join(SOLUTION_DIR, "best_solution4.pickle"), "rb") as hd:
            results = pickle.load(hd)

        brkga.evolve_population(0)
        self.assertEqual(brkga.get_best_fitness(), results["fitness1"])
        self.assertEqual(brkga.get_best_chromosome(), results["chromosome1"])
        print(f"Elapsed time: {time() - self.start_time :.2f}")

        brkga.evolve_population(1)
        self.assertEqual(brkga.get_best_fitness(), results["fitness2"])
        self.assertEqual(brkga.get_best_chromosome(), results["chromosome2"])
        print(f"Elapsed time: {time() - self.start_time :.2f}")

        brkga.evolve_population(2)
        self.assertEqual(brkga.get_best_fitness(), results["fitness3"])
        self.assertEqual(brkga.get_best_chromosome(), results["chromosome3"])
        print(f"Elapsed time: {time() - self.start_time :.2f}")

        for _ in range(100):
            brkga.evolve_population(0)
            brkga.evolve_population(1)
            brkga.evolve_population(2)
        self.assertEqual(brkga.get_best_fitness(), results["fitness103"])
        self.assertEqual(brkga.get_best_chromosome(), results["chromosome103"])
        print(f"Elapsed time: {time() - self.start_time :.2f}")

    ###########################################################################

    def test_evolve(self):
        """
        Tests evolve() method.
        """

        param_values = deepcopy(self.default_param_values)
        brkga_params = param_values["params"]
        brkga = BrkgaMpIpr(**param_values)

        # Not initialized
        with self.assertRaises(RuntimeError) as context:
            brkga.evolve()
        self.assertEqual(str(context.exception).strip(),
                         "The algorithm hasn't been initialized. "
                         "Call 'initialize()' before 'evolve()'")

        brkga.initialize()

        with self.assertRaises(ValueError) as context:
            brkga.evolve(-1)
        self.assertEqual(str(context.exception).strip(),
                         "Number of generations must be large than one. "
                         "Given -1")

        with open(os.path.join(STATE_DIR, "state5.pickle"), "rb") as hd:
            brkga = pickle.load(hd)

        with open(os.path.join(SOLUTION_DIR, "best_solution5.pickle"), "rb") as hd:
            results = pickle.load(hd)

        brkga.evolve()
        self.assertEqual(brkga.get_best_fitness(), results["fitness1"])
        self.assertEqual(brkga.get_best_chromosome(), results["chromosome1"])
        print(f"Elapsed time: {time() - self.start_time :.2f}")

        brkga.evolve(10)
        self.assertEqual(brkga.get_best_fitness(), results["fitness10"])
        self.assertEqual(brkga.get_best_chromosome(), results["chromosome10"])
        print(f"Elapsed time: {time() - self.start_time :.2f}")

        brkga.evolve(100)
        self.assertEqual(brkga.get_best_fitness(), results["fitness100"])
        self.assertEqual(brkga.get_best_chromosome(), results["chromosome100"])
        print(f"Elapsed time: {time() - self.start_time :.2f}")

###############################################################################

if __name__ == "__main__":
    unittest.main()
