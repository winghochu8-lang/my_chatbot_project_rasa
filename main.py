"""
聊天機器人主程式
"""

from nluu.intent_classifier import IntentClassifier
from nluu.entity_extractor import EntityExtractor
from dialogue.dialogue_manager import DialogueManager
from dialogue.response_generator import ResponseGenerator


class Chatbot:
    """整合 NLU、對話管理、回應生成的聊天機器人"""

    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = EntityExtractor()
        self.dialogue_manager = DialogueManager()
        self.response_generator = ResponseGenerator()

        self._ensure_intent_model_ready()

    def _ensure_intent_model_ready(self):
        """確保意圖分類模型可用：若無已訓練模型就先訓練一個基礎模型。"""
        if self.intent_classifier.load_model():
            return

        training_data = [
            ("你好", "greeting"),
            ("早上好", "greeting"),
            ("哈囉", "greeting"),
            ("今天天氣如何", "weather"),
            ("查詢天氣", "weather"),
            ("北京明天天氣", "weather"),
            ("有什麼新聞", "news"),
            ("最新新聞", "news"),
            ("幫助我", "help"),
            ("怎麼使用", "help"),
            ("謝謝", "general"),
            ("你是誰", "general"),
        ]
        self.intent_classifier.train(training_data)

    def process_user_input(self, user_input: str) -> str:
        """處理單輪使用者輸入，回傳並記錄機器人回應。"""
        intent = self.intent_classifier.predict(user_input)
        entities = self.entity_extractor.extract_dict(user_input)

        self.dialogue_manager.add_message("user", user_input, intent, entities)
        self.dialogue_manager.update_state(intent)

        context = self.dialogue_manager.get_context()
        response = self.response_generator.generate_response(intent, entities, context)

        self.dialogue_manager.add_message("assistant", response)

        print(f"\n👤 使用者: {user_input}")
        print(f"🤖 機器人: {response}")
        return response

    def get_conversation_summary(self):
        """取得對話摘要。"""
        return self.dialogue_manager.get_dialogue_summary()


if __name__ == "__main__":
    bot = Chatbot()
    print("🤖 聊天機器人已啟動，輸入 'exit' 離開。")

    while True:
        text = input("\n你: ").strip()
        if text.lower() in {"exit", "quit", "bye"}:
            print("👋 再見！")
            break

        if not text:
            print("請輸入內容。")
            continue

        bot.process_user_input(text)
