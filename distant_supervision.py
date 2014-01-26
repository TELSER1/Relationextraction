import os
from convenience_functions import preprocess, NE_expansion,NE_extraction,NE_tuples,relation_features,gen_lexical_features
class distant_supervisor:
    def __init__(self):
        self.text=[]
        return
    def get_files(self,directory=".",type_="txt"):
        '''Note: '.' points to your current directory'''
        self.files=[]
        for file_ in os.listdir(directory):
            if file_.endswith("."+type_):
                self.files.append(file_)
        return
    def preprocess_docs(self):
        for doc in self.files:
            file_=open(doc,"r")
            self.text+=preprocess(file_.read())
    def vectorize_corpus(self,window=1,stem_and_lem=True,only_relations=False,autolabel=False,example_file=None):
        if example_file is not None:
            with open(example_file,'Ur') as file_:
                examples=list(sorted(list(exemplar) for exemplar in csv.reader(file_,delimiter=',')))
        
        all_docs=[]
            
        if not only_relations:
            for sentence in self.text:
                all_docs=all_docs+gen_lexical_features(sentence,k=window,stem_and_lem=stem_and_lem)
        else:
            for sentence in self.text:
                named_ents=NE_extraction(sentence)
                named_ents=NE_tuples(named_ents)
                for pair in named_ents:
                    r_f=[relation_features(sentence,pair,k=window,stem_and_lem=stem_and_lem)]
                    if autolabel is True:
                        if r_f[0]['relation'] in examples:
                            r_f[0]['is_relation']=1
                        else:
                            r_f[0]['is_relation']=0
                    all_docs=all_docs+r_f
    
        return(all_docs)
    

