======
WsAppy
======

A bit more higher level of asyncio websocket server

Overview
========

**wsappy** provides base classes for creating websocket API server using request handlers and client routes.

Usage example
=============

.. literalinclude:: ../examples/simple/server.py
    :caption: Server
    :language: python

.. literalinclude:: ../examples/simple/client.py
    :caption: Client
    :language: python

.. code-block:: bash

    python3 server.py

.. code-block:: bash

    python3 client.py

...on client will result in:

.. code-block:: bash

    --> {"method": "get", "module": "entity", "data": {"item_id": 42}, "request_id": 1}
    <-- {"request_id": 1, "event": "result", "module": "entity", "data": {"items": [{"id": 42, "name": "a"}]}}
    --> {"method": "get", "module": "entity", "data": {"item_id": 15}, "request_id": 1}
    <-- {"request_id": 1, "event": "result", "module": "entity", "data": {"items": [{"id": 15, "name": "b"}]}}
    --> {"method": "get", "module": "entity", "data": {"item_id": 30}, "request_id": 1}
    <-- {"request_id": 1, "event": "result", "module": "entity", "data": {"items": [{"id": 30, "name": "c"}]}}
    items {42: {'name': 'a', 'id': 42}, 30: {'name': 'c', 'id': 30}, 15: {'name': 'b', 'id': 15}}

See :ref:`examples-simple` example for details

Features
========

 * **Clients** - creating custom clients for URL routing
 * **Handlers** - creating custom handlers for handling separate modules/methods

Run tests
=========

.. code-block:: bash

    python3 -m unittest discover tests

TODO
====

* More complex URL routing
