"""
ASSIGNMENT 14
Various Uses of the Python Logging Module

Demonstrates logging levels, formatters, handlers, rotating files,
logger hierarchy, exception logging, filters, lazy formatting and dictConfig.
"""

import logging
import logging.config
import logging.handlers
import os
import tempfile


LOG_DIR = tempfile.mkdtemp(prefix="logdemo_")


def section(title):
    print(f"\n{'=' * 8} {title} {'=' * 8}")


# ---------------------------------------------------------------------
# 1. THE FIVE LEVELS
# ---------------------------------------------------------------------
def demo_levels():
    section("1. Levels (threshold = DEBUG, everything shows)")
    log = logging.getLogger("levels")
    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)-8s %(message)s"))
    log.addHandler(handler)
    log.propagate = False

    log.debug("detailed info for developers")
    log.info("normal progress message")
    log.warning("something unexpected, still working")
    log.error("an operation failed")
    log.critical("the program may not continue")

    print("--- raise threshold to WARNING: DEBUG and INFO are hidden ---")
    log.setLevel(logging.WARNING)
    log.debug("you will NOT see this")
    log.info("you will NOT see this either")
    log.warning("but you WILL see this warning")


# ---------------------------------------------------------------------
# 2. FORMATTERS - control what each line looks like
# ---------------------------------------------------------------------
def demo_formatter():
    section("2. Formatter (time | logger | level | function | message)")
    log = logging.getLogger("format")
    log.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | "
        "%(funcName)s:%(lineno)d | %(message)s",
        datefmt="%H:%M:%S"
    ))
    log.addHandler(handler)
    log.propagate = False
    log.info("Formatted entry with time, place and level")


# ---------------------------------------------------------------------
# 3. HANDLERS - send ONE message to MANY places
# ---------------------------------------------------------------------
def demo_handlers():
    section("3. Two handlers: console (INFO+) and file (WARNING+)")
    path = os.path.join(LOG_DIR, "app.log")
    log = logging.getLogger("handlers")
    log.setLevel(logging.DEBUG)
    log.propagate = False

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(
        "CONSOLE   %(levelname)s - %(message)s"
    ))

    file_handler = logging.FileHandler(path)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s"
    ))

    log.addHandler(console)
    log.addHandler(file_handler)

    log.debug("debug: goes nowhere (both handlers ignore it)")
    log.info("info: console only")
    log.warning("warning: console AND file")
    log.error("error: console AND file")

    file_handler.flush()
    print("\nContents of app.log (only WARNING and above):")
    with open(path, encoding="utf-8") as file:
        for line in file:
            print(" FILE    ", line.rstrip())

    console.close()
    file_handler.close()


# ---------------------------------------------------------------------
# 4. ROTATING FILE HANDLER - stop log files growing forever
# ---------------------------------------------------------------------
def demo_rotation():
    section("4. RotatingFileHandler (max 200 bytes, keep 2 backups)")
    path = os.path.join(LOG_DIR, "rotate.log")
    log = logging.getLogger("rotate")
    log.setLevel(logging.INFO)
    log.propagate = False

    handler = logging.handlers.RotatingFileHandler(
        path, maxBytes=200, backupCount=2
    )
    handler.setFormatter(logging.Formatter("%(message)s"))
    log.addHandler(handler)

    for i in range(1, 21):
        log.info("rotating entry number %d", i)

    handler.close()
    log.removeHandler(handler)
    print("Files created:", sorted(
        name for name in os.listdir(LOG_DIR) if name.startswith("rotate")
    ))


# ---------------------------------------------------------------------
# 5. LOGGER HIERARCHY - child loggers inherit from parents
# ---------------------------------------------------------------------
def demo_hierarchy():
    section("5. Logger hierarchy (shop -> shop.cart, shop.pay)")
    parent = logging.getLogger("shop")
    parent.setLevel(logging.INFO)
    parent.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
    parent.addHandler(handler)

    logging.getLogger("shop.cart").info("item added to cart")
    logging.getLogger("shop.pay").info("payment accepted")
    logging.getLogger("shop.pay").debug("hidden: parent level is INFO")

    handler.close()
    parent.removeHandler(handler)


# ---------------------------------------------------------------------
# 6. LOGGING EXCEPTIONS - keeps the full traceback
# ---------------------------------------------------------------------
def demo_exception():
    section("6. logger.exception() records the traceback")
    log = logging.getLogger("errors")
    log.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    log.addHandler(handler)

    try:
        10 / 0
    except ZeroDivisionError:
        log.exception("Division failed")

    handler.close()
    log.removeHandler(handler)


# ---------------------------------------------------------------------
# 7. FILTERS - decide per message whether it is logged
# ---------------------------------------------------------------------
class HideSecrets(logging.Filter):
    def filter(self, record):
        return "password" not in record.getMessage().lower()


def demo_filter():
    section("7. Filter (blocks messages containing 'password')")
    log = logging.getLogger("secure")
    log.setLevel(logging.INFO)
    log.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    handler.addFilter(HideSecrets())
    log.addHandler(handler)

    log.info("user rahul logged in")
    log.info("password for rahul is 1234")  # blocked
    log.info("user rahul opened dashboard")

    handler.close()
    log.removeHandler(handler)


# ---------------------------------------------------------------------
# 8. LAZY FORMATTING and EXTRA FIELDS
# ---------------------------------------------------------------------
def demo_lazy_and_extra():
    section("8. Lazy formatting and extra={...} fields")
    log = logging.getLogger("extras")
    log.setLevel(logging.INFO)
    log.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "%(levelname)s user=%(user)s %(message)s"
    ))
    log.addHandler(handler)

    log.info(
        "order %d placed, total Rs.%.2f",
        42,
        1999.5,
        extra={"user": "rahul"}
    )

    handler.close()
    log.removeHandler(handler)


# ---------------------------------------------------------------------
# 9. dictConfig - configure everything in one dictionary
# ---------------------------------------------------------------------
def demo_dictconfig():
    section("9. dictConfig (whole setup in one dictionary)")
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "short": {
                "format": "%(levelname)s:%(name)s:%(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "short",
                "level": "INFO"
            }
        },
        "loggers": {
            "configured": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False
            }
        }
    }

    logging.config.dictConfig(config)
    logging.getLogger("configured").info(
        "configured entirely from a dict"
    )


if __name__ == "__main__":
    demo_levels()
    demo_formatter()
    demo_handlers()
    demo_rotation()
    demo_hierarchy()
    demo_exception()
    demo_filter()
    demo_lazy_and_extra()
    demo_dictconfig()
    print(f"\nLog files were written to: {LOG_DIR}")
