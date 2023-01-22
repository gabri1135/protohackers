class BadRequest(Exception):
    def __init__(self, message, eof=False):
        self.message = message
        self.eof = eof
        super().__init__(self.message)