import pandas as pd
import io
import jieba

# 直接测试Excel解析
test_file = 'backend/tests/八17期末下.xlsx'

print('直接读取Excel文件:')
try:
    excel_file = pd.ExcelFile(test_file)
    for sheet_name in excel_file.sheet_names:
        print(f'  工作表: {sheet_name}')
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        print(f'  列名: {list(df.columns)}')
        print(f'  前5行数据:')
        print(df.head())
        
        # 测试分词
        print('  分词测试:')
        for col in df.columns:
            if df[col].dtype == 'object':
                for value in df[col].dropna():
                    if isinstance(value, str) and '物理' in value:
                        print(f'    原始值: {value}')
                        # 分词
                        words = list(jieba.cut_for_search(value))
                        print(f'    分词结果: {words}')
                        print(f'    分词后字符串: {" ".join(words)}')
                        break
except Exception as e:
    print(f'  读取失败: {str(e)}')

# 测试当前的Excel解析逻辑
print('\n测试当前的Excel解析逻辑:')
try:
    with open(test_file, 'rb') as f:
        file_content = f.read()
    
    excel_file = pd.ExcelFile(io.BytesIO(file_content))
    content_parts = []
    
    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        sheet_content = ' '.join([' '.join(map(str, row)) for _, row in df.iterrows()])
        content_parts.append(f"工作表 {sheet_name}: {sheet_content}")
    
    full_content = ' '.join(content_parts)
    print(f'解析后的内容长度: {len(full_content)}')
    print(f'内容前200字符: {full_content[:200]}...')
    
    # 检查是否包含"物理"
    if '物理' in full_content:
        print('✓ 解析后的内容中包含"物理"')
    else:
        print('✗ 解析后的内容中不包含"物理"')
        
    # 测试分词
    print('分词后的内容前200字符:')
    if jieba.is_chinese(full_content):
        tokenized = ' '.join(jieba.cut_for_search(full_content))
        print(tokenized[:200])
        if '物理' in tokenized:
            print('✓ 分词后的内容中包含"物理"')
        else:
            print('✗ 分词后的内容中不包含"物理"')
except Exception as e:
    print(f'  解析失败: {str(e)}')
