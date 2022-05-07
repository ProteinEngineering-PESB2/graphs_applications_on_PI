import logging
import numpy as np
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

        
class App():

    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bass"), encrypted=False) 

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def buscador(self, query):
        with self.driver.session(database="neo4j") as session:
            # Read transactions allow the driver to handle retries and transient errors
            
            result = session.read_transaction(
                self._return_graphlet, query)

        graphlets = []
        for i in result:
            graphlet = i['n1']['nodo']+i['m']['nodo']+i['n2']['nodo']

            #QUITAR X
            graphlet = graphlet.replace("X", "")

            graphlets.append(graphlet)
        
        return(graphlets)
            
    @staticmethod
    def _return_graphlet(tx, query):

        result = tx.run(query)

        try:
            return result.data()
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise


if __name__ == "__main__":

    app = App()


    query = """
        MATCH (n1:PROTEIN)<-[r1:ENLACE]-(m:PROTEIN)-[r2:ENLACE]->(n2:PROTEIN)
        RETURN n1,m,n2,r1,r2 LIMIT 10
    """
    protein1_graphlet1 = app.buscador(query)

    print(protein1_graphlet1)

    query = """
        MATCH (n1:PROTEIN2)<-[r1:ENLACE2]-(m:PROTEIN2)-[r2:ENLACE2]->(n2:PROTEIN2)
        RETURN n1,m,n2,r1,r2 LIMIT 10
    """

    protein2_graphlet1 = app.buscador(query)

    print(protein2_graphlet1)

    #result = np.equal(protein1_graphlet1, protein2_graphlet1, dtype=object)

    #print(result)

    app.close()