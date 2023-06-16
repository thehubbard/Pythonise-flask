from flask import Flask

app = Flask(__name__)
# May not be best practice check.
if app.config["TESTING"] == True:
    app.config.from_object("config.TestingConfig")
elif app.config["DEBUG"] == True:
    app.config.from_object("config.DevelopmentConfig")
else:
    app.config.from_object("config.ProductionConfig")


from app import views
from app import admin_views
from app import error_handlers
