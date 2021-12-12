MicroPython scikit-fuzzy
=========================

`micropython-scikit-fuzzy` is a fuzzy logic toolkit ported from Python's [SciPy scikit-fuzzy](https://github.com/scikit-fuzzy/scikit-fuzzy) toolkit.

The goals of micropython-scikit-fuzzy are:
* To provide the community with a robust toolkit of independently developed and
  implemented fuzzy logic algorithms
* To increase the attractiveness of scientific MicroPython/CPython as a valid alternative to
  closed-source options.
* To allow experimenting with embedded control systems without installing software or using cloud based services.

Important notice from `scikit-fuzzy`: Please cite [![DOI](https://zenodo.org/badge/8872608.svg)](https://zenodo.org/badge/latestdoi/8872608)
if you find scikit-fuzzy useful.  A formal paper describing this package is in
preparation.

Source
------

https://github.com/JorgeGMarques/micropython-scikit-fuzzy

Documentation
-------------

The documentation of the `scikit-fuzzy` library can be found here: https://scikit-fuzzy.github.io/scikit-fuzzy 

`micropython-scikit-fuzzy` shares exactly the same methods, but some examples are tuned down to run in constrained systems.


What's working
--------------
There are many tools in `scikit-fuzzy`, the list below shows which modules have been ported:

* cluster/_cmeans.py `✅ Done`
* cluster/normalize_columns.py `✅ Done`
* defuzzify/defuzz.py `✅ Done`
* membership/generatemf.py `✅ Done`
* fuzzymath/fuzzy_ops.py`👷 Doing`
* fuzzymath/fuzzy_logic.py `⏰ ToDo`
* fuzzymath/_continuous_to_discrete.py `⏰ ToDo`
* intervals/intervalops.py `⏰ ToDo`
* filters/fire.py `⏰ ToDo`
* control/antecedent_consequent.py `⏰ ToDo`
* control/controlsystem.py `⏰ ToDo`
* control/antecedent_consequent.py `⏰ ToDo`
* control/fuzzyvariable.py `⏰ ToDo`
* control/rule.py `⏰ ToDo`
* control/state.py `⏰ ToDo`
* control/term.py `⏰ ToDo`
* control/visualization.py `⏰ ToDo`

Examples:

* plot_cmeans.py `✅ Done`
* plot_defuzzify.py `✅ Done`
* plot_control_system_advanced.py `⏰ ToDo`
* plot_tipping_problem.py `❌ legacy, won't port`
* plot_tipping_problem_newapi.py `👷 Doing`

Plotting and Programming
--------------------------------

You can use [BIPES](www.bipes.net.br/ide) to easily program MicroPython boards
and BIPES's Databoard to visualize/plot the fuzzy computations.

The examples have been changed to automatically plot in
the BIPES platform, replacing matplot.


Online Discussion & Mailing List
--------------------------------

`scikit-fuzzy`'s public chat room on Gitter.im
[![Gitter](https://badges.gitter.im/JoinChat.svg)](https://gitter.im/scikit-fuzzy/scikit-fuzzy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

`scikit-fuzzy`'s  Google Groups mailing list
http://groups.google.com/group/scikit-fuzzy

BIPES discussion forum
https://github.com/BIPES/BIPES/discussions

Installation
------------

MicroPython-Scikit-Fuzzy depends on

  * [MicroPython](https://github.com/micropython/micropython/) > v1.17
  * [micropython-ulab](https://github.com/v923z/micropython-ulab/) > v3.3.6

Therefore, MicroPython-Scikit-Fuzzy requires a embedded device (or emulated) runnig MicroPython
with ulab module.

If you need help compiling the custom firmware, check out [ulab's readme](https://github.com/v923z/micropython-ulab/), 
(for the ESP-32 I recommend using this [script](https://github.com/v923z/micropython-ulab/blob/master/build/esp32-cmake.sh))


License
-------

Please read LICENSE.txt in this directory.

IEEE Rounding for Matlab users
------------------------------

It should be noted that Matlab rounds incorrectly. The IEEE standard (which is
how this package behaves) requires rounding to the nearest EVEN number if
exactly between, e.g. 1.5 --> 2; 2.5 --> 2; 3.5 --> 4; 4.5 --> 4, etc. This
minimizes systematic rounding error. Thus, if re-implementing algorithms from
Matlab code, slight inconsistencies in rounded results are expected. These are
not bugs, and will not be fixed.
