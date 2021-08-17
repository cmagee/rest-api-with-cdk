""" Lambda Handler """
import json
import logging
from dataclasses import dataclass, field

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


@dataclass
class Request:
    """API Request Class"""

    path: str
    http_method: str
    headers: dict
    query_string_parameters: dict
    path_parameters: dict
    stage_variables: dict
    request_context: dict
    body: str
    multi_value_headers: dict = field(default_factory=lambda: {})
    multi_value_query_string_parameters: dict = field(default_factory=lambda: {})


@dataclass
class Response:
    """API Response Class"""

    statusCode: int
    headers: dict = field(
        default_factory=lambda: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        }
    )
    isBase64Encoded: bool = False
    body: str = ""

    def set_header(self, key: str, value: str):
        """Set response header"""
        self.headers[key] = value


def unmarshall_event(event: dict):
    return Request(
        path=event["path"],
        http_method=event["httpMethod"],
        headers=event["headers"],
        multi_value_headers=event["multiValueHeaders"],
        query_string_parameters=event["queryStringParameters"],
        multi_value_query_string_parameters=event["multiValueQueryStringParameters"],
        path_parameters=event["pathParameters"],
        stage_variables=event["stageVariables"],
        request_context=event["requestContext"],
        body=event["body"],
    )


def lambda_handler(event, _context):
    """Main entry point"""
    response = None
    LOGGER.info("Incoming API Request: %s", event)
    request = unmarshall_event(event)

    if request.http_method == "GET" and request.path == "/v1/healthcheck":
        response = Response(
            statusCode=200, body=json.dumps({"status": "API Available"})
        )

    return response.__dict__
