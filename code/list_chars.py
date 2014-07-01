#!/usr/bin/env python

from __future__ import print_function

from py2neo.neo4j import *


graph = GraphDatabaseService()
for char in graph.find("Character"):
    print(char["name"])

