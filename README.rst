Stempel Stemmer
===============

.. image:: https://badge.fury.io/py/pystempel.svg
    :target: https://badge.fury.io/py/pystempel

Python port of Stempel, an algorithmic stemmer for Polish language, originally written in Java.

The original stemmer has been implemented as part of `Egothor Project`_, taken virtually unchanged to
`Stempel Stemmer Java library`_ by Andrzej Białecki and next included as part of `Apache Lucene`_,
a free and open-source search engine library. It is also used by `Elastic Search`_ search engine.

.. _Egothor Project: https://www.egothor.org/product/egothor2/
.. _Stempel Stemmer Java library: http://www.getopt.org/stempel/index.html
.. _Apache Lucene: https://lucene.apache.org/core/3_1_0/api/contrib-stempel/index.html
.. _Elastic Search: https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-stempel.html

This package includes also high-quality stemming tables for Polish: original one pretrained by
Andrzej Białecki on 20,000 training sets, and new one, pretrained on 259,080 training sets
from `Polimorf dictionary`_ by me.

The port does not include code for compiling stemming tables.

.. _sjp.pl: https://sjp.pl/slownik/en/
.. _Polimorf dictionary: https://clarin-pl.eu/dspace/handle/11321/577

How to use
----------

Install in your local environment:

.. code:: console

  pip install pystempel

Use in your code:

.. code:: python

  >>> from pystempel import Stemmer

    Choose original (called default) version of a stemmer:

.. code:: python

  >>> stemmer = StempelStemmer.default()

or a version with new stemming table pretrained on training sets from Polimorf dictionary:

.. code:: python

 >>> stemmer = StempelStemmer.polimorf()

Stem:

.. code:: python

  >>> for word in ['książka', 'książki', 'książkami', 'książkowa', 'książkowymi']:
  ...   print(stemmer(word))
  ...
  książek
  książek
  książek
  książkowy
  książkowy


Choosing stemming table
-----------------------

Performance between original (default) and new stemming table (Polimorf-based) varies significantly.
The stemmer for the default stemming table is *understemming*, i.e., for multiple forms of the
same lemma provides different stems more often (63%) than when using Polimorf-based stemming table
(13%). However, the file footprint of the latter is bigger (2.2MB vs 0.3MB). Also loading takes
longer (7.5 seconds vs. 1.3 seconds), though this happens only once, when a stemmer is created. Also,
for original stemming table, the stemmer stems slightly faster: ~60000 vs ~51000 words per second.
See `Evaluation Jupyter Notebook`_ for the detailed evaluation results.

.. _Evaluation Jupyter Notebook: http://htmlpreview.github.io/?https://github.com/dzieciou/pystempel/blob/master/Evaluation.html

Note also, that the licensing schema of both stemming tables differs, and hence licensing of
data generated with each one. See "Licensing" section for the details.



Choosing between port and wrapper
---------------------------------

If you work on an NLP project in Python you can choose between Python port and Python wrapper.
Python port is what pystempel tries to achieve: translation from Java implementation to Python.
Python wrapper is what I used in `tests`_: Python functions to call the original Java implementation of
stemmer. You can find more about wrappers and ports in `Stackoverflow comparision post`_. Here, I
compare both approaches to help you decide:

* **Same accuracy**. I have verified Python port by comparing its output
  with output of original Java implementation for 331224 words from Free Polish dictionary
  (`sjp.pl`_) and for 100% of words it returns same output.
* **Similar performance**. For mentioned dataset both stemmer versions achieved comparable performance.
  Python port completed stemming in 4.4 seconds, while Python wrapper -- in 5 seconds (Intel Core
  i5-6000 3.30 GHz, 16GB RAM, Windows 10, OpenJDK)
* **Different setup**. Python wrapper requires additionally installation of Cython and pyjnius.
  Python wrapper will make also `debugging harder`_ (switching between two programming languages).

.. _Stackoverflow comparision post: https://stackoverflow.com/questions/10113218/how-to-decide-when-to-wrap-port-write-from-scratch
.. _debugging harder: https://stackoverflow.com/questions/6970359/find-an-efficient-way-to-integrate-different-language-libraries-into-one-project
.. _tests: tests/

Options
-------

To disable a progress bar when loading stemming tables, set environment variable ``DISABLE_TQDM=True``.

Development setup
-----------------

To setup environment for development you will need `Anaconda`_ installed.

.. _Anaconda: https://anaconda.org/

.. code:: console

    conda env create --file environment.yml
    conda activate pystempel-env
    pre-commit install

To run tests:

.. code:: console

    curl https://repo1.maven.org/maven2/org/apache/lucene/lucene-analyzers-stempel/8.1.1/lucene-analyzers-stempel-8.1.1.jar > stempel-8.1.1.jar
    pytest ./tests/

To run benchmark:

.. code:: console

    set PYTHONPATH=%PYTHONPATH%;%cd%
    python tests\test_benchmark.py

Licensing
---------

* **Code**: Most of the code is covered by `Egothor`_ Open Source License, an Apache-style license.
  The rest of the code is covered by the `Apache License 2.0`_. This should be clear from a preamble
  of each file.

* **Data**:

  * The original pretrained stemming table is covered by `Apache License 2.0`_.

  * The new pretrained stemming table is covered by `2-Clause BSD License`_, similarly to the
    `Polimorf dictionary` it has been derived from. The copyright owner of both the stemming table
    and the dictionary is `Institute of Computer Science at Polish Academy of Science`_ (IPI PAN).

  * Polish dictionary used by the unit tests comes from `sjp.pl`_  and is covered by
    `Apache License 2.0`_ as well.

.. _Egothor: https://www.egothor.org/product/egothor2/
.. _Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0
.. _Polimorf dictionary: dicts/
.. _2-Clause BSD License: data/polimorf/LICENSE.txt
.. _Institute of Computer Science at Polish Academy of Science: https://ipipan.waw.pl/en/



Alternatives
------------

* `Estem`_ is Erlang wrapper (not port) for Stempel stemmer.
* `pl_stemmer`_ is a Python stemmer based on Porter's Algorithm.
* `polish-stem`_ is a Python stemmer using Finite State Transducers.


.. _Estem: https://github.com/arcusfelis/estem
.. _pl_stemmer: https://github.com/Tutanchamon/pl_stemmer
.. _polish-stem: https://github.com/eugeniashurko/polish-stem

