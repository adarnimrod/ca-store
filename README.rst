CA store
########

An Ansible role to setup the CA store. The end goal is too have the same setup
on both OSes, meaning:

- Certificates owned by the ssl-cert group.
- All upstream provided certificates at :code:`/usr/share/ca-certificates`.
- All locally provided certificates at :code:`/usr/local/share/ca-certificates`.
- A single concatenated file of all SSL certificates at
  :code:`/etc/ssl/certs/ca-certificates.crt`.
- All certificates by name and hash symlinked at :code:`/etc/ssl/certs`.
- Keys should go in to :code:`/etc/ssl/private`.:
- :code:`update-ca-certificates` script for updating both symlinks and
  concatenated file after locally adding a certificate.
- High bit count DH params file at :code:`/etc/ssl/dhparams.pem`.
- A self-signed key and cert at :code:`/etc/ssl/private/ssl-cert-snakeoil.key`
  and :code:`/etc/ssl/certs/ssl-cert-snakeoil.pem` respectfully.

Afterwards you'll be able to do the following:

- Point to :code:`/etc/ssl/certs` for a list of known certs by hash.
- Point to :code:`/etc/ssl/certs/ca-certificates.crt` for a single concatenated
  file of all known certs.
- Add your certs at :code:`/usr/local/share/ca-certificates`, run
  :code:`update-ca-certificates` to update all locations.
- Run the role again to update to the latest list of certs provided by upstream.
- Save private keys at :code:`/etc/ssl/private` owned by root:ssl-cert and have
  them securely stored.

Requirements
------------

See :code:`meta/main.yml`, :code:`tests/requirements.yml` and assertions at
the top of :code:`tasks/main.yml`.

Role Variables
--------------

See :code:`defaults/main.yml`.

Dependencies
------------

See :code:`meta/main.yml`.

Example Playbook
----------------

See :code:`tests/playbook.yml`.

Testing
-------

Testing requires Virtualbox and Vagrant and Python 2.7. Install the Python
dependencies, add pre-commit hooks by running:

.. code:: shell

    pip install -r tests/requirements.txt
    pre-commit install

To run the full test suite:

.. code:: shell

    ansible-galaxy install git+file://$(pwd),$(git rev-parse --abbrev-ref HEAD) -p .molecule/roles
    molecule test --platform all
    pre-commit run --all-files

License
-------

This software is licensed under the MIT license (see the :code:`LICENSE.txt`
file).

Author Information
------------------

Nimrod Adar, `contact me <nimrod@shore.co.il>`_ or visit my `website
<https://www.shore.co.il/>`_. Patches are welcome via `git send-email
<http://git-scm.com/book/en/v2/Git-Commands-Email>`_. The repository is located
at: https://www.shore.co.il/git/.
