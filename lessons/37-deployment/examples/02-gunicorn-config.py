"""
Gunicorn Configuration Example
==============================

Bu fayl Gunicorn WSGI server uchun production-ready konfiguratsiyani ko'rsatadi.

Usage:
    gunicorn --config gunicorn_config.py config.wsgi:application

Or in systemd service:
    ExecStart=/path/to/venv/bin/gunicorn --config /path/to/gunicorn_config.py config.wsgi:application
"""

import multiprocessing
import os

# ============================================================================
# SERVER SOCKET
# ============================================================================

# Bind address
# bind = "0.0.0.0:8000"  # Listen on all interfaces
bind = "127.0.0.1:8000"  # Only local (recommended with Nginx)

# Maximum number of pending connections
backlog = 2048


# ============================================================================
# WORKER PROCESSES
# ============================================================================

# Number of worker processes
# Formula: (2 x $num_cores) + 1
workers = multiprocessing.cpu_count() * 2 + 1

# The type of workers to use
# Options: sync, eventlet, gevent, tornado, gthread
worker_class = "sync"

# Maximum number of simultaneous clients (for eventlet/gevent)
worker_connections = 1000

# Workers silent for more than this many seconds are killed and restarted
timeout = 30

# The maximum number of requests a worker will process before restarting
max_requests = 1000
max_requests_jitter = 50  # Add randomness to prevent all workers restarting at once

# Timeout for graceful workers restart
graceful_timeout = 30

# Number of seconds to wait for the next request on a Keep-Alive HTTP connection
keepalive = 2


# ============================================================================
# PROCESS NAMING
# ============================================================================

# A base to use with setproctitle for process naming
proc_name = "library-api"


# ============================================================================
# SERVER MECHANICS
# ============================================================================

# Daemonize the Gunicorn process (detach & enter background)
daemon = False  # False for systemd, True for traditional init

# A filename to use for the PID file
pidfile = "/var/run/gunicorn/gunicorn.pid"

# Switch worker processes to run as this user
user = "www-data"
group = "www-data"

# A directory to use for the worker heartbeat temporary file
worker_tmp_dir = "/dev/shm"  # Use RAM instead of disk

# A directory to store temporary uploaded files
tmp_upload_dir = None


# ============================================================================
# LOGGING
# ============================================================================

# Access log file
accesslog = "/var/log/gunicorn/access.log"
# accesslog = "-"  # Log to stdout

# Error log file
errorlog = "/var/log/gunicorn/error.log"
# errorlog = "-"  # Log to stderr

# The granularity of error log outputs
# Options: debug, info, warning, error, critical
loglevel = "info"

# Access log format
# h: remote address
# l: '-'
# u: user name
# t: date of the request
# r: status line (e.g. GET / HTTP/1.1)
# s: status
# b: response length
# f: referer
# a: user agent
# T: request time in seconds
# D: request time in microseconds
# L: request time in decimal seconds
# p: process ID
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'

# Disable redirect access logs to syslog
disable_redirect_access_to_syslog = False

# Redirect stdout/stderr to specified files
# capture_output = True
# accesslog = "/var/log/gunicorn/stdout.log"
# errorlog = "/var/log/gunicorn/stderr.log"


# ============================================================================
# SSL/HTTPS
# ============================================================================

# SSL key file
keyfile = None
# keyfile = "/path/to/keyfile"

# SSL certificate file
certfile = None
# certfile = "/path/to/certfile"

# SSL version to use
# ssl_version = 2  # TLSv1

# CA certificates file
# ca_certs = "/path/to/ca_certs"

# Suppress ragged EOFs (see Python documentation)
# suppress_ragged_eofs = True

# Whether cert reqs are from the client side
# cert_reqs = 0  # ssl.CERT_NONE

# SSL ciphers
# ciphers = 'TLSv1'


# ============================================================================
# SECURITY
# ============================================================================

# Limit the maximum size of HTTP request header fields
limit_request_fields = 100

# Limit the maximum size of HTTP request line
limit_request_line = 4094

# Limit the allowed size of an HTTP request header field
limit_request_field_size = 8190


# ============================================================================
# SERVER HOOKS
# ============================================================================

def on_starting(server):
    """
    Called just before the master process is initialized.
    """
    print("Gunicorn server is starting...")


def on_reload(server):
    """
    Called to recycle workers during a reload via SIGHUP.
    """
    print("Gunicorn server is reloading...")


def when_ready(server):
    """
    Called just after the server is started.
    """
    print(f"Gunicorn server is ready. Listening on: {bind}")


def pre_fork(server, worker):
    """
    Called just before a worker is forked.
    """
    pass


def post_fork(server, worker):
    """
    Called just after a worker has been forked.
    """
    print(f"Worker {worker.pid} spawned")


def pre_exec(server):
    """
    Called just before a new master process is forked.
    """
    print("Forked child, re-executing.")


def worker_int(worker):
    """
    Called when a worker receives the INT or QUIT signal.
    """
    print(f"Worker {worker.pid} received INT or QUIT signal")


def worker_abort(worker):
    """
    Called when a worker receives the SIGABRT signal.
    """
    print(f"Worker {worker.pid} received SIGABRT signal")


def post_worker_init(worker):
    """
    Called just after a worker has initialized the application.
    """
    print(f"Worker {worker.pid} initialized")


def worker_exit(server, worker):
    """
    Called just after a worker has been exited.
    """
    print(f"Worker {worker.pid} exited")


def nworkers_changed(server, new_value, old_value):
    """
    Called just after num_workers has been changed.
    """
    print(f"Number of workers changed from {old_value} to {new_value}")


def on_exit(server):
    """
    Called just before exiting Gunicorn.
    """
    print("Gunicorn server is shutting down...")


# ============================================================================
# DEVELOPMENT CONFIGURATION
# ============================================================================

"""
Development Configuration
------------------------

For development, use simpler settings:

# gunicorn_dev.py
bind = "0.0.0.0:8000"
workers = 2
worker_class = "sync"
timeout = 60
loglevel = "debug"
reload = True  # Auto-reload on code changes
accesslog = "-"
errorlog = "-"
"""


# ============================================================================
# PERFORMANCE TUNING
# ============================================================================

"""
Performance Tuning Tips
----------------------

1. Workers:
   - Formula: (2 x CPU cores) + 1
   - For CPU-bound: CPU cores + 1
   - For I/O-bound: (2 x CPU cores) + 1
   
2. Worker Class:
   - sync: Default, good for most use cases
   - gevent: For high concurrency, I/O-bound
   - eventlet: Similar to gevent
   - gthread: Multi-threaded workers
   
3. Timeout:
   - Default: 30 seconds
   - Long-running tasks: Increase timeout
   - Or use Celery for async tasks
   
4. Max Requests:
   - Prevents memory leaks
   - Workers restart after X requests
   - Recommended: 1000-5000
   
5. Worker Tmp Dir:
   - Use RAM (/dev/shm) instead of disk
   - Faster heartbeat mechanism
   
6. Keepalive:
   - Lower for many clients
   - Higher for fewer clients
"""


# ============================================================================
# MONITORING & DEBUGGING
# ============================================================================

"""
Monitoring Commands
------------------

# View running workers
ps aux | grep gunicorn

# Check worker count
pgrep -c -f "gunicorn: worker"

# Send signals
kill -HUP <master-pid>   # Reload configuration
kill -USR2 <master-pid>  # Upgrade Gunicorn on the fly
kill -TERM <master-pid>  # Graceful shutdown
kill -QUIT <master-pid>  # Quick shutdown

# View logs
tail -f /var/log/gunicorn/access.log
tail -f /var/log/gunicorn/error.log

# Monitor with systemd
systemctl status gunicorn
journalctl -u gunicorn -f
"""


# ============================================================================
# EXAMPLE: PRODUCTION CONFIGURATION
# ============================================================================

"""
# Production optimized configuration

import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 2000
max_requests_jitter = 100
graceful_timeout = 30

user = "www-data"
group = "www-data"
worker_tmp_dir = "/dev/shm"

accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

proc_name = "library-api"
pidfile = "/var/run/gunicorn/gunicorn.pid"

# SSL (if not using Nginx for SSL termination)
# keyfile = "/etc/ssl/private/server.key"
# certfile = "/etc/ssl/certs/server.crt"
"""


# ============================================================================
# EXAMPLE: HIGH CONCURRENCY CONFIGURATION
# ============================================================================

"""
# For high concurrency with gevent

import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
worker_connections = 10000  # Much higher for gevent
timeout = 60

# Install: pip install gevent

# Note: gevent requires greenlet-compatible code
# Not all Django code is greenlet-compatible
"""


# ============================================================================
# TROUBLESHOOTING
# ============================================================================

"""
Common Issues
------------

1. Workers timeout:
   - Increase timeout value
   - Check for slow database queries
   - Use Celery for long tasks

2. High memory usage:
   - Reduce number of workers
   - Lower max_requests
   - Check for memory leaks

3. Connection refused:
   - Check bind address
   - Verify firewall rules
   - Check if socket file exists

4. Workers die unexpectedly:
   - Check error logs
   - Increase graceful_timeout
   - Check system resources

5. 502 Bad Gateway (Nginx):
   - Verify Gunicorn is running
   - Check bind address matches Nginx config
   - Check socket permissions
"""