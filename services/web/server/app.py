import os

from flask import Flask
from flask_caching import Cache
import server.controller.views as views

cache = Cache()
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    cacheConfig={
        'CACHE_TYPE': 'simple',
        # 'DEBUG': True,
        'CACHE_DEFAULT_TIMEOUT': 300
    }
    app.config.from_mapping(cacheConfig)
    cache.init_app(app, cacheConfig)

    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    API_URI_PREFIX='/api/v1'
    @app.route(API_URI_PREFIX+'/', methods=['GET'])
    @cache.cached(timeout=app.config.get('API_CACHE_TIMEOUT', 10))
    def home():
        return views.home()
    @app.route(API_URI_PREFIX+'/total_trips', methods=['GET'])
    @cache.cached(timeout=app.config.get('API_CACHE_TIMEOUT', 10))
    def total_trips():
        return views.total_trips()
    @app.route(API_URI_PREFIX+'/average_fare_heatmap', methods=['GET'])
    @cache.cached(timeout=app.config.get('API_CACHE_TIMEOUT', 10))
    def average_fare_heatmap():
        return views.average_fare_heatmap()
    @app.route(API_URI_PREFIX+'/average_speed_24hrs', methods=['GET'])
    @cache.cached(timeout=app.config.get('API_CACHE_TIMEOUT', 10))
    def average_speed_24hrs():
        return views.average_speed_24hrs()
    @app.route(API_URI_PREFIX+'/ping', methods=['GET'])
    # @cache.cached(timeout=app.config.get('API_CACHE_TIMEOUT', 10))
    def dowork():
        return views.dowork()
    @app.route(API_URI_PREFIX+'/spark', methods=['GET'])
    # @cache.cached(timeout=app.config.get('API_CACHE_TIMEOUT', 10))
    def dospark():
        return views.dospark()
    
    
    # @app.route('/ping')
    # @cache.cached(timeout=app.config.get('API_CACHE_TIMEOUT', 10))
    # def hello():
        
    #     return 'pong'

    return app, cache