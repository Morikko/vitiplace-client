# Vitiplace client

This module helps to interact with your wine collection data from the [vitiplace website](https://www.vitiplace.com/).

It is able to contact the vitiplace website to fetch information about:
- Wine
- Millesime
- Location
- Purchase history

One of the main feature is to save your data on your filesystem in `json` format.

# Usage
1. Require python 3.6+
2. Install the dependencies
3. Set up your credential through env vars to be used automatically (optional)
   1. `export VITIPLACE_CLIENT_EMAIL=your_email`
   2. `export VITIPLACE_CLIENT_PASSWORD=your_password`

## As code

```python
from vitiplace_client.website_view import (
    VitiplaceView,
)

viti_view = VitiplaceView()
viti_view.login() 
# Or if env vars are not net: 
# viti_view.login(
#   email="your_email",
#   password="your_password"
# )
page = viti_view.get_board_page()
```

## From CLI
```bash
python vitiplace_client/cli.py backup \
    -f /path/to/backup/file.json \
    # Following arguments if env vars are not net
    # --username your_username \
    # --password your_password
```

# About

## Contribution

Any contribution is welcome as long as the code is of quality. Please open an issue first. You are welcome to fork the project :)

## Data privacy

No data is collected by a third party.

Everything is run on your computer locally. All the code is visible here if you have doubt. You should provider yourself your credentials to connect to your vitiplace account.

## Affiliation

This project is **not** affiliated to the official vitiplace website. It is a project I made for backuping my data as the feature is not provided and I never got an answer from them.




