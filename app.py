from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from openpyxl import load_workbook
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
# 엑셀화
# 크롤링

# 파이몽고
client = MongoClient('localhost', 27017)
db = client.dbsparta

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<INDEX HTML을 주는 부분


@app.route('/')
def home():
    return render_template('main.html')

# API 역할을 하는 부분


@app.route('/word', methods=['POST'])
def make_word():
    word_receive = request.form['word_give']
    title_receive = request.form['title_give']
    url = "http://endic.naver.com/search.nhn?query=" + word_receive
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    result = ""
    try:
        result += soup.find('dl', {'class': 'list_e2'}).find(
            'dd').find('span', {'class': 'fnt_k05'}).get_text()
    except:
        result = "네이버 사전에 등재되어 있지 않습니다."

    doc = {'title': title_receive,
           'word': word_receive,
           'meaning': result}
    db.wordcards.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '등록완료!'})


@app.route('/card', methods=['GET'])
def listing():
    result=list(db.wordcards.find({'_id':0}))
    return jsonify({'result': 'success', 'wordcards': result})


@app.route('/nocard', methods=['post'])
def delete():
    word_receive = request.form['word_give']
    db.wordcards.delete_one({'word': word_receive})
    return jsonify({'result': 'success', 'msg': '삭제되었습니다.'})

# @app.route('/changecard', methods=['post'])
# def edit():
#     return jsonify({'result': 'success', 'msg': '수정되었습니다.'})

# # 엑셀화
# @app.route('/excel', methods=['POST'])
# def excel_file():
#     work_book = load_workbook('prac01.xlsx')
#     work_sheet = work_book['prac']
#     words = db.wordcards.find({'word'})
#     meanings =db.wordcards.find({'meaning'})
#     rank=1
#     rank=2
#     for word in words:
#         work_sheet.cell(row=row, column=1, value='rank')
#         work_sheet.cell(row=row, column=2, value='word')
#         work_sheet.cell(row=row, column=3, value='meaning')
#         row +=1
#         rank+=1

#         work_book.save('prac01.xlsx')
#         return jsonify({'result': 'success', 'wordcards': result})
# --------------------------------------------------
# target_movie=db.movies.find_one({'title':'헬프'})
# target_star=target_movie['star']
#     print(word)
#     work_sheet.cell(row=2, column=2, value='dfsfd')
#     return jsonify({'result': 'success', 'wordcards': result})


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<MAIN.HTML화면 연결하기
@app.route('/listpage')
def wordlist():
    return render_template('index.html')

# @app.route('/new', methods=['POST'])
# def startnew():
#     db.wordcards.delete_many({})
#     return jsonify({'result': 'success', 'msg': '삭제되었습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
