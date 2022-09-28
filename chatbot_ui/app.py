from flask import Flask, render_template, jsonify, request
import NER
import intent 
import intent_NER_to_answer

app = Flask(__name__)

# first initialization page was set as index.html
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', **locals())

# This is the part that is ran when the user asks a question and presses send. The function below receives user's question and makes an response.
@app.route('/chatbot', methods=["GET", "POST"])
def chatbot_Answer():

    # this was written so that if the recieved action was POST.
    if request.method == 'POST':

        # get user question
        user_question = request.form['question']
        
        # prediction intent
        intent_predict= intent.intent_classification(user_question)
        # prediction NER
        NER_predict= NER.NER_predict(user_question)
        
        # added console print to check if intent and NER were generated correctly
        print(intent_predict,NER_predict)
        
        # make answer by intent and NER 
        response = intent_NER_to_answer.make_answer(intent_predict,NER_predict)

        # return generated answer.
    return jsonify({"response": response })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)
