import pandas as pd
from pandas import DataFrame
from pathlib import Path
import ast
import json

def get_top_reviewers_json(df, top_n=10):
    """
    Retorna o Top N reviewers calculando o limiar de votos mínimos 
    de forma dinâmica (média entre o maior e o menor número de interações).
    """
    
    if not df.empty and isinstance(df['helpful'].iloc[0], str):
        df['helpful'] = df['helpful'].apply(ast.literal_eval)
    
    df['helpful_pos'] = df['helpful'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else 0)
    df['helpful_total'] = df['helpful'].apply(lambda x: x[1] if isinstance(x, list) and len(x) > 1 else 0)
    
    grouped = df.groupby(['reviewerID', 'reviewerName']).agg(
        positive_interactions=('helpful_pos', 'sum'),
        total_interactions=('helpful_total', 'sum')
    ).reset_index()
    
    if grouped.empty:
        return []
    
    max_votes = grouped['total_interactions'].max()
    min_votes = grouped['total_interactions'].min()
    dynamic_min_votes = (max_votes + min_votes) / 2
    
    filtered = grouped[grouped['total_interactions'] >= dynamic_min_votes].copy()
    
    filtered['notation'] = round(filtered['positive_interactions'] / filtered['total_interactions'].replace(0, 1), 2)
    
    top_df = filtered.sort_values(
        by=['notation', 'positive_interactions'], 
        ascending=False
    ).head(top_n)
    
    result_list = top_df[[
        'reviewerID', 
        'reviewerName', 
        'notation', 
        'total_interactions', 
        'positive_interactions'
    ]].to_dict(orient='records')
    
    return result_list

def get_top_rated_products_dynamic(df, top_n=10):
    """
    Retorna os melhores produtos com pesos de helpful, suavização Bayesiana 
    e limiar mínimo de reviews calculado dinamicamente (média entre o max e min de reviews por produto).
    """
    
    if not df.empty and isinstance(df['helpful'].iloc[0], str):
        df['helpful'] = df['helpful'].apply(ast.literal_eval)
        
    df['helpful_pos'] = df['helpful'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else 0)
    df['helpful_total'] = df['helpful'].apply(lambda x: x[1] if isinstance(x, list) and len(x) > 1 else 0)
    
    # 3. Calcula o peso de cada review (dando menos peso para [0,0])
    def calculate_review_weight(row):
        pos = row['helpful_pos']
        total = row['helpful_total']
        
        if total == 0:
            return 0.5  # Peso menor para [0,0]
        
        rate = pos / total
        weight = (pos * 2) + (total * rate) + 1.0
        return weight

    df['review_weight'] = df.apply(calculate_review_weight, axis=1)
    df['weighted_score'] = df['overall'] * df['review_weight']
    
    grouped = df.groupby('asin').agg(
        total_reviews=('overall', 'count'),
        sum_weighted_score=('weighted_score', 'sum'),
        sum_weights=('review_weight', 'sum'),
        raw_average_overall=('overall', 'mean')
    ).reset_index()
    
    if grouped.empty:
        return []
    
    max_reviews = grouped['total_reviews'].max()
    min_reviews = grouped['total_reviews'].min()
    dynamic_min_product_reviews = (max_reviews + min_reviews) / 2
    
    filtered = grouped[grouped['total_reviews'] >= dynamic_min_product_reviews].copy()
    
    if filtered.empty:
        median_reviews = grouped['total_reviews'].median()
        filtered = grouped[grouped['total_reviews'] >= median_reviews].copy()
        
    if filtered.empty:
        return []

    C = filtered['raw_average_overall'].mean()
    m = max(3, int(filtered['total_reviews'].median()))
    
    filtered['weighted_rating'] = filtered['sum_weighted_score'] / filtered['sum_weights'].replace(0, 1)
    
    filtered['bayesian_final_rating'] = (
        (filtered['total_reviews'] / (filtered['total_reviews'] + m)) * filtered['weighted_rating'] +
        (m / (filtered['total_reviews'] + m)) * C
    )
    
    top_products = filtered.sort_values(
        by=['bayesian_final_rating', 'total_reviews'], 
        ascending=False
    ).head(top_n)
    
    top_products['bayesian_final_rating'] = round(top_products['bayesian_final_rating'],2)
    top_products['raw_average_overall'] = round(top_products['raw_average_overall'],2)
    
    # 8. Retorna para a API
    result_list = top_products[[
        'asin', 
        'total_reviews', 
        'raw_average_overall',
        'bayesian_final_rating'
    ]].to_dict(orient='records')
    
    return result_list

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

SAVE_PATH = BASE_DIR / "processed"
SAVE_PATH.mkdir(parents=True, exist_ok=True)

df_reviews: DataFrame = pd.read_json(f'{(DATA_DIR / 'Cell_Phones_and_Accessories_5.json').as_posix()}', lines=True)

top_reviwers: list[dict()] = get_top_reviewers_json(df=df_reviews, top_n=10)
top_products: list[dict()] = get_top_rated_products_dynamic(df=df_reviews, top_n=10)

response_data = {
    "melhores_produtos": top_products,
    "melhores_avaliadores": top_reviwers
}

file_output_path = SAVE_PATH / 'metrics.json'

with open(file_output_path, 'w', encoding='utf-8') as f:
    json.dump(response_data, f, ensure_ascii=False, indent=4)