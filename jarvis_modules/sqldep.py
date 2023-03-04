from flask import Blueprint
from flask import request
from sqlglot import parse_one, exp

sqldep_bp = Blueprint("sqldep", __name__)

@sqldep_bp.route("/sqldep")
def get_dependencies():
    data = request.get_json(silent=True)
    if data is not None and "sql" in data.keys():
        tables = parse_one(data['sql']).find_all(exp.Table)
        return [table.name for table in tables]
    return ("bad request", 400)
