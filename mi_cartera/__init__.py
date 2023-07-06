from flask import Flask

app = Flask(__name__)
app.config.from_prefixed_env() #Le digo que me coja la config del prefixed env. Y lo prefijamos