# Django France Connect starter kit

This starter kit provides a simple Django implementation of France Connect authentication system.
It provides a simple `FranceConnectAuth()` object that you can use in your Django application.

## Usage

### Requirements

- Python 3+
- pipenv
- Content of requirements.txt file

### Preparation

- Clone the repo

- Adapt settings :
France Connect settings are in `djangofranceconnect/settings.py`. It's provided with test credentials and URLs, but you can change with your own if needed:

```python
FRANCE_CONNECT_URL = 'https://fcp.integ01.dev-franceconnect.fr'
FRANCE_CONNECT_CLIENT_ID = '211286433e39cce01db448d80181bdfd005554b19cd51b3fe7943f6b3b86ab6e'
FRANCE_CONNECT_CLIENT_SECRET = '2791a731e6a59f56b6b4dd0d08c9b1f593b5f3658b9fd731cb24248e2669af4b'
FRANCE_CONNECT_CALLBACK_URL = "http://localhost:8080/callback"
FRANCE_CONNECT_CALLBACK_DISCONNECT_URL = "http://localhost:8080/logout"
```

### Installation

```bash
pipenv install
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate
```

### Run

- Run the demo server :

```bash
pipenv run python manage.py runserver 8080
```

- Access to your localhost endpoint `127.0.0.1:8080`.

- Check code exemples in `djangofranceconnect/franceconnect/views.py`

## Full documentation

Official documentation [here](https://partenaires.franceconnect.gouv.fr/fcp/fournisseur-service).

## Warning

This implementation is a simple starter kit to develop your own FranceConnect FS integration.
Provided 'as is', it does not provide any security against CRSF attach nor replay attack. Depending on your implementation, you MUST implement a serious STATE and NONCE checking (see 9. Glossaire: STATE and NONCE in official [documentation](https://partenaires.franceconnect.gouv.fr/fcp/fournisseur-service)).
