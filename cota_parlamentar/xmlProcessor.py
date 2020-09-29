import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm

root = ET.parse('./data/AnoAtual.xml').getroot()

df = pd.DataFrame()

for expense in tqdm(root.findall('dados/despesa')):
    tmp_df = {}
    for child in expense:
        tmp_df[child.tag] = child.text
    df = df.append(tmp_df, ignore_index=True)
        
df.to_csv('./data/AnoAtual.csv', index=False)
print(df.columns)