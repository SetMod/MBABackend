from marshmallow import Schema, fields, post_load
from typing import List
from datetime import datetime


class AnalyzeOptions:
    def __init__(
        self,
        lines_limit: int,
        lines: List[str],
        recreate: bool = False,
        scheduled_time: datetime = None,
    ) -> None:
        self.lines_limit = lines_limit
        self.lines = lines
        self.recreate = recreate
        self.scheduled_time = scheduled_time


class AnalyzeOptionsSchema(Schema):
    lines_limit = fields.Int()
    lines = fields.List(fields.Str())
    recreate = fields.Bool()
    scheduled_time = fields.DateTime("iso")

    @post_load
    def make_analyze_options(self, data, **kwargs):
        return AnalyzeOptions(**data)

    # @post_load
    # def format_lines(self, in_data, **kwargs):
    #     def format_lines(line: str):
    #         if "-" in line:
    #             line = line.split("-")
    #             lines = range(int(line[0]), (line[1]))
    #             return lines
    #         else:
    #             return int(line)

    #     in_data["lines"] = map(format_lines, in_data["lines"])
    #     return in_data


analyze_options_schema = AnalyzeOptionsSchema()
