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
def make_word():
    word_receive = request.form['word_give']
    doc = {
       'word': word_receive
    }
    db.wordcards.insert_one(doc)
    return jsonify({'result':'success', 'msg': '등록완료!'})

@app.route('/card', methods=['GET'])
def listing():
    result = list(db.wordcards.find({},{'_id':0}))
    return jsonify({'result': 'success', 'wordcards': result})

@app.route('/nocard', methods=['post'])
def delete():
    word_receive = request.form['word_give']
    db.wordcards.delete_one({'word':word_receive})
    return jsonify({'result': 'success', 'msg': '삭제되었습니다.'})

@app.route('/changecard', methods=['post'])
def edit():
    # db.wordcards.delete_one({})
    return jsonify({'result': 'success', 'msg': '수정되었습니다.'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
