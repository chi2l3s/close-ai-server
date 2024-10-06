from flask import Flask, request, jsonify
from flask_cors import CORS
import g4f

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех маршрутов

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}],
        stream=True,
    )

    msg = ''
    for message in response:
        msg += message

    if user_message:
        return jsonify({'response': msg}), 200
    else:
        return jsonify({'error': 'Сообщение не получено'}), 400

# Vercel требует, чтобы вы использовали эту функцию
if __name__ == '__main__':1
    app.run()
