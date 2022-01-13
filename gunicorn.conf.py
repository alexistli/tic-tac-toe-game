"""Gunicorn configuration file."""
import re

import structlog


# --- Structlog logging initialisation code

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
        del event_dict["time"]  # timestamper already in pre-chain
        del event_dict["agent"]  # not interested in agent

    return event_dict


structlog.configure(
    processors=[
        structlog.threadlocal.merge_threadlocal,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.ConsoleRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory,
    cache_logger_on_first_use=True,
)


# --- Gunicorn logger configuration code

# Add some info if the log entry is not from structlog.
pre_chain = [
    structlog.stdlib.add_log_level,
    structlog.stdlib.add_logger_name,
    timestamper,
    combined_logformat,
]

logfmt_processor = structlog.processors.LogfmtRenderer(
    key_order=["timestamp", "event", "view", "request_id", "peer"], drop_missing=True
)

logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "logfmt_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": logfmt_processor,
            "foreign_pre_chain": pre_chain,
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "logfmt_formatter",
        }
    },
    "loggers": {
        "gunicorn": {
            "propagate": False,
            "handlers": ["console"],
        },
    },
}
