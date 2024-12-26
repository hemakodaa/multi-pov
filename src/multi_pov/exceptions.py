class FileEmptyError(Exception):
    """
    Raised when a file is found, but the file is empty.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
