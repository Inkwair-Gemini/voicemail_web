from flask import jsonify, Blueprint, current_app, request
import mysql.connector

loginUser = Blueprint('loginUser', __name__)

class User:
    def __init__(self, user_id, avatar_url, username, delete_count):
        self.user_id = user_id
        self.avatar_url = avatar_url
        self.username = username
        self.delete_count = delete_count
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
                user = User(back[2], back[3], back[4], back[5])  # 创建User对象
                results.append(user)
        print(f'数据库结果：{results}')

        # 修改这部分以返回User对象
        if results and results[0]:
            login_result_message = {'result': True,
                                    'user': results[0].__dict__}  # 转换为字典
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
