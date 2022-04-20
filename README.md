# Use library

Connect to lightbull:

    from lightbull import Lightbull
    l = Lightbull("http://localhost:8080", "lightbull password")

You can store the API URL and password in the config file (`~/.lightbull`):

    [lightbull]
    api_url = http://localhost:8080
    password = lightbull password

The API URL and password are not required then:

    from lightbull import Lightbull
    l = Lightbull()

# Code check

We use pre-commit for code and styleguide checks.

Install it once as git hook:

    pre-commit install

Run pre-commit manually:

    pre-commit run --all-files
