################################################################################
# decoders.py: decoders for tests.
#
# (c) Copyright 2019, Carlos Eduardo de Andrade. All Rights Reserved.
#
# This code is released under LICENSE.md.
#
# Created on:  Nov 09, 2019 by ceandrade
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
################################################################################

from brkga_mp_ipr.types import BaseChromosome
from tests.instance import Instance

class SumDecode():
    def __init__(self, instance: Instance):
        self.instance = instance

    def decode(self, chromosome: BaseChromosome, rewrite: bool) -> float:
        tmp = [x + y for x, y in zip(chromosome, self.instance.data)]
        tmp = [x / max(tmp) for x in tmp]
        if rewrite:
            for i in range(len(chromosome)):
                chromosome[i] = tmp[i]
        return sum(tmp)

################################################################################

class RankDecode():
    def __init__(self, instance: Instance):
        self.instance = instance

    def decode(self, chromosome: BaseChromosome, rewrite: bool) -> float:
        tmp = [x + y for x, y in zip(chromosome, self.instance.data)]
        rank = 0
        for i, value in enumerate(tmp[1:]):
            if value > tmp[i]:
                rank += 1
        if rewrite:
            for i in range(len(chromosome)):
                chromosome[i] = tmp[i]
        return float(rank)
