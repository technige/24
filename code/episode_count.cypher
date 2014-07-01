MATCH (c:Character)-[a:APPEARED_IN]->(season)
RETURN c.name, sum(a.episodes) AS episodes
ORDER BY episodes DESC
