from py2neo import Graph
from neo4j import GraphDatabase
uri = "bolt://192.168.20.100:7687"
user = "neo4j"
password = "test123456"
driver = GraphDatabase.driver(uri, auth=(user, password))
def run_query(query):
    with driver.session() as session:
        result = session.run(query)
        records = []
        for record in result:
            records.append(record)
        return records

def neo4j_query(cid):
    query = (f"MATCH p=(a)-[r:`参股`]->(b:`企业`) where b.cid = '{cid}' RETURN a.cid as cid, a.name as "
             f"name, a.personId as pId, r.amount as amount, r.percent as percent limit 10")
    results = run_query(query)
    driver.close()
    return results


if __name__ == '__main__':
    cid = 'CAICT_COM_100006_A423AEA48EEAF8324DC270A3D207EDEC'
    result = neo4j_query(cid)
    print(result)