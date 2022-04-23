import os

from pymol import cmd

def get_antigen_chain(antigen_pdb, antigen_chain, complex_folder):
    try:
        cmd.load(os.path.join(os.getcwd(), "antigens", antigen_pdb))
        pdb_code = antigen_pdb.replace(".ent", "").replace(".pdb", "")
        cmd.select("chainAntigen", str(pdb_code) + " and chain "+ antigen_chain)
        cmd.alter((f"chain {antigen_chain}"), "chain = 'A'")
        cmd.indicate("hetatm")
        cmd.remove("indicate")
        cmd.save(os.path.join(complex_folder, f"{pdb_code}_{antigen_chain}.pdb"), "chainAntigen", -1, "pdb")

        return True
    except:
        return False