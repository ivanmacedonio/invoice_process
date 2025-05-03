import unittest
from unittest.mock import patch
from app.domain.decorators.error_handling_provider import error_handling_provider
import requests


class TestErrorHandlingProvider(unittest.TestCase):

    def setup_functions_that_raises(self):

        def raise_value_error():
            raise ValueError("unhandled value error")

        def raise_type_error():
            raise TypeError("unhandled type error")

        def raise_key_error():
            raise KeyError("unhandled key error")

        def raise_attribute_error():
            raise AttributeError("unhandled attribute error")

        def raise_request_exception_error():
            raise requests.RequestException("unhandled request error")

        def raise_general_exception():
            raise Exception("unhandled general error")

        self.raise_value_error = error_handling_provider(raise_value_error)
        self.raise_type_error = error_handling_provider(raise_type_error)
        self.raise_key_error = error_handling_provider(raise_key_error)
        self.raise_attribute_error = error_handling_provider(
            raise_attribute_error)
        self.raise_request_exception_error = error_handling_provider(
            raise_request_exception_error)
        self.raise_general_exception = error_handling_provider(
            raise_general_exception)

    def setUp(self):
        self.setup_functions_that_raises()

    @patch("app.config.logger.logger.error")
    def test_handler_value_error(self, mock_logger):

        self.raise_value_error()
        mock_logger.assert_any_call(
            "Unexpected Value error: unhandled value error")

    @patch("app.config.logger.logger.error")
    def test_handler_type_error(self, mock_logger):

        self.raise_type_error()
        mock_logger.assert_any_call(
            "Unexpected Type error: unhandled type error")

    @patch("app.config.logger.logger.error")
    def test_handler_key_error(self, mock_logger):

        self.raise_key_error()
        mock_logger.assert_any_call(
            "Unexpected Key error: 'unhandled key error'")

    @patch("app.config.logger.logger.error")
    def test_handler_attribute_error(self, mock_logger):

        self.raise_attribute_error()
        mock_logger.assert_any_call(
            "Unexpected Attribute error: unhandled attribute error")

    @patch("app.config.logger.logger.error")
    def test_handler_request_exception_error(self, mock_logger):

        self.raise_request_exception_error()
        mock_logger.assert_any_call(
            "Unexpected request error: unhandled request error")

    @patch("app.config.logger.logger.error")
    def test_handler_general_exception(self, mock_logger):

        self.raise_general_exception()
        mock_logger.assert_any_call(
            "Unexpected unhandled exception: unhandled general error")


if __name__ == "__main__":
    unittest.main()
