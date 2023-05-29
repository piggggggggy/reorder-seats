import json


class MemberInfoManager:
    def __init__(self, json_file):
        self.json_file = json_file
        self.members = []

    def load_members_from_json(self):
        try:
            with open(self.json_file, "r", encoding='utf-8') as file:
                self.members = json.load(file)
        except FileNotFoundError:
            self.members = []

    def save_members_to_json(self):
        with open(self.json_file, "w", encoding='utf-8') as file:
            json.dump(self.members, file, ensure_ascii=False)

    def update_members(self, data):
        self.members = data
