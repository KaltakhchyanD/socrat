import unittest

from flask import Flask
from flask.globals import _app_ctx_stack, _request_ctx_stack


class TestContext(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.testing = True

        assert _app_ctx_stack.top is None
        assert _request_ctx_stack.top is None

    def test_client_without_app_context(self):
        with self.app.test_client() as c:
            assert _app_ctx_stack.top is None
            assert _request_ctx_stack.top is None

            c.get('/')

            # application context is created implicitly by request context
            assert _app_ctx_stack.top is not None
            # request context is preserved because test client set
            # WSGI environment flask._preserve_context to True
            assert _request_ctx_stack.top is not None

        # implicitly created application context is popped by request
        # context's pop method
        assert _app_ctx_stack.top is None
        # request context is popped by test client's __exit__ method
        assert _request_ctx_stack.top is None

    def test_client_with_app_context(self):
        with self.app.app_context():
            # application context is created explicitly by app_context()
            assert _app_ctx_stack.top is not None
            assert _request_ctx_stack.top is None

            app_ctx = _app_ctx_stack.top

            with self.app.test_client() as c:
                assert _app_ctx_stack.top is app_ctx
                assert _request_ctx_stack.top is None

                c.get('/')

                # application context is not created by request context
                assert _app_ctx_stack.top is app_ctx
                # request context is preserved because test client set
                # WSGI environment flask._preserve_context to True
                assert _request_ctx_stack.top is not None

            # explicitly created application context is not popped by request
            # context's pop method
            assert _app_ctx_stack.top is app_ctx
            # request context is popped by test client's __exit__ method
            assert _request_ctx_stack.top is None

        # explicitly created application context is popped by application
        # context's __exit__ method
        assert _app_ctx_stack.top is None
        assert _request_ctx_stack.top is None

    def test_request_context_without_app_context(self):
        with self.app.test_request_context('/'):
            # application context is created implicitly by request context
            assert _app_ctx_stack.top is not None
            # request context is created
            assert _request_ctx_stack.top is not None

        # implicitly created application context is popped by request
        # context's pop method
        assert _app_ctx_stack.top is None
        # request context is popped by request context's __exit__ method
        assert _request_ctx_stack.top is None

    def test_request_context_with_app_context(self):
        with self.app.app_context():
            # application context is created explicitly by app_context()
            assert _app_ctx_stack.top is not None
            assert _request_ctx_stack.top is None

            app_ctx = _app_ctx_stack.top

            with self.app.test_request_context('/'):
                # application context is not created by request context
                assert _app_ctx_stack.top is app_ctx
                # request context is created
                assert _request_ctx_stack.top is not None

            # explicitly created application context is not popped by request
            # context's pop method
            assert _app_ctx_stack.top is app_ctx
            # request context is popped by request context's __exit__ method
            assert _request_ctx_stack.top is None

        # explicitly created application context is popped by application
        # context's __exit__ method
        assert _app_ctx_stack.top is None
        assert _request_ctx_stack.top is None

    def test_cilent_and_test_request_context_without_app_context(self):
        with self.app.test_request_context():
            assert _app_ctx_stack.top is not None
            assert _request_ctx_stack.top is not None

            app_ctx = _app_ctx_stack.top
            req_ctx = _request_ctx_stack.top

            with self.app.test_client() as c:
                assert _app_ctx_stack.top is app_ctx
                assert _request_ctx_stack.top is req_ctx

                c.get('/')

                assert _app_ctx_stack.top is app_ctx
                assert _request_ctx_stack.top is not req_ctx

            assert _app_ctx_stack.top is app_ctx
            assert _request_ctx_stack.top is req_ctx

        assert _app_ctx_stack.top is None
        assert _request_ctx_stack.top is None

    def test_cilent_and_test_request_context_with_app_context(self):
        with self.app.app_context():
            assert _app_ctx_stack.top is not None
            assert _request_ctx_stack.top is None

            app_ctx = _app_ctx_stack.top

            with self.app.test_request_context():
                assert _app_ctx_stack.top is app_ctx
                assert _request_ctx_stack.top is not None

                req_ctx = _request_ctx_stack.top

                with self.app.test_client() as c:
                    assert _app_ctx_stack.top is app_ctx
                    assert _request_ctx_stack.top is req_ctx

                    c.get('/')

                    assert _app_ctx_stack.top is app_ctx
                    assert _request_ctx_stack.top is not req_ctx

                assert _app_ctx_stack.top is app_ctx
                assert _request_ctx_stack.top is req_ctx

            assert _app_ctx_stack.top is app_ctx
            assert _request_ctx_stack.top is None

        assert _app_ctx_stack.top is None
        assert _request_ctx_stack.top is None


if __name__ == '__main__':
    unittest.main()