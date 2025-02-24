import unittest
from unittest.mock import patch, Mock
import httpx  # type: ignore

from fraud_checker import (
    ParcelFraudChecker,
    ParcelHistory,
    APIError,
    InvalidMobileNumberError,
)


class TestParcelFraudChecker(unittest.TestCase):
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mobile_number = "01712345678"
        self.client = ParcelFraudChecker()

    def test_validate_mobile_number_valid(self) -> None:
        """Test that a valid mobile number returns True."""
        self.assertTrue(self.client.validate_mobile_number("01312345678"))
        self.assertTrue(self.client.validate_mobile_number("01412345678"))
        self.assertTrue(self.client.validate_mobile_number("01512345678"))
        self.assertTrue(self.client.validate_mobile_number("01612345678"))
        self.assertTrue(self.client.validate_mobile_number("01712345678"))
        self.assertTrue(self.client.validate_mobile_number("01812345678"))
        self.assertTrue(self.client.validate_mobile_number("01912345678"))

    def test_validate_mobile_number_invalid(self) -> None:
        """Test that an invalid mobile number returns False."""
        self.assertFalse(
            self.client.validate_mobile_number("01112345678")
        )  # Invalid prefix
        self.assertFalse(self.client.validate_mobile_number("0171234567"))  # Too short
        self.assertFalse(self.client.validate_mobile_number("017123456789"))  # Too long
        self.assertFalse(
            self.client.validate_mobile_number("0171234567a")
        )  # Non-digit character
        self.assertFalse(
            self.client.validate_mobile_number("0171234567 ")
        )  # Trailing space

    def test_generate_random_headers(self) -> None:
        """Test that random headers are generated correctly."""
        headers = self.client._generate_random_headers()
        self.assertIsInstance(headers, dict)
        self.assertIn("accept", headers)
        self.assertIn("user-agent", headers)
        self.assertIn("sec-fetch-dest", headers)

    def test_generate_cookie_header(self) -> None:
        """Test that random cookie headers are generated correctly."""
        cookie_header = self.client._generate_cookie_header()
        self.assertIsInstance(cookie_header, str)
        self.assertIn("_ga=GA1.1.", cookie_header)
        self.assertIn("_ga_GBPSJZSK7Z=GS1.1.", cookie_header)

    @patch("httpx.Client")
    def test_check_parcel_history_success(self, mock_httpx_client: Mock) -> None:
        """Test a successful API request."""
        # Mock the API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "user_name": None,
            "courierData": [
                {"label": "pathao", "order": 0, "cancell": 0},
                {"label": "steadfast", "order": 3, "cancell": 0},
                {"label": "redx", "order": 0, "cancell": 0},
                {"label": "paperfly", "order": 0, "cancell": 0},
            ],
            "source": "1",
        }
        mock_httpx_client.return_value.get.return_value = mock_response

        # Call the method
        result = self.client.check_parcel_history(self.mobile_number)

        # Validate the result
        self.assertIsInstance(result, ParcelHistory)
        self.assertEqual(result.user_name, None)
        self.assertEqual(len(result.courier_data), 1)
        self.assertEqual(result.courier_data[0].label, "Label")

    @patch("httpx.Client")
    def test_check_parcel_history_invalid_mobile_number(
        self, mock_httpx_client: Mock
    ) -> None:
        """Test that an invalid mobile number raises InvalidMobileNumberError."""
        with self.assertRaises(InvalidMobileNumberError):
            self.client.check_parcel_history("01112345678")  # Invalid prefix

    @patch("httpx.Client")
    def test_check_parcel_history_api_error(self, mock_httpx_client: Mock) -> None:
        """Test that an API error raises APIError."""
        # Mock an API error
        mock_httpx_client.return_value.get.side_effect = httpx.HTTPStatusError(
            "API error", request=None, response=None
        )

        with self.assertRaises(APIError):
            self.client.check_parcel_history(self.mobile_number)

    @patch("httpx.Client")
    def test_check_parcel_history_network_error(self, mock_httpx_client: Mock) -> None:
        """Test that a network error raises APIError."""
        # Mock a network error
        mock_httpx_client.return_value.get.side_effect = httpx.RequestError(
            "Network error"
        )

        with self.assertRaises(APIError):
            self.client.check_parcel_history(self.mobile_number)


if __name__ == "__main__":
    unittest.main()
