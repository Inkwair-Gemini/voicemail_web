from flask import jsonify, Blueprint, current_app, request
import mysql.connector

addUser = Blueprint('addUser', __name__)


@addUser.route('/user/addUser', methods=['POST'])
def adduser():
    try:
        db_pool = current_app.config.get('db_pool')
        # 从连接池获取连接
        connection = db_pool.get_connection()

        # 创建游标
        cursor = connection.cursor()

        # 获取请求中的数据
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        print(f'用户注册请求:username={username},password={password}')

        # 调用存储过程
        cursor.callproc('addUser', (username, password,))
        connection.commit()

        # 获取结果
        results = []
        for result in cursor.stored_results():
            backs = result.fetchall()
            for back in backs:
                results.append(back)
        print(f'数据库结果：{results}')
        response_result = {'result': True if results[0][0] == 1 else False,
                           'reason': results[0][1]}

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
