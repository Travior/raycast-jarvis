from flask import Blueprint
from flask import request
from sqllineage.runner import LineageRunner

sqldep_bp = Blueprint("sqldep", __name__)


@sqldep_bp.route("/sqldep")
def get_dependencies():
    data = request.get_json(silent=True)
    if data is not None and "sql" in data.keys():
        response = {"number_of_statements": 0, "dependencies": []}
        result = LineageRunner(data["sql"])
        response["number_of_statements"] = len(result.statements())
        for statement in result.statements():
            result = LineageRunner(statement)
            response["dependencies"].append(
                {
                    "statement": statement,
                    "tables": [str(t) for t in result.source_tables],
                }
            )
        return response
    return ("bad request", 400)
