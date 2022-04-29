# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 09:50:41 2022

@author: srandrad
"""

import os
import pandas as pd
import numpy as np
from transformers import Trainer, AutoTokenizer, DataCollatorForTokenClassification, BertForTokenClassification
from module.NER_utils import *
from module.FMEA_class import FMEA
from datasets import load_from_disk, Dataset
from torch import cuda

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

if __name__ == '__main__':
    #model_checkpoint = os.path.join(os.getcwd(),"models", "FMEA-ner", "checkpoint-4490")
    model_checkpoint = os.path.join(os.getcwd(),"models", "FMEA-ner-model", "checkpoint-1424")
    #device = 'cuda' if cuda.is_available() else 'cpu'
    #cuda.empty_cache()
    device = 'cpu'
    print(device)
    
    fmea = FMEA()
    fmea.load_model(model_checkpoint)
    print("loaded model")
    
    #file = "data/srandrad_safecom_v2.jsonl"
    file = "data/SAFECOM_UAS_fire_data.csv"
    #TODO: join annotations to raw df
    #file = "data/NER_test_dataset"
    input_data = fmea.load_data(file, formatted=False, text_col='Text')
    
    print("loaded data")
    preds = fmea.predict()
    #print(preds)
    df = fmea.get_entities_per_doc()
    fmea.display_doc(doc_id="21-0098", save=True, output_path="", colors_path=os.path.join(os.getcwd(),'data','NER_label_config.json'))
    #fmea.group_docs_with_meta()
    #"""
    manual_cluster_file = os.path.join(os.getcwd(),"data", "SAFECOM_UAS_clusters_V1.xlsx")
    fmea.group_docs_manual(manual_cluster_file, grouping_col='Mode')
    fmea.calc_severity(calc_severity)
    fmea.calc_frequency()
    fmea.calc_risk()
    fmea.post_process_fmea(max_words=10)
    #"""
    fmea.fmea_df.to_csv("results/safecom_fmea_.csv")
    #df.to_csv("test_docs_with_ents.csv")
    #print(labels[0])
    #print(fmea.input_data)#['tokens'][0])
    #print(raw_pred[0], label_ids[0])
    
    #metrics = fmea.evaluate_preds()
    #print(metrics["Confusion Matrix"])
