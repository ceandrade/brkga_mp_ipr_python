"""
test_algorithm_initialization.py: Tests constructor and initialization methods.

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

    def test_constructor(self):
        """
        Tests BrkgaParams constructor.
        """

        brkga = BRKGA_MP_IPR()

    ###########################################################################

    def test_set_initial_population(self):
        """
        Tests set_initial_population() method.
        """

        brkga = BRKGA_MP_IPR()
        self.assertRaises(NotImplementedError, brkga.set_initial_population, [])

    ###########################################################################

    def test_set_bias_custom_function(self):
        """
        Tests set_bias_custom_function() method.
        """

        brkga = BRKGA_MP_IPR()
        self.assertRaises(NotImplementedError, brkga.set_bias_custom_function,
                          lambda x : None)

    ###########################################################################

    def test_initialize(self):
        """
        Tests initialize() method.
        """

        brkga = BRKGA_MP_IPR()
        self.assertRaises(NotImplementedError, brkga.initialize)


###############################################################################

if __name__ == "__main__":
    unittest.main()
