import spacy
import joblib

# function that generates intent classification
def intent_classification(msg):
    
    # get en_core_web_md from spacy, extract NER of the question from below
    nlp = spacy.load("en_core_web_md")
    
    # part to get trained XGboost model from pkl file. 
    model = joblib.load('../trained.pkl',"r+")

    # to change the class number that model predicted to intents make a list with all the intent labels.
    intent_list = [ 
    'atis_airfare', 
    'atis_airline', 
    'atis_flight', 
    'atis_flight_time', 
    'current_location', 
    'distance', 
    'timezone', 
    'travel_suggestion', 
    'weather' ]

    #part where model predicts.
    cls_result = model.predict([nlp(msg).vector])

    # part where class numbers that model predicted into corresponding intents.
    intent_result = intent_list[cls_result[0]]
    return intent_result    