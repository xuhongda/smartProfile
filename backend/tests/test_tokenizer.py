from tokenizer import ChineseTokenizer

# 测试分词功能
print("测试分词工具模块")
print("=" * 50)

# 测试中文文本分词
chinese_text = "这是一段中文文本，用于测试分词功能"
tokenized_text = ChineseTokenizer.tokenize_text(chinese_text)
print(f"原始文本: {chinese_text}")
print(f"分词结果: {tokenized_text}")
print()

# 测试搜索查询分词
chinese_query = "中文分词测试"
tokenized_query = ChineseTokenizer.tokenize_query(chinese_query)
print(f"原始查询: {chinese_query}")
print(f"分词结果: {tokenized_query}")
print()

# 测试英文文本（应该保持不变）
english_text = "This is an English text for testing"
tokenized_english = ChineseTokenizer.tokenize_text(english_text)
print(f"原始英文文本: {english_text}")
print(f"分词结果: {tokenized_english}")
print()

# 测试混合语言文本
mixed_text = "这是中文English混合文本"
tokenized_mixed = ChineseTokenizer.tokenize_text(mixed_text)
print(f"原始混合文本: {mixed_text}")
print(f"分词结果: {tokenized_mixed}")
print()

# 测试是否包含中文字符
print(f"判断是否包含中文字符:")
print(f"'中文' -> {ChineseTokenizer.is_chinese('中文')}")
print(f"'English' -> {ChineseTokenizer.is_chinese('English')}")
print(f"'中文English' -> {ChineseTokenizer.is_chinese('中文English')}")

print("\n测试完成！")
