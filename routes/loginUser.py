from flask import jsonify, Blueprint, current_app, request
import mysql.connector

loginUser = Blueprint('loginUser', __name__)


@loginUser.route('/user/loginUser', methods=['POST'])
def loginuser():
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
        print('登录请求:username={username},password={password}'.format(username=username, password=password))

        # 调用存储过程
        cursor.callproc("LoginVerify", (username, password))
        connection.commit()

        # 获取结果集
        results = []
        for result in cursor.stored_results():
            backs = result.fetchall()
            for back in backs:
                results.append(back)
        print(f'数据库结果：{results}')
        if results[0][0] == '1':
            login_result_message = {'result': True,
                                    'delete_num': results[0][2]}
        else:
            login_result_message = {'result': False}

        # 返回结果
        print(login_result_message)
        response_data = {"result": login_result_message}
        return jsonify(response_data)

    except mysql.connector.Error as err:
        print("数据库错误:", err)
        return jsonify({"error": "数据库错误"}), 500

    finally:
        # 关闭游标和连接
        if cursor:
            cursor.close()
        if connection:
            connection.close()
