import json
class Information:
    def __init__(self):
        self.file_name = 'data.json'
        self.game_users = []

    def put(self, name, idd):
        with open(self.file_name, 'r') as file_rd:
            dct_ids = json.load(file_rd)
            if name not in dct_ids:
                dct_ids[name] = idd
                dct_ids[idd] = name
                with open(self.file_name, 'w') as file_wr:
                    json.dump(dct_ids, file_wr)
            else:
                print('user is already registered!!!')

    def show(self, name):
        with open(self.file_name, 'r') as file:
            dct_ids = json.load(file)
            if name in dct_ids:
                return dct_ids[name]
            else:
                return False

    def app_user(self, name):
        self.game_users.append(name)

    def first_pl(self):
        return self.game_users[0]

    def second_pl(self):
        #returns false if only one user in users
        try:
            return self.game_users[1]
        except:
            return False