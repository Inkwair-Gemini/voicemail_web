from flask import jsonify, Blueprint, current_app, request
import mysql.connector

recoverById = Blueprint('recoverById', __name__)


@recoverById.route('/delete/recoverById', methods=['GET'])
def recoverByid():
    try:
        db_pool = current_app.config.get('db_pool')
        # 从连接池获取连接
        connection = db_pool.get_connection()

        # 创建游标
        cursor = connection.cursor()

        # 获取请求中的数据
        id= request.args.get("id")
        # 调用存储过程
        cursor.callproc("recoverById", (id,))
        connection.commit()
        result = cursor.stored_results()
        validation_result = list(result)[0].fetchone()[0]
        print(f'数据库验证结果：{validation_result}')
        response_data = {"result": True if validation_result == True else False}
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
