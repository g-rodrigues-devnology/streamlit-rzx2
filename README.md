# Installation Guide

To set up the project, please install the required dependencies and activate the virtual environment. Follow the steps below:

1. Ensure you have Python installed on your system.
2. Open a terminal and navigate to the project directory.
3. Create a virtual environment by running:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

5. Install the dependencies listed in `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

You're now ready to use the project!

```
streamlint run src/render/format.py
```

All other scripts should be ran independently.