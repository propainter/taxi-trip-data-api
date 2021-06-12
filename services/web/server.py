import os
from server import app
# from server.controller import views

app,cache = app.create_app()


app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

# app.register_blueprint(views.main_blueprint)


app.run(
    threaded= True,
    host= '0.0.0.0',
    port= 5000
    )

