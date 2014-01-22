import nltk

def preprocess(document):
    '''This function splits documents into sentences, sentences into lists of words, 
    and then labels parts of speech and tags named entities'''
    sentences=nltk.sent_tokenize(document)
    sentences=[nltk.word_tokenize(sent) for sent in sentences]
    sentences=[nltk.pos_tag(sent) for sent in sentences]
    sentences=[nltk.ne_chunk(sent) for sent in sentences]
    return(sentences)

def gen_lexical_features(sentence,k=1, pair=None,stem_and_lem=True):
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
    return(featurelist)

def find_pair(pair,doc):
'''this function finds and returns sentences with the word pair in them'''
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
