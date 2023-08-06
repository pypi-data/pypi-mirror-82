import logging

from genericclient_base import (
    ParsedResponse,
    BaseEndpoint, BaseGenericClient, BaseResource, exceptions, utils,
)

from . import routes

import aiohttp
from aiohttp.client_exceptions import ClientConnectionError, ContentTypeError
from failsafe import Failsafe, RetryPolicy, CircuitBreaker


_version = "1.4.2"
__version__ = VERSION = tuple(map(int, _version.split('.')))


logger = logging.getLogger(__name__)


def convert_lookup(lookup):
    items = lookup.items()
    multi_dict = []
    for k, v in items:
        if isinstance(v, (tuple, list)):
            for item in v:
                multi_dict.append((k, str(item)))
        else:
            multi_dict.append((k, str(v)))
    return multi_dict


class Resource(BaseResource):
    async def save(self):
        if self.pk is not None:
            url = self._urljoin(self.pk)
            try:
                response = await self._endpoint.request('put', url, json=self.payload)
            except exceptions.BadRequestError:
                response = await self._endpoint.request('patch', url, json=self.payload)
        else:
            response = await self._endpoint.request('post', self._endpoint.url, json=self.payload)
        self.payload = response.data
        return self

    async def delete(self):
        url = self._urljoin(self.pk)
        await self._endpoint.request('delete', url)


class Endpoint(BaseEndpoint):
    resource_class = Resource
    detail_route_class = routes.DetailRoute
    list_route_class = routes.ListRoute

    def __call__(self, _method='post', **kwargs):
        if kwargs:
            return self.detail_route_class(self, _method, **kwargs)
        else:
            return self.list_route_class(self, _method)

    def convert_lookup(self, lookup):
        return convert_lookup(lookup)

    async def http_request(self, session, method, url, *args, **kwargs):
        async with session.request(method, url, *args, **kwargs) as response:
            if response.status in (401, 403):
                if self.api.auth:
                    msg = "Failed request to `{}`. Cannot authenticate user `{}` on the API.".format(
                        url, self.api.auth.login,
                    )
                    raise exceptions.NotAuthenticatedError(
                        response, msg,
                    )
                else:
                    raise exceptions.NotAuthenticatedError(response, "User is not authenticated on the API")

            elif response.status == 400:
                text = await response.text()
                raise exceptions.BadRequestError(
                    response,
                    "Bad Request 400: {}".format(text)
                )
            status = response.status
            headers = response.headers
            data = await self.api.hydrate_data(response)
        return ParsedResponse(status_code=status, headers=headers, data=data)

    async def request(self, method, url, *args, **kwargs):
        async with aiohttp.ClientSession(auth=self.api.auth, headers={
            'Content-Type': 'application/json',
        }) as session:
            response = await self.api.failsafe.run(lambda: self.http_request(session, method, url, *args, **kwargs))
        return response

    async def filter(self, **kwargs):
        params = self.convert_lookup(kwargs)
        results = []
        url = self.url
        if self.api.autopaginate is not None:
            response, results = await self.api.autopaginate(self, params)
        else:
            response = await self.request('get', url, params=params)
            results += response.data

        return self.resource_set_class(response, [self.resource_class(self, **result) for result in results])

    async def all(self):
        return await self.filter()

    async def get(self, **kwargs):
        try:
            pk = utils.find_pk(kwargs)
            params = None
            url = self._urljoin(pk)
        except exceptions.UnknownPK:
            params = self.convert_lookup(kwargs)
            url = self.url
        response = await self.request('get', url, params=params)

        if response.status_code == 404:
            raise exceptions.ResourceNotFound("No `{}` found for {}".format(self.name, kwargs))

        result = response.data

        if isinstance(result, list):
            if len(result) == 0:
                raise exceptions.ResourceNotFound("No `{}` found for {}".format(self.name, kwargs))
            if len(result) > 1:
                raise exceptions.MultipleResourcesFound("Found {} `{}` for {}".format(len(result), self.name, kwargs))

            return self.resource_class(self, **result[0])

        return self.resource_class(self, **result)

    async def create(self, payload):
        response = await self.request('post', self.url, json=payload)
        if response.status_code != 201:
            raise exceptions.HTTPError(response)

        return self.resource_class(self, **response.data)

    async def get_or_create(self, **kwargs):
        defaults = kwargs.pop('defaults', {})
        try:
            resource = await self.get(**kwargs)
            return resource
        except exceptions.ResourceNotFound:
            params = {k: v for k, v in kwargs.items()}
            params.update(defaults)
            return await self.create(params)

    async def create_or_update(self, payload):
        if 'id' in payload or 'uuid' in payload:
            resource = self.resource_class(self, **payload)
            return await resource.save()

        return await self.create(payload)

    async def delete(self, pk):
        url = self._urljoin(pk)

        response = await self.request('delete', url)

        if response.status_code == 404:
            raise exceptions.ResourceNotFound("No `{}` found for pk {}".format(self.name, pk))

        if response.status_code != 204:
            raise exceptions.HTTPError(response)

        return None


class GenericClient(BaseGenericClient):
    endpoint_class = Endpoint

    def __init__(self, url, auth=None, session=None, trailing_slash=False, retries=6, autopaginate=None):
        if auth is not None and not isinstance(auth, aiohttp.BasicAuth):
            auth = aiohttp.BasicAuth(*auth)
        super(GenericClient, self).__init__(url, auth, session, trailing_slash, autopaginate)
        max_failures = retries - 1
        circuit_breaker = CircuitBreaker(maximum_failures=max_failures)
        retry_policy = RetryPolicy(
            allowed_retries=retries,
            retriable_exceptions=[ClientConnectionError],
            abortable_exceptions=[
                exceptions.BadRequestError,
                exceptions.NotAuthenticatedError,
                exceptions.ResourceNotFound,
                exceptions.MultipleResourcesFound,
                exceptions.HTTPError,
                ValueError,
            ],
        )
        self.failsafe = Failsafe(circuit_breaker=circuit_breaker, retry_policy=retry_policy)

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(auth=self.auth, headers={
            'Content-Type': 'application/json',
        })
        return self

    async def __aexit__(self, *args, **kwargs):
        if not self._session.closed:
            await self._session.__aexit__(*args, **kwargs)

    async def hydrate_data(self, response):
        if response.status == 204:
            return None
        try:
            result = await response.json()
            return result
        except (ValueError, ContentTypeError):
            text = await response.text()
            raise ValueError(
                "Response from server is not valid JSON. Received {}: {}".format(
                    response.status,
                    text,
                ),
            )
