from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from routes.cargo_routes import cargo_bp
from routes.optimization_routes import optimization_bp
from routes.warehouse_routes import warehouse_bp
from routes.equipment_routes import equipment_bp
from algorithms.lstm_model import build_lstm_model
from database import db

app = Flask(__name__)
CORS(app)  # 支持跨域请求

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/smart_stacking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 注册蓝图
app.register_blueprint(cargo_bp, url_prefix='/api/cargo')
app.register_blueprint(optimization_bp, url_prefix='/api/optimization')
app.register_blueprint(warehouse_bp, url_prefix='/api/warehouse')
app.register_blueprint(equipment_bp, url_prefix='/api/equipment')

# 初始化LSTM模型
lstm_model = build_lstm_model()

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/cargo')
def cargo():
    return render_template('cargo.html')

@app.route('/optimization')
def optimization():
    return render_template('optimization.html')

if __name__ == '__main__':
    app.run(debug=True)