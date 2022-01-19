"""Logging configuration for Gunicorn and Flask using structlog."""
import logging.config
import re

import structlog
from gunicorn import glogging


def combined_logformat(_, __, event_dict):
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


timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
pre_chain = [
    # Add the log level and a timestamp to the event_dict if the log entry
    # is not from structlog.
    structlog.stdlib.add_log_level,
    # Add extra attributes of LogRecord objects to the event dictionary
    # so that values passed in the extra parameter of log methods pass
    # through to log output.
    structlog.stdlib.ExtraAdder(),
    timestamper,
    combined_logformat,
]

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(),
                "foreign_pre_chain": pre_chain,
            },
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
                "foreign_pre_chain": pre_chain,
            },
        },
        "handlers": {
            "development": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
            "production": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "json",
            },
        },
        "loggers": {
            "": {"handlers": ["development"], "level": "DEBUG", "propagate": True}
        },
    }
)

structlog.configure(
    processors=[
        structlog.threadlocal.merge_threadlocal,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


class GunicornLogger(glogging.Logger):
    """Subclass of the original Gunicorn logging class.

    A subclass of https://github.com/benoitc/gunicorn/blob/master/gunicorn/glogging.py
    to provide structlog logging in gunicorn.
    """

    def __init__(self, cfg):
        """Constructor or the GunicornLogger class.

        Some arguments are redefined to benefit from structlog,
        and some unused arguments are removed.
        """
        self.error_log = structlog.get_logger("gunicorn.error")
        self.error_log.propagate = False
        self.access_log = structlog.get_logger("gunicorn.access")
        self.access_log.propagate = False
        self.error_handlers = []
        self.access_handlers = []
        self.cfg = cfg

    def reopen_files(self) -> None:
        """Some method we do not need."""
        pass  # we don't support files

    def close_on_exec(self) -> None:
        """Some method we do not need."""
        pass  # we don't support files
