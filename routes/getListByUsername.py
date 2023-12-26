from flask import jsonify, Blueprint, current_app, request
import mysql.connector

getListByUsername = Blueprint('getListByUsername', __name__)


@getListByUsername.route('/delete/getListByUsername', methods=['POST'])
def getListByusername():
    try:
        db_pool = current_app.config.get('db_pool')
        # 从连接池获取连接
        connection = db_pool.get_connection()
        # 创建游标
        cursor = connection.cursor()
        # 获取数据
        data = request.get_json()
        username = data.get('username')

        # 调用存储过程
        cursor.callproc("getListByUsername", (username,))
        connection.commit()
        # 获取结果
        results = []
        for result in cursor.stored_results():
            voicemails = result.fetchall()
            for voicemail in voicemails:
                results.append({
                    "id": str(voicemail[0]),
                    "username": voicemail[1],
                    "title":voicemail[2],
                    "timestamp": voicemail[3].isoformat(),  # 转换为 ISO 格式
                    "text": voicemail[4],
                })
        print(f'数据库结果：{results}')
        if results is not None:
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
