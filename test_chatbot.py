"""
測試聊天機器人的各個模塊
"""

import sys
sys.path.insert(0, '.')

from nluu.intent_classifier import IntentClassifier
from nluu.entity_extractor import EntityExtractor
from dialogue.dialogue_manager import DialogueManager
from dialogue.response_generator import ResponseGenerator
from main import Chatbot


def test_intent_classifier():
    """測試意圖分類"""
    print("\n" + "="*50)
    print("測試 1：意圖分類")
    print("="*50)
    
    classifier = IntentClassifier()
    
    training_data = [
        ("你好", "greeting"),
        ("早上好", "greeting"),
        ("天氣怎樣", "weather"),
        ("今天天氣", "weather"),
    ]
    
    classifier.train(training_data)
    
    test_cases = [
        "你好，今天天氣如何？",
        "早上好",
        "查詢天氣"
    ]
    
    for text in test_cases:
        intent, conf = classifier.predict(text, confidence=True)
        print(f"  '{text}' → {intent} ({conf:.2f})")


def test_entity_extractor():
    """測試實體抽取"""
    print("\n" + "="*50)
    print("測試 2：實體抽取")
    print("="*50)
    
    extractor = EntityExtractor()
    
    test_cases = [
        "明天北京的天氣",
        "查詢 2024-05-30 深圳的天氣",
        "今天上海下午 3 點"
    ]
    
    for text in test_cases:
        entities = extractor.extract_dict(text)
        print(f"  '{text}'")
        print(f"    → {entities}")


def test_dialogue_manager():
    """測試對話管理"""
    print("\n" + "="*50)
    print("測試 3：對話管理")
    print("="*50)
    
    manager = DialogueManager()
    
    # 模擬對話
    manager.add_message('user', '你好', 'greeting', {})
    manager.update_state('greeting')
    
    manager.add_message('user', '今天天氣如何？', 'weather', {'date': ['今天']})
    manager.update_state('weather')
    
    summary = manager.get_dialogue_summary()
    print(f"  對話回合: {summary['total_turns']}")
    print(f"  當前狀態: {summary['current_state']}")
    print(f"  上下文意圖: {summary['context']['last_intent']}")


def test_response_generator():
    """測試回應生成"""
    print("\n" + "="*50)
    print("測試 4：回應生成")
    print("="*50)
    
    generator = ResponseGenerator()
    
    # 測試問候
    response = generator.generate_response('greeting')
    print(f"  問候: {response}")
    
    # 測試天氣（帶實體）
    entities = {'city': ['北京'], 'date': ['明天']}
    response = generator.generate_response('weather', entities)
    print(f"  天氣: {response}")
    
    # 測試幫助
    response = generator.generate_response('help')
    print(f"  幫助: {response}")


def test_full_chatbot():
    """測試完整聊天機器人"""
    print("\n" + "="*50)
    print("測試 5：完整聊天機器人")
    print("="*50)
    
    chatbot = Chatbot()
    
    test_inputs = [
        "你好",
        "今天天氣如何？",
        "北京明天天氣怎樣？",
        "謝謝"
    ]
    
    for user_input in test_inputs:
        chatbot.process_user_input(user_input)
    
    print("\n📊 對話摘要:")
    summary = chatbot.get_conversation_summary()
    print(f"  - 總回合數: {summary['total_turns']}")
    print(f"  - 最終狀態: {summary['current_state']}")


# ===== 運行所有測試 =====
if __name__ == "__main__":
    print("\n🧪 開始測試聊天機器人...")
    
    try:
        test_intent_classifier()
        test_entity_extractor()
        test_dialogue_manager()
        test_response_generator()
        test_full_chatbot()
        
        print("\n" + "="*50)
        print("✅ 所有測試完成！")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ 測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
