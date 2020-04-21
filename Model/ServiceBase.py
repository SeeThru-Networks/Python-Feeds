from datetime import datetime


class ServiceBase:
    def __init__(self, name, **kwargs):
        self.status = "red"
        self.message = ""
        self.name = name
        if "output" in kwargs: self.output = kwargs["output"]

    def get_name(self): return self.name

    def run(self):
        pass

    def get_value(self):
        return ""

    def evaluate(self, value):
        self.status = "red"
        self.message = "Not implemented"

    def dump(self):
        print("Status: " + self.status)
        print("Message: " + self.message)

    def get_result(self):
        return "{\"color\":\"%s\", \"message\":\"%s\", \"time\":\"%s\"}" % (
            self.status,
            self.message,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    #Requires the output argument to be passed into the service initialiser
    def export(self):
        if self.output:
            file = open(self.output, "w")
            file.write(self.get_result())
            file.close()
