import os
import json
from datetime import datetime
from flask import jsonify, Blueprint, current_app, request
import mysql.connector
import speech_recognition as sr
import openai
from pydub import AudioSegment
from pydub.playback import play
def get_api_key():
    openai_key_file = "../api/apiKey.json"
    with open(openai_key_file, 'r', encoding='utf-8') as f:
        openai_key = json.loads(f.read())
    return openai_key['api']

os.environ["HTTP_PROXY"] = "127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "127.0.0.1:7890"

addVoice = Blueprint('addVoice', __name__)

@addVoice.route('/user/addVoice', methods=['POST'])
def addvoice():
    try:
        db_pool = current_app.config.get('db_pool')
        connection = db_pool.get_connection()
        cursor = connection.cursor()

        audio = request.files['audio']
        username = request.form['username']
        timestamp_str = request.form['timestamp']
        formatted_timestamp = timestamp_str.replace(":", "_").replace("T", "_")
        timestamp_1 = datetime.strptime(timestamp_str, '%a %b %d %Y %H:%M:%S GMT%z (香港标准时间)')
        timestamp = timestamp_1.date()

        local_path = r'../voice/'
        file_name = f'{username}_{formatted_timestamp}.wav'
        url = os.path.join(local_path, file_name)

        with open(url, "wb") as file:
            file.write(audio.read())

        # 使用 pydub 打开音频文件并转换为 WAV 格式
        audio = AudioSegment.from_file(url)
        audio.export(url, format="wav")

        r = sr.Recognizer()
        with sr.AudioFile(url) as source:
            audio = r.record(source)

        print("语音识别内容:")
        text = r.recognize_google(audio, language="zh-CN")
        print(text)

        openai.api_key = get_api_key()

        # 使用openai.Completion.create替代openai.ChatCompletion.create
        rsp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "根据以下内容总结一个8个字以内的主题" + text},
            ],
            max_tokens=30,
            temperature=0.7
        )

        title = rsp.choices[0].message["content"].strip()

        print("标题："+title)

        cursor.callproc('addVoice', (username, title, timestamp, text, url))
        connection.commit()

        results = []
        for result in cursor.stored_results():
            backs = result.fetchall()
            for back in backs:
                results.append(back)
        print(f'数据库结果：{results}')

        response_result = {'success': True if results[0][0] == '添加成功' else False}
        print(response_result)
        return jsonify(response_result)

    except mysql.connector.Error as err:
        print("数据库错误:", err)
        return jsonify({"error": "数据库错误"}), 500
    except sr.UnknownValueError as e:
        print(f"无法识别音频内容：{e}")
        # 处理无法识别的情况，例如返回错误响应
    except sr.RequestError as e:
        print(f"请求错误：{e}")
        # 处理请求错误的情况，例如返回错误响应
    except Exception as e:
        print(f"发生其他异常：{e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
