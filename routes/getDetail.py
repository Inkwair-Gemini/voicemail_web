from flask import jsonify, Blueprint, current_app, request
import mysql.connector
from gtts import gTTS
from io import BytesIO
import base64

getDetail = Blueprint('getDetail ', __name__)


@getDetail .route('/user/getDetail', methods=['POST'])
def getdetail ():
    try:
        db_pool = current_app.config.get('db_pool')
        # 从连接池获取连接
        connection = db_pool.get_connection()
        # 创建游标
        cursor = connection.cursor()
        # 获取数据
        data = request.get_json()
        id = data.get('id')
        print(id)

        # 调用存储过程
        cursor.callproc("gettexttielByid", (id,))
        connection.commit()
        # 获取结果
        results = []
        for result in cursor.stored_results():
            voicemails = result.fetchall()
            for voicemail in voicemails:
                results.append({
                    "title": voicemail[1],
                    "text": voicemail[0],
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
