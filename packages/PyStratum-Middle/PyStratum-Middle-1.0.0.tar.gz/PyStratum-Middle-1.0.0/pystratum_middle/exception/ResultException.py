import os


class ResultException(RuntimeError):
    """
    Exception for situations where the result (set) of a query does not meet the expectations. Either a mismatch between
    the actual and expected numbers of rows selected or an unexpected NULL value was selected.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, expected_row_count: str, actual_row_count: int, query: str):
        """
        Object constructor.

        :param str expected_row_count: The expected row count.
        :param int actual_row_count: The actual row count.
        :param str query: The query.
        """
        RuntimeError.__init__(self, self.__message(expected_row_count, actual_row_count, query))

        self._expected_row_count: str = expected_row_count
        """
        The expected row count.
        """

        self._actual_row_count: int = actual_row_count
        """
        The actual row count.
        """

        self._query: str = query
        """
        The query.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def expected_row_count(self) -> str:
        """
        The expected row count.

        :rtype: str
        """
        return self._expected_row_count

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def actual_row_count(self) -> int:
        """
        The actual row count.

        :rtype: str
        """
        return self._actual_row_count

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def query(self) -> str:
        """
        The query.

        :rtype: str
        """
        return self._query

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __message(expected_row_count: str, actual_row_count: int, query: str) -> str:
        """
        Composes the exception message.

        :param str expected_row_count: The expected row count.
        :param int actual_row_count: The actual row count.
        :param str query: The query.

        :rtype: str
        """
        query = query.strip()

        message = 'Wrong number of rows selected'
        message += os.linesep
        message += 'Expected number of rows: {}'.format(expected_row_count)
        message += os.linesep
        message += 'Actual number of rows: {}'.format(actual_row_count)
        message += os.linesep
        message += 'Query:'
        message += os.linesep if os.linesep in query else ' '
        message += query

        return message

# ----------------------------------------------------------------------------------------------------------------------
