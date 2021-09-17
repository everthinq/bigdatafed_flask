from flask import Blueprint, render_template, request
from flask import jsonify
import json

main = Blueprint('main', __name__)


@main.route('/data')
def get_data():
    """
    To get the data user need to pass both week_start and week_end dates.
    The process may be simplified by passing only one date and
    checking if the dates is in between week_start and week_end range.
    For example user passes '2016-08-05' that is between '2016-07-31' and '2016-08-06'
    so we can return data that related to week_start == '2016-07-31' and week_end == '2016-08-06'
    :return: json data for the exact period of time.
    """

    week_start = request.args.get('week_start')
    week_end = request.args.get('week_end')

    with open('data.json') as f:
        for item in json.load(f):
            if week_start == item['week_start'] and week_end == item['week_end']:
                return jsonify(item)

    return 'Input a valid week_start and week_end'


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/', methods=['POST'])
def index_post():
    """
    I've added more interaction here, so user can upload custom files and get the data from them instantly.
    Every time user uploads any files, I'm merging everything into data.json file and updating it, which
    may be good for the test task, but not so good for production.
    :return: json data from all uploaded xls files. Creates a data.json file which is used for API.
    """
    if request.method == 'POST':
        if request.form['action'] == 'Upload':
            import re
            from datetime import datetime
            from openpyxl import load_workbook
            files = request.files.getlist('files')

            future_json = []
            for file in files:
                workbook = load_workbook(file)

                for sheet in workbook:
                    temp_dict = {}

                    week_start = re.findall('\d{2}-\d{2}-\d{4}', sheet['A3'].value)[0]
                    week_start = str(datetime.strptime(week_start, '%m-%d-%Y').date())
                    week_end = re.findall('\d{2}-\d{2}-\d{4}', sheet['A3'].value)[1]
                    week_end = str(datetime.strptime(week_end, '%m-%d-%Y').date())

                    temp_dict['0test_filename'] = file.filename
                    temp_dict['0test_page'] = sheet.title
                    temp_dict['week_start'] = week_start
                    temp_dict['week_end'] = week_end

                    for row in sheet['A7':'C30']:
                        if row[0].value is not None:
                            temp_dict[row[0].value] = row[2].value

                    future_json.append(temp_dict)

            with open('data.json', 'w') as f:
                f.write(json.dumps(future_json, sort_keys=False))

            return jsonify(future_json)

    return 'This thing didnt work as expected. ' \
           'Whether your method is not POST or ' \
           'your request.form[action] is not Upload. ' \
           'Or something else?'
