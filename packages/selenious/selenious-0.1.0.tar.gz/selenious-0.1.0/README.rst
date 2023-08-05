Selenious
*********


.. image:: https://img.shields.io/pypi/v/selenious.svg
        :target: https://pypi.python.org/pypi/selenious

.. image:: https://img.shields.io/pypi/dm/selenious.svg
        :target: https://pypi.python.org/pypi/selenious

.. image:: https://github.com/bonafideduck/selenious/workflows/Sanity/badge.svg
        :target: https://github.com/bonafideduck/selenious/actions?query=branch%3Amaster+workflow%3A%22Sanity%22

.. image:: https://readthedocs.org/projects/selenious/badge/?version=latest
        :target: https://selenious.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Library that allows deep extraction of layered data structures (like JSON).


* Free software: BSD license
* Documentation: https://selenious.readthedocs.io.


Introduction
============

Selenious enhances Selenium WebDriver ``find_element*`` functions to have a
``timeout``, ``debounce``, ``poll_frequency``, ``recover``, and for ``find_elements*``, 
a ``min`` count.

Selenium already has an ``implicitly_wait`` and a ``WebDriverWait`` function.
Neither of these have the versatility and natural feel that Selenious add
to the code.  To add a 5 second timeout to a single call, Selenious would
be:

    driver.find_element_by_id('popup', timeout=5)

While with ``implicitly_wait`` the code would be

    driver.implicitly_wait(5)
    driver.find_element_by_id('popup')
    driver.implicitly_wait(hopefully_you_know_what_the_setting_was_before)

And ``WebDriverWait`` would be 

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "popup"))
    )

Features
========

Enhancement to the find_element function
----------------------------------------

* ``timeout`` - The maximum time in seconds to wait for a succesful find.

* ``poll_frequency`` - How often to poll the driver for the element

* ``debounce`` - For ``find_elements*`` wait for this time period for the count to not change.

* ``min`` - For ``find_elements*`` the minimum count to find.

* ``recover`` - If the item or min items are not found, call this periodically and try again.

Drop-in replacement for selenium webdriver
------------------------------------------

Instead of ``from selenium.webdriver import Chrome`` a convenience
of ``from selenious.webdriver import Chrome`` can be used that
imports the ``SeleniousMixin`` for you.


Settings can be set in the function or globally
-----------------------------------------------

Locally, `webdriver.find_element_by_id('id', timeout=5)`, or globaly,
``webdriver.timeout = 5``.

Credits
=======

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
