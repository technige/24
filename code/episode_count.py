#!/usr/bin/env python

from __future__ import print_function
from py2neo.neo4j import *

graph_db = GraphDatabaseService()

q = """\
MATCH (c:Character)-[a:APPEARED_IN]->(season)
RETURN c.name, sum(a.episodes) AS episodes
ORDER BY episodes DESC
"""

query = CypherQuery(graph_db, q)

for record in query.execute():
    print(record)

