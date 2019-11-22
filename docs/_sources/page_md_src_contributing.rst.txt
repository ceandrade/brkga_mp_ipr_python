.. index:: pair: page; Contributing
.. _doxid-md_src_contributing:

Contributing
===============================================================================

Although the code is an experimental one, we aim to write an efficient and
consistent code. So, you should keep in mind the balance between memory
utilization and code efficiency and pay special attention to cache utilization.

Style
-------------------------------------------------------------------------------

Please, follow the general `PEP8 coding style <https://pep8.org>`_. Since it is
too long to describe all details here, study the code already written.
However, in general:

* Name classes, methods, and variables as clear and meaningful as possible;

* Write short commentaries on the code flow to reading more accessible and
  faster;

* Properly document the code, especially the data structures and methods
  definitions. Do not forget to link/refer them;

* All classes, attributes, methods, functions, and so must have type
  annotations. The user must be able to know exactly what kind of objects
  he/she is dealing with. Use the ``typing`` package, and use ``from __future__
  import annotations``;

* No trailing spaces,kd no tabs, Unix/POSIX end of line. Try to keep line
  within 80 columns and do not exceed 90 columns;

* We encourage the use of Python f-strings where the make the code easier to
  read;

* Use section separations (sequence of `#`), for clarity, especially into
  BrkgaMpIpr class. This class has lots of long methods, which can be
  categorized into different groups of functionality.

* Do not use system specific code/headers. Your code must compile in several
  systems with minimum change;

* All submissions will need to pass the "pylint" test using the supplied
  ``pylintrc`` file. Note that this file is pretty generic, but it may be
  changed in the future;

* Make sure that, for each method/function, you write unit tests that cover
  all corner cases, and few regular cases (> 1);

* New code without proper unit tests will not be merged;

* Do not commit or do a pull request until the code pass in all tests.

