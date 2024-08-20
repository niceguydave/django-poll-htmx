![Tests](https://github.com/niceguydave/django-polls-htmx/workflows/Django%20CI%2FCD/badge.svg)

# Django Polls App with HTMX

This is a simple poll application using the [Django polls tutorial](https://docs.djangoproject.com/en/5.1/intro/tutorial01/) 
and enhancing it with [HTMX](https://htmx.org/) for a better, more dynamic user experience. 
HTMX allows you to add AJAX, CSS Transitions, WebSockets, and Server-Sent Events directly 
in HTML using attributes, providing a more interactive and responsive web application.

## Features

- Create and manage polls with multiple questions.
- Vote in polls and see real-time results using HTMX.
- Dynamically load content without a full page reload.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.x

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/niceguydave/django-poll-htmx.git
    cd django-poll-htmx
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

6. Open your browser and navigate to `http://127.0.0.1:8000/` to see the application in action.

## Usage

- **Create Polls:** Access the admin panel to create and manage polls. Navigate to `http://127.0.0.1:8000/admin/` and log in with your admin credentials.
- **Vote in Polls:** Users can vote in the polls directly on the poll detail pages. The results will be updated dynamically thanks to HTMX.
- **View Results:** Results are shown immediately after voting, providing real-time feedback without requiring a page refresh.

## Testing
The standard Django test suite is being used at present.

To verify that the tests work, run `python manage.py test`.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a Pull Request.

Please make sure your code follows the existing style and includes relevant tests.

## License

This project is licensed under the  BSD-2-Clause license - see the [LICENSE](https://github.com/niceguydave/django-poll-htmx/blob/main/LICENSE) file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [HTMX](https://htmx.org/)

