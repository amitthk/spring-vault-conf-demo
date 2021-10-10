import ConfigParser
from flask import Flask
import os
import hvac


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/config/')
def config():
    str = []
    str.append('<p> Debug: '+app.config['DEBUG']+'</p>')
    str.append('<p>'+'port: '+app.config['PORT']+'</p>')
    str.append('<p>'+'ip_address: '+app.config['IP_ADDRESS']+'</p>')
    str.append('<p>'+'db_user: '+app.config['dbuser']+'</p>')
    str.append('<p>'+'db_password: '+app.config['dbpass']+'</p>')
    return '<br/>'.join(str)

def init(app):
    config = ConfigParser.ConfigParser()
    try:
        config_location = "config/app.cfg"
        config.read(config_location)
        app.config['DEBUG'] = config.get("config", "DEBUG")
        app.config['IP_ADDRESS'] = config.get("config", "IP_ADDRESS")
        app.config['PORT'] = config.get("config", "PORT")
        app.config['VAULT_ADDR'] = config.get("config","VAULT_ADDR")
        app.config['VAULT_TOKEN'] = config.get("config","VAULT_TOKEN")
        app.config['VAULT_KEYS_PATH'] = config.get('config','VAULT_KEYS_PATH')
        print("Succesfully read configs from: " + config_location)
    except:
        print("Couldn't read configs from: " + config_location)
    try:
        client = hvac.Client(url=app.config['VAULT_ADDR'])
        client.token=token=app.config['VAULT_TOKEN']
        keys_path=app.config['VAULT_KEYS_PATH']
        keys_data=client.read(keys_path)
        for appkey in keys_data['data']['data']:
            app.config[appkey]=keys_data['data']['data'][appkey]
    except Exception as exc:
        print("Couldn't fetch config from vault: " + str(exc))
        raise exc

if __name__ == '__main__':
    init(app)
    app.run(
        host=app.config['IP_ADDRESS'],
        port=int(app.config['PORT']))
