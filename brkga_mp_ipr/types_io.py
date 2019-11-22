###############################################################################
# types_io.py: I/O functions for parameters (types).
#
# (c) Copyright 2019, Carlos Eduardo de Andrade. All Rights Reserved.
#
# This code is released under LICENSE.md.
#
# Created on:  Nov 06, 2019 by ceandrade
# Last update: Nov 07, 2019 by ceandrade
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

from itertools import chain

from brkga_mp_ipr.types import BrkgaParams, ExternalControlParams
from brkga_mp_ipr.exceptions import LoadError

###############################################################################

def load_configuration(configuration_file: str) -> \
        (BrkgaParams, ExternalControlParams):
    """
    Loads the parameters from `configuration_file` returning them as a tuple.

    Args:
        configuration_file (str): plain text file containing the configuration.

    Returns:
        A tuple containing a `BrkgaParams` and a `ExternalControlParams` object.

    Raises:
        IsADirectoryError: If `configuration_file` is a folder.

        FileNotFoundError: If `configuration_file` does not exist.

        LoadError: In cases of missing data or bad-formatted data.
    """

    brkga_params = BrkgaParams()
    control_params = ExternalControlParams()

    param_names_types = {
        name: type(value)
        for name, value in chain(vars(brkga_params).items(),
                                 vars(control_params).items())
    }

    param_given = {name: False for name in param_names_types.keys()}

    with open(configuration_file) as hd:
        lines = hd.readlines()

    if not lines:
        raise LoadError(f"Cannot read {configuration_file}")

    for (line_number, line) in enumerate(lines):
        line = line.strip()
        if len(line) == 0 or line[0] == '#':
            continue

        param_name = None
        value = None

        try:
            param_name, value = [x.strip().lower() for x in line.split()]
        except ValueError:
            raise LoadError(f"Line {line_number}: "
                            f"missing parameter or value")

        if param_name in vars(brkga_params):
            data = brkga_params
        elif param_name in vars(control_params):
            data = control_params
        else:
            raise LoadError(f"Line {line_number}: "
                            f"parameter '{param_name}' unknown")
        try:
            setattr(data, param_name, param_names_types[param_name](value))
            param_given[param_name] = True
        except ValueError:
            raise LoadError(f"Line {line_number}: "
                            f"invalid value for '{param_name}': {value}")
    # end for

    missing_params = []
    for name, value in param_given.items():
        if not value:
            missing_params.append(name)

    if missing_params:
        missing_params = ", ".join(missing_params)
        raise LoadError(f"Missing parameters: {missing_params}")

    return (brkga_params, control_params)

###############################################################################

def write_configuration(filename: str, brkga_params: BrkgaParams,
                        external_params: ExternalControlParams) -> None:
    """
    Writes `brkga_params` and `external_params` into `filename`.

    Args:
        filename (str): A file where the configuration will be written.

        brkga_params (BrkgaParams): The BRKGA-MP-IPR parameters.

        external_params (ExternalControlParams): The control parameters.

    Raises:
        IsADirectoryError: If `filename` is a folder.

        PermissionError: If we cannot write into the file.
    """

    output_string = ""

    for name, value in vars(brkga_params).items():
        output_string += f"{name} {value}\n"

    for name, value in vars(external_params).items():
        output_string += f"{name} {value}\n"

    with open(filename, "w") as hd:
        hd.write(output_string)
