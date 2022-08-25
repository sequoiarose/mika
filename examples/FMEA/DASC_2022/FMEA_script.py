# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 09:50:41 2022

@author: srandrad
"""

import os
import pandas as pd
import numpy as np
from transformers import Trainer, AutoTokenizer, DataCollatorForTokenClassification, BertForTokenClassification
from mika.kd.NER import *
from mika.kd import FMEA #import FMEA
from datasets import load_from_disk, Dataset
from torch import cuda
import random

def calc_severity(df):
    severities = []
    for i in range(len(df)):
        severities.append(safecom_severity(df.iloc[i]['Hazardous Materials'], df.iloc[i]['Injuries'], df.iloc[i]['Damages']))
    df['severity'] = severities
    return df

def safecom_severity(hazardous_mat, injury, damage):
    key_dict = {"No":0, "Yes":1}
    severity = key_dict[hazardous_mat] + key_dict[injury] + key_dict[damage]
    if np.isnan(severity):
        severity=0
    return severity

def safenet_severity(injuries, fatalities, damages):
    """
    1: injuries = 0, damages = 0
    2: injuries = 1 or damages = 1
    3: injuries >1 
    4: >1 fatality
    5: >2 fatalities"""
    if injuries == 0 and fatalities == 0 and damages == 0:
        severity = 1
    elif fatalities == 0:
        if injuries < 2 or damages < 2:
            severity = 2
        else:
            severity = 3
    elif fatalities == 1:
        severity = 4
    elif fatalities > 1:
        severity = 5
    return severity

def calc_safenet_severity(df, grouped_df):
    severities = []
    df = df.set_index('Hazard name')
    df = df.reindex(grouped_df.index).fillna(0)
    for i in range(len(df)):
        severities.append(safenet_severity(df.iloc[i]['injuries'], df.iloc[i]['fatalities'], df.iloc[i]['damages']))
    df['severity'] = severities
    return df

if __name__ == '__main__':
    """
    fmea = FMEA()
    file = "data/annotated_LLIS_IAA/srandrad_safecom_v2.jsonl"
    input_data = fmea.load_data(file, formatted=False, text_col='data')
    fmea.display_doc(doc_id="21-0098", save=True, output_path="results/21-0098_display_annotated", colors_path=os.path.join(os.getcwd(),'data','NER_label_config.json'), pred=False)
    """
    model_checkpoint = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir, os.pardir)),"models", "FMEA-ner-model", "checkpoint-1424")
    device = 'cuda' if cuda.is_available() else 'cpu'
    cuda.empty_cache()
    #device = 'cpu'
    print(device)
    
    fmea = FMEA()
    
    fmea.load_model(model_checkpoint)
    print("loaded model")
    
    file = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir, os.pardir)),"data/SAFECOM/SAFECOM_UAS_fire_data.csv")
    #file = "results/safenet_topics_May-04-2022/preprocessed_data.csv"#"results/SAFECOM_hazards_lda_topics_Apr-04-2022/preprocessed_data.csv"
    #TODO: join annotations to raw df
    #file = "data/NER_test_dataset"
    input_data = fmea.load_data(file, formatted=False, text_col='Text', id_col="Tracking #") #Text
    
    print("loaded data")
    preds = fmea.predict()
    df = fmea.get_entities_per_doc()
    fmea.display_doc(doc_id="21-0098", pred=True, save=False, output_path="", colors_path=os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir, os.pardir)),'data','doccano','NER_label_config.json'))
    #fmea.group_docs_with_meta()
    """
    #manual_cluster_file = os.path.join(os.getcwd(),"data", "SAFECOM_UAS_clusters_V1.xlsx")
    manual_cluster_file = os.path.join(os.getcwd(),"results", "safenet_topics_May-04-2022", 'hazard_docs.csv')
    fmea.group_docs_manual(manual_cluster_file, grouping_col='Hazard', additional_cols=[]) #Mode
    fmea.grouped_df.to_csv(os.path.join(os.getcwd(),"results", "safenet_topics_May-04-2022", "grouped_df.csv"))
    file_name = os.path.join(os.getcwd(),"results", "safenet_topics_May-04-2022","hazard_interpretation.xlsx")
    fmea.calc_severity(calc_safenet_severity, from_file=True, file_name=file_name, file_kwargs={'sheet_name':['topic-focused']})
    fmea.get_year_per_doc(year_col='Event Start Date', config='/')
    fmea.calc_frequency(year_col='Year')
    fmea.calc_risk()
    fmea.post_process_fmea(phase_name='', id_name='SAFENET', max_words=50)
    """
    #fmea.fmea_df.to_csv(os.path.join(os.getcwd(),"results/safenet_topics_May-04-2022/safenet_fmea_2.csv"))
    
    #metrics = fmea.evaluate_preds()
    #print(metrics["Confusion Matrix"])
