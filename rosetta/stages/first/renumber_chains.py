import os

from pymol import cmd


def renumber_chains(row, complex_name):
    try:
        first_line = open(os.path.join(
            row[0], f"{complex_name}.pdb")).readline().split(" ")
        list_numbers = []
        list_nothing = []

        for i in first_line:
            try:
                number = int(i)
                list_numbers.append(number)
            except:
                list_nothing.append(i)

        cmd.load(os.path.join(row[0], f"{complex_name}.pdb"))

        cmd.select("chainA", "chain A")
        cmd.select("chainH", "chain H")
        cmd.select("chainL", "chain L")
        large_chain = len(cmd.get_model("chainA").get_residues())
        heavy_chain = len(cmd.get_model("chainH").get_residues())

        cmd.alter("chainA", "resi=str(int(resi)-" +
                  str(int(list_numbers[-1])-1)+")")
        cmd.alter("chainH", "resi=str(int(resi)+"+str(large_chain)+")")
        cmd.alter("chainL", "resi=str(int(resi)+" +
                  str(large_chain+heavy_chain)+")")
        cmd.sort()
        cmd.select("complex", "all")
        cmd.save(os.path.join(
            row[0], f"{complex_name}_renumbered.pdb"), "complex")
        cmd.reinitialize()

        return True
    except:
        return False
