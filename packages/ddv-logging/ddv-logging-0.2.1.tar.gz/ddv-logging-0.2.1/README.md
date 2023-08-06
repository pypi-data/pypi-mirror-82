# DDV Logging

Python logging formatters, filters, and convenience methods.

**GitLab:** https://gitlab.com/davidevi/ddv-logging

**PyPi:** https://pypi.org/project/ddv-logging/

**Features:**
- Can enable printing of logs to `stdout`
- Can indent logs based on position in stack trace
- Can colour the log level
- Can filter out modules from the log output based on verbosity levels

### Usage Example

The code:
```python
import logging

from ddv.logging import log_to_stdout

logger = logging.getLogger(__name__)


class A(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__ + ".A")
        self.logger.debug("Creating instance of A")
        self.b = B()
        self.A1()

    def A1(self):
        self.logger.info("A1 has been called")


class B(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__ + ".B")
        self.logger.debug("Creating instance of B")
        self.c = C()
        self.B1()

    def B1(self):
        self.logger.info("B1 has been called")


class C(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__ + ".C")
        self.logger.debug("Creating instance of C")
        self.C1()

    def C1(self):
        self.logger.info("C1 has been called")


def main():

    verbosity_filters = {  # Verbosity 0 will display none
        1: ["__main__.A"], # Verbosity 1 will display A
        2: ["__main__.B"], # Verbosity 2 will display A and B
        3: ["__main__.C"]  # Verbosity 3 will display A, B, and C
    }

    log_to_stdout(
        logging_level=logging.DEBUG,
        enable_colours=True,
        enable_indentation=True,
        verbosity_filters=verbosity_filters,
        verbosity_level=2,
    )

    logger.info("Main has been called")
    A()
    logger.warning("Execution complete")


if __name__ == "__main__":
    main()
```

The output:

![Output](https://gitlab.com/davidevi/ddv-logging/-/raw/master/docs/output.png)

Verbosity levels could come from the command line:
```
program --arg1 --arg2 -vvv
```
Where the number of `v` dictates the verbosity level.

You could simply use the length of `-vvv` to determine verbosity level.  
