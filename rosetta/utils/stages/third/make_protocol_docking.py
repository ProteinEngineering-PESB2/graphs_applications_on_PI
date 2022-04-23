import os
import pandas as pd
from Bio import SeqIO
import xml.etree.ElementTree as ET

def make_protocol_docking(complex_folder, structure_selected):
    structure_selected = structure_selected + ".pdb"
    docking_protocol = os.path.join(complex_folder, "docking_full3.xml")
    docking_protocol = docking_protocol.replace("\n", "")
    antibody=structure_selected.split("/")[-1].split("-")[0]

    cdr_prediction_location = os.path.join(os.getcwd(), "antibodies_cdr3.csv")
    cdr_prediction = pd.read_csv(cdr_prediction_location)
    row_loc=cdr_prediction.loc[cdr_prediction["id"] == antibody]
    seq = ""
    for record in SeqIO.parse(structure_selected, "pdb-atom"):
        seq = seq + record.seq
    
    heavy_cdr= seq.find(row_loc["cdr3_heavy"].values[0])+1
    light_cdr=seq.find(row_loc["cdr3_light"].values[0])+1
    list_indexes=[]
    for n in range(len(list(row_loc["cdr3_heavy"].values[0]))):
        list_indexes.append(str(heavy_cdr+n))
    for n in range(len(list(row_loc["cdr3_light"].values[0]))):
        list_indexes.append(str(light_cdr+n))
    mytree = ET.parse(docking_protocol)
    myroot = mytree.getroot()
    indexes_protocol=",".join(list_indexes)
    for neighbor in myroot.iter('PreventResiduesFromRepacking'):
        neighbor.set("residues", indexes_protocol)
    mytree.write(docking_protocol)