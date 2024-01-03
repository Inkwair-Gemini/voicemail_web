from flask import jsonify, Blueprint, current_app, request, send_file
import mysql.connector
from gtts import gTTS
from io import BytesIO

getVoice = Blueprint('getVoice', __name__)


def text_to_audio(text, audio_id):
    # 使用 gTTS 将文本转换为中文语音
    tts = gTTS(text=text, lang='zh-cn')
    # 将音频数据保存到 BytesIO 对象中
    audio_data = BytesIO()
    tts.write_to_fp(audio_data)

    # 将音频数据保存到文件
    file_name = f'audio_{audio_id}.wav'
    audio_data.seek(0)
    with open(file_name, 'wb') as audio_file:
        audio_file.write(audio_data.getvalue())

    return file_name

@getVoice.route('/user/getVoice', methods=['GET'])
def getvoice():
    try:
        db_pool = current_app.config.get('db_pool')
        # 从连接池获取连接
        connection = db_pool.get_connection()

        # 创建游标
        cursor = connection.cursor()

        # 获取请求中的数据
        id = request.args.get('id')

        # 调用存储过程
        cursor.callproc("gettextByid", (id,))
        connection.commit()
        result = cursor.stored_results()
        validation_result = list(result)[0].fetchone()[0]
        print(f'数据库验证结果：{validation_result}')

        # 生成语音文件
        audio_file_path = text_to_audio(validation_result, id)

        # 发送语音文件到前端
        return send_file(audio_file_path, as_attachment=True)

    except mysql.connector.Error as err:
        print("数据库错误:", err)
        return jsonify({"error": "数据库错误"}), 500

    finally:
        # 关闭游标和连接
        if cursor:
            cursor.close()
        if connection:
            connection.close()
