"""
test_types.py: Tests for types.

(c) Copyright 2019, Carlos Eduardo de Andrade. All Rights Reserved.

This code is released under LICENSE.md.

Created on:  Nov 06, 2019 by ceandrade
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

import unittest
from brkga_mp_ipr.types import *

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

    ###########################################################################

    def test_BrkgaParams(self):
        """
        Tests BrkgaParams constructor.
        """

        brkga_params = BrkgaParams()

        self.assertEqual(brkga_params.population_size, 0)
        self.assertEqual(brkga_params.elite_percentage, 0.0)
        self.assertEqual(brkga_params.mutants_percentage, 0.0)
        self.assertEqual(brkga_params.num_elite_parents, 0)
        self.assertEqual(brkga_params.total_parents, 0)
        self.assertEqual(brkga_params.bias_type, BiasFunctionType.CONSTANT)
        self.assertEqual(brkga_params.num_independent_populations, 0)
        self.assertEqual(brkga_params.pr_number_pairs, 0)
        self.assertEqual(brkga_params.pr_minimum_distance, 0.0)
        self.assertEqual(brkga_params.pr_type, PathRelinkingType.DIRECT)
        self.assertEqual(brkga_params.pr_selection, PathRelinkingSelection.BESTSOLUTION)
        self.assertEqual(brkga_params.alpha_block_size, 0.0)
        self.assertEqual(brkga_params.pr_percentage, 0.0)

    ###########################################################################

    def test_ExternalControlParams(self):
        """
        Tests ExternalControlParams constructor.
        """

        extra_params = ExternalControlParams()
        self.assertEqual(extra_params.exchange_interval, 0)
        self.assertEqual(extra_params.num_exchange_indivuduals, 0)
        self.assertEqual(extra_params.reset_interval, 0)

        extra_params = ExternalControlParams(10, 20, 30)
        self.assertEqual(extra_params.exchange_interval, 10)
        self.assertEqual(extra_params.num_exchange_indivuduals, 20)
        self.assertEqual(extra_params.reset_interval, 30)

        extra_params = ExternalControlParams(
            exchange_interval = 30,
            num_exchange_indivuduals = 10,
            reset_interval = 20
        )
        self.assertEqual(extra_params.exchange_interval, 30)
        self.assertEqual(extra_params.num_exchange_indivuduals, 10)
        self.assertEqual(extra_params.reset_interval, 20)

    ###########################################################################

    def test_BaseChromosome(self):
        """
        Tests BaseChromosome constructor.
        """

        tmp = BaseChromosome([1, 2, 3])
        self.assertEqual(tmp, [1, 2, 3])

        class SchedulingChromosome(BaseChromosome):
            def __init__(self, value):
                super().__init__(value)
                self.makespan = 0.0
                self.total_completion_time = 0.0

        tmp = SchedulingChromosome([1, 2, 3])
        self.assertEqual(tmp, [1, 2, 3])
        self.assertEqual(tmp.makespan, 0.0)
        self.assertEqual(tmp.total_completion_time, 0.0)

    ###########################################################################

    def test_Population(self):
        """
        Tests BaseChromosome constructor.
        """

        pop1 = Population()
        self.assertEqual(pop1.chromosomes, list())
        self.assertEqual(pop1.fitness, list())

        pop1.chromosomes = [1, 2, 3]
        pop1.fitness = [(1, 10), (2, 20), (3, 30)]
        pop2 = Population(pop1)

        self.assertIsNot(pop1, pop2)
        self.assertEqual(pop1.chromosomes, pop2.chromosomes)
        self.assertIsNot(pop1.chromosomes, pop2.chromosomes)
        self.assertEqual(pop1.fitness, pop2.fitness)
        self.assertIsNot(pop1.fitness, pop2.fitness)


###############################################################################

if __name__ == "__main__":
    unittest.main()
