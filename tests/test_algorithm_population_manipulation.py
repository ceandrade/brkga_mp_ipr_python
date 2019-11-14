"""
test_algorithm_population_manipulation.py: Tests the populaiton manipulation
methods.

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

    def test_exchange_elite(self):
        """
        Tests exchange_elite() method.
        """

        param_values = deepcopy(self.default_param_values)
        brkga = BrkgaMpIpr(**param_values)
        self.assertRaises(NotImplementedError, brkga.exchange_elite, 0)

    ###########################################################################

    def test_reset(self):
        """
        Tests reset() method.
        """

        param_values = deepcopy(self.default_param_values)
        params = param_values["params"]
        brkga = BrkgaMpIpr(**param_values)

        with self.assertRaises(RuntimeError) as context:
            brkga.reset()
        self.assertEqual(str(context.exception).strip(),
                         "The algorithm hasn't been initialized. "
                         "Call 'initialize()' before 'reset()'")

        brkga.initialize()

        # Create a local RNG and advance it until the same state as the
        # internal BRKGA RNG after initialization.
        local_rng = Random(param_values["seed"])
        skip = 1000 + params.num_independent_populations * \
               params.population_size * brkga.chromosome_size
        for _ in range(skip):
            local_rng.random()

        # Assert the both generators are in the same state.
        self.assertEqual(brkga._rng.getstate(), local_rng.getstate())

        # Create a local chromosome and applied the decoder on it.
        local_chr = BaseChromosome([
            local_rng.random() for _ in range(param_values["chromosome_size"])
        ])
        param_values["decoder"].decode(local_chr, rewrite=True)

        # Reset and test the first individual.
        brkga.reset()
        self.assertEqual(brkga._current_populations[0].chromosomes[0],
                         local_chr)

        # After reset, the reset phase flag should be deactivated.
        self.assertFalse(brkga._reset_phase)

    ###########################################################################

    def test_shake(self):
        """
        Tests shake() method.
        """

        param_values = deepcopy(self.default_param_values)
        brkga = BrkgaMpIpr(**param_values)
        self.assertRaises(NotImplementedError, brkga.shake, 0,
                          ShakingType.SWAP, 0)

    ###########################################################################

    def test_inject_chromosome(self):
        """
        Tests inject_chromosome() method.
        """

        param_values = deepcopy(self.default_param_values)
        brkga = BrkgaMpIpr(**param_values)
        self.assertRaises(NotImplementedError, brkga.inject_chromosome,
                          BaseChromosome(), 0, 0, 0)


###############################################################################

if __name__ == "__main__":
    unittest.main()