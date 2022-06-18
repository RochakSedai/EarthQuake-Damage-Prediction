import imp
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle

# df = pd.read_csv("earthquake\packages\csv_building_structure.csv")
# def find_house(building_id):
#     '''
#     building_id : Data obtained from the user at frontend which is their building number.

#     '''
#     if df.loc[df['building_id'] == building_id].shape[0] > 0:
#         return df.loc[df['building_id'] == building_id].damage_grade.to_list()[0]

#     else:
#         return'House not Found!!!'

def find_house(building_id):
    '''
    building_id : Data obtained from the user at frontend which is their building number.
 
    '''
    # dataset path
    df = pd.read_csv("earthquake\packages\csv_building_structure.csv")
    # 
    df.dropna(inplace=True)
    if df.loc[df['building_id'] == building_id].shape[0] > 0:
        # return df.loc[df['building_id'] == building_id].damage_grade.to_list()[0]
        # columns with numeric values | no need to encode
        numeric = ['building_id','district_id','vdcmun_id','ward_id','count_floors_pre_eq','count_floors_post_eq','age_building','plinth_area_sq_ft','height_ft_pre_eq','height_ft_post_eq','has_superstructure_adobe_mud','has_superstructure_mud_mortar_stone','has_superstructure_stone_flag','has_superstructure_cement_mortar_stone','has_superstructure_mud_mortar_brick','has_superstructure_cement_mortar_brick','has_superstructure_timber','has_superstructure_bamboo','has_superstructure_rc_non_engineered','has_superstructure_rc_engineered']
        # category can either be nominal or ordinal 
        cat_ordinal=["land_surface_condition","position","damage_grade","technical_solution_proposed","condition_post_eq"]
        cat_nominal=["foundation_type","roof_type","ground_floor_type","other_floor_type","plan_configuration"]
        damage_grades = ['Grade 1','Grade 2', 'Grade 3', 'Grade 4', 'Grade 5']
    
        df[cat_ordinal] = df[cat_ordinal].apply(LabelEncoder().fit_transform)
        df = pd.get_dummies(df,columns=cat_nominal,prefix=cat_nominal)
 
        X_normal = df.loc[df['building_id'] == building_id].drop(['damage_grade','building_id','district_id','vdcmun_id','ward_id'],axis=1)
        forest_best = pickle.load(open('earthquake\packages\model_tuned.pkl','rb'))
        y_pred_normal = forest_best.predict(X_normal.to_numpy())
        return damage_grades[y_pred_normal[0]]
 
    else:
        return'House not Found!!!'