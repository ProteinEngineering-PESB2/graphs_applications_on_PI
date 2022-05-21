import logging
import numpy as np
import pandas as pd
import sys
import os
import errno
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from multiprocessing import Pool
from return_querys import group_of_querys

        
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
            graphlet = i['n1']['id']+"_"+i['m']['id']+"_"+i['n2']['id']
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


def export_csv(data, type_graphlet, name_export):


    try:
        os.mkdir("data_output/"+name_export)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    df_export = pd.DataFrame(data, columns=[type_graphlet])
    df_export.to_csv("data_output/"+name_export+"/"+type_graphlet+".csv", index=False)

if __name__ == "__main__":

    name_export = sys.argv[1]
    app = App()

    #export_csv(g1,'g1',name_export)
    querys = []

    for i in range(1,14):
        querys.append(group_of_querys.querys(i))

    for query in querys:
        app.buscador(query)

