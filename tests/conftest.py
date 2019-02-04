import pytest
from flask import _request_ctx_stack, json, Response
from werkzeug import cached_property

from twitter_bastion import Application


class TestResponse(Response):
    @cached_property
    def json(self):
        return json.loads(self.data)


@pytest.fixture(scope='session')
def app(request):
    app = Application('test')
    app.response_class = TestResponse

    ctx = app.app_context()
    ctx.push()
    request.addfinalizer(ctx.pop)

    return app


@pytest.fixture
def app_ctx(request, app):
    ctx = app.app_context()
    ctx.push()
    request.addfinalizer(ctx.pop)
    return ctx


@pytest.fixture(scope='class')
def app_ctx_in_class_scope(request, app):
    return app_ctx(request, app)


@pytest.yield_fixture
def request_ctx(request, app):
    ctx = app.test_request_context()
    ctx.push()
    yield ctx
    if _request_ctx_stack.top and _request_ctx_stack.top.preserved:
        _request_ctx_stack.top.pop()
    ctx.pop()


@pytest.fixture
def client(request, app):
    return app.test_client()


def xhr_test_client(client):
    original_open = client.open

    def decorated_open(self, *args, **kwargs):
        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])
        kwargs['content_type'] = 'application/json'
        headers = kwargs.pop('headers', {})
        headers['X-Requested-With'] = 'XMLHttpRequest'
        kwargs['headers'] = headers
        return original_open(self, *args, **kwargs)

    client.open = decorated_open
    return client


@pytest.fixture
def xhr_client(request, app, client):
    return xhr_test_client(client)
