class PayloadValidator:
    def __init__(self):
        pass
        
    def validate(self, payload, expected_keys):

        if len(payload) != len(expected_keys):
            return False

        for key in expected_keys:
            if key not in payload or payload[key] == "":
                return False
        
        return True
            