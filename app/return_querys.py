
class group_of_querys():

    def querys(type_query):

        if(type_query == 1 ):
            #QUERY_GRAPHLET_1
            return_query = """
                MATCH (m:GEN)-[r1:EDGE]->(n1:GEN)
                MATCH (m:GEN)-[r2:EDGE]->(n2:GEN)
                WHERE n1.id <> m.id AND n2.id <> m.id AND n1.id <> n2.id 
                AND NOT (n2)-[:EDGE]->(m)
                AND NOT (n1)-[:EDGE]->(m)
                AND NOT (n2)-[:EDGE]->(n1)
                AND NOT (n2)<-[:EDGE]-(n1)
                RETURN n1,m,n2,r1,r2
            """
        elif(type_query == 2):
            #QUERY_GRAPHLET_2
            return_query = """
                MATCH (m:GEN)-[r1:EDGE]->(n1:GEN)
                MATCH (m:GEN)<-[r2:EDGE]-(n2:GEN)
                WHERE n1.id <> m.id AND n2.id <> m.id AND n1.id <> n2.id 
                AND NOT (n2)<-[:EDGE]-(m)
                AND NOT (n1)-[:EDGE]->(m)
                AND NOT (n2)-[:EDGE]->(n1)
                AND NOT (n2)<-[:EDGE]-(n1)
                RETURN n1,m,n2,r1,r2
            """
        elif(type_query == 3):
            #QUERY_GRAPHLET_3
            return_query= """
                MATCH (m:GEN)-[r1:EDGE]->(n1:GEN)
                MATCH (m:GEN)<-[r2:EDGE]-(n1:GEN)
                MATCH (m:GEN)-[r3:EDGE]->(n2:GEN)
                WHERE n1.id <> m.id AND n2.id <> m.id AND n1.id <> n2.id 
                AND NOT (m)<-[:EDGE]-(n2)
                AND NOT (n1)-[:EDGE]->(n2)
                AND NOT (n1)<-[:EDGE]-(n2)
                RETURN n1,m,n2
            """
        elif(type_query == 4):
            #QUERY_GRAPHLET_4
            return_query = """
                MATCH (m:GEN)-[r1:EDGE]->(n1:GEN)
                MATCH (n1:GEN)<-[r2:EDGE]-(n2:GEN)
                WHERE n1.id <> m.id AND n2.id <> m.id AND n1.id <> n2.id 
                AND NOT (m)<-[:EDGE]-(n2)
                AND NOT (m)-[:EDGE]->(n2)
                AND NOT (n1)-[:EDGE]->(n2)
                AND NOT (n1)-[:EDGE]->(m)
                RETURN n1,m,n2
            """
        elif(type_query == 5):
            #QUERY_GRAPHLET_5
            return_query= """
                MATCH (m:GEN)-[r1:EDGE]->(n1:GEN)
                MATCH (m:GEN)-[r2:EDGE]->(n2:GEN)
                MATCH (n1:GEN)-[r3:EDGE]->(n2:GEN)
                WHERE n1.id <> m.id AND n2.id <> m.id AND n1.id <> n2.id
                AND NOT (m)<-[:EDGE]-(n1)
                AND NOT (m)<-[:EDGE]-(n2)
                AND NOT (n1)<-[:EDGE]-(n2)
                RETURN n1,m,n2
            """
        elif(type_query == 6):
            #QUERY_GRAPHLET_6
            return_query= """
                MATCH (m:GEN)-[r1:EDGE]->(n1:GEN)
                MATCH (m:GEN)-[r2:EDGE]->(n2:GEN)
                MATCH (m:GEN)<-[r3:EDGE]-(n1:GEN)
                MATCH (n1:GEN)-[r4:EDGE]->(n2:GEN)
                WHERE n1.id <> m.id AND n2.id <> m.id AND n1.id <> n2.id 
                AND NOT (n2)-[:EDGE]->(n1)
                AND NOT (m)<-[:EDGE]-(n2)
                RETURN n1,m,n2,r1,r2,r3,r4
            """
        elif(type_query == 7):
            #QUERY_GRAPHLET_7
            return_query = """
                MATCH (m:GEN)-[r1:EDGE]->(n1:GEN)
                MATCH (m:GEN)<-[r2:EDGE]-(n1:GEN)
                MATCH (m:GEN)<-[r3:EDGE]-(n2:GEN)
                WHERE n1.id <> m.id AND n2.id <> m.id AND n1.id <> n2.id 
                AND NOT (m)-[:EDGE]->(n2)
                AND NOT (n1)<-[:EDGE]-(n2)
                AND NOT (n2)<-[:EDGE]-(n1)
                RETURN n1,m,n2,r1,r2,r3
            """
        elif(type_query == 8):
            #QUERY_GRAPHLET_8
            return_query= """
                MATCH (m:GEN)-[r1:EDGE]->(n1:GEN)
                MATCH (m:GEN)-[r2:EDGE]->(n2:GEN)
                MATCH (m:GEN)<-[r3:EDGE]-(n1:GEN)
                MATCH (m:GEN)<-[r4:EDGE]-(n2:GEN)
                WHERE n1.id <> m.id AND n2.id <> m.id AND n1.id <> n2.id 
                AND NOT (n2)-[:EDGE]->(n1)
                AND NOT (n1)-[:EDGE]->(n2)
                RETURN n1,m,n2,r1,r2,r3,r4
            """
        elif(type_query == 9):

            #QUERY_GRAPHLET_9
            return_query = """
                MATCH (m:GEN)-[r1:EDGE]->(n1:GEN)
                MATCH (m:GEN)<-[r2:EDGE]-(n2:GEN)
                MATCH (n1:GEN)-[r3:EDGE]->(n2:GEN)
                WHERE n1.id <> m.id AND n2.id <> m.id AND n1.id <> n2.id 
                AND NOT (n2)-[:EDGE]->(n1)
                AND NOT (m)-[:EDGE]->(n2)
                AND NOT (n1)-[:EDGE]->(m)
                RETURN n1,m,n2,r1,r2,r3
            """
        elif(type_query == 10):
            #QUERY_GRAPHLET_10
            return_query = """
                MATCH (m:GEN)-[r1:EDGE]->(n1:GEN)
                MATCH (m:GEN)<-[r2:EDGE]-(n1:GEN)
                MATCH (n2:GEN)-[r3:EDGE]->(n1:GEN)
                MATCH (m:GEN)-[r4:EDGE]->(n2:GEN)
                WHERE n1.id <> m.id AND n2.id <> m.id AND n1.id <> n2.id 
                AND NOT (n2)-[:EDGE]->(m)
                AND NOT (n1)-[:EDGE]->(n2)
                RETURN n1,m,n2,r1,r2,r3,r4
            """
        elif(type_query == 11):
            #QUERY_GRAPHLET_11
            return_query = """
                MATCH (m:GEN)-[r1:EDGE]->(n1:GEN)
                MATCH (m:GEN)-[r2:EDGE]->(n2:GEN)
                MATCH (n2:GEN)-[r3:EDGE]->(n1:GEN)
                MATCH (n1:GEN)-[r4:EDGE]->(n2:GEN)
                WHERE n1.id <> m.id AND n2.id <> m.id AND n1.id <> n2.id 
                AND NOT (n2)-[:EDGE]->(m)
                AND NOT (n1)-[:EDGE]->(m)
                RETURN n1,m,n2,r1,r2,r3,r4
            """
        elif(type_query == 12):
            #QUERY_GRAPHLET_12
            return_query = """
                MATCH (m:GEN)-[r1:EDGE]->(n1:GEN)
                MATCH (m:GEN)-[r2:EDGE]->(n2:GEN)
                MATCH (n2:GEN)-[r3:EDGE]->(m:GEN)
                MATCH (n1:GEN)-[r4:EDGE]->(m:GEN)
                MATCH (n2:GEN)-[r5:EDGE]->(n1:GEN)
                WHERE n1.id <> m.id AND n2.id <> m.id AND n1.id <> n2.id 
                AND NOT (n1)-[:EDGE]->(n2)
                RETURN n1,m,n2,r1,r2,r3,r4,r5
            """
        elif(type_query == 13):
            #QUERY_GRAPHLET_13
            return_query = """
                MATCH (m:GEN)-[r1:EDGE]->(n1:GEN)
                MATCH (m:GEN)-[r2:EDGE]->(n2:GEN)
                MATCH (n1:GEN)-[r3:EDGE]->(n2:GEN)
                MATCH (n1:GEN)-[r4:EDGE]->(m:GEN)
                MATCH (n2:GEN)-[r5:EDGE]->(n1:GEN)
                MATCH (n1:GEN)-[r6:EDGE]->(n2:GEN)
                WHERE n1.id <> m.id AND n2.id <> m.id AND n1.id <> n2.id 
                RETURN n1,m,n2,r1,r2,r3,r4,r5,r6
            """

        return return_query