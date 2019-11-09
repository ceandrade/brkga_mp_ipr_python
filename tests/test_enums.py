"""
test_enums.py: Tests for enumerations.

(c) Copyright 2019, Carlos Eduardo de Andrade. All Rights Reserved.

This code is released under LICENSE.md.

Created on:  Nov 06, 2019 by ceandrade
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

import unittest
from brkga_mp_ipr.enums import *

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

    def test_ParsingEnum(self):
        """
        Tests ParsingEnum methods.
        """

        MyEnum = ParsingEnum('Animal', 'ANT BEE CAT DOG')

        self.assertEqual(MyEnum("ANT"), MyEnum.ANT)
        self.assertEqual(MyEnum("ant"), MyEnum.ANT)
        self.assertEqual(str(MyEnum.ANT), "ANT")

        self.assertEqual(MyEnum("BEE"), MyEnum.BEE)
        self.assertEqual(MyEnum("bEe"), MyEnum.BEE)
        self.assertEqual(str(MyEnum.BEE), "BEE")

    ###########################################################################

    def test_Sense(self):
        """
        Tests Sense constructor.
        """

        self.assertEqual(Sense(Sense.MINIMIZE), Sense.MINIMIZE)
        self.assertEqual(Sense(Sense.MAXIMIZE), Sense.MAXIMIZE)
        self.assertEqual(Sense(0), Sense.MINIMIZE)
        self.assertEqual(Sense(1), Sense.MAXIMIZE)
        self.assertEqual(Sense("MINIMIZE"), Sense.MINIMIZE)
        self.assertEqual(Sense("MAXIMIZE"), Sense.MAXIMIZE)
        self.assertEqual(Sense("minimize"), Sense.MINIMIZE)
        self.assertEqual(Sense("maximize"), Sense.MAXIMIZE)
        self.assertRaises(ValueError, Sense, "min")
        self.assertRaises(ValueError, Sense, "max")
        self.assertRaises(ValueError, Sense, -1)
        self.assertRaises(ValueError, Sense, 3)

    ###########################################################################

    def test_BiasFunctionType(self):
        """
        Tests BiasFunction constructor.
        """

        self.assertEqual(BiasFunctionType("CONSTANT"), BiasFunctionType.CONSTANT)
        self.assertEqual(BiasFunctionType("constant"), BiasFunctionType.CONSTANT)
        self.assertEqual(BiasFunctionType("CUBIC"), BiasFunctionType.CUBIC)
        self.assertEqual(BiasFunctionType("cubic"), BiasFunctionType.CUBIC)
        self.assertEqual(BiasFunctionType("EXPONENTIAL"), BiasFunctionType.EXPONENTIAL)
        self.assertEqual(BiasFunctionType("exponential"), BiasFunctionType.EXPONENTIAL)
        self.assertEqual(BiasFunctionType("LINEAR"), BiasFunctionType.LINEAR)
        self.assertEqual(BiasFunctionType("linear"), BiasFunctionType.LINEAR)
        self.assertEqual(BiasFunctionType("LOGINVERSE"), BiasFunctionType.LOGINVERSE)
        self.assertEqual(BiasFunctionType("loginverse"), BiasFunctionType.LOGINVERSE)
        self.assertEqual(BiasFunctionType("QUADRATIC"), BiasFunctionType.QUADRATIC)
        self.assertEqual(BiasFunctionType("quadratic"), BiasFunctionType.QUADRATIC)
        self.assertEqual(BiasFunctionType("CUSTOM"), BiasFunctionType.CUSTOM)
        self.assertEqual(BiasFunctionType("custom"), BiasFunctionType.CUSTOM)

        self.assertRaises(ValueError, BiasFunctionType, "invalid")
        self.assertRaises(ValueError, BiasFunctionType, -1)

    ###########################################################################

    def test_PathRelinkingType(self):
        """
        Tests PathRelinkingType constructor.
        """

        self.assertEqual(PathRelinkingType("DIRECT"), PathRelinkingType.DIRECT)
        self.assertEqual(PathRelinkingType("direct"), PathRelinkingType.DIRECT)
        self.assertEqual(PathRelinkingType("PERMUTATION"), PathRelinkingType.PERMUTATION)
        self.assertEqual(PathRelinkingType("permutation"), PathRelinkingType.PERMUTATION)

        self.assertRaises(ValueError, PathRelinkingType, "invalid")
        self.assertRaises(ValueError, PathRelinkingType, -1)

    ###########################################################################

    def test_PathRelinkingSelection(self):
        """
        Tests PathRelinkingSelection constructor.
        """

        self.assertEqual(PathRelinkingSelection("BESTSOLUTION"), PathRelinkingSelection.BESTSOLUTION)
        self.assertEqual(PathRelinkingSelection("bestsolution"), PathRelinkingSelection.BESTSOLUTION)
        self.assertEqual(PathRelinkingSelection("RANDOMELITE"), PathRelinkingSelection.RANDOMELITE)
        self.assertEqual(PathRelinkingSelection("randomelite"), PathRelinkingSelection.RANDOMELITE)

        self.assertRaises(ValueError, PathRelinkingSelection, "invalid")
        self.assertRaises(ValueError, PathRelinkingSelection, -1)

    ###########################################################################

    def test_PathRelinkingResult(self):
        """
        Tests PathRelinkingResult bitwise operations.
        """

        PRR = PathRelinkingResult
        self.assertEqual(PRR.TOO_HOMOGENEOUS | PRR.TOO_HOMOGENEOUS, PRR.TOO_HOMOGENEOUS)
        self.assertEqual(PRR.TOO_HOMOGENEOUS | PRR.NO_IMPROVEMENT, PRR.NO_IMPROVEMENT)
        self.assertEqual(PRR.TOO_HOMOGENEOUS | PRR.ELITE_IMPROVEMENT, PRR.ELITE_IMPROVEMENT)
        self.assertEqual(PRR.TOO_HOMOGENEOUS | PRR.BEST_IMPROVEMENT, PRR.BEST_IMPROVEMENT)
        self.assertEqual(PRR.NO_IMPROVEMENT | PRR.NO_IMPROVEMENT, PRR.NO_IMPROVEMENT)
        self.assertEqual(PRR.NO_IMPROVEMENT | PRR.ELITE_IMPROVEMENT, PRR.ELITE_IMPROVEMENT)
        self.assertEqual(PRR.NO_IMPROVEMENT | PRR.BEST_IMPROVEMENT, PRR.BEST_IMPROVEMENT)
        self.assertEqual(PRR.ELITE_IMPROVEMENT | PRR.ELITE_IMPROVEMENT, PRR.ELITE_IMPROVEMENT)
        self.assertEqual(PRR.ELITE_IMPROVEMENT | PRR.BEST_IMPROVEMENT, PRR.BEST_IMPROVEMENT)
        self.assertEqual(PRR.BEST_IMPROVEMENT | PRR.BEST_IMPROVEMENT, PRR.BEST_IMPROVEMENT)

    ###########################################################################

    def test_ShakingType(self):
        """
        Tests ShakingType constructor.
        """

        self.assertEqual(ShakingType("CHANGE"), ShakingType.CHANGE)
        self.assertEqual(ShakingType("change"), ShakingType.CHANGE)
        self.assertEqual(ShakingType("SWAP"), ShakingType.SWAP)
        self.assertEqual(ShakingType("swap"), ShakingType.SWAP)

        self.assertRaises(ValueError, ShakingType, "invalid")
        self.assertRaises(ValueError, ShakingType, -1)

###############################################################################

if __name__ == "__main__":
    unittest.main()
