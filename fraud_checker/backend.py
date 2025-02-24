from __future__ import annotations

import random
import re
from typing import Any, Self, Optional

import httpx  # type: ignore

from .exceptions import APIError, InvalidMobileNumberError
from .models import ParcelHistory


class ParcelFraudChecker:
    """
    A client for interacting with the courier fraud check API.

    Handles request construction, validation, and error handling while maintaining
    proper separation of concerns and encapsulation.
    """

    MOBILE_NUMBER_PATTERN = re.compile(
        r"^01[3-9]\d{8}$"
    )  # Compile regex once for reuse

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://llcgteam.com/courier-fraud-checker",
        request_timeout: float = 10.0,
    ):
        """
        Initialize the API client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API endpoint
            request_timeout: Timeout for API requests in seconds
        """
        self.api_key = api_key or "a350886c400925aaed32f3bb4ead7c8799"  # Enjoy
        self.base_url = base_url.rstrip("/")
        self.request_timeout = request_timeout
        self._client = httpx.Client(timeout=request_timeout)

    @staticmethod
    def validate_mobile_number(mobile_number: str) -> bool:
        """
        Validate Bangladeshi mobile number format.

        Args:
            mobile_number: Number to validate (11 digits starting with 013-019)

        Returns:
            bool: True if valid, False otherwise
        """
        return bool(ParcelFraudChecker.MOBILE_NUMBER_PATTERN.match(mobile_number))

    def _generate_random_headers(self) -> dict[str, str]:
        """Generate randomized headers to mimic browser behavior."""
        chrome_version = random.randint(100, 140)
        platform = random.choice(
            [
                "X11; Linux x86_64",
                "Windows NT 10.0; Win64; x64",
                "Macintosh; Intel Mac OS X 10_15_7",
            ]
        )

        return {
            "accept": "application/json",
            # "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "cookie": self._generate_cookie_header(),
            "priority": "u=1, i",
            "referer": f"{self.base_url}/",
            "sec-ch-ua": (
                f'"Not/A)Brand";v="99", "Google Chrome";v="{chrome_version}", '
                f'"Chromium";v="{chrome_version}"'
            ),
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": f'"{platform.split(";")[0].split(" ")[0]}"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": (
                f"Mozilla/5.0 ({platform}) AppleWebKit/537.36 "
                f"(KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36"
            ),
            # "x-requested-with": "XMLHttpRequest",
        }

    def _generate_cookie_header(self) -> str:
        """Generate random GA cookie values."""

        def rand_ga_part() -> str:
            return f"{random.randint(1000000000, 9999999999)}"

        return (
            f"_ga=GA1.1.{rand_ga_part()}.{rand_ga_part()}; "
            f"_ga_GBPSJZSK7Z=GS1.1.{rand_ga_part()}.1.1.{rand_ga_part()}.0.0.0"
        )

    def check_parcel_history(self, mobile_number: str) -> ParcelHistory:
        """
        Retrieve parcel history for a mobile number.

        Args:
            mobile_number: Valid Bangladeshi mobile number (11 digits)

        Returns:
            ParcelHistory: Parsed response data

        Raises:
            InvalidMobileNumberError: For invalid number format
            APIError: For failed API requests

        Example:
            >>> with ParcelFraudChecker(api_key="your api_key") as client:
            ...     history = await client.check_parcel_history("01712345678")
            ...     print(history)
            ParcelHistory(user_name="John Doe", ...)
            >>> print(type(history))
            <class 'fraud_checker.models.ParcelHistory'>
        """
        if not self.validate_mobile_number(mobile_number):
            raise InvalidMobileNumberError(f"Invalid mobile number: {mobile_number}")

        try:
            response = self._client.get(
                url=f"{self.base_url}/fatch.php",
                params={"api_key": self.api_key, "term": mobile_number},
                headers=self._generate_random_headers(),
            )
            return ParcelHistory.from_json(response.json())

        except httpx.HTTPStatusError as e:
            raise APIError(f"API request failed: {e.response.status_code}") from e

        except httpx.RequestError as e:
            raise APIError(f"Network error: {str(e)}") from e
