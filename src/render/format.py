import json
from typing import List

from helpers import get_asset_path, get_country_name
from models import Comment, CountryData, SentimentScore
import streamlit as st


def get_average_score(data)-> SentimentScore:
    scores = {}

    for value in data:        
        if (value['text'] == '[deleted]'):
            continue


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

            comments_list: List[Comment] = []
            most_liked = None
            most_disliked = None
            most_positive = None
            most_negative = None

            for comment in comments:
                comment = Comment.from_json(comment)

                if (comment.body == '[deleted]'):
                    continue

                comments_list.append(comment)

                if most_liked is None or comment.karma > most_liked.karma:
                    most_liked = comment

                if most_disliked is None or comment.karma < most_disliked.karma:
                    most_disliked = comment

                if most_positive is None or comment.scores.average > most_positive.scores.average:
                    most_positive = comment

                if most_negative is None or comment.scores.average < most_negative.scores.average:
                    most_negative = comment

            result.append(
                CountryData(
                    scores=get_average_score(comments),
                    name=get_country_name(country),
                    code=country,
                    flag=f'https://flagcdn.com/h120/{country}.png',
                    data_count=len(comments),
                    comments=comments_list,
                    most_liked=most_liked,
                    most_disliked=most_disliked,
                    most_positive=most_positive,
                    most_negative=most_negative,
                )
            )

    def sort_by_average(country: CountryData):
        return country.scores.average

    result.sort(key=sort_by_average, reverse=True)

    return result


result = process_country_data(get_asset_path('scored.json'))

st.write(
    """
    # Análise de Sentimento

    Países com maior média de sentimento positivo baseado em comentários e posts de emigrantes brasileiros em comunidades do Reddit.
    """
)

# Inputs
min_data_count = st.number_input(
    "Número mínimo de posts/comentários para exibir o país:",
    min_value=0,
    value=100,
    step=10
)

index = 0

for country in result:
    if country.data_count < min_data_count:
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
            
    with st.expander("Detalhes"):
        st.write(
            f"**Segurança:** {country.scores.safety:.2f}, "
            f"**Cultura:** {country.scores.culture:.2f}, "
            f"**Carreira:** {country.scores.carreer:.2f}, "
            f"**Custo de Vida:** {country.scores.life_cost:.2f}"
        )
        st.write('### Comentários em Destaque')

        def _write_comment(comment: Comment, title: str):
            st.write(f"[**{title}**](https://www.reddit.com{comment.permalink}) (Positividade: {comment.scores.average:.2f}) ({comment.karma})")
            st.write(comment.body)

        _write_comment(country.most_positive, "Mais positivo")
        _write_comment(country.most_negative, "Mais negativo")
        _write_comment(country.most_liked, "Mais curtido")
        _write_comment(country.most_disliked, "Mais descurtido")

    st.write("\n")