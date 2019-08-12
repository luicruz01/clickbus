FLASK
===============

Installation Instructions:


1. Install virtualenv and pip (actually, pip should be installed automatically as a dependency of recent virtualenv versions):

    `easy_install virtualenv pip`

2. Create a virtual environment

    `virtualenv .venv`

3. Activate your virtual environment

    `source .venv/bin/activate`

4. Install requirements.

    `pip install -r requirements.txt`
    
5. Add repository dir to PYTHONPATH environment variable. In this example the repo is at `/central_maestra/`

    `export PYTHONPATH=/clickbus/:$PYTHONPATH`
    
9. Run the API server.
     `python /clickbus/api/server/api_server.py`
