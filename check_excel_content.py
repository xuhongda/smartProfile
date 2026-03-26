import pandas as pd
import io

# 读取 Excel 文件内容
test_files = [
    'backend/tests/八17期末下.xlsx',
    'backend/tests/成绩单.xlsx'
]

for file_path in test_files:
    print(f'检查文件: {file_path}')
    try:
        excel_file = pd.ExcelFile(file_path)
        for sheet_name in excel_file.sheet_names:
            print(f'  工作表: {sheet_name}')
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            # 检查是否包含"物理"
            for col in df.columns:
                if df[col].dtype == 'object':
                    contains_physics = df[col].astype(str).str.contains('物理').any()
                    if contains_physics:
                        print(f'    列 {col} 包含 "物理"')
                        # 显示包含物理的行
                        physics_rows = df[df[col].astype(str).str.contains('物理', na=False)]
                        for _, row in physics_rows.iterrows():
                            print(f'      内容: {row[col]}')
    except Exception as e:
        print(f'  读取失败: {str(e)}')
    print('---')
