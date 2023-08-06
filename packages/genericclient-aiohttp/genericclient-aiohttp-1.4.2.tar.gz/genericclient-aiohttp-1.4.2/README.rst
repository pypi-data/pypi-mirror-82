=============
genericclient
=============

.. image:: https://travis-ci.org/genericclient/genericclient-aiohttp.svg?branch=master
    :target: https://travis-ci.org/genericclient/genericclient-aiohttp
    
.. image:: https://coveralls.io/repos/github/genericclient/genericclient-aiohttp/badge.svg?branch=master
    :target: https://coveralls.io/github/genericclient/genericclient-aiohttp?branch=master

A generic client for RESTful APIs based on ``aiohttp``. Python 3.5+ only.


Installation
============

::

    $ pip install genericclient-aiohttp

Quickstart
==========

.. code:: python

    import asyncio

    from genericclient_aiohttp import GenericClient

    async def main():
        myclient = GenericClient(api_url)

        myresource = await myclient.resources.get(id=1)

        actives = await myclient.posts.filter(active=True)

        # or you can make multiple HTTP sharing the same session
        async with myclient as session:
            myresource = await session.resources.get(id=1)
            actives = await session.posts.filter(active=True)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

Usage
=====

Instantiation
-------------

.. code:: python

    myclient = GenericClient(url, auth=None, session=None, trailing_slash=False, retries=3, autopaginate=None)


Arguments:

* ``url``: The root URL of your API
* ``auth``: The auth for your API. You can pass anything that ``aiohttp.ClientSession`` can accept as auth.
* ``session``: Pass a session instance to have ``aiohttp`` use that session. If ``None`` (the default), it will instantiate an instance of ``aiohttp.ClientSession`` for you.
* ``trailing_slash``: You can set this to ``True`` if your API's URLs end with a ``/``
* ``retries``: How many times should the client retry the http call after a ``ClientConnectionError``
* ``autopaginate``: You can set this to a coroutine to fetch all pages resulting from a request. Currently, the only coroutine included is ``genericclient_aiohttp.pagination.link_header``, which supports [RFC5988](https://tools.ietf.org/html/rfc5988).

Endpoints
---------

Endpoints are available as properties or items on the main instance:

.. code:: python

    await myclient.posts.all()  # GET /posts/
    await myclient["active-users"].all()  # GET /active-users/

``.all()``
~~~~~~~~~~

Retrieves all resources (essentially a simple ``GET`` on the endpoint):

.. code:: python

    await myclient.posts.all()  # GET /posts/

``.filter()``
~~~~~~~~~~~~~

``.filter(**kwargs)`` calls a ``GET`` with ``kwargs`` as querystring values:

.. code:: python

    await myclient.posts.filter(blog=12, status=1)  # GET /posts/?blog=12&status=1

``.get(**kwargs)``
~~~~~~~~~~~~~~~~~~

A special case of ``.filter()``.

If ``kwargs`` contains ``id``, ``pk``, ``slug`` or ``username``, that value will
be used in the URL path, in that order.

Otherwise, it calls a ``GET`` with ``kwargs`` as querystring values.

If the returned list is empty, will raise ``ResourceNotFound``.

If the returned list contains more than 1 resource, will raise ``MultipleResourcesFound``

Note that ``.get()`` will return a ``Resource``, not a list of ``Resource`` s

.. code:: python

    await myclient.posts.filter(blog=12, status=1)  # GET /posts/?blog=12&status=1
    await myclient.posts.filter(id=12)  # GET /posts/12/
    await myclient.posts.filter(slug='12-ways-clickbait')  # GET /posts/12-ways-clickbait/

``.create(payload)``
~~~~~~~~~~~~~~~~~~~~

Will result in a ``POST``, with ``payload`` (a ``dict``) as the request's body,
returning a new ``Resource``:

.. code:: python

    post = await myclient.posts.create({'blog': 12, 'status': 1})  # POST /posts/

``.get_or_create(defaults, **kwargs)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Issues a GET to fetch the resource. If the resource is not found, issues a POST
to create the resource:

.. code:: python

    # Assuming it doesn't exist
    post = await myclient.posts.get_or_update(slug='my-post', defaults={'status': 1})  # GET /posts/my-post/, then POST /posts/


``.create_or_update(payload)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If ``payload`` contains a key called ``'id'``, will issue a ``PUT``. If the
server returns a `400` error, a ``PATCH`` request will be re-issued.
If `payload`` does not contains ``'id'``, it will issue a ``POST``:

.. code:: python

    post = await myclient.posts.create_or_update({'status': 1})  # POST /posts/
    post = await myclient.posts.create_or_update({'id': 1234, 'status': 1})  # PUT /posts/1234/

    post = await myclient.posts.create_or_update({'id': 1234})  # PUT /posts/1234/
    # <- server returns 400
    # -> PATCH /posts/1234/

``.delete(pk)``
~~~~~~~~~~~~~~~

Will issue a ``DELETE``, and will use ``pk`` as part of the URL:

.. code:: python

    await myclient.posts.delete(24)  # DELETE /posts/24/

Resources
---------

All endpoints methods (with the exception of ``.delete()``) return either a
``Resource`` or a list of ``Resource`` s.

A ``Resource`` is just a wrapping class for a ``dict``, where keys can be accessed
as properties.

Additionally, ``Resource`` s have a special property called ``.payload``, which
contains the original payload received from the server.

``Resource`` s have the following methods:

``Resource.delete()`` will result in a ``DELETE``, with ``Resource.id`` as
par of the URL:

.. code:: python

    blog = await myclient.posts.create({'blog': 12, 'status': 1})  # POST /posts/
    await blog.delete()  # DELETE /blog/345/ -- the ID 345 was returned by the server in the previous response

``Resource.save()`` will result in a ``PUT``, with ``Resource.id`` as
par of the URL. If the
server returns a `400` error, a ``PATCH`` request will be re-issued:

.. code:: python

    post = await myclient.posts.create({'blog': 12, 'status': 1})  # POST /posts/
    post.status = 2
    await post.save()  # PUT /posts/345/

    post = Resource(id=345, status=1)
    await post.save()  # PUT /posts/345/
    # <- server returns 400
    # -> PATCH /posts/345/

ResourceSets
------------

Whenever a method returns a list of Resources, they list will be wrapped in a ``ResultSet``.

A ResultSet is a just a ``list`` object, with the addition of a ``.response`` containing the original response from the server.

Customizing Endpoints and Resources
-----------------------------------

Resources can be customized by subclassing ``genericclient_aiohttp.Resource``.

The most common reason is specifying the name of the primary key:

.. code:: python

    from genericclient_aiohttp import Resource


    class PostResource(Resource):
        pk_name = 'slug'


Endpoints can be customized by subclassing ``genericclient_aiohttp.Endpoint``:

.. code:: python

    form genericclient_aiohttp import Endpoint


    class PostEndpoint(Endpoint):
        resource_class = PostResource


You can then subclass ``genericclient_aiohttp.GenericClient`` to tell the client which endpoint classes to use on each endpoint:

.. code:: python

    from genericclient_aiohttp import GenericClient

    class Client(GenericClient):
        endpoint_classes = {
            'posts': PostEndpoint,
        }

Routes
------

If your API has some non-RESTful calls within the main endpoints (sometimes referred as ``detail_route`` and ``list_route``), you can use ``genericclient`` to call them:

.. code:: python

    await myclient.posts(id=123).publish(date=tomorrow)

.. code:: python

    await myclient.blogs().ping() 


Routes http calls use ``POST`` by default, but you can specify something else by using the ``_method`` argument:

.. code:: python

    await myclient.posts(_method='get', id=123).pingbacks()

.. code:: python

    await myclient.blogs(_method='get').visits()

Note that this calls will return an instance of ``genericclient.ParsedResponse``, instead of instances of ``genericclient.Resource``,

License
=======

Licensed under the MIT License.
