.. raw:: html

   <h1>

Mockit - Easy REST API Mock

.. raw:: html

   </h1>

|Python 3.7+| |License: MIT|

A very simple to use mock server which runs in a separate process, can
be easily used with pytest.

It allows to mock JSON and String responses using all available HTTP
methods(GET, POST, PUT, PATCH, DELETE, ext..).

.. raw:: html

   <h3>

Installation:

.. raw:: html

   </h3>

Install with pip:

.. code:: buildoutcfg

    $ pip install mockit

.. raw:: html

   <h3>

Examples:

.. raw:: html

   </h3>
   <h5> 

Get Started:

.. raw:: html

   </h5>

.. code:: python


    from mockit import MockitServer

    m_s = MockitServer()

Mock Json Endpoints:

.. code:: python

    m_s.add_json_response(url="/json_endpoint", serializable={"endpoint": "json"}, methods=("GET", ))

Mock XML Endpoints:

.. code:: python

    m_s.add_string_response(
        url="/xml_endpoint",
        response="""
        <xml-tag>
            <tag>text</tag>
        </xml-tag>
    """, methods=("GET", )
    )

Start mock service:

.. code:: python

    m_s.start()

.. raw:: html

   <h5> 

With Pytest:

.. raw:: html

   </h5> 

.. code:: python

    import requests

    from mock_service import MockServer


    class TestPersonalities:
        @classmethod
        def setup_class(cls):
            cls.m_s = MockServer()
            cls.m_s.add_json_response(url="/json_endpoint", serializable={"endpoint": "json"}, methods=("GET", ))
            cls.m_s.start()


        def test_json_endpoint(self):

            response = requests.get(f"{self.m_s.url}/json_endpoint")

            assert response.status_code == 200
            assert "endpoint" in response.json()

        @classmethod
        def teardown_class(cls):
            cls.m_s.terminate()

.. raw:: html

   <h3>

Features:

.. raw:: html

   </h3>
   <li>

Mocking REST API.

.. raw:: html

   </li>
   <li>

Mocking JSON, XML and String responses.

.. raw:: html

   </li>


   <h3>

Bug report:

.. raw:: html

   </h3>

If you have any trouble, report bug at GitHub Issue
https://github.com/victorvasiliev/mockit/issues

.. |Python 3.7+| image:: https://img.shields.io/badge/python-3.7+-blue.svg
   :target: https://www.python.org/downloads/
.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
