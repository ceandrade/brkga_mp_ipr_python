"""
test_algorithm_population_manipulation.py: Tests the populaiton manipulation
methods.

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
from brkga_mp_ipr.enums import ShakingType
from brkga_mp_ipr.types import BaseChromosome

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

    def test_exchange_elite(self):
        """
        Tests exchange_elite() method.
        """

        brkga = BRKGA_MP_IPR()
        self.assertRaises(NotImplementedError, brkga.exchange_elite, 0)

    ###########################################################################

    def test_reset(self):
        """
        Tests reset() method.
        """

        brkga = BRKGA_MP_IPR()
        self.assertRaises(NotImplementedError, brkga.reset)

    ###########################################################################

    def test_shake(self):
        """
        Tests shake() method.
        """

        brkga = BRKGA_MP_IPR()
        self.assertRaises(NotImplementedError, brkga.shake, 0,
                          ShakingType.SWAP, 0)

    ###########################################################################

    def test_inject_chromosome(self):
        """
        Tests inject_chromosome() method.
        """

        brkga = BRKGA_MP_IPR()
        self.assertRaises(NotImplementedError, brkga.inject_chromosome,
                          BaseChromosome(), 0, 0, 0)


###############################################################################

if __name__ == "__main__":
    unittest.main()