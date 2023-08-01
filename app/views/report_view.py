from datetime import datetime

from flask import jsonify, request

from app.utils.date_utils import parse_date, convert_date_to_int, date_in_range, validate_date_format
from app.services.report_service import generate_report


def generate_report_data(date):
    if request.method != 'GET':
        return jsonify({'error': 'Invalid request method. Only GET requests are allowed.'}), 405

    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify(
            {'error': f"Invalid date: {date}, date must exist and between range 2019-08-01 and 2019-09-29."}), 400

    validate_date_format(date)
    parsed_date = parse_date(date)
    check_date = convert_date_to_int(date)

    if date_in_range(check_date):

        report_data = generate_report(parsed_date)
        return report_data
    else:
        return jsonify(
            {'error': f"Date out of range: {parsed_date}, date must be range 2019-08-01 and 2019-09-29."}), 400
