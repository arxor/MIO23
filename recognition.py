import json


class Jesture:
    items = []

    def __init__(self):
        self.items.append(self)
        self.name = "jf"
        self.data = None

    def save_to_file(self):

        try:
            with open("gestures.json", "r") as f:
                gestures = json.load(f)
        except json.decoder.JSONDecodeError:
            gestures = []

        for gesture in gestures:
            if gesture['name'] == self.name:
                gesture['data'].append(self.data)
                break
        else:
            save = {"name": self.name, "index": len(gestures), "data": [self.data]}
            gestures.append(save)

        with open("gestures.json", "w") as f:
            json.dump(gestures, f, indent=4)
