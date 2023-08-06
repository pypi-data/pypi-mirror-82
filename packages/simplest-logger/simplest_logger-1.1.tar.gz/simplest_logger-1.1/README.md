## simplest_logger

simplest_logger is a very simple library for logging for Python 3.5+


# Usage examples

### Creating a Logger object

    from simplest_logger import Logger

    logger = Logger("my_logging_file.log")

You can also log something only in the console:

    logger = Logger()  # print_to_console is True by default

Or you can specify the encoding of your records:

    logger = Logger("my_logging_file.log", encoding="cp1251")  # Cyrillic encoding

### Logging something

    logger.log("MY LOG TYPE", "My message")  # Writes or/and prints a record

Record will look like `[CURRENT DATE AND TIME] [LOG TYPE] - MESSAGE\n`

There is also shortcuts to some frequently used log types.

    # Record type is DEBUG
    logger.debug(f"Variable {a=}")

    # Record type is INFO
    logger.info(f"Received a message from user {user.id}: {message.text}")

    # Record type is WARNING
    logger.warning(
        f"Cached info about user {user.id} not found, it will be downloaded!"
    )

    # Record type is ERROR
    logger.error(f"Error while serving the user {user.id}:\n{get_traceback(exc)}")

    # Record type is CRITICAL
    logger.error(f"Database file {db_file_path} not found!")

You can inherit from the Logger class and add more shortcuts if you want.
