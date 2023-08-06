==============
Token provider
==============

OpenStack Identity supports customizable token providers. This is specified
in the ``[token]`` section of the configuration file. The token provider
controls the token construction, validation, and revocation operations.

You can register your own token provider by configuring the following property:

.. note::

   More commonly, you can use this option to change the token provider to one
   of the ones built in. Alternatively, you can use it to configure your own
   token provider.

* ``provider`` - token provider driver.
  Defaults to ``fernet``.
  Implemented by :class:`keystone.token.providers.fernet.Provider`. This is the
  entry point for the token provider in the ``keystone.token.provider``
  namespace.

Below is the detailed list of the token formats supported by keystone.:

Fernet
 ``fernet`` tokens do not need to be persisted at all, but require that you run
 ``keystone-manage fernet_setup`` (also see the
 ``keystone-manage fernet_rotate`` command).

.. warning::

    Fernet tokens are bearer tokens. They must be protected from unnecessary
    disclosure to prevent unauthorized access.

JWS
 ``jws`` tokens do not need to be persisted at all, but require that you
 configure an asymmetric key pair to sign and validate tokens. The key pair can
 be generated using ``keystone-manage create_jws_keypair`` or it can be
 generated out-of-band manually so long as it is compatible with the JWT
 ``ES256`` Elliptic Curve Digital Signature Algorithm (ECDSA) using a P-256
 curve and a SHA-256 hash algorithm.

.. warning::

    JWS tokens are bearer tokens. They must be protected from unnecessary
    disclosure to prevent unauthorized access.
