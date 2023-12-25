import mysql.connector
import os
from flask import jsonify, Blueprint, current_app, request
import mysql.connector
import speech_recognition as sr
import openai
import json
def get_api_key():
    openai_key_file = "D:\桌面\\apiKey.json"
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
        # 从连接池获取连接
        connection = db_pool.get_connection()

        # 创建游标
        cursor = connection.cursor()
        # 获取请求中的数据
        audio = request.files['audio']
        username = request.form['username']
        timestamp = request.form['timestamp']
        print(username)
        print(timestamp)

        # 将wav格式的音频文件保存到制定路径
        local_path = r'D:\桌面\大三上\人机交互和界面设计\课程设计\语音文件\保存路径'
        formatted_timestamp = timestamp.replace(":", "_").replace("T", "_")
        file_name = f'{username}_{formatted_timestamp}.wav'
        url = os.path.join(local_path, file_name)
        print(url)
        with open(url, "wb") as file:
            file.write(audio.read())

        # 使用语音识别库进行语音识别并保存结果到text
        r = sr.Recognizer()
        with sr.AudioFile(url) as source:
            audio = r.record(source)
            print(audio)
        print("语音识别内容:")
        text = r.recognize_google(audio, language="zh-CN")
        print(text)

        #用GPT3.5总结text生成title
        openai.api_key = get_api_key()
        rsp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "user", "content": "根据以下内容总结一个8个字以内的主题"+text},
        ])
        title=rsp.choices[0].message["content"]
        print("标题："+title)

        # 调用存储过程
        cursor.callproc('addVoice', (username,title, timestamp, text, url))
        connection.commit()

        # 获取结果
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

    finally:
        # 关闭游标和连接
        if cursor:
            cursor.close()
        if connection:
            connection.close()
