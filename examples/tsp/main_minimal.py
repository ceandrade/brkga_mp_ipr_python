###############################################################################
# main_minimal.py: minimal script for calling BRKGA algorithms to solve
#                  instances of the Traveling Salesman Problem.
#
# (c) Copyright 2019, Carlos Eduardo de Andrade.
# All Rights Reserved.
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

import sys

from brkga_mp_ipr.enums import Sense
from brkga_mp_ipr.types_io import load_configuration
from brkga_mp_ipr.algorithm import BrkgaMpIpr

from tsp_instance import TSPInstance
from tsp_decoder import TSPDecoder

###############################################################################

def main() -> None:
    if len(sys.argv) < 4:
        print("Usage: python main_minimal.py <seed> <config-file> "
              "<num-generations> <tsp-instance-file>")
        sys.exit(1)

    ########################################
    # Read the command-line arguments and the instance
    ########################################

    seed = int(sys.argv[1])
    configuration_file = sys.argv[2]
    num_generations = int(sys.argv[3])
    instance_file = sys.argv[4]

    print("Reading data...")
    instance = TSPInstance(instance_file)

    ########################################
    # Read algorithm parameters
    ########################################

    print("Reading parameters...")
    brkga_params, _ = load_configuration(configuration_file)

    ########################################
    # Build the BRKGA data structures and initialize
    ########################################

    print("Building BRKGA data and initializing...")

    decoder = TSPDecoder(instance)

    brkga = BrkgaMpIpr(
        decoder=decoder,
        sense=Sense.MINIMIZE,
        seed=seed,
        chromosome_size=instance.num_nodes,
        params=brkga_params
    )

    # NOTE: don't forget to initialize the algorithm.
    brkga.initialize()

    ########################################
    # Find good solutions / evolve
    ########################################

    print(f"Evolving {num_generations} generations...")
    brkga.evolve(num_generations)

    best_cost = brkga.get_best_fitness()
    print(f"Best cost: {best_cost}")

###############################################################################

if __name__ == "__main__":
    main()
