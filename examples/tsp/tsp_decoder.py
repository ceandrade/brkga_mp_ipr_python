###############################################################################
# tsp_decoder.py: simple permutation decoder for the Traveling Salesman Problem.
#
# (c) Copyright 2019, Carlos Eduardo de Andrade. All Rights Reserved.
#
# This code is released under LICENSE.md.
#
# Created on:  Nov 18, 2019 by ceandrade
# Last update: Nov 18, 2019 by ceandrade
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

from brkga_mp_ipr.types import BaseChromosome
from tsp_instance import TSPInstance

class TSPDecoder():
    """
    Simple Traveling Salesman Problem decoder. It creates a permutation of
    nodes induced by the chromosome and computes the cost of the tour.
    """

    def __init__(self, instance: TSPInstance):
        self.instance = instance

    ###########################################################################

    def decode(self, chromosome: BaseChromosome, rewrite: bool) -> float:
        """
        Given a chromossome, builds a tour.

        Note that in this example, ``rewrite`` has not been used.
        """

        permutation = sorted(
            (key, index) for index, key in enumerate(chromosome)
        )

        cost = self.instance.distance(permutation[0][1], permutation[-1][1])
        for i in range(len(permutation) - 1):
            cost += self.instance.distance(permutation[i][1],
                                           permutation[i + 1][1])
        return cost
