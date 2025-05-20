import json
from typing import List

from helpers import get_asset_path, get_country_name
from models import CountryData, SentimentScore
import streamlit as st


def get_average_score(data)-> SentimentScore:
    scores = {}

    for value in data:        
        for key, item in value['sentiment'].items():

            if key not in scores:
                scores[key] = 0

            scores[key] += item
            
    for key, item in scores.items():
        scores[key] = item / len(data)

    return SentimentScore.from_json(scores)


def process_country_data(file_path: str) -> List[CountryData]:
    result = []

    with open(file_path, 'r') as f:
        data = json.load(f)

        for country, comments in data.items():
            if country == 'None':
                continue

            result.append(
                CountryData(
                    scores=get_average_score(comments),
                    name=get_country_name(country),
                    code=country,
                    flag=f'https://flagcdn.com/h120/{country}.png',
                    data_count=len(comments)
                )
            )

    def sort_by_average(country: CountryData):
        return country.scores.average

    result.sort(key=sort_by_average, reverse=True)

    return result


result = process_country_data(get_asset_path('scored.json'))

st.write(
    """
    # Tema 7: Análise de Sentimento.

    Países com maior média de sentimento positivo baseado em comentários e posts de emigrantes brasileiros
    """
)

# Write Top 10 most positive countries.
st.write(
    """
    ## Países com maior média de sentimento positivo
    """
)

index = 0

for country in result:
    if country.data_count < 100:
        continue

    index += 1
    
    col1, col2, col3, col4, col5 = st.columns([0.5, 1, 2, 1, 2])

    with col1:
        st.write(f"**{index}**")
    with col2:
        st.image(country.flag, width=50)
    with col3:
        st.write(f"{country.name} ({country.code}) ", unsafe_allow_html=True)
    with col4:
        st.write(f"**Média:** {country.scores.average:.2f}")
    with col5:
        st.write(f"**Total:** {country.data_count} posts/comentários")