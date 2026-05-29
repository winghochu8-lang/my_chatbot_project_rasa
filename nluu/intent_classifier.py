"""
第 1 步：意圖分類 (Intent Classification)
==========================================
使用機器學習模型分類用戶的意圖
"""

import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import os

class IntentClassifier:
    """意圖分類器 - 判斷用戶輸入的意圖"""
    
    def __init__(self, model_path='models/intent_classifier_model.pkl'):
        self.model_path = model_path
        self.pipeline = None
        self.intents = {
            '問候': 'greeting',
            '天氣': 'weather',
            '新聞': 'news',
            '幫助': 'help',
            '通用': 'general'
        }
        self.intent_to_chinese = {v: k for k, v in self.intents.items()}
    
    def train(self, training_data):
        """
        訓練意圖分類模型
        
        Args:
            training_data: List[tuple(text, intent)]
                例如: [("你好", "greeting"), ("天氣如何", "weather")]
        """
        texts = [item[0] for item in training_data]
        labels = [item[1] for item in training_data]
        
        # 創建管道：TF-IDF + 樸素貝葉斯
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=100, ngram_range=(1, 2))),
            ('classifier', MultinomialNB())
        ])
        
        # 訓練模型
        self.pipeline.fit(texts, labels)
        print(f"✅ 意圖分類模型訓練完成")
        
        # 保存模型
        os.makedirs('models', exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.pipeline, f)
        print(f"✅ 模型已保存到 {self.model_path}")
    
    def load_model(self):
        """加載已訓練的模型"""
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                self.pipeline = pickle.load(f)
            print(f"✅ 模型已加載")
            return True
        return False
    
    def predict(self, text, confidence=False):
        """
        預測用戶輸入的意圖
        
        Args:
            text: 用戶輸入文本
            confidence: 是否返回置信度
            
        Returns:
            intent (str) 或 (intent, confidence_score)
        """
        if self.pipeline is None:
            raise ValueError("模型未訓練或未加載")
        
        intent = self.pipeline.predict([text])[0]
        
        if confidence:
            proba = self.pipeline.predict_proba([text])[0]
            confidence_score = np.max(proba)
            return intent, confidence_score
        
        return intent
    
    def predict_top_3(self, text):
        """返回概率最高的前 3 個意圖"""
        if self.pipeline is None:
            raise ValueError("模型未訓練或未加載")
        
        probas = self.pipeline.predict_proba([text])[0]
        classes = self.pipeline.classes_
        
        # 排序
        sorted_idx = np.argsort(probas)[::-1][:3]
        results = [(classes[i], probas[i]) for i in sorted_idx]
        
        return results


# ===== 使用範例 =====
if __name__ == "__main__":
    # 訓練數據
    training_data = [
        ("你好", "greeting"),
        ("早上好", "greeting"),
        ("Hi", "greeting"),
        ("Hey", "greeting"),
        ("天氣怎樣", "weather"),
        ("今天天氣如何", "weather"),
        ("查詢天氣", "weather"),
        ("天氣預報", "weather"),
        ("有什麼新聞", "news"),
        ("最新新聞", "news"),
        ("今日新聞", "news"),
        ("幫助我", "help"),
        ("怎麼使用", "help"),
        ("有什麼功能", "help"),
        ("你是誰", "general"),
        ("謝謝", "general"),
    ]
    
    # 初始化分類器
    classifier = IntentClassifier()
    
    # 訓練模型
    classifier.train(training_data)
    
    # 測試
    print("\n=== 測試意圖分類 ===")
    test_texts = [
        "你好，今天天氣如何？",
        "有什麼新聞嗎？",
        "你能幫我嗎？",
        "早上好"
    ]
    
    for text in test_texts:
        intent, conf = classifier.predict(text, confidence=True)
        print(f"輸入: '{text}'")
        print(f"意圖: {classifier.intent_to_chinese.get(intent, intent)} (信心度: {conf:.2f})\n")