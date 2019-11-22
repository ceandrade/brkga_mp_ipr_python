###############################################################################
# enums.py: Definitions of useful enumerations.
#
# (c) Copyright 2019, Carlos Eduardo de Andrade. All Rights Reserved.
#
# This code is released under LICENSE.md.
#
# Created on:  Nov 05, 2019 by ceandrade
# Last update: Nov 09, 2019 by ceandrade
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###############################################################################

from enum import Enum, Flag, unique

###############################################################################
# Enumerations
###############################################################################

class ParsingEnum(Enum):
    """
    Implements a base Enum class that returns an Enum object from a string
    (case insensitive).
    """

    @classmethod
    def _missing_(cls, name):
        """
        When the constructor cannot find the attribute, it calls this
        function. Then, we check if the string of the given name/object is in
        the attribute list of the Enum. If so, we return the attribute.
        """
        for member in cls:
            if member.name.upper() == str(name).upper():
                return member
        return None

    def __str__(self):
        """
        Just return the name instead of <name, value>.
        """
        return self.name

###############################################################################

@unique
class Sense(ParsingEnum):
    """
    Tells the algorithm either to ``MINIMIZE`` or ``MAXIMIZE`` the
    objective function.
    """
    MINIMIZE = 0
    MAXIMIZE = 1

###############################################################################

@unique
class BiasFunctionType(ParsingEnum):
    r"""
    Specifies a bias function when choosing parents to mating. This function
    substitutes the :math:`\rho` (rho) parameter from the original BRKGA.
    For a given rank :math:`r`, we have the following functions:

    - ``CONSTANT``: 1 / number of parents for mating (all individuals have the
      same probability)

    - ``CUBIC``: :math:`r^{-3}`

    - ``EXPONENTIAL``: :math:`\epsilon^{-r}`

    - ``LINEAR``: :math:`1 / r`

    - ``LOGINVERSE``: :math:`1 / \log(r + 1)`

    - ``QUADRATIC``: :math:`r^{-2}`
    """
    CONSTANT = 0
    CUBIC = 1
    EXPONENTIAL = 2
    LINEAR = 3
    LOGINVERSE = 4
    QUADRATIC = 5
    CUSTOM = 6

###############################################################################

@unique
class PathRelinkingType(ParsingEnum):
    """
    Specifies type of path relinking:

    - ``DIRECT``: changes each key for the correspondent in the other
      chromosome.

    - ``PERMUTATION``: switches the order of a key for that in the other
      chromosome.
    """
    DIRECT = 0
    PERMUTATION = 1

###############################################################################

@unique
class PathRelinkingSelection(ParsingEnum):
    """
    Specifies which individuals used to build the path:

    - ``BESTSOLUTION``: selects, in the order, the best solution of each
      population.

    - ``RANDOMELITE``: chooses uniformly random solutions from the elite sets.
    """
    BESTSOLUTION = 0
    RANDOMELITE = 1

###############################################################################

@unique
class PathRelinkingResult(Flag):
    """
    Specifies the result type/status of path relink procedure:

    - ``TOO_HOMOGENEOUS``: the chromosomes among the populations are too
      homogeneous and the path relink will not generate improveded solutions.

    - ``NO_IMPROVEMENT``: path relink was done but no improveded solution was
      found.

    - ``ELITE_IMPROVEMENT``: an improved solution among the elite set was
      found, but the best solution was not improved.

    - ``BEST_IMPROVEMENT``: the best solution was improved.
    """
    TOO_HOMOGENEOUS = 0
    NO_IMPROVEMENT = 1
    ELITE_IMPROVEMENT = 3
    BEST_IMPROVEMENT = 7

################################################################################

@unique
class ShakingType(ParsingEnum):
    """
    Specifies the type of shaking to be performed.

    - ``CHANGE``: applies the following perturbations:
        1) Inverts the value of a random chosen, i.e., from :math:`value` to
           :math:`1 - value`;
        2) Assigns a random value to a random key.

    - ``SWAP``: applies two swap perturbations:
        1) Swaps the values of a randomly chosen key :math:`i` and its
           neighbor :math:`i + 1`;
        2) Swaps values of two randomly chosen keys.
    """
    CHANGE = 0
    SWAP = 1
