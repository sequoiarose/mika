# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 13:19:22 2021

@author: srandrad
"""
import pandas as pd
import os
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
import tomotopy as tp
import sys
import os
sys.path.append(os.path.join("..", "..", ".."))
from mika.kd import Topic_Model_plus


list_of_attributes = ['Narrative']#'narr_public']#, 'corrective_public', 'notes']
extra_cols_doi = ['region', 'agency', 'duplicate_yn', 'completed_yn', 'rep_by_org',
                   'air_number', 'air_type', 'air_model', 'air_manufacturer',
                   'air_owner', 'mission_destination', 'mission_depart', 'mission_hazmat',
                   'mission_special_use', 'mission_pax', 'mission_procurement_other',
                   'mission_procurement', 'mission_type_other', 'mission_type',
                   'event_damage', 'event_injuries', 'event_org', 'event_org_other',
                   'event_state', 'event_location', 'event_time', 'event_date',
                   'public_yn', 'sequence_number', 'fiscal_year', 'unitid', 'safecomid',
                   'id']
extra_cols = ['Agency', 'Region', 'Location', 'Date', 'Date Submitted', 'Tracking #',
              'Mission Type', 'Persons Onboard', 'Departure Point', 'Destination',
              'Special Use', 'Damages', 'Injuries', 'Hazardous Materials', 'Other Mission Type',
              'Type', 'Manufacturer', 'Model', 'Hazard', 'Incident	Management',
              'UAS', 'Accident', 'Airspace', 'Maintenance', 'Mishap Prevention'
              ]
document_id_col = 'Tracking #'#id'
csv_file_name = os.path.join('data','SAFECOM_data.csv')
name = os.path.join('safecom')
"""
safecom = Topic_Model_plus(list_of_attributes=list_of_attributes, document_id_col=document_id_col, 
                        csv_file=csv_file_name, database_name=name, extra_cols=extra_cols)
num_topics ={'Narrative': 96}
safecom.prepare_data()
fire_missions = [mission for mission in list(safecom.data_df['Mission Type']) if type(mission) is str and 'fire' in mission.lower()]
safecom.data_df = safecom.data_df.loc[safecom.data_df['Mission Type'].isin(fire_missions)].reset_index(drop=True)
safecom.doc_ids = safecom.data_df[document_id_col].tolist()
raw_text = safecom.data_df[safecom.list_of_attributes] 
raw_attrs = ['Raw_'+attr for attr in safecom.list_of_attributes]
safecom.data_df[raw_attrs] = raw_text
"""
#safecom.preprocess_data()
#safecom.save_preprocessed_data()
#"""
#"""#Extract preprocessed data
file = os.path.join('topic_model_results','preprocessed_data.csv')
safecom = Topic_Model_plus(document_id_col=document_id_col, extra_cols=extra_cols, list_of_attributes=list_of_attributes, database_name=name, combine_cols=False)
safecom.extract_preprocessed_data(file)
#"""
"""#run hdp to get topic numbers
safecom.database_name = "SAFECOM_hazards_hdp"
safecom.hdp()
for attr in list_of_attributes:
    print(safecom.hdp_models[attr].k)
safecom.save_lda_results()
safecom.save_lda_models()
for attr in list_of_attributes:
    safecom.lda_visual(attr)
"""
#"""
num_topics ={'Narrative': 100}
safecom.database_name = "SAFECOM_hazards_lda"
safecom.lda(min_cf=1, num_topics=num_topics)
safecom.save_lda_results()
safecom.save_lda_models()
for attr in list_of_attributes:
    safecom.lda_visual(attr)
#"""

"""#Run hlda
safecom.hlda(levels=3, eta=0.50, min_cf=1, min_df=1)
safecom.save_hlda_models()
safecom.save_hlda_results()
for attr in list_of_attributes:
    safecom.hlda_visual(attr)
"""

"""#Run Bertopic
safecom.data_df[safecom.list_of_attributes] = raw_text
vectorizer_model = CountVectorizer(ngram_range=(1, 2), stop_words="english") #removes stopwords
hdbscan_model = HDBSCAN(min_cluster_size=3, min_samples=3) #allows for smaller topic sizes/prevents docs with no topics
safecom.bert_topic(count_vectorizor=vectorizer_model, hdbscan=hdbscan_model)
safecom.save_bert_results()
#get coherence
#coh = ICS.get_bert_coherence(coh_method='c_v')
safecom.save_bert_vis()
safecom.reduce_bert_topics(num=100)
safecom.save_bert_results()
safecom.save_bert_vis()
"""