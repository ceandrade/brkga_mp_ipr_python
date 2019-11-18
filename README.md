![BRKGA-MP-IPR logo](https://github.com/ceandrade/brkga_mp_ipr_python/blob/master/src_docs/src/assets/logo.png)

BRKGA-MP-IPR - Python version
================================================================================

[![Build Status](https://travis-ci.org/ceandrade/brkga_mp_ipr_python.svg?branch=master)](https://travis-ci.org/ceandrade/brkga_mp_ipr_python)

[![Coverage Status](https://coveralls.io/repos/ceandrade/brkga_mp_ipr_python/badge.svg?branch=master&service=github)](https://coveralls.io/github/ceandrade/brkga_mp_ipr_python?branch=master)

[![codecov.io](http://codecov.io/github/ceandrade/brkga_mp_ipr_python/coverage.svg?branch=master)](http://codecov.io/github/ceandrade/brkga_mp_ipr_python?branch=master)

BRKGA-MP-IPR provides a _very easy-to-use_ framework for the
Multi-Parent Biased Random-Key Genetic Algorithm with Implict Path Relink
(**BRKGA-MP-IPR**). Assuming that your have a _decoder_ to your problem,
we can setup, run, and extract the value of the best solution in less than
5 commands (obvisiously, you may need few other lines fo code to do a proper
test).

This Python version is very flexible and suitable for prototyping. However,
it is not as fast as the
[C++ version](https://github.com/ceandrade/brkga_mp_ipr_cpp) or the
[Julia version](https://github.com/ceandrade/brkga_mp_ipr_julia).
Moreover, due to Python Interpreter limitations (see
(https://wiki.python.org/moin/GlobalInterpreterLock)), real multithread is
not possible, defeating the BRKGA's capability of parallel decoding, which
speeds up the optimization by large paces.

If Python is not suitable to you, we may find useful the
[C++ version](https://github.com/ceandrade/brkga_mp_ipr_cpp) or the
[Julia version](https://github.com/ceandrade/brkga_mp_ipr_julia) of this
framework. At this moment, we have no plans to implement the BRKGA-MP-IPR in
other languages such as Java or C#. But if you want to do so, you are must
welcome. But please, keep the API as close as possible to the C++ API (or
Julia API in case you decide go C), and use the best coding and documentation
practices of your chosen language/framework.

If you are not familiar with how BRKGA works, take a look on
[Standard BRKGA](http://dx.doi.org/10.1007/s10732-010-9143-1) and
[Multi-Parent BRKGA](http://dx.doi.org/xxx).
In the future, we will provide a _Prime on BRKGA-MP_
section.

Tutorial (complete)
--------------------------------------------------------------------------------

The tutorial is a working-in-progress yet. Meanwhile, the reader can use
the [C++ tutorial](https://ceandrade.github.io/brkga_mp_ipr_cpp) or
the [Julia tutorial](https://ceandrade.github.io/brkga_mp_ipr_julia)
since the APIs are very similar each other.

License and Citing
--------------------------------------------------------------------------------

BRKGA-MP-IPR uses a permissive BSD-like license and it can be used as it
pleases you. And since this framework is also part of an academic effort, we
kindly ask you to remember to cite the originating paper of this work.
Indeed, Clause 4 estipulates that "all publications, softwares, or any other
materials mentioning features or use of this software and/or the data used to
test it must cite explicitly the following article":

> C.E. Andrade. R.F. Toso, J.F. Gonçalves, M.G.C. Resende. The Multi-Parent
> Biased Random-key Genetic Algorithm with Implicit Path Relinking. _European
> Journal of Operational Research_, volume XX, issue X, pages xx-xx, 2019.
> DOI [to be determined](http://dx.doi.org/xxx)

Contributing
--------------------------------------------------------------------------------

[Contribution guidelines for this project](CONTRIBUTING.md)
