class ResponseBody:
    def __init__(self, message, code, data):
        self.message = message
        self.code = code
        self.data = data
    def to_dict(self):
        return {
            "message": self.message,
            "code": self.code,
            "data": str(self.data)
        }