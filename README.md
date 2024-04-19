# Contact Form API

Welcome to Contact Form API documentation. This is FastAPI-based API is designed for submitting contact forms and receiving notifications. Follow the instructions below to install and use the API.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)

## Requirements

- Python 3.8+

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nguyenhongthe/contact_form_api.git
   cd contact_form_api
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and set the necessary environment variables. Refer to the `.env.example` file for guidance.

4. Run the API server:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

The API should now be up and running at http://localhost:8000.

## Usage

API documentation can be accessed through the following URLs:

- [Swagger UI - http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- [ReDoc - http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)
- [OpenAPI JSON - http://localhost:8000/api/openapi.json](http://localhost:8000/api/openapi.json)

### Submitting a Contact Form

To submit a contact form, send a POST request to the `/submit-contact-form` endpoint with the following form parameters:

- `name`: Name of the sender
- `email`: Email of the sender
- `phone`: Phone number of the sender
- `title`: Title of the message
- `message`: Message content

Example using cURL:

```bash
curl -X POST "http://localhost:8000/submit-contact-form" -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "name=John%20Doe&email=john@example.com&phone=123456789&budget=High&message=Hello%20World"
```

## Configuration

The application uses environment variables for configuration. Make sure to define these variables in the `.env` file before running the application. Refer to the `.env.example` file for a list of required variables.

For detailed configuration options, consult the `Settings` class in the `main.py` file.

## Contributing

Contributions are welcome! Feel free to [open an issue](https://github.com/nguyenhongthe/contact_form_api/issues) or submit a [pull request](https://github.com/nguyenhongthe/contact_form_api/pulls) if you find a bug or want to improve the API.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more information.