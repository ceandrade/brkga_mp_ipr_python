"""
types.py: Definitions of internal data structures and external API.

(c) Copyright 2019, Carlos Eduardo de Andrade. All Rights Reserved.

This code is released under LICENSE.md.

Created on:  Nov 05, 2019 by ceandrade
Last update: Nov 05, 2019 by ceandrade

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

from enum import Enum, Flag, unique

###############################################################################
# Enumerations
###############################################################################

@unique
class Sense(Enum):
    """
    Tells the algorithm either to `MINIMIZE` or `MAXIMIZE` the
    objective function.
    """
    MINIMIZE = 0
    MAXIMIZE = 1

###############################################################################

@unique
class BiasFunction(Enum):
    """
    Specifies a bias function when choosing parents to mating. This function
    substitutes the ``\\rho`` (rho) parameter from the original BRKGA.
    For a given rank ``r``, we have the following functions:

    - `CONSTANT`: 1 / number of parents for mating (all individuals have the
                    same probability)

    - `CUBIC`: ``r^{-3}``

    - `EXPONENTIAL`: ``ϵ^{-r}``

    - `LINEAR`: ``1 / r``

    - `LOGINVERSE`: ``1 / \\log(r + 1)``

    - `QUADRATIC`: ``r^{-2}``
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
class PathRelinkingType(Enum):
    """
    Specifies type of path relinking:

    - `DIRECT`: changes each key for the correspondent in the other chromosome.

    - `PERMUTATION`: switches the order of a key for that in the other
      chromosome.
    """
    DIRECT = 0
    PERMUTATION = 1

###############################################################################

@unique
class PathRelinkingSelection(Enum):
    """
    Specifies which individuals used to build the path:

    - `BESTSOLUTION`: selects, in the order, the best solution of each
      population.

    - `RANDOMELITE`: chooses uniformly random solutions from the elite sets.
    """
    BESTSOLUTION = 0
    RANDOMELITE = 1

###############################################################################

@unique
class PathRelinkingResult(Flag):
    """
    Specifies the result type/status of path relink procedure:

    - `TOO_HOMOGENEOUS`: the chromosomes among the populations are too
                         homogeneous and the path relink will not generate
                         improveded solutions.

    - `NO_IMPROVEMENT`: path relink was done but no improveded solution was
                        found.

    - `ELITE_IMPROVEMENT`: an improved solution among the elite set was found,
                           but the best solution was not improved.

    - `BEST_IMPROVEMENT`: the best solution was improved.
    """
    TOO_HOMOGENEOUS = 0
    NO_IMPROVEMENT = 1
    ELITE_IMPROVEMENT = 3
    BEST_IMPROVEMENT = 7

################################################################################

@unique
class ShakingType(Enum):
    """
    Specifies the type of shaking to be performed.

    - `CHANGE`: applies the following perturbations:
        1) Inverts the value of a random chosen, i.e., from `value` to
        `1 - value`;
        2) Assigns a random value to a random key.

    - `SWAP`: applies two swap perturbations:
        1) Swaps the values of a randomly chosen key `i` and its
        neighbor `i + 1`;
        2) Swaps values of two randomly chosen keys.
    """
    CHANGE = 0
    SWAP = 1

###############################################################################
# Data structures
###############################################################################

class BrkgaParams:
    """
    Represents the BRKGA and IPR hyper-parameters.
    """

    def __init__(self):
        """
        Initialize a BrkgaParams object.
        """

        ########################################
        # BRKGA Hyper-parameters
        ########################################

        self.population_size = 0
        """ Number of elements in the population [> 0]. """

        self.elite_percentage = 0.0
        """Percentage of individuals to become the elite set (0, 1]."""

        self.mutants_percentage = 0.0
        """Percentage of mutants to be inserted in the population."""

        self.num_elite_parents = 0
        """Number of elite parents for mating [> 0]."""

        self.total_parents = 0
        """Number of total parents for mating [> 0]."""

        self.bias_type = BiasFunction.CONSTANT
        """Type of bias that will be used."""

        self.num_independent_populations = 0
        """Number of independent parallel populations."""

        ########################################
        # Path Relinking parameters
        ########################################

        self.pr_number_pairs = 0
        """Number of pairs of chromosomes to be tested to path relinking."""

        self.pr_minimum_distance = 0.0
        """Mininum distance between chromosomes selected to path-relinking."""

        self.pr_type = PathRelinkingType.DIRECT
        """Path relinking type."""

        self.pr_selection = PathRelinkingSelection.BESTSOLUTION
        """Individual selection to path-relinking."""

        self.alpha_block_size = 0.0
        """Defines the block size based on the size of the population."""

        self.pr_percentage = 0.0
        """Percentage / path size to be computed. Value in (0, 1]."""

###############################################################################

class ExternalControlParams:
    """
    Represents additional control parameters that can be used outside this
    framework.
    """

    def __init__(self, exchange_interval: int = 0,
                 num_exchange_indivuduals: int = 0,
                 reset_interval: int = 0):
        """
        Initialize a ExternalControlParams object.
        """

        self.exchange_interval = exchange_interval
        """
        Interval at which elite chromosomes are exchanged
        (0 means no exchange) [> 0].
        """

        self.num_exchange_indivuduals = num_exchange_indivuduals
        """
        Number of elite chromosomes exchanged from each population [> 0].
        """

        self.reset_interval = reset_interval
        """
        Interval at which the populations are reset (0 means no reset) [> 0].
        """
