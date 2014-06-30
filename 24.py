#!/usr/bin/env python3


import json

from httpstream import get
from bs4 import BeautifulSoup


titles = ["Dr.", "President", "First Lady", "Russian President", "Secretary of Defense"]

def node_name(name):
    return name.replace(" ", "_").replace("'", "_").replace("-", "_").replace(".", "").lower()


def get_cast(season):
    src = get("http://24.wikia.com/wiki/Season_{}".format(season)).content
    soup = BeautifulSoup(src)
    cast_heading = soup.select("#Cast")[0].parent
    cast_lists = cast_heading.find_next_siblings("ul")
    for cast_list in cast_lists:
        for cast_item in cast_list.children:
            terms = list(cast_item.children)
            try:
                as_pos = terms.index(" as ")
            except ValueError:
                pass
            else:
                actor = terms[as_pos - 1].text
                character = terms[-2].text
                trailing_words = terms[-1].strip().strip("()").split(",")
                first_bits = [x.partition("episode")[0].strip() for x in trailing_words if "episode" in x]
                episodes = int(first_bits[0])
                for title in titles:
                    title += " "
                    if character.startswith(title):
                        character = character[len(title):]
                yield actor, character, episodes


def get_season(season):
    file_name = "24_{}.geoff".format(season)

    actors = {}
    characters = {}
    casting_rels = []
    
    for actor, character, episodes in get_cast(season):
        actor_id = node_name(actor)
        character_id = node_name(character)
        actors[actor_id] = {"name": actor}
        characters[character_id] = {"name": character}
        casting_rels.append((actor_id, "STARRED_AS", character_id, "APPEARED_IN", episodes, "season_{}".format(season)))

    with open(file_name, "w") as f:
        f.write("/* Season */\n")
        f.write('(season_%s:Season!number {"number":%s,"name":"Season %s"})\n' % (season, season, season))
        f.write("\n")
        f.write("/* Actors */\n")
        for actor_id, actor in sorted(actors.items()):
            f.write('(%s:Actor!name %s)\n' % (actor_id, json.dumps(actor, separators=",:", ensure_ascii=False)))
        f.write("\n")
        f.write("/* Characters */\n")
        for character_id, character in sorted(characters.items()):
            f.write('(%s:Character!name %s)\n' % (character_id, json.dumps(character, separators=",:", ensure_ascii=False)))
        f.write("\n")
        f.write("/* Casting */\n")
        for rel in casting_rels:
            f.write('(%s)-[:%s!]->(%s)-[:%s! {"episodes":%s}]->(%s)\n' % rel)
        f.write("\n")


if __name__ == "__main__":
    for season in range(1, 10):
        get_season(season)

