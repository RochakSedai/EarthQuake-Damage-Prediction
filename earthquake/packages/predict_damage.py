# library 
import csv
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import matplotlib.ticker as mtick
import pickle
import time
from copy import deepcopy
# from . import csv_building_structure


# function to predict damage
def predict_damage(input_data):
    """
    input_data : This is the dictionary obtained from frontend 
    e.g.:
    input_data = {
    'count_floors_pre_eq' : 4,
    'count_floors_post_eq' : 0,
    'age_building' : 42,
    'plinth_area_sq_ft' : 420,
    'height_ft_pre_eq' : 28,
    'height_ft_post_eq' : 0,  
    'land_surface_condition' : 'Flat',
    'position' : 'Attached-1 side',
    'has_superstructure' : 'adobe_mud',
    'condition_post_eq' : 'Damage-Rubble Clear-New building built',
    'technical_solution_proposed' : 'Reconstruction',
    'foundation_type' : 'Mud mortar-Stone/Brick',
    'roof_type' : 'Bamboo/Timber-Light roof',
    'ground_floor_type' : 'Mud',
    'other_floor_type' : 'Timber/Bamboo-Mud',
    'plan_configuration' : 'Rectangular'    
    }
    """
    # print(input_data)
    input_data = deepcopy(input_data)
    # print(input_data)

    df = pd.read_csv("earthquake\packages\csv_building_structure.csv")
    
    df.dropna(inplace=True)

    df_web = pd.Series(input_data)
    cat_nominal=["foundation_type","roof_type","ground_floor_type","other_floor_type","plan_configuration"]
    nominal_categories = {}
    for nom in cat_nominal:
        nominal_categories[f'{nom}s']=list(df[nom].unique())
    # Label Encoded cols
    land_surface_conditions = ['Flat','Moderate slope','Steep slope']
    positions = ['Attached-1 side','Attached-2 side','Attached-3 side','Not attached']
    damage_grades = ['Grade 1','Grade 2', 'Grade 3', 'Grade 4', 'Grade 5']
    technical_solutions_proposed = ['Major repair','Minor repair','No need','Reconstruction']
    conditions_post_eq = ['Covered by landslide','Damaged-Not used','Damaged-Repaired and used','Damaged-Rubble Clear-New building built','Damaged-Rubble clear','Damaged-Rubble unclear','Damaged-Used in risk','Not damaged']

    # Load pickle model
    forest_best = pickle.load(open('earthquake\packages\model_tuned.pkl','rb'))
    
    # label encoding for web variable
    df_web['land_surface_condition'] = land_surface_conditions.index(df_web['land_surface_condition'])
    df_web['position'] = positions.index(df_web['position'])
    df_web['condition_post_eq'] = conditions_post_eq.index(df_web['condition_post_eq'])
    df_web['technical_solution_proposed'] = technical_solutions_proposed.index(df_web['technical_solution_proposed'])

    # One hot encoding for web variable 
    # has_superstructure, foundation_type, roof_type, ground_floor_type, other_floor_type, plan_configuration
    # * superstructure
    superstructures = ['adobe_mud','mud_mortar_stone','stone_flag','cement_mortar_stone','mud_mortar_brick','cement_mortar_brick','timber','bamboo','rc_non_engineered','rc_engineered','other']
    for superstructure in superstructures:
        df_web[f'has_superstructure_{superstructure}'] = 1 if input_data['has_superstructure'] == superstructure else 0

    # * foundation_type
    for foundation_type in nominal_categories['foundation_types']:
        df_web[f'foundation_type_{foundation_type}'] = 1 if input_data['foundation_type'] == foundation_type else 0

    # * roof_type
    for roof_type in nominal_categories['roof_types']:
        df_web[f'roof_type_{roof_type}'] = 1 if input_data['roof_type'] == roof_type else 0

    # * ground_floor_type
    for ground_floor_type in nominal_categories['ground_floor_types']:
        df_web[f'ground_floor_type_{ground_floor_type}'] = 1 if input_data['ground_floor_type'] == ground_floor_type else 0

    # * other_floor_type 
    for other_floor_type in nominal_categories['other_floor_types']:
        df_web[f'other_floor_type_{other_floor_type}'] = 1 if input_data['other_floor_type'] == other_floor_type else 0

    # * plan_configuration
    for plan_configuration in nominal_categories['plan_configurations']:
        df_web[f'plan_configuration_{plan_configuration}'] = 1 if input_data['plan_configuration'] == plan_configuration else 0
    
    # removing unwanted cols 
    cols_to_remove = ['has_superstructure', 'foundation_type', 'roof_type', 'ground_floor_type', 'other_floor_type', 'plan_configuration']
    df_test_web = df_web.drop(cols_to_remove)

    df_test_web = df_test_web.to_frame().transpose()

    y_pred = forest_best.predict(df_test_web)

    # print(damage_grades[y_pred[0]])

    predicted_output = damage_grades[y_pred[0]]

    return predicted_output

# if __name__ == '__main__':
#     input_data = {
#         'count_floors_pre_eq' : 4,
#         'count_floors_post_eq' : 0,
#         'age_building' : 42,
#         'plinth_area_sq_ft' : 420,
#         'height_ft_pre_eq' : 28,
#         'height_ft_post_eq' : 0,  
#         'land_surface_condition' : 'Flat',
#         'position' : 'Attached-1 side',
#         'has_superstructure' : 'adobe_mud',
#         'condition_post_eq' : 'Damage-Rubble Clear-New building built',
#         'technical_solution_proposed' : 'Reconstruction',
#         'foundation_type' : 'Mud mortar-Stone/Brick',
#         'roof_type' : 'Bamboo/Timber-Light roof',
#         'ground_floor_type' : 'Mud',
#         'other_floor_type' : 'Timber/Bamboo-Mud',
#         'plan_configuration' : 'Rectangular'    
#         }
#     start_time = time.time()
#     print(predict_damage(input_data))
#     end_time = time.time()
#     time_taken = end_time - start_time
#     print(f'Total Time taken: {time_taken} seconds')