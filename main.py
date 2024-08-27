from ustc_passport_login import USTCPassportLogin

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/token', methods=['POST'])
def getToken():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    resultInput = data.get('resultInput')
    Mysession = USTCPassportLogin()
    # 登录
    loginSuccess = Mysession.login(username, password, resultInput)
    token = ''
    if loginSuccess:
        token = Mysession.token

    return jsonify(token = token)

if __name__ == "__main__":
    app.run()
