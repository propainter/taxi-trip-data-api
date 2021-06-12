# services/web/server/main/views.py
import sys
import datetime as dt
from s2 import s2
# from flask import Blueprint,
from flask import  jsonify, request, current_app
# from server.appcache import cache
from server.controller.tasks import sparkTasks 

app = current_app
# main_blueprint = Blueprint('main', __name__,url_prefix="/api/v1")


DATE_FORMAT_ISO = "%Y-%m-%d"


# @main_blueprint.route('/', methods=['GET'])
def home():
    response_object = {
        'status': 'OK',
        'msg': "Hello Word!",
        'method': sys._getframe(  ).f_code.co_name
    }
    return jsonify(response_object), 200





# @main_blueprint.route('/total_trips', methods=['GET'])
def total_trips():
    
    '''
    Total number of trips per day

    GET /total_trips?start=start-date&end=end-date
    curl http://localhost:8080/total_trips?start=2019-01-31

    {
    "data": [
    { "date": "2020-01-01", "total_trips": 321 },
    { "date": "2020-01-02", "total_trips": 432 },
    '''
    start_date_string = request.args.get('start-date', default = "", type = str)
    end_date_string = request.args.get('end-date', default = "", type = str)
    
    try:
        start_date = dt.datetime.strptime(start_date_string, DATE_FORMAT_ISO)
        end_date = dt.datetime.strptime(end_date_string, DATE_FORMAT_ISO)
        if  len(start_date_string) == 0 or len(end_date_string) == 0:
            return jsonify(response_object = {
                'status': 'FAIL',
                'msg': "Invalid Arguments!"
            }), 200
        if end_date < start_date:
            return jsonify(response_object = {
                'status': 'FAIL',
                'msg': "Invalid Arguments! end_date less than start date"
            }), 200
        # --
            # run spark job here
        
        try:
            result = []
            for item in sparkTasks.total_trips_counts_between_dates(start_date, end_date):
                result.append({ "date" : dt.datetime.strftime(item[0], DATE_FORMAT_ISO), "total_trips": item[1]})
            return jsonify(response_object = {
                'status': 'OK',
                'msg': "Hello Word!",
                'data': result,
                'method': sys._getframe(  ).f_code.co_name
            }), 200
        except:
            return jsonify(response_object = {
                'status': 'FAIL',
                'msg': "Something went wrong!"
            }), 500
    except:
        return jsonify(response_object = {
                'status': 'FAIL',
                'msg': "required args missing OR not in correct dateformat!"
            }), 500
        

# @main_blueprint.route('/average_fare_heatmap', methods=['GET'])
def average_fare_heatmap():

    '''
    Fare heatmap

    average fare  per pick up location S2ID at level 16 for given date

    $ curl http://localhost:8080/average_fare_heatmap?date=2019-01-01
    {
    "data": [
    { "s2id": "951977d37", "fare": 13.21 },
    { "s2id": "951977d39", "fare": 4.32 },
    { "s2id": "951977d40", "fare": 5.43 },
    '''
    date_string = request.args.get('date', default = "", type = str)
    try:
        if len(date_string) == 0:
            return jsonify(response_object = {
                'status': 'FAIL',
                'msg': "Invalid Arguments!"
            }), 200
        input_date = dt.datetime.strptime(date_string, DATE_FORMAT_ISO)
        try:
            # run spark job here
            result = []
            for item in sparkTasks.average_fare_heatmap_by_date(input_date):
                p = item[0]
                try:
                    if p.startswith('POINT'):
                        items = [float(_) for _ in p[p.index('(')+1:p.index(')')].split(' ')]
                        s2id = s2.geo_to_s2(items[0], items[1], 16)
                        result.append({ "s2id" : s2id, "fare": float("{0:.2f}".format(item[1]))})
                except:
                    app.logger.error("Cannot parse POINT {}".format(p))
            
            return jsonify(response_object = {
                'status': 'OK',
                'msg': "Hello Word!",
                'data': result,
                'method': sys._getframe(  ).f_code.co_name
            }), 200
        except:
            return jsonify(response_object = {
                'status': 'FAIL',
                'msg': "Something went wrong!"
            }), 500
    except:
        return jsonify(response_object = {
                'status': 'FAIL',
                'msg': "required args missing OR not in correct dateformat!"
            }), 500
            


# @main_blueprint.route('/average_speed_24hrs', methods=['GET'])
def average_speed_24hrs():
    '''
    Average speed in the past 24 hours
    GET /average_speed_24hrs?date=<date>

    $ curl http://localhost:8080/average_speed_24hrs?date=2019-01-01
    "data": [
    { "average_speed": 24.7 }

    '''
    date_string = request.args.get('date', default = "", type = str)
    try:
        if len(date_string) == 0:
            return jsonify(response_object = {
                'status': 'FAIL',
                'msg': "Invalid Arguments!"
            }), 200
        input_date = dt.datetime.strptime(date_string, DATE_FORMAT_ISO)

        try:
            # run spark job here
            speed = sparkTasks.average_speed_24hrs(input_date)[0][0]
            speed_output = float("{0:.2f}".format(speed))
            result= {"average_speed": speed_output}
            return jsonify(response_object = {
                'status': 'OK',
                'msg': "Hello Word!",
                'data': result,
                'method': sys._getframe(  ).f_code.co_name
            }), 200
        except:
            return jsonify(response_object = {
                'status': 'FAIL',
                'msg': "Something went wrong!"
            }), 500
    except:
        return jsonify(response_object = {
                'status': 'FAIL',
                'msg': "required args missing OR not in correct dateformat!"
            }), 500



# @main_blueprint.route('/work', methods=['GET'])
def dowork():
    try:
        # import time
        # time.sleep(10)
        return jsonify(response_object = {
                    'status': 'OK',
                    'msg': "pong"
                }), 200
    except:
        return jsonify(response_object = {
                'status': 'FATAL',
                'msg': "Something wrong happened!"
            }), 500


# @main_blueprint.route('/spark', methods=['GET'])
def dospark():
    
    try:
        
        countVal = sparkTasks.sample_work()
        return jsonify(response_object = {
                    'status': 'OK',
                    'msg': "countValue is {}".format(countVal)
                }), 200
    except:
        return jsonify(response_object = {
                'status': 'FATAL',
                'msg': "Something wrong happened!"
            }), 500

try:
    from pyspark import SparkContext, SparkConf
except:
    pass

