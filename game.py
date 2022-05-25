class Game:
    def __init__(self, dire_heroes, radiant_heroes):
        self.dire_heroes = dire_heroes
        self.radiant_heroes = radiant_heroes

    def display(self):  # returns message about current teams' states
        text = ''
        text += 'dire:\n'
        for hero in self.dire_heroes:
            text += '\t' + str(hero) + '\n'
        text += 'radiant:\n'
        for hero in self.radiant_heroes:
            text += '\t' + str(hero) + '\n'
        return text

    def add_dire(self, hero):
        self.dire_heroes.append(hero)

    def add_radiant(self, hero):
        self.radiant_heroes.append(hero)

    def reset(self):
        self.radiant_heroes.clear()
        self.dire_heroes.clear()
