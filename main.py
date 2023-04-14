import importlib
from flask import Flask
from flask import Blueprint
import os

app = Flask(__name__)

for filename in os.listdir("jarvis_modules"):
    if filename.endswith(".py") and not filename.endswith("__init__.py"):
        module = importlib.import_module(f"jarvis_modules.{filename[:-3]}")
        for name in dir(module):
            if isinstance(getattr(module, name), Blueprint):
                app.register_blueprint(getattr(module, name))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3141)
