.. letxbe documentation master file, created by
   sphinx-quickstart on Mon May 15 10:22:46 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to letxbe's documentation!
==================================

|pydantic shield 1| |pydantic shield 2| |black shield| |license shield| |circle ci shield|

.. |pydantic shield 1| image:: https://img.shields.io/badge/dependencies-pydantic-brightgreen
   :target: https://pydantic-docs.helpmanual.io/
.. |pydantic shield 2| image:: https://img.shields.io/badge/dependencies-requests-brightgreen
   :target: https://pypi.org/project/requests
.. |black shield| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
.. |license shield| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
.. |circle ci shield| image:: https://img.shields.io/circleci/build/bitbucket/onogone/letxbe?token=00601288e2fce2f6e8f35da8bcc0e154342f8eed

Connect and control `LetXbe <http://letxbe.ai/>`__ API services.

``letxbe`` is the Python SDK of LetXbe API. Notably, it contains:

   - :ref:`LXB <lxb>`: main class to connect and control LetXBe services.
   - Provider (under construction, for developers)
   - :ref:`Type <type>`: the typing for all objects used in the API.


.. toctree::
   :maxdepth: 1
   :caption: First Steps

   Installation Guide <first_steps.installation>
   Basic usage <first_steps.basic_usage>
   Known Issues <first_steps.known_issues>

.. toctree::
   :maxdepth: 1
   :caption: Modules

   LXB <modules.letxbe>
   Provider <modules.provider>
   Type <modules.type>

.. toctree::
   :maxdepth: 1
   :caption: Developers

   Installation Guide <developers.installation>
   Todo <developers.todo>
   Release Notes <developers.release_notes>
