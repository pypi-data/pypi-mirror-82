==================
The bpelib project
==================

.. start-badges
.. list-table::
  :stub-columns: 1

  * - coverage
    - | |test-coverage|
  * - tests
    - | |test-results|

.. |test-coverage| image:: https://api.travis-ci.org/pytest-dev/pytest-cov.svg?branch=master
    :alt: test coverage
    :target: https://Skyzip.gitlab.io/bpelib/htmlcov

.. |test-results| image:: https://api.travis-ci.org/pytest-dev/pytest-cov.svg?branch=master
    :alt: test results
    :target: https://Skyzip.gitlab.io/bpelib/pytest-html

.. end-badges

Byte Pair Encoding for Natural Language Processing.

Installation
============

Install with pip::

  pip install bpelib

Uninstalling
------------

Uninstall with pip::

  pip uninstall bpelib

Usage
=====

  Import the BPE class.

.. code-block:: python

  from bpelib import bpe

..

  Learn encoding on construct or at a later time:

.. code-block:: python

  bpe = BPE(['start', 'learning', 'now'])
  # or ...
  bpe.learn_encoding(['start', 'learning', 'now'])
..

  To encode or decode a word, simply call the BPE object.

.. code-block:: python

  encoded = bpe('encode')  # '<w/> e n c o d e </w>'
  decoded = bpe(encoded)  # 'encode'
  assert 'encode' == decoded
..

  You can call encode or decode explicitly, too.

.. code-block:: python

  encoded = bpe.encode('encode')  # '<w/> e n c o d e </w>'
  decoded = bpe.decode(encoded)  # 'encode'
  assert 'encode' == decoded
..

  You can also specify maximum vocabulary size and the used encoding.

.. code-block:: python

  bpe = BPE(max_vocab_size=1024, encoding='ascii')
..
