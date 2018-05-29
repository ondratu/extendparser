Contribution
============


Tests
-----
``test`` command in setup.py run unittest and doctest automatically, you can
run unittest manually by next commands:

.. code:: sh

    # unittest (builtin)
    ~$ python -m unittest discover -v ./tests

    # pytest (extra module)
    ~$ pytest -v

    # doctest (builtin - not output means example codes are OK)
    ~$ python -m doctest extendparser/*.py

**pytest** package have many additional extensions so you can use that.
Next command check all .rst files, source code with pep8 and doctest checkers.

.. code:: sh

    # check pep8 and doctest with pytest (pytest + pep8 extension + doctest-plus)
    ~$ pytest -v --pep8 --doctest-plus --doctest-rst
