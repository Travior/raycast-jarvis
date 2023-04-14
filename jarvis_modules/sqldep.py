from flask import Blueprint
from flask import request
from sqllineage.runner import LineageRunner
import re

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
            if len(result.target_tables) >= 1:
                target = str(result.target_tables[0]) 
            else:
                target = ""
            response["dependencies"].append(
                {
                    "statement": re.sub(r"(' +')", " ", statement.strip().replace("\n", "")),
                    "tables": [str(t) for t in result.source_tables],
                    "target": target
                }
            )
        return response
    return ("bad request", 400)

@sqldep_bp.route("/sqlcoldep")
def get_column_level_dependencies():
    data = request.get_json(silent=True)
    if data is not None and "sql" in data.keys():
        response = {"number_of_statements": 0, "dependencies": []}
        result = LineageRunner(data["sql"])
        response["number_of_statements"] = len(result.statements())
        for statement in result.statements():
            r = LineageRunner(statement)
            cols = r.get_column_lineage()
            if len(result.target_tables) >= 1:
                target = str(result.target_tables[0]) 
            else:
                target = ""
            response["dependencies"].append(
                {
                    "statement": re.sub(r"(' +')", " ", statement.strip().replace("\n", "")),
                    "tables": [str(t) for t in r.source_tables],
                    "columns": [{"column":str(c[-1]), "dependencies":[str(col) for col in c[:-1]]} for c in cols],
                    "target": target
                })
        print(response)
        return response
    return("",200)
