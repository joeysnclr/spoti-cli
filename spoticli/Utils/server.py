from flask import Flask, request
import json
import os
import logging
import requests
from spoticli.Utils.utils import userdata

# create flask app
app = Flask(__name__)
log = False
if not log:
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'
    app.logger.disabled = True
    log = logging.getLogger('werkzeug')
    log.disabled = True


@app.route('/auth')
def hello_world():
    error = request.args.get("error", False)
    if error:
        return "error! try again please"
    code = request.args.get("code")

    userdata.set("code", code)
    return "success!"


@app.route('/shutdown')
def shutdown():
    quit()


def runServer():
    app.run()
