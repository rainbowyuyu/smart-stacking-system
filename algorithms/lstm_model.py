import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from datetime import datetime, timedelta
import joblib

def build_lstm_model(input_shape=(30, 5)):
    """构建LSTM模型用于预测货物出库时间"""
    model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(64))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1))  # 预测出库时间差（天）
    
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

def prepare_training_data(cargo_history, look_back=30):
    """准备训练数据"""
    # 提取特征和目标变量
    # 特征：货物类型、重量、尺寸、是否危险品、入库时间等
    # 目标：在库时间（天）
    
    features = []
    targets = []
    
    for cargo in cargo_history:
        # 提取特征
        if cargo.actual_out_time and cargo.entry_time:
            days_in_storage = (cargo.actual_out_time - cargo.entry_time).days
            
            # 构建特征向量
            feature_vector = [
                1 if cargo.cargo_type == '集装箱' else 0,  # 货物类型（示例：集装箱）
                1 if cargo.cargo_type == '散货' else 0,
                1 if cargo.cargo_type == '件杂货' else 0,
                cargo.weight,
                float(cargo.dimensions.split('x')[0]),  # 长度
                float(cargo.dimensions.split('x')[1]),  # 宽度
                float(cargo.dimensions.split('x')[2]),  # 高度
                1 if cargo.is_hazardous else 0,
                cargo.turnover_rate == '高',
                cargo.turnover_rate == '中',
                cargo.turnover_rate == '低',
                # 可以添加更多特征...
            ]
            
            features.append(feature_vector)
            targets.append(days_in_storage)
    
    # 转换为numpy数组
    X = np.array(features)
    y = np.array(targets)
    
    # 标准化特征
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 保存标准化器供预测使用
    joblib.dump(scaler, 'scaler.pkl')
    
    # 重塑数据为LSTM所需的形状 [样本数, 时间步, 特征数]
    # 由于我们没有时间序列数据，这里假设每个样本是一个时间步
    X_reshaped = X_scaled.reshape(X_scaled.shape[0], 1, X_scaled.shape[1])
    
    return X_reshaped, y, scaler

def train_lstm_model(cargo_history, epochs=50, batch_size=32):
    """训练LSTM模型"""
    X, y, scaler = prepare_training_data(cargo_history)
    
    # 构建模型
    model = build_lstm_model(input_shape=(X.shape[1], X.shape[2]))
    
    # 设置早停
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    
    # 训练模型
    history = model.fit(
        X, y,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.2,
        callbacks=[early_stopping],
        verbose=1
    )
    
    # 保存模型
    model.save('lstm_model.h5')
    
    return model, history

def predict_out_time(cargo_features):
    """使用LSTM模型预测货物出库时间"""
    try:
        # 加载模型和标准化器
        model = tf.keras.models.load_model('lstm_model.h5')
        scaler = joblib.load('scaler.pkl')
        
        # 标准化输入特征
        features_scaled = scaler.transform(cargo_features)
        
        # 重塑数据为LSTM所需的形状
        features_reshaped = features_scaled.reshape(features_scaled.shape[0], 1, features_scaled.shape[1])
        
        # 预测
        prediction = model.predict(features_reshaped)
        
        # 返回预测的在库天数
        return max(1, int(prediction[0][0]))  # 至少1天
    
    except Exception as e:
        print(f"预测出错: {e}")
        # 如果模型加载失败或预测出错，返回默认值
        return 14  # 默认预测14天    