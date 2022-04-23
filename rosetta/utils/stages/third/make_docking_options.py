import os

def make_docking_options(complex_folder, structure_selected):
    docking_options = os.path.join(complex_folder, "docking_new.options")
    docking_file = open(docking_options, "r")
    list_of_lines = docking_file.readlines()
    list_of_lines[6] = "-s "+structure_selected+".pdb"+"\n" 
    list_of_lines[11] = "-out:path:all "+complex_folder+"/\n"
    a_file = open(docking_options, "w")
    a_file.writelines(list_of_lines)
    a_file.close()