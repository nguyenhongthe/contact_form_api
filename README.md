# Contact Form API

Welcome to Contact Form API documentation. This is FastAPI-based API is designed for submitting contact forms and receiving notifications. Follow the instructions below to install and use the API.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)

## Features

- Submit contact forms with the following fields:
  - Name
  - Email
  - Phone
  - Title
  - Message
- Send email notifications to the recipient using an SMTP server
- Send Discord notifications to a Discord webhook
- Store contact form submissions in a PostgreSQL database
- API documentation using Swagger UI and ReDoc

## Requirements

- Python 3.8+

The API is built using the following libraries:

- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Pydantic](https://pypi.org/project/pydantic-settings/) - Settings management using Pydantic
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [PostgreSQL](https://www.postgresql.org/) - Database
- [Psycopg](https://pypi.org/project/psycopg2-binary/) - psycopg2 - Python-PostgreSQL Database Adapter
- [Python-Multipart](https://pypi.org/project/python-multipart/) - A streaming multipart parser for Python.
- [smtp](https://docs.python.org/3/library/smtplib.html) - Email sending
- [uvicorn](https://www.uvicorn.org/) - ASGI server
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Environment variables
- [httpx](https://www.python-httpx.org/) - HTTP client
- [Discord Webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) - Discord Webhooks

## Installation

### Running Locally

To run the API locally, follow these steps:

**Note:**

   - Make sure you have Python 3.8+ installed on your system.
   - You need to have a PostgreSQL database running on your system and create a database for the API. Refer to the [PostgreSQL documentation](https://www.postgresql.org/docs/) for more information.

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

- Swagger UI - [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- ReDoc - [http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)
- OpenAPI JSON - [http://localhost:8000/api/openapi.json](http://localhost:8000/api/openapi.json)

### Submitting a Contact Form

To submit a contact form, send a POST request to the `/submit-contact-form` endpoint with the following form parameters:

- `name`: Name of the sender
- `email`: Email of the sender
- `phone`: Phone number of the sender
- `title`: Title of the message
- `message`: Message content

Example using cURL:

```bash
curl -X 'POST' \
  'http://localhost:8000/submit-contact-form' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'name=My%20Name&email=myname%40gmail.com&phone=0123456789&title=Hello&message=Hello%20World'
```

## Configuration

The application uses environment variables for configuration. Make sure to define these variables in the `.env` file before running the application. Refer to the `.env.example` file for a list of required variables.

For detailed configuration options, consult the `Settings` class in the `main.py` file.

## Contributing

Contributions are welcome! Feel free to [open an issue](https://github.com/nguyenhongthe/contact_form_api/issues) or submit a [pull request](https://github.com/nguyenhongthe/contact_form_api/pulls) if you find a bug or want to improve the API.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more information.