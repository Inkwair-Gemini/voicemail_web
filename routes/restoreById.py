from flask import jsonify, Blueprint, current_app, request
import mysql.connector

restoreById = Blueprint('restoreById', __name__)


@restoreById.route('/delete/recoverById', methods=['POST'])
def restoreByid():
    try:
        db_pool = current_app.config.get('db_pool')
        # 从连接池获取连接
        connection = db_pool.get_connection()

        # 创建游标
        cursor = connection.cursor()

        # 获取请求中的数据
        data = request.get_json()
        id= data.get('id')
        # 调用存储过程
        cursor.callproc("recoverById", (id,))
        connection.commit()
        result = cursor.stored_results()
        validation_result = list(result)[0].fetchone()[0]
        print(f'数据库验证结果：{validation_result}')
        response_data = {"result": True if validation_result == 'avatarUrl changed successfully.' else False}
        return jsonify()

        # 获取结果集
        results = cursor.stored_results()

        validation_result = list(results)[0].fetchone()
        print('数据库验证结果', validation_result)
        login_result_message = True
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
