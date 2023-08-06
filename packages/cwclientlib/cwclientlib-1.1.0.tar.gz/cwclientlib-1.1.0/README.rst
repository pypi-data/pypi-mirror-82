.. -*- coding: utf-8 -*-

=============
 CwClientLib
=============

Summary
-------

A Python library to easily build CubicWeb_ clients:

* execute RQL_ queries remotely (using rqlcontroller_),
* access instances that requires authentication (using signedrequest_).

It also provides a simple command line tool (cwrql) to execute simple requests.

Requirements
------------

client side:

- requests_ (>= 2.0)

server side:

- CubicWeb (>= 3.18.3) with the cubes rqlcontroller_ and signedrequest_


Configuration
-------------

``cwclientlib`` implements a ``cwproxy_for(instance)`` function that
will build a ``CWProxy`` for the given instance, reading
authentication credentials from a configuration file (can be a ini
file, json or yaml). The default configuration file name is
`~/.config/cwclientlibrc` (using the ini file format), but this can be
changed using the ``CWCLCONF`` environment variable. For example:

.. code-block:: bash

   david@perseus:~$ cat ~/.config/cwclientlibrc
   [cwo]
   url = https://www.cubicweb.org/
   token-id = my_cwo_token
   secret = <my-secret>

   [elo]
   url = https://www.logilab.org
   token-id = my_elo_token
   secret = <my-secret>

makes it possible to write:

.. code-block:: bash

   david@perseus:~$ cwrql cwo "Any N,S WHERE P eid 1251664, P name N, P summary S"
   projman a project management tool

   david@perseus:~$ cwrql -v ejsonexport -j cwo "Any P WHERE P eid 1251664"
   [{"description": "It reads project descriptions [...]",
   "modification_date": "2015/02/13 18:12:40",
   "icon_format": null,
   "description_format": "text/rest",
   "summary": "a project management tool",
   "downloadurl": "http://download.logilab.org/pub/projman",
   "cwuri": "http://www.logilab.org/873",
   "__cwetype__": "Project",
   "eid": 1251664,
   "creation_date": "2006/09/28 17:44:38",
   "homepage": null,
   "debian_source_package": null,
   "name": "projman"}]

or:

.. code-block:: python

   from cwclientlib import cwproxy_for

   client = cwproxy_for('cwo')
   # or client = cwproxy_for('https://www.cubicweb.org/')
   query = 'Any X WHERE X is Ticket, X concerns P, P name "cwclientlib"'
   resp = client.rql(query)
   data = resp.json()

Note that the config file may contain credentials, so its permissions
must be readable only by the user (checked on posix platforms only).


Using signed requests
---------------------

Once the cube signedrequest_ is added, in the WebUI:

#. View a ``CWUser`` and click the action ``add an AuthToken``
#. Give an identifier to the token and make it enabled
#. Use the token identifier and the token in your source code


Configuration
-------------

You can define url and credentials for commonly used cubicweb
endpoints in a config file. By default, on Linux, it will be a ini
file located at ``$HOME/.config/cwclientlibrc`` but you may define the
``CWCLCONF`` environmentvariable to specify it.  This config file can
also be a YAML (file name must end with .yaml) or a JSON file (.json).

The file will look like:

.. code-block:: ini

   [cwo]
   url = https://www.cubicweb.org/
   token-id = my token id
   secret = <my secret>


Command line tools
------------------

cwclientlib comes with 3 simple command-line tools allowing to easily
request a cubicweb application from a shell:

`cwrql` to make RQL queries:

.. code-block:: bash

   david@perseus:~$ cwrql -h
   Usage: cwrql [options] (url|instance_id) rqlquery [rqlquery2] ...

   Options:
     -h, --help         show this help message and exit
     -j, --json         produce JSON data
     -v VID, --vid=VID  vid to use (default is jsonexport)
     -S, --no-ssl       do NOT verify ssl server certificate; ignored if --ca is
                        given
     -c CA, --ca=CA     Bundle CA to use to verify server certificate
     -w, --rqlio        use rqlio
   david@perseus:~$ cwrql  cwo  "Any VN, VS WHERE V version_of P,
   > P name 'cwclientlib', V num VN, V in_state S, S name VS"
   0.2.1 published
   0.3.0 dev
   0.2.0 published
   0.1.0 published

`cwget` to make any king of GET request (ie. call a specific cubicweb controller):

.. code-block:: bash

   david@perseus:~$ cwget cwo /testconfig/1251730 \
   vid=apycot.get_configuration  environment=4209277
   [{"pylint_threshold": "7", "install": "python_setup", "pycoverage_threshold": "70"}]

`cwshell` to connect to a cubicweb endopint and start an interactive
python shell with a few additional builtins ``rql`` and
``client``. This shell also provides RQL auto-completion:

.. code-block:: bash

   david@perseus:~$ cwshell cwo
   You are connected to https://www.cubicweb.org
   >>> client.execute('Any X WHERE X is P
   Patch               Plan                Project             ProjectEnvironment
   >>> rql('Any P, N WHERE X is Project, X name P ,V version_of X, V in_state S, V num N, S name "ready"')
   [[u'cubicweb-pyramid', u'0.2.0'], [u'cubicweb-simplefacet', u'0.3.2']]
   >>>

Available extra builtins:

:client: is the CWProxy instance connected to the cubicweb endpoint.

:rql: shortcut for ``client.execute()``.



Python examples
---------------

Simple read only query:

.. code-block:: python

   from cwclientlib import cwproxy

   client = cwproxy.CWProxy('http://www.cubicweb.org/')
   query = 'Any X WHERE X is Ticket, X concerns P, P name "cwclientlib"'
   resp = client.rql(query)
   data = resp.json()

Creating an entity, authenticating with signedrequest_ with
credentials read from the config file:

.. code-block:: python

   from cwclientlib import cwproxy_for

   client = cwproxy_for('cwo')
   queries = [('INSERT CWUser U: U login %(l)s, U upassword %(p)s',
               {'l': 'Babar', 'p': 'cubicweb rulez & 42'}), ]
   resp = client.rqlio(queries)
   data = resp.json()

Creating an entity, authenticating with signedrequest_ building the
authentifier by hand:

.. code-block:: python

   from cwclientlib import cwproxy

   auth = cwproxy.SignedRequestAuth('my token', '6ed44d82172211e49d9777269ec78bae')
   client = cwproxy.CWProxy('https://www.cubicweb.org/', auth)
   queries = [('INSERT CWUser U: U login %(l)s, U upassword %(p)s',
               {'l': 'Babar', 'p': 'cubicweb rulez & 42'}), ]
   resp = client.rqlio(queries)
   data = resp.json()

Creating a file entity, authenticating with signedrequest_:

.. code-block:: python

   from io import BytesIO
   from cwclientlib import cwproxy_for

   client = cwproxy_for('cwo')
   queries = [('INSERT File F: F data %(content)s, F data_name %(fname)s',
               {'content': BytesIO('some binary data'), 'fname': 'toto.bin'})]
   resp = client.rqlio(queries)
   data = resp.json()

.. _CubicWeb: http://www.cubicweb.org/
.. _RQL: http://docs.cubicweb.org/annexes/rql/language
.. _rqlcontroller: http://www.cubicweb.org/project/cubicweb-rqlcontroller/
.. _signedrequest: http://www.cubicweb.org/project/cubicweb-signedrequest/
.. _requests: http://docs.python-requests.org/en/latest/
