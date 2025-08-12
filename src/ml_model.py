from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import numpy as np

def prepare_features(df):
    """Prepare features and target for ML model"""
    df = df.copy().dropna()
    
    # Create target: 1 if next day close > current close, 0 otherwise
    df['next_close'] = df['Close'].shift(-1)
    df['target'] = (df['next_close'] > df['Close']).astype(int)
    
    # Select features
    features = df[['RSI', 'MACD', 'MACD_SIGNAL', 'SMA_diff', 'Volume']].dropna()
    target = df.loc[features.index, 'target']
    
    return features, target

def train_and_eval(features, target):
    """Train Decision Tree model and evaluate performance"""
    if len(features) < 50:
        return {'model': None, 'accuracy': 0, 'report': 'Insufficient data'}
    
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42, shuffle=False
    )
    
    clf = DecisionTreeClassifier(max_depth=5, random_state=42)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    
    acc = accuracy_score(y_test, preds)
    report = classification_report(y_test, preds, zero_division=0)
    
    # Feature importance
    feature_importance = dict(zip(features.columns, clf.feature_importances_))
    
    return {
        'model': clf, 
        'accuracy': acc, 
        'report': report,
        'feature_importance': feature_importance
    }

def predict_next_day(model, latest_data):
    """Predict next day movement using trained model"""
    if model is None:
        return None
    
    features = latest_data[['RSI', 'MACD', 'MACD_SIGNAL', 'SMA_diff', 'Volume']].iloc[-1:]
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]
    
    return {
        'prediction': 'UP' if prediction == 1 else 'DOWN',
        'probability': max(probability),
        'up_probability': probability[1],
        'down_probability': probability[0]
    }
