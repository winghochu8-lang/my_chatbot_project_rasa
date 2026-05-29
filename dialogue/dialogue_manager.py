"""
第 3 步：對話管理 (Dialogue Management)
=====================================
追蹤對話狀態並決定下一步動作
"""

import json
from datetime import datetime
from typing import Dict, List, Any

class DialogueManager:
    """對話管理器 - 追蹤對話狀態和上下文"""
    
    def __init__(self):
        # 當前對話狀態
        self.current_state = "start"
        
        # 對話歷史
        self.dialogue_history = []
        
        # 當前上下文 (context)
        self.context = {
            'user_info': {},
            'last_intent': None,
            'last_entities': {},
            'user_id': None,
            'session_start': datetime.now().isoformat()
        }
        
        # 狀態轉移規則
        self.state_transitions = {
            'start': {
                'greeting': 'greeting_response',
                'weather': 'weather_request',
                'news': 'news_request',
                'help': 'help_response',
                'general': 'general_response'
            },
            'greeting_response': {
                'weather': 'weather_request',
                'news': 'news_request',
                'help': 'help_response',
                'general': 'general_response',
            },
            'weather_request': {
                'greeting': 'greeting_response',
                'weather': 'weather_request',
                'general': 'general_response',
                'exit': 'end'
            },
            'end': {
                'greeting': 'greeting_response',
                'weather': 'weather_request',
            }
        }
    
    def update_state(self, intent: str):
        """根據意圖更新對話狀態"""
        if self.current_state in self.state_transitions:
            if intent in self.state_transitions[self.current_state]:
                old_state = self.current_state
                self.current_state = self.state_transitions[self.current_state][intent]
                print(f"📍 狀態轉移: {old_state} → {self.current_state}")
                return True
        
        return False
    
    def add_message(self, role: str, text: str, intent: str = None, entities: Dict = None):
        """添加消息到對話歷史"""
        message = {
            'timestamp': datetime.now().isoformat(),
            'role': role,  # 'user' 或 'assistant'
            'text': text,
            'intent': intent,
            'entities': entities or {}
        }
        self.dialogue_history.append(message)
        
        if role == 'user':
            self.context['last_intent'] = intent
            self.context['last_entities'] = entities or {}
    
    def get_context(self) -> Dict:
        """獲取當前對話上下文"""
        return self.context.copy()
    
    def update_context(self, **kwargs):
        """更新上下文信息"""
        for key, value in kwargs.items():
            if key in self.context:
                if isinstance(self.context[key], dict):
                    self.context[key].update(value)
                else:
                    self.context[key] = value
            else:
                self.context[key] = value
    
    def get_dialogue_summary(self) -> Dict:
        """獲取對話摘要"""
        return {
            'total_turns': len(self.dialogue_history),
            'current_state': self.current_state,
            'context': self.context,
            'history': self.dialogue_history
        }
    
    def reset(self):
        """重置對話狀態"""
        self.current_state = "start"
        self.dialogue_history = []
        self.context = {
            'user_info': {},
            'last_intent': None,
            'last_entities': {},
            'session_start': datetime.now().isoformat()
        }
        print("✅ 對話狀態已重置")


# ===== 使用範例 =====
if __name__ == "__main__":
    manager = DialogueManager()
    
    print("=== 對話管理測試 ===\n")
    
    # 模擬對話流程
    conversations = [
        ('user', '你好', 'greeting', {}),
        ('assistant', '你好！有什麼我可以幫助你的嗎？', None, None),
        ('user', '明天北京天氣如何？', 'weather', {'city': ['北京'], 'date': ['明天']}),
        ('assistant', '明天北京多雲，氣溫 20-28°C', None, None),
        ('user', '謝謝', 'general', {}),
    ]
    
    for role, text, intent, entities in conversations:
        manager.add_message(role, text, intent, entities)
        
        if intent:
            manager.update_state(intent)
        
        print(f"[{role.upper()}]: {text}")
        if intent:
            print(f"  意圖: {intent}")
            if entities:
                print(f"  實體: {entities}")
        print()
    
    # 顯示對話摘要
    print("=== 對話摘要 ===")
    summary = manager.get_dialogue_summary()
    print(f"總回合數: {summary['total_turns']}")
    print(f"當前狀態: {summary['current_state']}")
    print(f"上下文: {json.dumps(summary['context'], ensure_ascii=False, indent=2)}")