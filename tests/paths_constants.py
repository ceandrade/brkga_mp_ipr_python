"""
tests.paths_constants Version 0.1 - Nov 01, 2019

This module contains paths and constants for tests.

@author: Carlos Eduardo de Andrade <cea@research.att.com>

(c) Copyright 2019, AT&T Labs Research.
    AT&T Intellectual Property. All Rights Reserved.

Created on  Nov 01, 2019 by andrade
Modified on Nov 15, 2019 by andrade

See LICENSE.md file for license information.

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

import os
import pkg_resources

###############################################################################
# Resources for testing
###############################################################################

RESOURCE_DIR = pkg_resources.resource_filename(__name__, "resources")
CONFIG_DIR = os.path.join(RESOURCE_DIR, "configuration_files")
STATE_DIR = os.path.join(RESOURCE_DIR, "states")
SOLUTION_DIR = os.path.join(RESOURCE_DIR, "solutions")
