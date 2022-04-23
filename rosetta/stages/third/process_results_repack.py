import os
import re

from utils.create_file import create_file

def process_results_repack(complex_folder, antibody, antigen, rosetta_path):
    structure_selected=""
    file_results=open(os.path.join(complex_folder, "repack.fasc"), "r").read().splitlines()[2:]
    score=0
    rep_force=20
    for line in file_results:
        results= re.sub(' +', ' ',line).split(" ")
        if float(results[1]) < score and float(results[6]) < rep_force:
            structure_selected=results[-1]
            score=float(results[1])
            rep_force=float(results[6])

    if not structure_selected:
        return False
    else:
        #rosetta_database_direct = f"/home/claudio/tesis/rosetta_src_2021.16.61629_bundle/main/database/"
        rosetta_database_direct = f"{rosetta_path}/database/"

        content = f"-database {rosetta_database_direct}\n-docking						# the docking option group\n	-partners HL_A					# set rigid body docking partners\n	-dock_pert 3 8					# set coarse perturbation parameters (degrees and angstroms)\n	-dock_mcm_trans_magnitude 0.1			# refinement translational perturbation\n	-dock_mcm_rot_magnitude 5.0			# refinement rotational perturbation\n-s {structure_selected}.pdb\n-run:max_retry_job 50					# if the mover fails, retry 50 times\n-use_input_sc						# add the side chains from the input pdb to the rotamer library\n-ex1							# increase rotamer bins to include mean +- 1 standard deviation\n-ex2                                                    # increase rotamer bins to include mean +- 2 standard deviations\n-out:path:all ../results/{antibody}-{antigen}/\n-out							# out option group\n	-file						# out:file option group\n		-scorefile docking2.fasc			# the name of the model score file\n-score:weights talaris2014.wts	# Set talaris2014 as default score function"
        create_file("docking_new.options", content, complex_folder)

        content = f'<ROSETTASCRIPTS>\n	<SCOREFXNS>\n	</SCOREFXNS>\n	<TASKOPERATIONS>\n		<InitializeFromCommandline name="ifcl" />\n		<RestrictToRepacking name="rtr" />\n		Restrict to residues within a distance and vector cutoff of the protein-protein interface\n		<RestrictToInterfaceVector CB_dist_cutoff="10.0" chain1_num="1,2" chain2_num="3" name="rtiv" nearby_atom_cutoff="5.5" vector_angle_cutoff="75" vector_dist_cutoff="9.0" />\n		Fix residues known experimentally to be critical in interaction\n		<PreventResiduesFromRepacking name="prfrp" residues="187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,302,303,304,305,306,307,308,309,310,311,312,313,314" />\n	</TASKOPERATIONS>\n	<FILTERS>\n	</FILTERS>\n	<MOVERS>\n		MINIMIZATION MOVERS\n		Single cycle of FastRelax to minimize backbone of docking partners\n		<FastRelax name="minimize_interface" repeats="1" scorefxn="talaris2014" task_operations="ifcl,rtr,rtiv,prfrp" />\n\n		DOCKING MOVERS\n		<Docking conserve_foldtree="0" design="0" fullatom="0" ignore_default_docking_task="0" jumps="1" local_refine="0" name="dock_low" optimize_fold_tree="1" score_high="talaris2014" score_low="score_docking_low" task_operations="ifcl,prfrp" />\n		<Docking conserve_foldtree="0" design="0" fullatom="1" jumps="1" local_refine="1" name="dock_high" optimize_fold_tree="1" score_high="talaris2014" score_low="score_docking_low" task_operations="ifcl,prfrp" />\n\n		<SaveAndRetrieveSidechains allsc="0" name="srsc" /> Speeds the move from centroid to full atom mode\n\n	</MOVERS>\n	<APPLY_TO_POSE>\n	</APPLY_TO_POSE>\n	<PROTOCOLS>\n		Run docking protocol\n		<Add mover="dock_low" />\n		<Add mover="srsc" />\n		<Add mover="dock_high" />\n\n		Minimize interface\n		<Add mover="minimize_interface" />\n	</PROTOCOLS>\n	<OUTPUT scorefxn="talaris2014" />\n</ROSETTASCRIPTS>'
        create_file("docking_full3.xml", content, complex_folder)

        return os.path.join(complex_folder, structure_selected)