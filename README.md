# Fraud Checker

A Python client for checking parcel fraud history for Bangladesh.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Support](#support)

---

## Features

- **Validate Bangladeshi Mobile Numbers**: Ensure the mobile number is in the correct format.
- **Check Parcel History**: Retrieve parcel history for a given mobile number.
- **Error Handling**: Properly handles invalid inputs and API errors.
- **Randomized Headers**: Mimics browser behavior to avoid detection.

---

## Installation

You can install the `fraud_checker` package via pip:

```bash
pip install fraud_checker
```

Alternatively, you can install it directly from the source:

```bash
git clone https://github.com/Almas-Ali/fraud_checker.git
cd fraud_checker
pip install .
```

---

## Usage

### Basic Example

```python
from fraud_checker import ParcelFraudChecker

client = ParcelFraudChecker()
history = client.check_parcel_history("01712345678")
print(history)
```

### Example Output

```python
ParcelHistory(
    user_name=None,
    courier_data=[
        ParcelData(label='pathao', order=0, cancel=0),
        ParcelData(label='steadfast', order=0, cancel=0),
        ParcelData(label='redx', order=0, cancel=0),
        ParcelData(label='paperfly', order=0, cancel=0)
    ],
    source="1"
)
```

---

## API Reference

### `ParcelFraudChecker`

#### `__init__(self, ..., request_timeout: float = 10.0)`

Initialize the API client.

- **`request_timeout`**: Timeout for API requests in seconds (default: 10.0).

#### `check_parcel_history(self, mobile_number: str) -> ParcelHistory`

Retrieve parcel history for a mobile number.

- **`mobile_number`**: A valid Bangladeshi mobile number (11 digits).
- **Returns**: A `ParcelHistory` object containing the parcel history data.
- **Raises**:
  - `InvalidMobileNumberError`: If the mobile number format is invalid.
  - `APIError`: If the API request fails.

#### `validate_mobile_number(self, mobile_number: str) -> bool`

Validate a Bangladeshi mobile number.

- **`mobile_number`**: The number to validate.
- **Returns**: `True` if valid, `False` otherwise.

---

### Models

#### `ParcelHistory`

Represents the parcel history data.

- **`user_name`**: The name associated with the mobile number (if available).
- **`courier_data`**: A list of `ParcelData` objects.
- **`source`**: The source of the data.

#### `ParcelData`

Represents a single parcel entry.

- **`label`**: The courier service name (e.g., "pathao").
- **`order`**: The number of orders.
- **`cancel`**: The number of cancellations.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Thanks to LLCG for providing the API.
- Inspired by the need for a simple and reliable way to check parcel fraud history.

---

## Support

For questions, issues, or feature requests, please open an issue on [GitHub](https://github.com/Almas-Ali/fraud_checker/issues).
