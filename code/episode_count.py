from py2neo import neo4j
graph_db = neo4j.GraphDatabaseService()

q = """MATCH (c:Character)-[a:APPEARED_IN]->(season)
       RETURN c.name, sum(a.episodes) AS episodes
       ORDER BY episodes DESC"""

query = neo4j.CypherQuery(graph_db, q)

for record in query.execute().data:
    print record

