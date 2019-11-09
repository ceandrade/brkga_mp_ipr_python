"""
test_types_io.py: Tests for I/O functions.

(c) Copyright 2019, Carlos Eduardo de Andrade. All Rights Reserved.

This code is released under LICENSE.md.

Created on:  Nov 06, 2019 by ceandrade
Last update: Nov 07, 2019 by ceandrade

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

import tempfile
import unittest

from brkga_mp_ipr.types import *
from brkga_mp_ipr.types_io import *
from tests.paths_constants import *

class Test(unittest.TestCase):
    """
    Test units for types I/O functions.
    """

    ###########################################################################

    def setUp(self):
        """
        Set up some configurations.
        """

        Test.maxDiff = None

    ###########################################################################

    def test_load_configuration(self):
        """
        Test load functions.
        """

        self.assertRaises(IsADirectoryError, load_configuration, ".")
        self.assertRaises(FileNotFoundError, load_configuration, "")

        filename = os.path.join(CONFIG_DIR, "empty.conf")
        with self.assertRaises(LoadError) as context:
            load_configuration(filename)
        self.assertEqual(str(context.exception).strip(),
                         f"Cannot read {filename}")

        filename = os.path.join(CONFIG_DIR, "unknown_param.conf")
        with self.assertRaises(LoadError) as context:
            load_configuration(filename)
        self.assertEqual(str(context.exception).strip(),
                         "Line 25: parameter 'population_sizee' unknown")

        filename = os.path.join(CONFIG_DIR, "missing_value.conf")
        with self.assertRaises(LoadError) as context:
            load_configuration(filename)
        self.assertEqual(str(context.exception).strip(),
                         "Line 25: missing parameter or value")

        filename = os.path.join(CONFIG_DIR, "wrong_type.conf")
        with self.assertRaises(LoadError) as context:
            load_configuration(filename)
        self.assertEqual(str(context.exception).strip(),
                         "Line 25: invalid value for 'population_size': 500.123")

        filename = os.path.join(CONFIG_DIR, "wrong_bias_function.conf")
        with self.assertRaises(LoadError) as context:
            load_configuration(filename)
        self.assertEqual(str(context.exception).strip(),
                         "Line 40: invalid value for 'bias_type': loginvrse")

        filename = os.path.join(CONFIG_DIR, "wrong_pr_selection.conf")
        with self.assertRaises(LoadError) as context:
            load_configuration(filename)
        self.assertEqual(str(context.exception).strip(),
                         "Line 55: invalid value for 'pr_selection': worseones")

        filename = os.path.join(CONFIG_DIR, "missing_param.conf")
        with self.assertRaises(LoadError) as context:
            load_configuration(filename)
        self.assertEqual(str(context.exception).strip(),
                         "Missing parameters: population_size, mutants_percentage, total_parents, bias_type")

        brkga_params, control_params = \
            load_configuration(os.path.join(CONFIG_DIR, "regular.conf"))

        self.assertEqual(brkga_params.population_size, 500)
        self.assertEqual(brkga_params.elite_percentage, 0.30)
        self.assertEqual(brkga_params.mutants_percentage, 0.15)
        self.assertEqual(brkga_params.num_elite_parents, 2)
        self.assertEqual(brkga_params.total_parents, 3)
        self.assertEqual(brkga_params.bias_type, BiasFunctionType.LOGINVERSE)
        self.assertEqual(brkga_params.num_independent_populations, 3)
        self.assertEqual(brkga_params.pr_number_pairs, 0)
        self.assertEqual(brkga_params.pr_minimum_distance, 0.15)
        self.assertEqual(brkga_params.pr_type, PathRelinkingType.PERMUTATION)
        self.assertEqual(brkga_params.pr_selection, PathRelinkingSelection.RANDOMELITE)
        self.assertEqual(brkga_params.alpha_block_size, 1.0)
        self.assertEqual(brkga_params.pr_percentage, 1.0)
        self.assertEqual(control_params.exchange_interval, 200)
        self.assertEqual(control_params.num_exchange_indivuduals, 2)
        self.assertEqual(control_params.reset_interval, 600)

    ###########################################################################

    def test_write_configuration(self):
        """
        Test write functions.
        """

        #########################
        # From config file
        #########################

        brkga_params, control_params = \
            load_configuration(os.path.join(CONFIG_DIR, "regular.conf"))

        self.assertRaises(PermissionError, write_configuration,
                          "/invalid", brkga_params, control_params)

        self.assertRaises(IsADirectoryError, write_configuration,
                          ".", brkga_params, control_params)

        tmp = tempfile.NamedTemporaryFile(mode="r")
        write_configuration(tmp.name, brkga_params, control_params)

        tmp.seek(0)
        result = tmp.read().lower()
        tmp.close()

        standard = """population_size 500
elite_percentage 0.3
mutants_percentage 0.15
num_elite_parents 2
total_parents 3
bias_type loginverse
num_independent_populations 3
pr_number_pairs 0
pr_minimum_distance 0.15
pr_type permutation
pr_selection randomelite
alpha_block_size 1.0
pr_percentage 1.0
exchange_interval 200
num_exchange_indivuduals 2
reset_interval 600
"""
        self.assertEqual(result, standard)

        #########################
        # TODO: From direct building
        #########################

###############################################################################

if __name__ == "__main__":
    unittest.main()
