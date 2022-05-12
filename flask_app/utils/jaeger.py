import functools
import os

import jaeger_client
from flask import request
from flask_opentracing import FlaskTracer
from jaeger_client import Config


def _setup_jaeger():
    return Config(
        config={
            "sampler": {"type": "const", "param": 1},
            "local_agent": {
                "enabled": os.getenv("JAEGER_TRACING", False),
                "reporting_port": os.environ.get(
                    "JAEGER_AGENT_PORT", jaeger_client.config.DEFAULT_REPORTING_PORT
                ),
                "reporting_host": os.environ.get("JAEGER_AGENT_HOST", "jaeger_auth_6"),
            },
            "logging": os.environ.get("JAEGER_LOGGING", False),
        },
        service_name=os.environ.get("JAEGER_SERVICE_NAME", "auth_jaeger_6"),
        validate=True,
    ).initialize_tracer()


def init_jaeger(app):
    tracer = FlaskTracer(_setup_jaeger, True, app=app)

    @tracer.trace()
    @app.before_request
    def before_request():
        request_id = request.headers.get("X-Request-Id")
        parent_span = tracer.get_span()
        parent_span.set_tag("http.request_id", request_id)
