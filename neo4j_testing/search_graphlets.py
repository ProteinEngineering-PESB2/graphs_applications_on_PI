import multiprocessing
import time
import csv
import pandas as pd
import argparse
import neo4j
from neo4j import GraphDatabase
from csv import reader
import json
import numpy as np
from pprint import pprint
import multiprocessing
import json
#from multiprocessing.pool import ThreadPool
from functools import partial
#uri = "bolt://45.236.130.68:7478"
#driver = GraphDatabase.driver(uri, auth=("neo4j", "123qwe"))
#uriEntrada = "bolt://45.236.130.68:7689" # http://45.236.130.68:7476
#uriReferencia = "bolt://45.236.130.68:7688" # http://45.236.130.68:7475
#uriEntrada = "bolt://localhost:7689" # http://45.236.130.68:7476
#uriReferencia = "bolt://localhost:7688" # http://45.236.130.68:7475

uriReferencia = "bolt://localhost:7689" # http://45.236.130.68:7476
uriEntrada = "bolt://localhost:7688" # http://45.236.130.68:7475


def insertarGenesNeo4j(tx,genes):
    nodes = {}
    nodes['Genes'] = list({"gen" : c} for c in genes)
    node = "UNWIND $json as data CREATE (n:Gen) SET n = data Return n"
    result = tx.run(node, json=nodes['Genes'])
    #print(result.single())

def generarClavesNeo4j(genes,session):
    session.write_transaction(insertarGenesNeo4j,genes)

def generarRelacionesGenes(archivoReferencia,uri):
    #session.write_transaction(insertarRelacionesNeo4j,archivoReferencia)
    insertarRelacionesNeo4j(archivoReferencia,uri)

def insertarRelacionesNeo4j(archivoReferencia,uri):
    print(uri)
    with open(archivoReferencia, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj, delimiter='\t')
        i = 0
        # Iterate over each row in the csv using reader object
        for relacion in csv_reader:
            i = i + 1
            # row variable is a list that represents a row in csv
            driver = GraphDatabase.driver(uri, auth=("neo4j", "changeme"))
            tx = driver.session(default_access_mode=neo4j.WRITE_ACCESS)
            query = "MATCH (a:Gen), (b:Gen) WHERE a.gen = $gen1 AND b.gen = $gen2 CREATE (a)-[r:TranscripcionRegulacional {interaccion: True, value:$valor}]->(b)  RETURN a,b"
            result = tx.run(query, gen1=relacion[0], gen2=relacion[1], valor=relacion[2])
            tx.close()
            driver.close()
            #print("data")
            #print(result.single())

def subqueryExclude(tx,gen):
    #print("P: "+multiprocessing.current_process().name+" // Buscando G1: "+gen)
    query = " MATCH p = (n1)-[r1]-(n2)-[r2]-(n3)-[r3]-(n1) "
    query += " where n2.gen=$gen1 "
    query += " with  collect( distinct(n1))+collect(distinct(n2))+collect(distinct(n3)) as dataCompleta "
    query += " unwind dataCompleta as data "
    query += "  match (data)"
    query += " where data.gen <> $gen2"
    query += " return distinct(data.gen) as genes"
    result = tx.run(query, gen1=gen,gen2=gen)
    genes = []
    for line in result:
        genes.append(line["genes"])
    return genes

def graphletOne(tx,gen,threshold,genes):
    g1 = {gen:[]}

    ##print(genes)

    # Encontrar los genes queery1
    query = " MATCH (n4)<-[r5]-(n6)-[r7]->(n8) "
    query += " WHERE NOT n4.gen IN $genesDescartados"
    query += " and NOT n6.gen IN $genesDescartados"
    query += " and NOT n8.gen IN $genesDescartados"
    query += " and n6.gen = $gen1 "
    query += " and toFloat(r5.value) >=  $threshold and  toFloat(r7.value) >= $threshold"
    query += " return n4,n6,n8,r5,r7"
    result = tx.run(query, genesDescartados=genes,gen1=gen,threshold=threshold)
    for line in result:
        ##print (line["n4"].get('gen')+"/"+line["n6"].get('gen')+"/"+line["n8"].get('gen'))
        g1[gen].append([line["n4"].get('gen'),line["n6"].get('gen'),line["n8"].get('gen')])
    ##print(g1)
    return g1
    #return g1[gen].append(result)

def graphletTwo(tx,gen,threshold,genes):
    g1 = {gen:[]}

    # Encontrar los genes queery1
    query = " MATCH (n4)<-[r5]-(n6)<-[r7]-(n8) "
    query += " WHERE NOT n4.gen IN $genesDescartados"
    query += " and NOT n6.gen IN $genesDescartados"
    query += " and NOT n8.gen IN $genesDescartados"
    query += " and n6.gen = $gen1 "
    query += " and toFloat(r5.value) >=  $threshold and  toFloat(r7.value) >= $threshold"
    query += " return n4,n6,n8,r5,r7"
    result = tx.run(query, genesDescartados=genes,gen1=gen,threshold=threshold)

    for line in result:
        ##print (line["n4"].get('gen')+"/"+line["n6"].get('gen')+"/"+line["n8"].get('gen'))
        g1[gen].append([line["n4"].get('gen'),line["n6"].get('gen'),line["n8"].get('gen')])
    ##print(g1)
    return g1
    #return g1[gen].append(result)

def graphletThree(tx,gen,threshold,genes):
    g1 = {gen:[]}

    # Encontrar los genes queery1
    query = " MATCH (n4)-[r5]-(n6)-[r7]->(n8) "
    query += " WHERE NOT n4.gen IN $genesDescartados"
    query += " and NOT n6.gen IN $genesDescartados"
    query += " and NOT n8.gen IN $genesDescartados"
    query += " and n6.gen = $gen1 "
    query += " and toFloat(r5.value) >=  $threshold and  toFloat(r7.value) >= $threshold"
    query += " return n4,n6,n8,r5,r7"
    result = tx.run(query, genesDescartados=genes,gen1=gen,threshold=threshold)
    for line in result:
        ##print (line["n4"].get('gen')+"/"+line["n6"].get('gen')+"/"+line["n8"].get('gen'))
        g1[gen].append([line["n4"].get('gen'),line["n6"].get('gen'),line["n8"].get('gen')])
    ##print(g1)
    return g1
    #return g1[gen].append(result)

def graphletFour(tx,gen,threshold,genes):
    g1 = {gen:[]}

    # Encontrar los genes queery1
    query = " MATCH (n4)-[r5]->(n6)<-[r7]-(n8) "
    query += " WHERE NOT n4.gen IN $genesDescartados"
    query += " and NOT n6.gen IN $genesDescartados"
    query += " and NOT n8.gen IN $genesDescartados"
    query += " and n6.gen = $gen1 "
    query += " and toFloat(r5.value) >=  $threshold and  toFloat(r7.value) >= $threshold"
    query += " return n4,n6,n8,r5,r7"
    result = tx.run(query, genesDescartados=genes,gen1=gen,threshold=threshold)

    for line in result:
        ##print (line["n4"].get('gen')+"/"+line["n6"].get('gen')+"/"+line["n8"].get('gen'))
        g1[gen].append([line["n4"].get('gen'),line["n6"].get('gen'),line["n8"].get('gen')])
    ##print(g1)
    return g1
    #return g1[gen].append(result)

def graphletFive(tx,gen,threshold):
    g1 = {gen:[]}
    #print("P: "+multiprocessing.current_process().name+" // Buscando G5: "+gen)

    # Encontrar los genes queery1
    query = "MATCH (n4)<-[r5]-(n6)-[r7]->(n8)-[r9]->(n4) "
    query += " where n6.gen = $gen1 "
    query += " and toFloat(r5.value) >=  $threshold and  toFloat(r7.value) >= $threshold and  toFloat(r9.value) >= $threshold"
    query += " return n4,n6,n8,r5,r7,r9"
    result = tx.run(query, gen1=gen, threshold=threshold)

    for line in result:
        ##print (line["n4"].get('gen')+"/"+line["n6"].get('gen')+"/"+line["n8"].get('gen'))
        g1[gen].append([line["n4"].get('gen'),line["n6"].get('gen'),line["n8"].get('gen')])
    ##print(g1)
    return g1
    #return g1[gen].append(result)

def graphletSix(tx,gen,threshold):
    g1 = {gen:[]}
    #print("P: "+multiprocessing.current_process().name+" // Buscando G6: "+gen)

    # Encontrar los genes queery1
    query = "MATCH  (n4)-[r5]-(n6)-[r7]->(n8)<-[r9]-(n4) "
    query += " where n6.gen = $gen1 "
    query += " and toFloat(r5.value) >=  $threshold and  toFloat(r7.value) >= $threshold and  toFloat(r9.value) >= $threshold"
    query += " return n4,n6,n8,r5,r7,r9"
    result = tx.run(query, gen1=gen, threshold=threshold)

    for line in result:
        ##print (line["n4"].get('gen')+"/"+line["n6"].get('gen')+"/"+line["n8"].get('gen'))
        g1[gen].append([line["n4"].get('gen'),line["n6"].get('gen'),line["n8"].get('gen')])
    ##print(g1)
    return g1
    #return g1[gen].append(result)

def graphletSeven(tx,gen,threshold, genes):
    g1 = {gen:[]}

    # Encontrar los genes queery1
    query = " MATCH (n4)-[r5]-(n6)<-[r7]-(n8) "
    query += " WHERE NOT n4.gen IN $genesDescartados"
    query += " and NOT n6.gen IN $genesDescartados"
    query += " and NOT n8.gen IN $genesDescartados"
    query += " and n6.gen = $gen1 "
    query += " and toFloat(r5.value) >=  $threshold and  toFloat(r7.value) >= $threshold"
    query += " return n4,n6,n8,r5,r7"
    result = tx.run(query, genesDescartados=genes,gen1=gen,threshold=threshold)

    for line in result:
        ##print (line["n4"].get('gen')+"/"+line["n6"].get('gen')+"/"+line["n8"].get('gen'))
        g1[gen].append([line["n4"].get('gen'),line["n6"].get('gen'),line["n8"].get('gen')])
    ##print(g1)
    return g1
    #return g1[gen].append(result)

def graphletEigth(tx,gen,threshold, genes):
    g1 = {gen:[]}

    # Encontrar los genes queery1
    query = " MATCH (n4)-[r5]-(n6)-[r7]-(n8) "
    query += " WHERE NOT n4.gen IN $genesDescartados"
    query += " and NOT n6.gen IN $genesDescartados"
    query += " and NOT n8.gen IN $genesDescartados"
    query += " and n6.gen = $gen1 "
    query += " and toFloat(r5.value) >=  $threshold and  toFloat(r7.value) >= $threshold"
    query += " return n4,n6,n8,r5,r7"
    result = tx.run(query, genesDescartados=genes,gen1=gen,threshold=threshold)

    for line in result:
        ##print (line["n4"].get('gen')+"/"+line["n6"].get('gen')+"/"+line["n8"].get('gen'))
        g1[gen].append([line["n4"].get('gen'),line["n6"].get('gen'),line["n8"].get('gen')])
    ##print(g1)
    return g1
    #return g1[gen].append(result)

def graphletNine(tx,gen,threshold):
    g1 = {gen:[]}
    #print("P: "+multiprocessing.current_process().name+" // Buscando G9: "+gen)

    # Encontrar los genes queery1
    query = "MATCH  (n4)-[r5]->(n6)-[r7]->(n8)-[r9]->(n4) "
    query += " where n6.gen = $gen1 "
    query += " and toFloat(r5.value) >=  $threshold and  toFloat(r7.value) >= $threshold and  toFloat(r9.value) >= $threshold"
    query += " return n4,n6,n8,r5,r7,r9"
    result = tx.run(query, gen1=gen, threshold=threshold)

    for line in result:
        ##print (line["n4"].get('gen')+"/"+line["n6"].get('gen')+"/"+line["n8"].get('gen'))
        g1[gen].append([line["n4"].get('gen'),line["n6"].get('gen'),line["n8"].get('gen')])
    ##print(g1)
    return g1
    #return g1[gen].append(result)

def graphletTen(tx,gen,threshold):
    g1 = {gen:[]}
    #print("P: "+multiprocessing.current_process().name+" // Buscando G10: "+gen)

    # Encontrar los genes queery1
    query = "MATCH  (n4)-[r5]-(n6)-[r7]->(n8)-[r9]->(n4) "
    query += " where n6.gen = $gen1 "
    query += " and toFloat(r5.value) >=  $threshold and  toFloat(r7.value) >= $threshold and  toFloat(r9.value) >= $threshold"
    query += " return n4,n6,n8,r5,r7,r9"
    result = tx.run(query, gen1=gen, threshold=threshold)

    for line in result:
        ##print (line["n4"].get('gen')+"/"+line["n6"].get('gen')+"/"+line["n8"].get('gen'))
        g1[gen].append([line["n4"].get('gen'),line["n6"].get('gen'),line["n8"].get('gen')])
    ##print(g1)
    return g1
    #return g1[gen].append(result)

def graphletEleven(tx,gen,threshold):
    g1 = {gen:[]}
    #print("P: "+multiprocessing.current_process().name+" // Buscando G11: "+gen)

    # Encontrar los genes queery1
    query = "MATCH  (n4)<-[r5]-(n6)-[r7]->(n8)-[r9]-(n4) "
    query += " where n6.gen = $gen1 "
    query += " and toFloat(r5.value) >=  $threshold and  toFloat(r7.value) >= $threshold and  toFloat(r9.value) >= $threshold"
    query += " return n4,n6,n8,r5,r7,r9"
    result = tx.run(query, gen1=gen, threshold=threshold)

    for line in result:
        ##print (line["n4"].get('gen')+"/"+line["n6"].get('gen')+"/"+line["n8"].get('gen'))
        g1[gen].append([line["n4"].get('gen'),line["n6"].get('gen'),line["n8"].get('gen')])
    ##print(g1)
    return g1
    #return g1[gen].append(result)

def graphletTwelve(tx,gen,threshold):
    g1 = {gen:[]}
    #print("P: "+multiprocessing.current_process().name+" // Buscando G12: "+gen)

    # Encontrar los genes queery1
    query = "MATCH  (n4)-[r5]-(n6)-[r7]-(n8)-[r9]->(n4) "
    query += " where n6.gen = $gen1 "
    query += " and toFloat(r5.value) >=  $threshold and  toFloat(r7.value) >= $threshold and  toFloat(r9.value) >= $threshold"
    query += " return n4,n6,n8,r5,r7,r9"
    result = tx.run(query, gen1=gen, threshold=threshold)

    for line in result:
        ##print (line["n4"].get('gen')+"/"+line["n6"].get('gen')+"/"+line["n8"].get('gen'))
        g1[gen].append([line["n4"].get('gen'),line["n6"].get('gen'),line["n8"].get('gen')])
    ##print(g1)
    return g1
    #return g1[gen].append(result)


def graphletThirteen(tx,gen,threshold):
    g1 = {gen:[]}
    #print("P: "+multiprocessing.current_process().name+" // Buscando G13: "+gen)

    # Encontrar los genes queery1
    query = "MATCH  (n4)-[r5]-(n6)-[r7]-(n8)-[r9]-(n4) "
    query += " where n6.gen = $gen1 "
    query += " and toFloat(r5.value) >=  $threshold and  toFloat(r7.value) >= $threshold and  toFloat(r9.value) >= $threshold"
    query += " return n4,n6,n8,r5,r7,r9"
    result = tx.run(query, gen1=gen, threshold=threshold)

    for line in result:
        ##print (line["n4"].get('gen')+"/"+line["n6"].get('gen')+"/"+line["n8"].get('gen'))
        g1[gen].append([line["n4"].get('gen'),line["n6"].get('gen'),line["n8"].get('gen')])
    ##print(g1)
    return g1
    #return g1[gen].append(result)

def searchGraphletReferencia(listadeGenes, threshold,q):
    print("P: "+multiprocessing.current_process().name)
    #print(uriReferencia)
    driverReferencia = GraphDatabase.driver(uriReferencia, auth=("neo4j", "changeme"))
    session = driverReferencia.session()
    graphletForGen = {}
    #dividir en hilos y recuperar en un array todo
    for gen in listadeGenes:
        print("buscando: "+gen)
        lista = subqueryExclude(session,gen)
        g1 = graphletOne(session,gen,threshold,lista)
        g2 = graphletTwo(session,gen,threshold,lista)
        g3 = graphletThree(session,gen,threshold,lista)
        g4 = graphletFour(session,gen,threshold,lista)
        g7 = graphletSeven(session,gen,threshold,lista)
        g8 = graphletEigth(session,gen,threshold,lista)
        g5 = graphletFive(session,gen,threshold)
        g6 = graphletSix(session,gen,threshold)
        g9 = graphletNine(session,gen,threshold)
        g10 = graphletTen(session,gen,threshold)
        g11 = graphletEleven(session,gen,threshold)
        g12 = graphletTwelve(session,gen,threshold)
        g13 = graphletThirteen(session,gen,threshold)
        #graphletForGen[gen]= {'g1':g1}
        graphletForGen[gen]={'g1':g1,'g2':g2,'g3':g3,'g4':g4,'g5':g5,'g6':g6,'g7':g7,'g8':g8,'g9':g9,'g10':g10,'g11':g11,'g12':g12,'g13':g13}
        nameFile = 'json/'+gen+'.json'
        with open(nameFile, 'w') as fp:
            json.dump(graphletForGen[gen], fp,  indent=4)
        graphletForGen = {}
    print("Procesados"+str(len(listadeGenes)))
    #q.put(graphletForGen)
    session.close()
    driverReferencia.close()
    return graphletForGen
    #return graphletForGen

def searchGraphletEntrada(listadeGenes, threshold,q):
    print("P: "+multiprocessing.current_process().name)
    #print(uriEntrada)
    driverEntrada = GraphDatabase.driver(uriEntrada, auth=("neo4j", "changeme"))
    session = driverEntrada.session()
    graphletForGen = {}
    #dividir en hilos y recuperar en un array todo
    for gen in listadeGenes:
        print("buscando: "+gen)
        lista = subqueryExclude(session,gen)
        g1 = graphletOne(session,gen,threshold,lista)
        g2 = graphletTwo(session,gen,threshold,lista)
        g3 = graphletThree(session,gen,threshold,lista)
        g4 = graphletFour(session,gen,threshold,lista)
        g7 = graphletSeven(session,gen,threshold,lista)
        g8 = graphletEigth(session,gen,threshold,lista)
        g5 = graphletFive(session,gen,threshold)
        g6 = graphletSix(session,gen,threshold)
        g9 = graphletNine(session,gen,threshold)
        g10 = graphletTen(session,gen,threshold)
        g11 = graphletEleven(session,gen,threshold)
        g12 = graphletTwelve(session,gen,threshold)
        g13 = graphletThirteen(session,gen,threshold)
        #graphletForGen[gen]= {'g1':g1}
        graphletForGen[gen]={'g1':g1,'g2':g2,'g3':g3,'g4':g4,'g5':g5,'g6':g6,'g7':g7,'g8':g8,'g9':g9,'g10':g10,'g11':g11,'g12':g12,'g13':g13}
        nameFile = 'json/'+gen+'.json'
        with open(nameFile, 'w') as fp:
            json.dump(graphletForGen[gen], fp,  indent=4)
        graphletForGen = {}
    print("Procesados"+str(len(listadeGenes)))
    ##print(graphletForGen)
    #q.put(graphletForGen)
    session.close()
    driverEntrada.close()
    return graphletForGen
    #return graphletForGen

def start_process():
    print('Starting', multiprocessing.current_process().name)

def threadingSearchGraphletReferencia(listadeGenes, threshold):
    manager = multiprocessing.Manager()
    q = manager.dict()
    numberOfThreads = 10
    jobs = []
    listadeGenesSplit = np.array_split(listadeGenes, numberOfThreads)

    p = ''

    for i in (range(numberOfThreads)):
        p = multiprocessing.Process(target=searchGraphletReferencia, args=(listadeGenesSplit[i], threshold,q))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()
    print("finish join referencia")
    print (len(q))
    return q

def threadingSearchGraphletEntrada(listadeGenes, threshold):
    manager = multiprocessing.Manager()
    q = manager.dict()
    numberOfThreads = 10
    jobs = []
    listadeGenesSplit = np.array_split(listadeGenes, numberOfThreads)

    p = ''

    for i in (range(numberOfThreads)):
        p = multiprocessing.Process(target=searchGraphletEntrada, args=(listadeGenesSplit[i], threshold,q))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()
    print("finish join entrada")
    print (len(q))
    return q

def sessionGraphlet(listadeGenes,q):
    with driver.session() as session:
        session.read_transaction(searchGraphlet, listadeGenes)
    driver.close()


def obtenerGenes(archivoReferencia):
    columnas=pd.read_csv(archivoReferencia,sep='\t',header=None)
    relaciones = columnas
    columnasDatosUnicos = columnas.apply(set)
    listaGenesUnicos = (columnasDatosUnicos[0]).union((columnasDatosUnicos[1]))
    return list(listaGenesUnicos), relaciones

def limpiarBdReferencia(tx):
    query = "MATCH (n) DETACH DELETE n"
    result = tx.run(query)

def limpiarBdEntrada(tx):
    query = "MATCH (n) DETACH DELETE n"
    result = tx.run(query)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Doloto')
    parser.add_argument('-g', type=str, nargs='?',  dest='archivoReferencia', required=True,
                help="""Ingresar ruta completa del archivo de referencia a utilizar""")
    parser.add_argument('-i', type=str, nargs='?',  dest='archivoEntrada', required=False,
                help="""Ingresar ruta completa del archivo de entrada a utilizar""")
    parser.add_argument('-t', nargs='?', type=float, default=0.0, const=0.0,  dest='threshold', required=False,
                help="""ingresar threshold a utilizar""")
    parser.add_argument('-c',nargs='?', type=str, dest='caso', required=False, const="",help="""Ingresar tipo de caso
     case 1 (ref and input contain all TP and TN, only those interactions in ref are considered)
     case 2 (ref and input contain only all TP, negatives are assumed to happen among all nodes without a true between them, default)
    """)
    parser.add_argument('-f', nargs='?', type=int, dest='carpetaSalida', required=False,
                help="""ingresar threshold a utilizar""")
    parser.add_argument('-o', nargs='?', type=int, dest='archivoSalida', required=False,
                help="""ingresar archivo de salida""")
    args = parser.parse_args()
    archivoReferencia = args.archivoReferencia
    archivoEntrada = args.archivoEntrada
    threshold = args.threshold
    caso = args.caso
    carpetaSalida = args.carpetaSalida
    archivoSalida = args.archivoSalida

    start_time = time.time()
    genesReferencia, relacionesReferencia = obtenerGenes(archivoReferencia)
    print("Obtener genes Referencia --- %s seconds ---" % (time.time() - start_time))
    driverReferencia = GraphDatabase.driver(uriReferencia, auth=("neo4j", "changeme"))
    sessionReferencia = driverReferencia.session()
    limpiarBdReferencia(sessionReferencia)
    start_time = time.time()
    generarClavesNeo4j(genesReferencia,sessionReferencia)
    print("Generar claves Referencia --- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    generarRelacionesGenes(archivoReferencia,uriReferencia)
    print("Generar relaciones Referencia --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    genesEntrada, relacionesEntrada = obtenerGenes(archivoEntrada)
    print("Obtener genes entrada --- %s seconds ---" % (time.time() - start_time))
    driverEntrada = GraphDatabase.driver(uriEntrada, auth=("neo4j", "changeme"))
    sessionEntrada = driverEntrada.session()
    limpiarBdEntrada(sessionEntrada)
    start_time = time.time()
    print("Generar claves entrada --- %s seconds ---" % (time.time() - start_time))
    generarClavesNeo4j(genesEntrada,sessionEntrada)
    start_time = time.time()
    generarRelacionesGenes(archivoEntrada,uriEntrada)
    print("Generar relaciones entrada --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    #print(*genesEntrada, sep = "\n")
    threadingSearchGraphletReferencia(genesReferencia,threshold)
    driverReferencia.close()
    print("Referencia --- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    threadingSearchGraphletEntrada(genesEntrada, threshold)
    print("Entrada --- %s seconds ---" % (time.time() - start_time))
    driverEntrada.close()