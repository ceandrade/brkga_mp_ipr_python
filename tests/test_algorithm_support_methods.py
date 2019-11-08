"""
test_algorithm_support_methods.py: Tests the support methods.

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

import unittest

from brkga_mp_ipr.algorithm import BRKGA_MP_IPR

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

    def test_get_current_population(self):
        """
        Tests get_current_population() method.
        """

        brkga = BRKGA_MP_IPR()
        self.assertRaises(NotImplementedError, brkga.get_current_population, 0)

    ###########################################################################

    def test_get_best_chromosome(self):
        """
        Tests get_best_chromosome() method.
        """

        brkga = BRKGA_MP_IPR()
        self.assertRaises(NotImplementedError, brkga.get_best_chromosome)

    ###########################################################################

    def test_get_best_fitness(self):
        """
        Tests get_best_fitness() method.
        """

        brkga = BRKGA_MP_IPR()
        self.assertRaises(NotImplementedError, brkga.get_best_fitness)

    ###########################################################################

    def test_get_chromosome(self):
        """
        Tests get_chromosome() method.
        """

        brkga = BRKGA_MP_IPR()
        self.assertRaises(NotImplementedError, brkga.get_chromosome, 0, 0)


###############################################################################

if __name__ == "__main__":
    unittest.main()