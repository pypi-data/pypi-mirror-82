=========================
API Configuration options
=========================

Configuration
~~~~~~~~~~~~~

The Identity service is configured in the ``/etc/keystone/keystone.conf`` file.

The following tables provide a comprehensive list of the Identity
service options.

.. only:: html

   For a sample configuration file, refer to :doc:`samples/keystone-conf`.

.. show-options::
   :config-file: config-generator/keystone.conf

Domain-specific Identity drivers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Identity service supports domain-specific Identity drivers
installed on an SQL or LDAP back end, and supports domain-specific
Identity configuration options, which are stored in domain-specific
configuration files. See :ref:`domain_specific_configuration`
for more information.
