import nltk,re
from itertools import product,permutations,combinations

def preprocess(document):
    '''This function splits documents into sentences, sentences into lists of words, 
    and then labels parts of speech and tags named entities'''
    sentences=nltk.sent_tokenize(document)
    sentences=[nltk.word_tokenize(sent) for sent in sentences]
    sentences=[nltk.pos_tag(sent) for sent in sentences]
    sentences=[nltk.ne_chunk(sent) for sent in sentences]
    return(sentences)
#determine if pair is found in sentence, only record those sentences(label propagation)

def gen_lexical_features(sentence,k=1,stem_and_lem=True):
    '''This function computes lexical features on a word by word basis for future processing.  <k> specifies the window around a token to extract part of speech tags
    and words from; stemming and lemmatizing options exist for the word token'''
    featurelist=[]
    f
    s_len=len(sentence)
    stemmer=nltk.stem.porter.PorterStemmer()
    lemmatizer=nltk.stem.wordnet.WordNetLemmatizer()
    #parse through sentence elements
    for ix,tup in enumerate(sentence):
        features={}
        if not isinstance(sentence[ix],nltk.tree.Tree):
            features['word']=sentence[ix][0]
        else:
            for tup in sentence[ix][0]:
                word.append(tup[0])
            features['word']=" ".join(word)
                    
            
        #get words/POS tags in neighborhood around a word
        for distance in range(1,k+1):
            #make sure we don't hit indexing errors
            if ix-distance<0:
                features['pos'+'l'+str(distance)]='beginningofsentence'
                features['word'+'l'+str(distance)]='beginningofsentence'
            else:
                #preprocessing leaves trees instead of tuples for named entities
                if not isinstance(sentence[ix-distance],nltk.tree.Tree):
                    features['pos'+'l'+str(distance)]=sentence[ix-distance][1]
                    #checking for stem setting
                    if stem_and_lem is False:
                        features['word'+'l'+str(distance)]=sentence[ix-distance][0]
                    else:
                        features['word'+'l'+str(distance)]=stemmer.stem(lemmatizer.lemmatize(sentence[ix-distance][0]))
                else:
                    features['pos'+'l'+str(distance)]=sentence[ix-distance].node
                    word=[]
                    for tup in sentence[ix-distance][0]:
                        word.append(tup[0])
                    if stem_and_lem is False:
                        features['word'+'l'+str(distance)]=" ".join(word)
                    else:
                        features['word'+'l'+str(distance)]=stemmer.stem(lemmatizer.lemmatize(" ".join(word)))                
                    
                    
            if ix+distance>(s_len-1):
                features['pos'+'r'+str(distance)]='endofsentence'
                features['word'+'r'+str(distance)]='endofsentence'
            else:
                if not isinstance(sentence[ix+distance],nltk.tree.Tree):
                    features['pos'+'r'+str(distance)]=sentence[ix+distance][1]
                    #checking for stem setting
                    if stem_and_lem is False:
                        features['word'+'r'+str(distance)]=sentence[ix+distance][0]
                    else:
                        features['word'+'r'+str(distance)]=stemmer.stem(lemmatizer.lemmatize(sentence[ix+distance][0]))
                else:
                    features['pos'+'r'+str(distance)]=sentence[ix+distance].node
                    word=[]
                    for tup in sentence[ix+distance][0]:
                        word.append(tup[0])
                    if stem_and_lem is False:
                        features['word'+'r'+str(distance)]=" ".join(word)
                    else:
                        features['word'+'r'+str(distance)]=stemmer.stem(lemmatizer.lemmatize(" ".join(word)))
        
        featurelist.append(features)
    features['pair']    
    return(featurelist)


#determine if pair is found in sentence, only record those sentences(label propagation)
def find_pair(pair,doc):
    '''This function finds and returns sentences with a pair of words them'''
    rs=[]
    for i in doc:
        word1=False
        word2=False
        for j in i:
            if pair[0].lower() in j:
                word1=True
            if pair[1].lower() in j:
                word2=True
            if word1==True and word2==True:
                rs.append(i)
                break
    return(rs)

def NE_expansion(tree):
    '''get full named entity from tree structure'''
    word=[]
    for tup in tree:
        word.append(tup[0])
    word=" ".join(word)
    return(word)

def NE_extraction(sentence):
    '''get named entities from a sentence'''
    Named_Entities=[]
    for ix,tup in enumerate(sentence):
        if isinstance(sentence[ix],nltk.tree.Tree):
            Named_Entities.append((ix,NE_expansion(sentence[ix])))
    return(Named_Entities)

def NE_tuples(relations):
    '''get all possible pairs of relation'''
    return(combinations(relations,r=2))
        
def relation_features(sentence,pair,k=1,stem_and_lem=True):
    features={}
    s_len=len(sentence)
    pos_sequence=[]
    word_sequence=[]
    stemmer=nltk.stem.porter.PorterStemmer()
    lemmatizer=nltk.stem.wordnet.WordNetLemmatizer()
    for ix in range(pair[0][0]+1,pair[1][0]):
        tup=sentence[ix]
        if isinstance(tup,nltk.tree.Tree):
            pos_sequence.append(tup.node)
            word_sequence.append(NE_expansion(tup))
        else:
            word_sequence.append(tup[0])
            pos_sequence.append(tup[1])
        features['pos_sequence']=" ".join(pos_sequence)
        if stem_and_lem is True:
            features['word_sequence']=stemmer.stem(lemmatizer.lemmatize(" ".join(word_sequence)))
        else:
            features['word_sequence']=" ".join(word_sequence)
    w=0
    for named_ent in pair:
        w=w+1
        for distance in range(1,k+1):
            #make sure we don't hit indexing errors
            if named_ent[0]-distance<0:
                features['pos'+'l'+str(distance)+str(w)]='beginningofsentence'
                features['word'+'l'+str(distance)+str(w)]='beginningofsentence'
            else:
                #preprocessing leaves trees instead of tuples for named entities
                if not isinstance(sentence[named_ent[0]-distance],nltk.tree.Tree):
                    features['pos'+'l'+str(distance)]=sentence[named_ent[0]-distance][1]
                    #checking for stem setting
                    if stem_and_lem is False:
                        features['word'+'l'+str(distance)+str(w)]=sentence[named_ent[0]-distance][0]
                    else:
                        features['word'+'l'+str(distance)+str(w)]=stemmer.stem(lemmatizer.lemmatize(sentence[named_ent[0]-distance][0]))
                else:
                    features['pos'+'l'+str(distance)]=sentence[named_ent[0]-distance].node
                    word=[]
                    for tup in sentence[named_ent[0]-distance][0]:
                        word.append(tup[0])
                    if stem_and_lem is False:
                        features['word'+'l'+str(distance)+str(w)]=" ".join(word)
                    else:
                        features['word'+'l'+str(distance)+str(w)]=stemmer.stem(lemmatizer.lemmatize(" ".join(word)))                
                    
                    
            if named_ent[0]+distance>(s_len-1):
                features['pos'+'r'+str(distance)+str(w)]='endofsentence'
                features['word'+'r'+str(distance)+str(w)]='endofsentence'
            else:
                if not isinstance(sentence[named_ent[0]+distance],nltk.tree.Tree):
                    features['pos'+'r'+str(distance)+str(w)]=sentence[named_ent[0]+distance][1]
                    #checking for stem setting
                    if stem_and_lem is False:
                        features['word'+'r'+str(distance)+str(w)]=sentence[named_ent[0]+distance][0]
                    else:
                        features['word'+'r'+str(distance)+str(w)]=stemmer.stem(lemmatizer.lemmatize(sentence[named_ent[0]+distance][0]))
                else:
                    features['pos'+'r'+str(distance)+str(w)]=sentence[named_ent[0]+distance].node
                    word=[]
                    for tup in sentence[named_ent[0]+distance][0]:
                        word.append(tup[0])
                    if stem_and_lem is False:
                        features['word'+'r'+str(distance)+str(w)]=" ".join(word)
                    else:
                        features['word'+'r'+str(distance)+str(w)]=stemmer.stem(lemmatizer.lemmatize(" ".join(word)))
        
    features['relation']=sorted([pair[0][1],pair[1][1]])
    return(features)    

