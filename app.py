from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from openpyxl import load_workbook
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

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

    print(url)

    result=""

    try:
        result += soup.find('dl', {'class': 'list_e2'}).find(
            'dd').find('span', {'class': 'fnt_k05'}).get_text()

    except:
        result = "네이버 사전에 등재되어 있지 않습니다."

    doc = {
        'title': title_receive,
        'word': word_receive,
        'meaning': result
    }

    db.wordcards.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '등록완료!'})


@app.route('/card', methods=['GET'])
def listing():
    title = request.args.get('title')
    wordcards = list(db.wordcards.find({'title': title}, {'_id': 0}))
    return jsonify({'result': 'success', 'wordcards': wordcards})


@app.route('/nocard', methods=['post'])
def delete():
    word_receive = request.form['word_give']
    title_receive = request.form['title_give']

    db.wordcards.delete_one({'word': word_receive, 'title': title_receive})

    return jsonify({'result': 'success', 'msg': '삭제되었습니다.'})


@app.route('/savetitle', methods=['post'])
def savetitle():
    title_receive = request.form['title_give']
    db.wordcards.update_many({'title': ''}, {'$set': {'title': title_receive}})
    return jsonify({'result': 'success'})

# @app.route('/changecard', methods=['post'])
# def edit():
#     return jsonify({'result': 'success', 'msg': '수정되었습니다.'})

# # 엑셀화


@app.route('/excel', methods=['POST'])
def excel():
    print('excel')
    title_receive = request.form['title_give']
    # word_receive = request.form['word_give']
    # meaning_receive = request.form['meaning_give']
    # print(title_receive)

    cards = list(db.wordcards.find({'title': title_receive}, {'_id': 0}))
    # print(cards)
  
    work_book = load_workbook('test.xlsx')
    work_sheet = work_book['prac']

    row = 2
    for card in cards:
        work_sheet.cell(row=row, column=2, value=card['title'])
        work_sheet.cell(row=row, column=3, value=card['word'])
        work_sheet.cell(row=row, column=4, value=card['meaning'])
        row += 1
        
        work_book.save('test.xlsx')
        
    return jsonify({'result': 'success', 'msg': '로딩완료'})


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<MAIN.HTML화면 연결하기
@app.route('/listpage')
def wordlist():
    return render_template('index.html')


@app.route('/listpage2')
def wordlist2():
    pagetitle = request.args.get('pagetitle')
    pagetitle = pagetitle.replace("'", "")
   
    return render_template('index2.html', pagetitle=pagetitle)


@app.route('/folderlist', methods=['GET'])
def folderlist():
    folderlists = db.wordcards.distinct("title")
    print(folderlists)
    return jsonify({'result': 'success', 'folderlists': folderlists})


@app.route('/deletefolder', methods=['get'])
def deletefoler():
    pagetitle = request.args.get('pagetitle')
    pagetitle = pagetitle.replace("'", "")
    db.wordcards.delete_many({'title': pagetitle})
    return jsonify({'result': 'success', 'msg': '삭제되었습니다.'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
