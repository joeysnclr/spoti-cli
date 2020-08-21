from flask import Flask, request
import json
import os
import logging
import requests


# config methods
def readConfig():
    with open("./clify.json", "r+") as file:
        config = json.load(file)
    return config


def writeConfig(config):
    with open("./clify.json", "w+") as file:
        json.dump(config, file)


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

    config = readConfig()
    config['code'] = code
    writeConfig(config)

    return "enjoy clify!"


@app.route('/shutdown')
def shutdown():
    quit()


def run():
    app.run()
