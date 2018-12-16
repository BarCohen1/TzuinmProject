class Prof:

    def __init__(self, name, units, grade):
        self.name = str(name)
        self.units = str(units)
        self.grade = str(grade)

    def __repr__(self):
        return self.name + ' ,' + self.units + ' ,' + self.grade

class Request:

    def __init__(self, url, Parsed_payload, headers):
        self.url = str(url)
        self.Payload = str(Parsed_payload)
        self.headers = dict(headers)