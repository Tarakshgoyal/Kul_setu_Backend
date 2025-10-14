# Gunicorn configuration file
import multiprocessing

# Bind to all interfaces on port 10000
bind = "0.0.0.0:10000"

# Number of worker processes
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class
worker_class = "sync"

# Worker timeout - increase to 300 seconds (5 minutes) for long operations like database initialization
timeout = 300

# Graceful timeout
graceful_timeout = 30

# Keep alive
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
