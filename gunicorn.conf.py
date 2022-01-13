"""Gunicorn configuration file."""
import logging
import re
import sys

import structlog


# ================ Structlog logging initialization code

logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)


timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")


def combined_logformat(logger, name, event_dict):
    """Custom processor for Gunicorn access events."""
    if event_dict.get("logger") == "gunicorn.access":
        message = event_dict["event"]

        parts = [
            r"(?P<host>\S+)",  # host %h
            r"\S+",  # indent %l (unused)
            r"(?P<user>\S+)",  # user %u
            r"\[(?P<time>.+)\]",  # time %t
            r'"(?P<request>.+)"',  # request "%r"
            r"(?P<status>[0-9]+)",  # status %>s
            r"(?P<size>\S+)",  # size %b (careful, can be '-')
            r'"(?P<referer>.*)"',  # referer "%{Referer}i"
            r'"(?P<agent>.*)"',  # user agent "%{User-agent}i"
        ]
        pattern = re.compile(r"\s+".join(parts) + r"\s*\Z")
        m = pattern.match(message)
        res = m.groupdict()

        if res["user"] == "-":
            res["user"] = None

        res["status"] = int(res["status"])

        if res["size"] == "-":
            res["size"] = 0
        else:
            res["size"] = int(res["size"])

        if res["referer"] == "-":
            res["referer"] = None

        event_dict.update(res)

        # Final selection
        del event_dict["event"]  # not interested in raw event
        del event_dict["host"]  # not interested in host
        del event_dict["user"]  # not interested in user
        del event_dict["time"]  # timestamper already in pre-chain
        del event_dict["size"]  # not interested in size
        del event_dict["agent"]  # not interested in agent

    return event_dict


structlog.configure(
    processors=[
        structlog.threadlocal.merge_threadlocal,
        structlog.dev.ConsoleRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory,
    cache_logger_on_first_use=True,
)

# ================ Gunicorn logger configuration code

#
# Server socket
#
#   bind - The socket to bind.
#
#       A string of the form: 'HOST', 'HOST:PORT', 'unix:PATH'.
#       An IP is a valid HOST.

bind = "0.0.0.0:8000"

#
# Worker processes
#
#   workers - The number of worker processes that this server
#       should keep alive for handling requests.
#
#       A positive integer generally in the 2-4 x $(NUM_CORES)
#       range. You'll want to vary this a bit to find the best
#       for your particular application's work load.
#
#   worker_class - The type of workers to use. The default
#       sync class should handle most 'normal' types of work
#       loads. You'll want to read
#       http://docs.gunicorn.org/en/latest/design.html#choosing-a-worker-type
#       for information on when you might want to choose one
#       of the other worker classes.
#
#       A string referring to a Python path to a subclass of
#       gunicorn.workers.base.Worker. The default provided values
#       can be seen at
#       http://docs.gunicorn.org/en/latest/settings.html#worker-class
#
#   worker_connections - For the eventlet and gevent worker classes
#       this limits the maximum number of simultaneous clients that
#       a single process can handle.
#
#       A positive integer generally set to around 1000.
#
#   timeout - If a worker does not notify the master process in this
#       number of seconds it is killed and a new worker is spawned
#       to replace it.
#
#       Generally set to thirty seconds. Only set this noticeably
#       higher if you're sure of the repercussions for sync workers.
#       For the non sync workers it just means that the worker
#       process is still communicating and is not tied to the length
#       of time required to handle a single request.
#
#   keepalive - The number of seconds to wait for the next request
#       on a Keep-Alive HTTP connection.
#
#       A positive integer. Generally set in the 1-5 seconds range.

workers = 4
worker_class = "eventlet"
worker_connections = 1000
timeout = 30
keepalive = 2

#
# Logging
#
#   capture_output - Redirect stdout/stderr to specified file in errorlog.

capture_output = True

# Add some info if the log entry is not from structlog.
pre_chain = [
    structlog.stdlib.add_log_level,
    structlog.stdlib.add_logger_name,
    timestamper,
    combined_logformat,
]

logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
            "foreign_pre_chain": pre_chain,
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console_formatter",
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "console_formatter",
        },
    },
    "loggers": {
        "gunicorn.error": {
            "propagate": False,
            "handlers": ["error_console"],
        },
        "gunicorn.access": {
            "propagate": False,
            "handlers": ["console"],
        },
        "app": {
            "propagate": False,
            "handlers": ["console"],
        },
    },
}
