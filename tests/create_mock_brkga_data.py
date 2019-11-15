###############################################################################
# create_mock_brkga_data.py: create BRKGA data mock object to be used in
# the evolutionary tests.
#
# (c) Copyright 2019, Carlos Eduardo de Andrade. All Rights Reserved.
#
# This code is released under LICENSE.md.
#
# Created on:  Nov 15, 2019 by ceandrade
# Last update: Nov 15, 2019 by ceandrade
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

from copy import deepcopy
from random import Random
from time import time
import dill as pickle
import math

from brkga_mp_ipr.algorithm import BrkgaMpIpr
from brkga_mp_ipr.enums import *
from brkga_mp_ipr.types import BaseChromosome, BrkgaParams
from brkga_mp_ipr.types_io import load_configuration

from tests.instance import Instance
from tests.decoders import SumDecode, RankDecode
from tests.paths_constants import *

###############################################################################

chromosome_size = 100
default_brkga_params = BrkgaParams()
default_brkga_params.population_size = 10
default_brkga_params.elite_percentage = 0.3
default_brkga_params.mutants_percentage = 0.1
default_brkga_params.num_elite_parents = 1
default_brkga_params.total_parents = 2
default_brkga_params.bias_type = BiasFunctionType.LOGINVERSE
default_brkga_params.num_independent_populations = 3
default_brkga_params.pr_number_pairs = 0
default_brkga_params.pr_minimum_distance = 0.0
default_brkga_params.pr_type = PathRelinkingType.DIRECT
default_brkga_params.pr_selection = PathRelinkingSelection.BESTSOLUTION
default_brkga_params.alpha_block_size = 1.0
default_brkga_params.pr_percentage = 1.0

instance = Instance(chromosome_size)
sum_decoder = SumDecode(instance)
rank_decoder = RankDecode(instance)

default_param_values = {
    "decoder": sum_decoder,
    "sense": Sense.MAXIMIZE,
    "seed": 98747382473209,
    "chromosome_size": chromosome_size,
    "params": default_brkga_params,
    "evolutionary_mechanism_on": True,
    "chrmosome_type": BaseChromosome
}

###############################################################################
# Configuration 1
###############################################################################

def gen_conf1():
    param_values = deepcopy(default_param_values)
    brkga_params = param_values["params"]

    brkga_params.population_size = 100
    brkga_params.elite_percentage = 0.3
    brkga_params.mutants_percentage = 0.1
    brkga_params.num_elite_parents = 1
    brkga_params.total_parents = 2
    brkga_params.bias_type = BiasFunctionType.LOGINVERSE
    brkga_params.num_independent_populations = 1
    brkga_params.pr_number_pairs = 0
    brkga_params.pr_minimum_distance = 0.0
    brkga_params.pr_type = PathRelinkingType.DIRECT
    brkga_params.pr_selection = PathRelinkingSelection.BESTSOLUTION
    brkga_params.alpha_block_size = 1.0
    brkga_params.pr_percentage = 1.0

    param_values["decoder"] = sum_decoder
    param_values["sense"] = Sense.MAXIMIZE
    param_values["seed"] = 4013750229
    param_values["chromosome_size"] = chromosome_size
    param_values["evolutionary_mechanism_on"] = True

    print("\n> Building configuration 1")
    brkga = BrkgaMpIpr(**param_values)
    brkga.initialize()

    print("> Writing configuration 1")
    with open(os.path.join(STATE_DIR, "state1.pickle"), "wb") as hd:
        pickle.dump(brkga, hd)

    print("> Evolving population 0")

    brkga.evolve_population(0)
    fitness1 = brkga.get_best_fitness()
    chromosome1 = brkga.get_best_chromosome()

    brkga.evolve_population(0)
    fitness2 = brkga.get_best_fitness()
    chromosome2 = brkga.get_best_chromosome()

    for _ in range(100):
        brkga.evolve_population(0)
    fitness102 = brkga.get_best_fitness()
    chromosome102 = brkga.get_best_chromosome()

    with open(os.path.join(SOLUTION_DIR, "best_solution1.pickle"), "wb") as hd:
        pickle.dump(
            {
                "fitness1": fitness1,
                "chromosome1": chromosome1,
                "fitness2": fitness2,
                "chromosome2": chromosome2,
                "fitness102": fitness102,
                "chromosome102": chromosome102,
            },
            hd
        )

###############################################################################
# Configuration 2
###############################################################################

def gen_conf2():
    param_values = deepcopy(default_param_values)
    brkga_params = param_values["params"]

    chromosome_size = 1000
    instance = Instance(chromosome_size)

    brkga_params.population_size = 500
    brkga_params.elite_percentage = 0.25
    brkga_params.mutants_percentage = 0.25
    brkga_params.num_elite_parents = 5
    brkga_params.total_parents = 50
    brkga_params.bias_type = BiasFunctionType.QUADRATIC
    brkga_params.num_independent_populations = 2
    brkga_params.pr_number_pairs = 0
    brkga_params.pr_minimum_distance = 0.0
    brkga_params.pr_type = PathRelinkingType.DIRECT
    brkga_params.pr_selection = PathRelinkingSelection.BESTSOLUTION
    brkga_params.alpha_block_size = 1.0
    brkga_params.pr_percentage = 1.0

    param_values["decoder"] = RankDecode(instance)
    param_values["sense"] = Sense.MINIMIZE
    param_values["seed"] = 1297832326904308
    param_values["chromosome_size"] = chromosome_size
    param_values["evolutionary_mechanism_on"] = True

    print("\n> Building configuration 2")
    brkga = BrkgaMpIpr(**param_values)
    brkga.initialize()

    print("> Writing configuration 2")
    with open(os.path.join(STATE_DIR, "state2.pickle"), "wb") as hd:
        pickle.dump(brkga, hd)

    print("> Evolving population 0...")
    brkga.evolve_population(0)
    fitness1 = brkga.get_best_fitness()
    chromosome1 = brkga.get_best_chromosome()

    print("> Evolving population 1...")
    brkga.evolve_population(1)
    fitness2 = brkga.get_best_fitness()
    chromosome2 = brkga.get_best_chromosome()

    print("> Evolving both populations for 100 generations...")
    for _ in range(100):
        start_time = time()
        brkga.evolve_population(0)
        brkga.evolve_population(1)
        print(f"Elapsed time: {time() - start_time :.2f}")

    fitness102 = brkga.get_best_fitness()
    chromosome102 = brkga.get_best_chromosome()

    with open(os.path.join(SOLUTION_DIR, "best_solution2.pickle"), "wb") as hd:
        pickle.dump(
            {
                "fitness1": fitness1,
                "chromosome1": chromosome1,
                "fitness2": fitness2,
                "chromosome2": chromosome2,
                "fitness102": fitness102,
                "chromosome102": chromosome102,
            },
            hd
        )

###############################################################################
# Configuration 3
###############################################################################

def gen_conf3():
    param_values = deepcopy(default_param_values)
    brkga_params = param_values["params"]

    chromosome_size = 500
    instance = Instance(chromosome_size)

    brkga_params.population_size = 100
    brkga_params.elite_percentage = 0.35
    brkga_params.mutants_percentage = 0.17
    brkga_params.num_elite_parents = 3
    brkga_params.total_parents = 5
    brkga_params.bias_type = BiasFunctionType.EXPONENTIAL
    brkga_params.num_independent_populations = 5
    brkga_params.pr_number_pairs = 0
    brkga_params.pr_minimum_distance = 0.0
    brkga_params.pr_type = PathRelinkingType.DIRECT
    brkga_params.pr_selection = PathRelinkingSelection.BESTSOLUTION
    brkga_params.alpha_block_size = 1.0
    brkga_params.pr_percentage = 1.0

    param_values["decoder"] = SumDecode(instance)
    param_values["sense"] = Sense.MINIMIZE
    param_values["seed"] = 253624607406
    param_values["chromosome_size"] = chromosome_size
    param_values["evolutionary_mechanism_on"] = True

    print("\n> Building configuration 3")
    brkga = BrkgaMpIpr(**param_values)
    brkga.initialize()

    print("> Writing configuration 3")
    with open(os.path.join(STATE_DIR, "state3.pickle"), "wb") as hd:
        pickle.dump(brkga, hd)

    print("> Evolving both populations for one generation...")
    for i in range(brkga_params.num_independent_populations):
        brkga.evolve_population(i)
    fitness1 = brkga.get_best_fitness()
    chromosome1 = brkga.get_best_chromosome()

    print("> Evolving both populations for another generation...")
    for i in range(brkga_params.num_independent_populations):
        brkga.evolve_population(i)
    brkga.evolve_population(1)
    fitness2 = brkga.get_best_fitness()
    chromosome2 = brkga.get_best_chromosome()

    print("> Evolving both populations for 100 generations...")
    for _ in range(100):
        start_time = time()
        for i in range(brkga_params.num_independent_populations):
            brkga.evolve_population(i)
        print(f"Elapsed time: {time() - start_time :.2f}")

    fitness102 = brkga.get_best_fitness()
    chromosome102 = brkga.get_best_chromosome()

    with open(os.path.join(SOLUTION_DIR, "best_solution3.pickle"), "wb") as hd:
        pickle.dump(
            {
                "fitness1": fitness1,
                "chromosome1": chromosome1,
                "fitness2": fitness2,
                "chromosome2": chromosome2,
                "fitness102": fitness102,
                "chromosome102": chromosome102,
            },
            hd
        )

    print("fitness", fitness1)
    # print("chromosome", chromosome1)

    print("fitness", fitness2)
    # print("chromosome", chromosome2)

    print("fitness", fitness102)
    # print("chromosome", chromosome102)

###############################################################################
# Configuration 4 (traditional BRKGA)
###############################################################################

def gen_conf4():
    param_values = deepcopy(default_param_values)
    brkga_params = param_values["params"]

    chromosome_size = 500
    instance = Instance(chromosome_size)

    brkga_params.population_size = 100
    brkga_params.elite_percentage = 0.35
    brkga_params.mutants_percentage = 0.15
    brkga_params.num_elite_parents = 1
    brkga_params.total_parents = 2
    brkga_params.bias_type = BiasFunctionType.EXPONENTIAL
    brkga_params.num_independent_populations = 3
    brkga_params.pr_number_pairs = 0
    brkga_params.pr_minimum_distance = 0.0
    brkga_params.pr_type = PathRelinkingType.DIRECT
    brkga_params.pr_selection = PathRelinkingSelection.BESTSOLUTION
    brkga_params.alpha_block_size = 1.0
    brkga_params.pr_percentage = 1.0

    param_values["decoder"] = SumDecode(instance)
    param_values["sense"] = Sense.MINIMIZE
    param_values["seed"] = 2947804214761
    param_values["chromosome_size"] = chromosome_size
    param_values["evolutionary_mechanism_on"] = True

    print("\n> Building configuration 4")
    brkga = BrkgaMpIpr(**param_values)
    brkga.initialize()

    rho = 0.75
    brkga.set_bias_custom_function(lambda x: rho if x == 1 else 1.0 - rho)

    print("> Writing configuration 4")
    with open(os.path.join(STATE_DIR, "state4.pickle"), "wb") as hd:
        pickle.dump(brkga, hd)

    print("> Evolving population 0...")
    brkga.evolve_population(0)
    fitness1 = brkga.get_best_fitness()
    chromosome1 = brkga.get_best_chromosome()

    print("> Evolving population 1...")
    brkga.evolve_population(1)
    fitness2 = brkga.get_best_fitness()
    chromosome2 = brkga.get_best_chromosome()

    print("> Evolving population 2...")
    brkga.evolve_population(2)
    fitness3 = brkga.get_best_fitness()
    chromosome3 = brkga.get_best_chromosome()

    print("> Evolving both populations for 100 generations...")
    for _ in range(100):
        start_time = time()
        brkga.evolve_population(0)
        brkga.evolve_population(1)
        brkga.evolve_population(2)
        print(f"Elapsed time: {time() - start_time :.2f}")

    fitness103 = brkga.get_best_fitness()
    chromosome103 = brkga.get_best_chromosome()

    with open(os.path.join(SOLUTION_DIR, "best_solution4.pickle"), "wb") as hd:
        pickle.dump(
            {
                "fitness1": fitness1,
                "chromosome1": chromosome1,
                "fitness2": fitness2,
                "chromosome2": chromosome2,
                "fitness3": fitness2,
                "chromosome3": chromosome2,
                "fitness103": fitness103,
                "chromosome103": chromosome103,
            },
            hd
        )

###############################################################################
# Configuration 5 for evolve()
###############################################################################

def gen_conf5():
    param_values = deepcopy(default_param_values)
    brkga_params = param_values["params"]

    chromosome_size = 100
    instance = Instance(chromosome_size)

    brkga_params.population_size = 100
    brkga_params.elite_percentage = 0.30
    brkga_params.mutants_percentage = 0.20
    brkga_params.num_elite_parents = 2
    brkga_params.total_parents = 3
    brkga_params.bias_type = BiasFunctionType.LOGINVERSE
    brkga_params.num_independent_populations = 3
    brkga_params.pr_number_pairs = 0
    brkga_params.pr_minimum_distance = 0.0
    brkga_params.pr_type = PathRelinkingType.DIRECT
    brkga_params.pr_selection = PathRelinkingSelection.BESTSOLUTION
    brkga_params.alpha_block_size = 1.0
    brkga_params.pr_percentage = 1.0

    param_values["decoder"] = SumDecode(instance)
    param_values["sense"] = Sense.MINIMIZE
    param_values["seed"] = 4659930950303
    param_values["chromosome_size"] = chromosome_size
    param_values["evolutionary_mechanism_on"] = True

    print("\n> Building configuration 5")
    brkga = BrkgaMpIpr(**param_values)
    brkga.initialize()

    print("> Writing configuration 5")
    with open(os.path.join(STATE_DIR, "state5.pickle"), "wb") as hd:
        pickle.dump(brkga, hd)

    print("> Evolving one generation...")
    brkga.evolve()
    fitness1 = brkga.get_best_fitness()
    chromosome1 = brkga.get_best_chromosome()

    print("> Evolving 10 generations...")
    brkga.evolve(10)
    fitness10 = brkga.get_best_fitness()
    chromosome10 = brkga.get_best_chromosome()

    print("> Evolving 100 generations...")
    brkga.evolve(100)
    fitness100 = brkga.get_best_fitness()
    chromosome100 = brkga.get_best_chromosome()

    with open(os.path.join(SOLUTION_DIR, "best_solution5.pickle"), "wb") as hd:
        pickle.dump(
            {
                "fitness1": fitness1,
                "chromosome1": chromosome1,
                "fitness10": fitness10,
                "chromosome10": chromosome10,
                "fitness100": fitness100,
                "chromosome100": chromosome100
            },
            hd
        )

    print("fitness", fitness1)
    print("fitness", fitness10)
    print("fitness", fitness100)

###############################################################################

if __name__ == "__main__":
    gen_conf1()
    gen_conf2()
    gen_conf3()
    gen_conf4()
    gen_conf5()
