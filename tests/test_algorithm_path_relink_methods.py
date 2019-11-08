"""
test_algorithm_path_relink_methods.py.py: Tests the path relink methods.

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

    def test__direct_path_relink(self):
        """
        Tests _direct_path_relink() method.
        """

        brkga = BRKGA_MP_IPR()
        self.assertRaises(NotImplementedError, brkga._direct_path_relink,
            None, None, None, None, 0, 0, 0.0)

    ###########################################################################

    def test__permutation_based_path_relink(self):
        """
        Tests _permutation_based_path_relink() method.
        """

        brkga = BRKGA_MP_IPR()
        self.assertRaises(NotImplementedError, brkga._permutation_based_path_relink,
            None, None, None, None, 0, 0, 0.0)

    ###########################################################################

    def test_path_relink(self):
        """
        Tests path_relink() method.
        """

        brkga = BRKGA_MP_IPR()
        self.assertRaises(NotImplementedError, brkga.path_relink,
            None, None, None, 0, 0.0)

###############################################################################

if __name__ == "__main__":
    unittest.main()