.. -*- restructuredtext -*-

========================
MSC extension for Sphinx
========================

:author: LoveIsGrief <loveisgrief@tuta.io>


About
=====

A fork of sphinxcontrib-mscgen_
This extension  allows Mscgen_\ -formatted :abbr:`MSC (Message Sequence Chart)`
diagrams to be included in Sphinx_-generated **HTML** documents inline.
It also supports JSON, MsGenny_, and Xu_.

Mscgen_ is a small program (inspired by `Graphviz Dot`_) that parses
:abbr:`MSC` descriptions and produces images as the output. :abbr:`MSC`\ s are
a way of representing entities and interactions over some time period, very
similar to UML sequence diagrams.

MscgenJS_ is a reimplementation of thaat using JS as a CLI tool and embeddable
on websites, the latter of which this extension takes advantage of.

You can see the latest documentation at the `sphinxcontrib-mscgenjs website`__.

__ http://packages.python.org/sphinxcontrib-mscgenjs/


Quick Example
-------------

This source::

   .. mscgenjs::
        :language: msgenny

        # OpenId Connect protocol
        # https://openid.net/specs/openid-connect-core-1_0.html#rfc.section.1.3
        wordwraparcs=true;

        eu : "end-user",
        rp : "relying party",
        op : "OpenID provider";

        eu =>> rp : "log me in";
        rp =>> op : "authentication request";
        op =>> eu : "authentication and authorization request";
        eu >> op : "authenticate and authorize";
        op >> rp : "authentication response";
        rp =>> op : "UserInfo request";
        op >> rp : "UserInfo response";
        rp >> eu : "Hi. You're logged in with {UserInfo.name}";

is rendered as:

.. mscgenjs::
    :language: msgenny

    # OpenId Connect protocol
    # https://openid.net/specs/openid-connect-core-1_0.html#rfc.section.1.3
    wordwraparcs=true;

    eu : "end-user",
    rp : "relying party",
    op : "OpenID provider";

    eu =>> rp : "log me in";
    rp =>> op : "authentication request";
    op =>> eu : "authentication and authorization request";
    eu >> op : "authenticate and authorize";
    op >> rp : "authentication response";
    rp =>> op : "UserInfo request";
    op >> rp : "UserInfo response";
    rp >> eu : "Hi. You're logged in with {UserInfo.name}";


Download
========

You can see all the `available versions`__ at PyPI_.

__ http://pypi.python.org/pypi/sphinxcontrib-mscgenjs


Install
=======


From source (tar.gz or checkout)
--------------------------------

Unpack the archive, enter the sphinxcontrib-mscgenjs-x.y directory and run::

    python setup.py install


Setuptools/PyPI_
----------------

Alternatively it can be installed from PyPI_, either manually downloading the
files and installing as described above or using::

    pip install -U sphinxcontrib-mscgenjs


Enabling the extension in Sphinx_
---------------------------------

Just add ``sphinxcontrib.mscgenjs`` to the list of extensions in the ``conf.py``
file. For example::

    extensions = ['sphinxcontrib.mscgenjs']


Usage
=====

This extension adds the ``mscgenjs`` directive.
Using the ``:language:`` option with ``json``, ``msgenny`` or ``xu``
different formats can be chosen.

For an example on using the ``mscgenjs`` directive see the `Quick Example`_.

Remember to enable the extension first (see Install_ for details).


.. Links:
.. _Sphinx: http://sphinx.pocoo.org/
.. _Mscgen: http://www.mcternan.me.uk/mscgen/
.. _MscgenJS: https://mscgen.js.org
.. _MsGenny: https://github.com/sverweij/mscgen_js/blob/develop/wikum/msgenny.md
.. _`Graphviz Dot`: http://www.graphviz.org/
.. _PyPI: http://pypi.python.org/pypi
.. _sphinxcontrib-mscgen: https://github.com/sphinx-contrib/mscgen
.. _Xu: https://github.com/sverweij/mscgen_js/blob/develop/wikum/xu.md
