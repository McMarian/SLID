# Installation Guide

## Application Setup

### With Docker

1. Clone the repository:
    ```
    git clone https://github.com/McMarian/SLID.git
    ```

2. Navigate to the project directory:
    ```
    cd SLID
    ```

3. Build and Run the Project Using Docker

    * Don't have Docker? Install it first:

        * For Windows: Download and install Docker Desktop from: [Docker For Windows](https://docs.docker.com/desktop/install/windows-install/).
        * For macOS: Download and install Docker Desktop from: [Docker For MacOS](https://docs.docker.com/desktop/install/mac-install/).
        * For Linux: Follow the instructions for your specific distribution in: [Docker For Linux](https://docs.docker.com/desktop/install/linux/).

    * Once Docker is installed, run the following command in your terminal:
        ```
        docker-compose up
        ```

4. Access the application locally at:
    `http://localhost:8000`


### Without Docker

1. Clone the repository:
    ```
    git clone https://github.com/McMarian/SLID.git
    ```

2. Navigate to the project directory:
    ```
    cd SLID
    ```

3. Create a virtual environment:
    ```
    python -m venv venv
    ```

4. Activate the virtual environment:
    * On Windows:
        ```
        venv\Scripts\activate
        ```
    * On macOS/Linux:
        ```
        source venv/bin/activate
        ```

5. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

6. Set up the database:
    ```
    python manage.py migrate
    ```

7. Run the development server:
    ```
    python manage.py runserver
    ```

8. Access the application locally at:
    `http://localhost:8000`

## Documentation Setup

If you want to run the documentation locally to view or contribute to it, you have two options:

### Using Docker (Recommended)

1. Make sure you have Docker installed (see instructions above)

2. Run the documentation server:
   ```bash
   docker-compose -f docker-compose-docs.yml up
   ```

3. Access the documentation at:
   `http://localhost:8080`

4. The documentation has live reload enabled - any changes you make to files in the `docs/` directory will automatically update in the browser.

### Without Docker

1. Create and activate a virtual environment (see instructions above)

2. Install documentation dependencies:
   ```bash
   pip install -r requirements-docs.txt
   ```

3. Run the MkDocs development server:
   ```bash
   mkdocs serve -a 0.0.0.0:8080
   ```

4. Access the documentation at:
   `http://localhost:8080`

## Building Documentation for Production

To build a static version of the documentation:

```bash
mkdocs build
```

This will create a `site/` directory with the static HTML files that can be deployed to any web server.

## Accessing the Hosted Documentation

The SLID documentation is automatically deployed to GitHub Pages whenever changes are pushed to the master branch of the repository. You can access the hosted documentation at:

[https://mcmarian.github.io/SLID/](https://mcmarian.github.io/SLID/)

### Deployment Process

The documentation is deployed through a GitHub Actions workflow that:

1. Runs when changes are pushed to the `docs/` directory or the `mkdocs.yml` file
2. Builds the documentation using MkDocs
3. Deploys the built site to the `gh-pages` branch
4. Makes the documentation available at the GitHub Pages URL

You can also manually trigger a deployment through the "Actions" tab in the GitHub repository.