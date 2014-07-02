#!/usr/bin/env python3


import json
import sys

from httpstream import get
from bs4 import BeautifulSoup

from quickgeoff import *


base = "http://24.wikia.com"
title = """\
/*****************
 *   ===, ,   ,  *
 *      | |   |  *
 *  ,===' '===|  *
 *  |         |  *
 *  '===      '  *
 *               *
 *    SEASON {}   *
 *               *
 *****************/
"""

# TODO change to href
def get_actor(name):
    return Node(name, "Actor", "name", {"name": name}), PathList()


def get_char(href):
    src = get("{}{}".format(base, href)).content
    soup = BeautifulSoup(src)

    name = soup.select("#WikiaPageHeader")[0].h1.text
    node = Node(name, "Character", "name", {"name": name})
    paths = PathList()
    sys.stderr.write(name + "\n")

    try:
        sidebar = soup.select(".sidebar")[0]
    except IndexError:
        # No sidebar - probably not a named character
        raise ValueError(name)
    else:
        
        def get_sidebar_value(adjacent_text, default=None):
            try:
                return sidebar.find_all(lambda tag: tag.name == "td" and adjacent_text in tag.text)[0].next_sibling.text.strip()
            except IndexError:
                return default
        
        node.properties["name"] = get_sidebar_value("Name", name)
        if node.properties["name"].endswith(")"):
            node.properties["name"] = node.properties["name"].rpartition("(")[0].strip()
        
        nationality = get_sidebar_value("Nationality")
        if nationality is not None:
            node.properties["nationality"] = nationality

    node.properties["alive"] = not ("Deceased characters" in soup.text)
    if "Killed by Jack Bauer" in soup.text:
        paths.append(Path("jack_bauer", "KILLED!", name))
    if "Killed by Tony Almeida" in soup.text:
        paths.append(Path("tony_almeida", "KILLED!", name))
    if "Killed by Chase Edmunds" in soup.text:
        paths.append(Path("chase_edmunds", "KILLED!", name))
    if "Killed by Curtis Manning" in soup.text:
        paths.append(Path("curtis_manning", "KILLED!", name))
    if "Killed by Mandy" in soup.text:
        paths.append(Path("mandy", "KILLED!", name))
    if "Killed by Nina Myers" in soup.text:
        paths.append(Path("nina_myers", "KILLED!", name))
    if "Killed by Renee Walker" in soup.text:
        paths.append(Path("renee_walker", "KILLED!", name))

    return node, paths


def iter_cast(season_node):
    season_number = season_node.properties["number"]
    src = get("{}/wiki/Season_{}".format(base, season_number)).content
    soup = BeautifulSoup(src)
    cast_heading = soup.select("#Cast")[0].parent
    cast_lists = cast_heading.find_next_siblings("ul")
    for cast_list in cast_lists:
        for cast_item in cast_list.children:
            terms = list(cast_item.children)
            found_as = False
            for term in cast_item.children:
                if isinstance(term, str) and term.startswith(" as "):
                    found_as = True
                    break
            if not found_as:
                continue
            links = cast_item.select("a")
            
            try:
                actor_a = links[0]
                actor_node, actor_paths = get_actor(actor_a.text)
                char_a = links[-1]
                char_node, char_paths = get_char(char_a["href"])
            except ValueError:
                pass
            else:
                paths = PathList()

                trailing_words = terms[-1].strip().strip("()").split(",")
                first_bits = [x.partition("episode")[0].strip() for x in trailing_words if "episode" in x]
                episodes = int(first_bits[0])
                paths.append(Path(actor_node.name, "STARRED_AS!", char_node.name, ("APPEARED_IN!", {"episodes": episodes}), season_node.name))

                paths.extend(actor_paths)
                paths.extend(char_paths)

                yield actor_node, char_node, paths
            

def get_season(season):
    season_name = "Season {}".format(season)
    file_name = "24_{}.geoff".format(season)

    season_node = Node(season_name, "Season", "number", {"number": season, "name": season_name})
    print(title.format(season))
    print(repr(season_node))
    print()

    actors = {}
    chars = {}
    char_paths = {}
    
    print("/* Actors */")
    for actor_node, char_node, paths in iter_cast(season_node):
        if actor_node.name in actors:
            for char_path in char_paths[char_node.name]:
                if len(char_path) == 2:
                    for path in paths:
                        if len(path) == 2:
                            char_path.parts[3][1]["episodes"] += path.parts[3][1]["episodes"]
        else:
            actors[actor_node.name] = actor_node
            chars[char_node.name] = char_node
            char_paths[char_node.name] = paths
            print(repr(actor_node))

    print()
    print("/* Characters */")
    for char_name, char_node in sorted(chars.items()):
        print(repr(char_node))
    print()
    print("/* Relationships */")
    for name, path_list in char_paths.items():
        print(repr(path_list))
    print()


if __name__ == "__main__":
    season = int(sys.argv[1])
    get_season(season)

