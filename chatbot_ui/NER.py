import spacy
#import en_core_web_sm

def NER_predict(msg):
    # spacy en_core_web_sm load  
    nlp = spacy.load("en_core_web_md")
    
    # msg to doc
    doc = nlp(msg)
    
    # extract NER
    hello =([(X.text, X.label_) for X in doc.ents])
    
    #print(hello)    
    
    # extract entity
    NER_result = list(map(lambda x: x[0] if x[1]=='GPE' else 0, hello))
    #print(NER_result)
    
    return NER_result
