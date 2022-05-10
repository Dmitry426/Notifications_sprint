import os

from functools import wraps
from authlib.integrations.flask_client import OAuth
from db.postgresql import init_db
from flasgger import Swagger
from flask import Flask, request
from flask_app.db.redis import redis_db
# from db.redis import redis_db
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
init_db(app)

# from flask_app.services.jaeger import init_jaeger
# init_jaeger(app)

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({
            SERVICE_NAME: "flask_auth"})
    )
)
jaeger_exporter = JaegerExporter(
    agent_host_name=os.environ.get('JAEGER_AGENT_HOST', '127.0.0.1'),
    agent_port=int(os.environ.get('JAEGER_AGENT_PORT', '6831'))
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)


def response_hook(span, status, response_headers):
    if span and span.is_recording():
        span.set_attribute("custom_response_headers", str(response_headers))
        span.set_attribute("http.request_id", str(request.headers.get("X-Request-Id")))
        span.set_attribute("custom_response_status", str(status))


FlaskInstrumentor().instrument_app(app, response_hook=response_hook)
RequestsInstrumentor().instrument()
tracer = trace.get_tracer(__name__)


SWAGGER_TEMPLATE = template = {
  'swagger': '2.0',
  'info': {
    'title': 'Auth API команд - 17/2',
    'description': 'Жалкая попытка сделать OpenAPI',
    'version': '0.0.2',
    'contact': {
      'name': 'Litvinov_N_Y',
      'url': 'https://pastseason.ru/',
    }
  },
  'securityDefinitions': {
    'Bearer': {
      'type': 'apiKey',
      'name': 'Authorization',
      'in': 'header',
      'description': 'JWT Authorization header using the Bearer scheme. Example: \'Authorization: Bearer {token}\''
    }
  },
  'security': [
    {
      'Bearer': [ ]
    }
  ]

}
swag = Swagger(app, template=SWAGGER_TEMPLATE)
oauth = OAuth(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

oauth.google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url=os.getenv('ACCESS_TOKEN_URL'),
    access_token_params=None,
    authorize_url=os.getenv('AUTHORIZE_URL'),
    authorize_params=None,
    api_base_url=os.getenv('API_BASE_URL'),
    userinfo_endpoint=os.getenv('USERINFO_ENDPOINT'),
    client_kwargs={'scope': 'openid worker_email profile'},
)

oauth.yandex = oauth.register(
            name='yandex',
            client_id=os.getenv('YANDEX_CLIENT_ID'),
            client_secret=os.getenv('YANDEX_CLIENT_SECRET'),
            access_token_params=None,
            authorize_url=os.getenv('YANDEX_AUTHORIZE_URL'),
            authorize_params=None,
            response_type="code",
            display="popup",
            scope="login:info login:worker_email",
        )

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token_in_redis = redis_db.get(jti)
    return token_in_redis is not None
