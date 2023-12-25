from flask import Flask
import mysql.connector
from flask_cors import CORS

import config
from routes import addUser, loginUser, updateUser, addVoice, sendAllVoice, deleteVoiceByid, selectUserByUsername, restoreById, deleteById, getListByUsername

app = Flask(__name__)
CORS(app, origins="*")

# 创建数据库连接池
db_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="my_pool", pool_size=5, **config.db_config)
app.config['db_pool'] = db_pool

# 注册蓝图并传递数据库连接池
app.register_blueprint(addUser.addUser)
app.register_blueprint(loginUser.loginUser)
app.register_blueprint(updateUser.updateUser)
app.register_blueprint(addVoice.addVoice)
app.register_blueprint(sendAllVoice.sendAllVoice)
app.register_blueprint(deleteVoiceByid.deleteVoiceByid)
app.register_blueprint(selectUserByUsername.selectUserByUsername)
app.register_blueprint(restoreById.restoreById)
app.register_blueprint(deleteById.deleteById)
app.register_blueprint(getListByUsername.getListByUsername)
if __name__ == "__main__":
    app.run(debug=True)