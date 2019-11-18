###############################################################################
# tsp_instance.py: data structures and support function to deal with instances
# of the Traveling Salesman Problem.
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

from brkga_mp_ipr.exceptions import LoadError

class TSPInstance():
    """
    Represents an instance for the Traveling Salesman Problem. The constructor
    loads a upper triangular matrix as following:

        number of nodes (n)
        dist12 dist13 dist14 ... dist1n
        dist23 dist24 ... dist2(n - 1)
        ...
        dist(n-2)(n-1)

    For example, for n = 4 we have

        4
        12 13 14
        23 24
        34
    """

    def __init__(self, filename: str):
        """
        Initializes the instance loading from a file.
        """

        with open(filename, "r") as hd:
            lines = hd.readlines()

        if not lines:
            raise LoadError(f"Cannot read file '{filename}'")

        line_number = 1
        try:
            self.num_nodes = int(lines[0])

            matrix_size = (self.num_nodes * (self.num_nodes - 1)) / 2
            self.distances = []

            for i in range(1, self.num_nodes):
                line_number = i + 1
                values = [float(x.strip()) for x in lines[i].split()]
                self.distances.extend(values)
        except Exception:
            raise LoadError(f"Error reading line {line_number} of '{filename}'")

    ###########################################################################

    def distance(self, i: int, j: int) -> float:
        """
        Returns the distance between nodes `i` and `j`.
        """
        if i > j:
            i, j = j, i
        return self.distances[(i * (self.num_nodes - 1)) - ((i - 1) * i // 2) +
                              (j - i - 1)]
