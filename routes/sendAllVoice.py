from flask import jsonify, Blueprint, current_app, request
import mysql.connector
from gtts import gTTS
from io import BytesIO
import base64

sendAllVoice = Blueprint('sendAllVoice', __name__)


def text_to_audio(text):
    # 使用 gTTS 将文本转换为中文语音
    tts = gTTS(text=text, lang='zh-cn')
    # 将音频数据保存到 BytesIO 对象中
    audio_data = BytesIO()
    tts.write_to_fp(audio_data)
    return audio_data.getvalue()


@sendAllVoice.route('/user/sendAllVoice', methods=['POST'])
def sendAllvoice():
    try:
        db_pool = current_app.config.get('db_pool')
        # 从连接池获取连接
        connection = db_pool.get_connection()
        # 创建游标
        cursor = connection.cursor()
        # 获取数据
        data = request.get_json()
        username = data.get('username')
        print(username)

        # 调用存储过程
        cursor.callproc("sendAllVoice", (username,))
        connection.commit()
        # 获取结果
        results = []
        for result in cursor.stored_results():
            voicemails = result.fetchall()
            for voicemail in voicemails:
                results.append({
                    "id": str(voicemail[0]),
                    "title": voicemail[2],
                })
        print(f'数据库结果：{results}')
        if results:
            return jsonify({'voicemails': results})
        else:
            return jsonify({"error": "检索失败"}), 500

    except mysql.connector.Error as err:
        print("数据库错误:", err)
        return jsonify({"error": "数据库错误"}), 500

    finally:
        # 关闭游标和连接
        if cursor:
            cursor.close()
        if connection:
            connection.close()
