from flask import Flask
from prometheus_client import Counter, generate_latest
from jaeger_client import Config
from flask_opentracing import FlaskTracing

app = Flask(__name__)

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')

# Tracing config
def init_tracer(service):
    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'logging': True,
        },
        service_name=service,
    )
    return config.initialize_tracer()

tracer = init_tracer('sample-app')
flask_tracer = FlaskTracing(tracer, True, app)

@app.route("/")
def hello():
    REQUEST_COUNT.inc()
    return "Hello World!"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
