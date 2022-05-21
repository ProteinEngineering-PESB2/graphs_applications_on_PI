BEGIN{
}
{
START_NODO[NR] = $1
END_NODO[NR] = $2
VAL_EDGES[NR] = $3 
DATA_CODIGO[NR] = $0
}
END {
    print(":START_ID,val,:END_ID,:TYPE")
    for(i = 1; i <= NR; i++){
        print(START_NODO[i]","VAL_EDGES[i]","END_NODO[i]",EDGE")
    }
}
