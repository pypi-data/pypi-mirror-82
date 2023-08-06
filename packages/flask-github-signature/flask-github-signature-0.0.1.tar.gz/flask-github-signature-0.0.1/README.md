# flask-github-signature

[![Python package](https://github.com/pabluk/flask-github-signature/workflows/Python%20package/badge.svg)](https://github.com/pabluk/flask-github-signature/actions?query=workflow%3A%22Python+package%22)

A Flask view decorator to verify [Github's webhook signatures](https://docs.github.com/en/free-pro-team@latest/developers/webhooks-and-events/securing-your-webhooks).

# Usage

```console
export GH_WEBHOOK_SECRET="xyz"
```

```python
from flask import Flask
from flask_github_signature import verify_signature 

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
@verify_signature
def hello_world():
    return "Hello, World!"
```

# Testing

If you want to test, play or contribute to this repo:

```console
git clone git@github.com:pabluk/flask-github-signature.git
cd flask-github-signature/
pip install -r requirements.txt
pip install -e .
python -m unittest tests/test_main.py
```
