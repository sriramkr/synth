from pandas import *
 
# reading CSV file
data = read_csv("large.csv", delimiter=",")
# wikidata_code,birth,death,updated_death_date,approx_birth,approx_death,birth_min,birth_max,death_min,death_max,gender,level1_main_occ,name,un_subregion,birth_estimation,death_estimation,bigperiod_birth_graph_b,bigperiod_death_graph_b,curid,level2_main_occ,freq_main_occ,freq_second_occ,level2_second_occ,level3_main_occ,bigperiod_birth,bigperiod_death,wiki_readers_2015_2018,non_missing_score,total_count_words_b,number_wiki_editions,total_noccur_links_b,sum_visib_ln_5criteria,ranking_visib_5criteria,all_geography_groups,string_citizenship_raw_d,citizenship_1_b,citizenship_2_b,list_areas_of_rattach,area1_of_rattachment,area2_of_rattachment,list_wikipedia_editions,un_region,group_wikipedia_editions,bplo1,dplo1,bpla1,dpla1,pantheon_1,level3_all_occ

vals = data['Birth Place'].tolist()
print(set(vals), sep=",")