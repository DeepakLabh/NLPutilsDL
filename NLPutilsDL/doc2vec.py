from tqdm import tqdm
import re
from nltk import sent_tokenize
import numpy as np

class data:
    '''--->> make_vector_data('Path to file', 'json', 'MongoClient().xtz.abc')
    '''

    def __init__(self, file_path, file_type, collection = None):
	self.file_path = file_path
	self.file_type = file_type
	self.collection = collection

    def create_vectors(self, sentence_field, word_key, vec_key, max_sent_len = 40, max_num_sents = 10, wordvec_dim = 300, sent_tokenize_flag = True, start_index=0, end_index=0):
        ''' --->> create_vectors('text', '_id', 'vec', 10, 5, 300)
	    --->> collection.find_one({woed_key:vec_key})[vec_key] --> mongo collection object query fields	'''
	zero_vec_sent = np.zeros((max_sent_len,wordvec_dim))
	zero_vec = np.zeros(wordvec_dim)
	rand_vec = np.random.random(wordvec_dim)
	x = []

	if self.file_type == 'json':
	    import json
	    data = json.load(open(self.file_path)) 
	if self.file_type == 'csv':
	    import pandas as pd
	    data = pd.read_csv(self.file_path)
        indexes = range(start_index, end_index) if end_index>0 else xrange(len(data))
	for i in tqdm(indexes):
	    if self.file_type == 'json':
	        paragraph = json.loads(data[i])[sentence_field].encode('ascii','ignore').lower().strip()
	    if self.file_type == 'csv':
	        paragraph = data[sentence_field][i].encode('ascii','ignore').lower().strip()
            sents = sent_tokenize(paragraph) if sent_tokenize_flag else [paragraph]
            para_vec = []
            for sent in sents:
                words = sent.strip().split()
                sent_vec = []
                for word in words:
                    try:
                        vec = self.collection.find_one({word_key:word})[vec_key]
                    except:
                        vec = zero_vec
                    sent_vec.append(vec)
                sent_vec = sent_vec[:max_sent_len] if len(sent_vec)>max_sent_len else sent_vec+[zero_vec]*(max_sent_len-len(sent_vec))
            
                para_vec.append(sent_vec)
	    if not sent_tokenize_flag: para_vec = para_vec[0]
            else: para_vec = para_vec[:max_num_sents] if len(para_vec)>max_num_sents else para_vec+[zero_vec_sent]*(max_num_sents-len(para_vec))
            x.append(para_vec)
	else: raise Exception('only json format supported till now')
	return np.array(x)
