###############################################################################
# (c) Copyright 2019, Carlos Eduardo de Andrade.
# All Rights Reserved.
#
#  Created on : Nov 21, 2019 by andrade
#  Last update: Nov 21, 2019 by andrade
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

.PHONY: all clean

all:
	sphinx-apidoc -f -e --extensions autodoc,todo,mathjax,viewcode \
		-o src/rst ../brkga_mp_ipr
	sphinx-build -b html src/rst build/html
	touch build/html/.nojekyll
	rm -rf ../docs
	cp -a build/html ../docs
	cp -a src/assets/logo*png ../docs/_static

clean:
	rm -rf build
