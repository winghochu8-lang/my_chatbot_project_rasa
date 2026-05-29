"""
第 2 步：實體抽取 (Entity Extraction)
====================================
從用戶輸入中抽取關鍵信息（如城市、日期等）
"""

import spacy
import re
from datetime import datetime

class EntityExtractor:
    """實體抽取器 - 從用戶輸入中提取關鍵信息"""
    
    def __init__(self):
        try:
            # 加載中文模型
            self.nlp = spacy.load("zh_core_web_sm")
        except OSError:
            print("❌ spaCy 模型未安裝")
            print("請運行: python -m spacy download zh_core_web_sm")
            self.nlp = None
        
        # 自定義實體模式
        self.custom_patterns = {
            'city': r'(北京|上海|廣州|深圳|杭州|南京|武漢|成都|西安|南昌)',
            'date': r'(今天|明天|後天|\d{4}-\d{2}-\d{2})',
            'time': r'(\d{1,2}:\d{2}|\d{1,2}點)',
            'number': r'\d+',
        }
    
    def extract_spacy(self, text):
        """使用 spaCy 提取實體"""
        if self.nlp is None:
            return []
        
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            })
        
        return entities
    
    def extract_custom(self, text):
        """使用正則表達式提取自定義實體"""
        custom_entities = []
        
        for entity_type, pattern in self.custom_patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                custom_entities.append({
                    'text': match.group(),
                    'label': entity_type,
                    'start': match.start(),
                    'end': match.end()
                })
        
        return custom_entities
    
    def extract_all(self, text):
        """提取所有實體（結合 spaCy 和自定義模式）"""
        # 先提取 spaCy 實體
        spacy_entities = self.extract_spacy(text)
        
        # 再提取自定義實體
        custom_entities = self.extract_custom(text)
        
        # 合併去重
        all_entities = spacy_entities + custom_entities
        
        # 按位置排序
        all_entities = sorted(all_entities, key=lambda x: x['start'])
        
        return all_entities
    
    def extract_dict(self, text):
        """返回字典格式的實體"""
        entities = self.extract_all(text)
        result = {}
        
        for entity in entities:
            label = entity['label']
            if label not in result:
                result[label] = []
            result[label].append(entity['text'])
        
        return result


# ===== 使用範例 =====
if __name__ == "__main__":
    extractor = EntityExtractor()
    
    print("=== 實體抽取測試 ===\n")
    
    test_texts = [
        "明天北京的天氣如何？",
        "後天上海下午 3 點的天氣預報",
        "查詢 2024-05-30 深圳的天氣",
        "今天杭州天氣怎樣？"
    ]
    
    for text in test_texts:
        print(f"輸入: '{text}'")
        
        # 顯示所有實體
        entities = extractor.extract_all(text)
        print("所有實體:")
        for entity in entities:
            print(f"  - {entity['text']} ({entity['label']})")
        
        # 顯示字典格式
        entity_dict = extractor.extract_dict(text)
        print("實體字典:", entity_dict)
        print()