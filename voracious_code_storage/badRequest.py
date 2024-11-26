class BadRequest(Exception):
    def __init__(self, message: str, eof: bool = False):
        self.message = message
        self.eof = eof
        super().__init__(self.message)
