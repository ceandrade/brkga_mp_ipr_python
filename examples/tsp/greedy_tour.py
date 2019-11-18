################################################################################
# greedy_tour.py: Simple greedy TSP tour linking the closest nodes in sequence.
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
################################################################################

from typing import List, Tuple

from tsp_instance import TSPInstance

"""
    function greedy_tour(instance::TSP_Instance)::Array{Int64, 1}

Build a greedy Traveling Salesman Problem tour starting from node 1.

# Returns
The tour cost and a permutation of the nodes representing it.
"""
def greedy_tour(instance: TSPInstance) -> Tuple[float, List]:
    """
    Builds a greedy Traveling Salesman Problem tour starting from node 0.

    Args:
        instance: a TSP instance.

    Returns:
        A tuple with the tour cost and a permutation of the nodes
        representing it.
    """

    tour = [0] * instance.num_nodes
    tour[0] = 0
    remaining_nodes = set(range(1, instance.num_nodes))

    INF = max(instance.distances) + 10.0
    cost = 0.0
    current_node = 0
    next_node = 0
    idx = 1
    while len(remaining_nodes) > 0:
        best_dist = INF
        for j in remaining_nodes:
            dist = instance.distance(current_node, j)
            if dist < best_dist:
                best_dist = dist
                next_node = j

        cost += best_dist
        tour[idx] = next_node
        remaining_nodes.remove(next_node)
        current_node = next_node
        idx += 1
    # end while

    cost += instance.distance(tour[0], tour[-1])
    return (cost, tour)
