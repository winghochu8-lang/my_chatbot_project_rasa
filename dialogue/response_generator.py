"""
第 4 步：回應生成 (Response Generation)
=====================================
根據意圖和實體生成適當的回應
"""

import random
from typing import Dict, List, Any

class ResponseGenerator:
    """回應生成器 - 根據意圖和實體生成回應"""
    
    def __init__(self):
        # 預定義的回應模板
        self.response_templates = {
            'greeting': [
                "你好！很高興認識你！有什麼我可以幫助的嗎？",
                "早上好！今天有什麼需要幫助的嗎？",
                "你好呀！有什麼問題嗎？",
                "Hi 😊 有什麼我可以做的？"
            ],
            'weather': [
                "正在為您查詢 {city} 的天氣...",
                "讓我查一下 {city} {date} 的天氣預報...",
                "為您查詢 {city} 的實時天氣情況...",
            ],
            'news': [
                "正在為您檢索最新新聞...",
                "讓我查找相關的新聞內容...",
                "為您查詢最新的新聞資訊...",
            ],
            'help': [
                "我可以幫助您：\n1. 查詢天氣\n2. 獲取新聞\n3. 通用對話",
                "我支持以下功能：\n• 天氣查詢\n• 新聞資訊\n• 閒聊對話",
                "您可以詢問我：\n- 天氣情況\n- 最新新聞\n- 日常問題",
            ],
            'general': [
                "我理解了。還有其他我可以幫助的嗎？",
                "好的，有其他問題嗎？",
                "明白了。還有什麼需要幫助的呢？",
            ],
            'weather_response': [
                "根據預報，{city} {date} 的天氣是：晴天，氣溫 20-28°C",
                "{city} {date} 天氣概況：多雲，氣溫 18-26°C，濕度 60%",
                "{city} {date} 預報：{weather_condition}，氣溫 {temperature}",
            ],
            'error': [
                "抱歉，我沒有理解。可以重新說一遍嗎？",
                "我沒聽懂，能否用其他方式表達？",
                "抱歉，我不太理解。能否提供更多信息？",
            ]
        }
    
    def generate_response(self, intent: str, entities: Dict = None, context: Dict = None) -> str:
        """
        根據意圖和實體生成回應
        
        Args:
            intent: 用戶意圖
            entities: 提取的實體
            context: 對話上下文
            
        Returns:
            生成的回應文本
        """
        entities = entities or {}
        context = context or {}
        
        # 獲取模板
        if intent in self.response_templates:
            templates = self.response_templates[intent]
            response = random.choice(templates)
            
            # 填充實體信息
            if entities:
                response = self._fill_template(response, entities, context)
            
            return response
        
        # 如果沒有模板，返回默認回應
        return random.choice(self.response_templates['general'])
    
    def _fill_template(self, template: str, entities: Dict, context: Dict) -> str:
        """填充模板中的變數"""
        # 填充城市
        if '{city}' in template and 'city' in entities:
            city = entities['city'][0] if isinstance(entities['city'], list) else entities['city']
            template = template.replace('{city}', city)
        
        # 填充日期
        if '{date}' in template and 'date' in entities:
            date = entities['date'][0] if isinstance(entities['date'], list) else entities['date']
            template = template.replace('{date}', date)
        
        # 填充天氣條件（示例）
        if '{weather_condition}' in template:
            template = template.replace('{weather_condition}', '晴天')
        
        # 填充溫度（示例）
        if '{temperature}' in template:
            template = template.replace('{temperature}', '20-28°C')
        
        return template
    
    def generate_follow_up(self, intent: str, satisfied: bool) -> str:
        """生成跟進問題"""
        follow_ups = {
            'weather': [
                "還想查詢其他地方的天氣嗎？",
                "需要查看詳細的天氣預報嗎？",
                "想要設置天氣提醒嗎？"
            ],
            'news': [
                "還想看其他新聞嗎？",
                "需要詳細的新聞內容嗎？",
                "想要訂閱新聞通知嗎？"
            ],
            'general': [
                "還有其他問題嗎？",
                "有什麼其他我可以幫助的？"
            ]
        }
        
        if intent in follow_ups:
            return random.choice(follow_ups[intent])
        
        return "還有其他我可以幫助的嗎？"


# ===== 使用範例 =====
if __name__ == "__main__":
    generator = ResponseGenerator()
    
    print("=== 回應生成測試 ===\n")
    
    # 測試案例 1：問候
    print("測試 1：問候")
    response = generator.generate_response('greeting')
    print(f"回應: {response}\n")
    
    # 測試案例 2：天氣查詢（帶實體）
    print("測試 2：天氣查詢")
    entities = {
        'city': ['北京'],
        'date': ['明天']
    }
    response = generator.generate_response('weather', entities)
    print(f"回應: {response}")
    follow_up = generator.generate_follow_up('weather', False)
    print(f"跟進: {follow_up}\n")
    
    # 測試案例 3：幫助
    print("測試 3：幫助")
    response = generator.generate_response('help')
    print(f"回應: {response}\n")
    
    # 測試案例 4：錯誤處理
    print("測試 4：未知意圖")
    response = generator.generate_response('unknown_intent')
    print(f"回應: {response}\n")