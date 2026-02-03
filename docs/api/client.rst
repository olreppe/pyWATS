Client Services
===============

.. module:: pywats_client
   :synopsis: Client-side services for GUI applications and file conversion

The ``pywats_client`` package provides services for building GUI applications,
managing file conversions, and handling client-side logging infrastructure.

This documentation covers client-specific services that are separate from the
main API layer (``pywats``).

.. toctree::
   :maxdepth: 2
   :caption: Client Services:

   client/logging

Overview
--------

Client services are designed for:

* **GUI Applications**: Desktop tools that interact with WATS servers
* **File Conversion**: Converting test data files between formats
* **Client-Side Logging**: Separate log management for client applications

Key Differences from API Layer
-------------------------------

+-------------------+----------------------------------+----------------------------------+
| Aspect            | API Layer (``pywats``)           | Client Layer (``pywats_client``) |
+===================+==================================+==================================+
| **Purpose**       | HTTP API communication           | GUI/conversion services          |
+-------------------+----------------------------------+----------------------------------+
| **Logging**       | Server request logging           | Client operations & conversions  |
+-------------------+----------------------------------+----------------------------------+
| **Users**         | Python scripts, automation       | Desktop applications, tools      |
+-------------------+----------------------------------+----------------------------------+
| **Deployment**    | Servers, containers, CI/CD       | User workstations                |
+-------------------+----------------------------------+----------------------------------+

See Also
--------

* :doc:`logging` - API-layer logging for server requests
* :doc:`client/logging` - Client-side logging and conversion logs
