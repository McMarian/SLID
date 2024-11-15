# Installation Guide

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