# Flask-Tus-Cont
Flask Extension implementing the Tus.io server protocol. This project was reuploaded to Pypi under the 'Flask-Tus-Cont' name to allow a modern working version of this repo to continue serving requirements.

This repo is a fork of the fixed repo from jzwolak on github, [repo found here](https://github.com/jzwolak/Flask-Tus).
jzwolak's repo is a pull request of the original repo by matthoskins1980 [found here](https://github.com/matthoskins1980/Flask-Tus)

## Prerequisites (redis)

Currently flask-tus-cont is reliant on a local redis server.  This is used for caching information about
uploads in progress.  It is on the roadmap to remove this dependancy.  You must install the redis python package
for this extension to work.

```
pip install redis
```

## Installation

Installation from source (this repository)

```
python setup.py install
```

Installation from PyPi repository (recommended for latest stable release)

```
pip install Flask-Tus-Cont
```

## Usage

### demo.py

```python
from flask import Flask, render_template, send_from_directory
from flask_tus_cont import tus_manager
import os

app = Flask(__name__)
tm = TusManager(app, upload_url='/file-upload', upload_folder='uploads/')
```

TusManager() registers two new url endpoint /file-upload and /file-upload/\<resource\>.  You can not define views for those
urls in your app.  Simply use any tus client and point it to  /file-upload as the endpoint
