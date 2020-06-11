from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

## API 역할을 하는 부분
@app.route('/word', methods=['POST'])
def test_post():
    word_receive = request.form['word_give']
    doc = {
       'word': word_receive
    }
    db.wordcards.insert_one(doc)
   
   return jsonify({'result':'success', 'msg': '이 요청은 POST!'})

@app.route('/card', methods=['GET'])
def test_get():
   title_receive = request.args.get('title_give')
   print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 GET!'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
