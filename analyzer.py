import requests
from bs4 import BeautifulSoup


class Analayzer:
    hero_list = ['abaddon', 'alchemist', 'ancient-apparition', 'anti-mage', 'axe', 'bane', 'batrider', 'beastmaster',
                 'bloodseeker', 'bounty-hunter', 'brewmaster', 'bristleback', 'broodmother', 'centaur-warrunner',
                 'chaos-knight', 'chen', 'clinkz', 'clockwerk', 'crystal-maiden', 'dark-seer', 'dazzle',
                 'death-prophet',
                 'disruptor', 'doom', 'dragon-knight', 'drow-ranger', 'earthshaker', 'earth-spirit', 'elder-titan',
                 'ember-spirit', 'enchantress', 'enigma', 'faceless-void', 'gyrocopter', 'huskar', 'invoker', 'io',
                 'jakiro',
                 'juggernaut', 'keeper-of-the-light', 'kunkka', 'legion-commander', 'leshrac', 'lich', 'lifestealer',
                 'lina',
                 'lion', 'lone-druid', 'luna', 'lycan', 'magnus', 'medusa', 'meepo', 'mirana', 'morphling',
                 'naga-siren',
                 'natures-prophet', 'necrophos', 'night-stalker', 'nyx-assassin', 'ogre-magi', 'omniknight',
                 'outworld-destroyer', 'phantom-assassin', 'phantom-lancer', 'phoenix', 'puck', 'pudge', 'pugna',
                 'queen-of-pain', 'razor', 'riki', 'rubick', 'sand-king', 'shadow-demon', 'shadow-fiend',
                 'shadow-shaman',
                 'silencer', 'skywrath-mage', 'slardar', 'slark', 'sniper', 'spectre', 'spirit-breaker', 'storm-spirit',
                 'sven',
                 'techies', 'templar-assassin', 'terrorblade', 'tidehunter', 'timbersaw', 'tinker', 'tiny',
                 'treant-protector',
                 'troll-warlord', 'tusk', 'undying', 'vengeful-spirit', 'venomancer', 'visage', 'warlock', 'weaver',
                 'windranger', 'witch-doctor', 'wraith-king', 'zeus', 'arc-warden', 'underlord', 'oracle',
                 'monkey-king']

    def __init__(self):
        self.hero_vs_hero_dict = dict()
        for hero in Analayzer.hero_list:
            self.hero_vs_hero_dict[hero] = dict()

            # parsing
            url = f'https://dotabuff.com/heroes/{hero}/counters'
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
            })
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', {'class': 'sortable'})
            rows = table.find_all('tr')
            for row in rows[1:]:
                columns = row.find_all('td')

                # name cutting
                name = row.find('a', {'class': "link-type-hero"}).renderContents()
                name = str(name)
                name = name[2:]
                name = name[:-1]
                name = name.replace(" ", "-").lower()

                # value cutting
                value = str(columns[2].renderContents())
                value = value[2:]
                value = value[:value.find('%')]

                # filling the dict
                self.hero_vs_hero_dict[hero][name] = float(value)
            print("parsing completed for", hero)
        print("DOTABUFF PARSING COMPLETED, READY")

    def analyze(self, game):
        d_heroes = game.dire_heroes
        r_heroes = game.radiant_heroes
        print('analyzer received', d_heroes, r_heroes)

        # analyze for dire
        dire_answer = []
        for hero in Analayzer.hero_list:
            if hero in d_heroes or hero in r_heroes:
                continue
            value = 0.5
            for r_hero in r_heroes:
                multiplier = self.hero_vs_hero_dict[hero][r_hero]
                value *= (50 - multiplier)/100
                value *= 2
            dire_answer.append((value, hero))
        dire_answer.sort(reverse=True)
        t_dire_answer = 'Лучший выбор для dire:\n'
        for tup in dire_answer[:5]:
            t_dire_answer += '\t' + str(tup[1]) + ' ' + str(tup[0]) + '\n'

        # analyze for radiant
        radiant_answer = []
        for hero in Analayzer.hero_list:
            if hero in d_heroes or hero in r_heroes:
                continue
            value = 0.5
            for d_hero in d_heroes:
                multiplier = self.hero_vs_hero_dict[hero][d_hero]
                value *= (50 - multiplier)/100
                value *= 2
            radiant_answer.append((value, hero))
        radiant_answer.sort(reverse=True)
        t_radiant_answer = 'Лучший выбор для radiant:\n'
        for tup in radiant_answer[:5]:
            t_radiant_answer += '\t' + str(tup[1]) + '\t' + str(tup[0]) + '\n'

        answer = t_dire_answer + '\n' + t_radiant_answer
        return 'Анализ для составов:\n' + game.display() + '\n' + answer
