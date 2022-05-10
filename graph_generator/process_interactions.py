import json
import pandas as pd
import sys, getopt
import textwrap
import os

def process_interactions(inter_response, path, name):
        '''
        Docstring
        '''
        interaction_data = inter_response['response_service']['detected_interactions']

        # Create dataframe
        df = pd.DataFrame(columns=['Node_1', 'Node_2', 'Weight'])

        for inter in interaction_data:
                res_1 = 'CA_' + inter['member1']['info_residue']['residue'] + (
                        inter['member1']['info_residue']['pos']) + '_' + (
                        inter['member1']['info_residue']['chain'])
                res_2 = 'CA_' + inter['member2']['info_residue']['residue'] + (
                        inter['member2']['info_residue']['pos']) + '_' + (
                        inter['member2']['info_residue']['chain'])
                weight = inter['value_interaction']
                row = pd.DataFrame([[res_1, res_2, weight]], columns=['Node_1', 'Node_2', 'Weight'])
                row_2 = pd.DataFrame([[res_2, res_1, weight]], columns=['Node_1', 'Node_2', 'Weight'])
                df = pd.concat([df, row], ignore_index=True)
                df = pd.concat([df, row_2], ignore_index=True)

        Name =  path + '/' + 'interactions_list_' + name + '.csv'
        df.to_csv(Name , index=False)