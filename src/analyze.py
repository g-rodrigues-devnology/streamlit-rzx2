import os
import json
from transformers import pipeline, AutoTokenizer

base_path = os.path.join(os.path.dirname(__file__), '..', 'assets')

tokenizer = AutoTokenizer.from_pretrained("tabularisai/multilingual-sentiment-analysis")
model = "tabularisai/multilingual-sentiment-analysis"

# Pipeline com truncation e padding
sentiment = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer,
    truncation=True,
    padding="max_length",
    max_length=512,
    return_all_scores=True
)


def load_spellings_map(langs):
    spellings_map = {}

    for lang in langs:
        with open(os.path.join(base_path, f'countries-{lang}.json'), 'r') as file:
            data = json.load(file)
            
            for c in data:
                code = c['alpha2']

                if code not in spellings_map:
                    spellings_map[code] = [
                        c['name'],
                    ]
                else:
                    spellings_map[code].append(c['name'])

    # A gente coloca o Brazil por último pq ele aparece com frequência por 
    # ser a base de comparação usada em vários comentários, porém nós só
    # queremos que o país seja reconhecido como Brasil caso seja a 
    # única menção ao país no comentário.
    if 'br' in spellings_map:
        brazil_names = spellings_map.pop('br')
        spellings_map['br'] = brazil_names

    return spellings_map

spell_map = load_spellings_map(['en', 'pt'])

params = ["Segurança", "Cultura", "Carreira", "Custo de Vida"]

# Mapeamento de labels para valores numéricos
_label_map = {
    "Very Negative": -2,
    "Negative":      -1,
    "Neutral":        0,
    "Positive":       1,
    "Very Positive":  2,
}

def collect_sentiment(text: str):
    aspect_scores = {}
    total = 0.0
    count = 0
    

    for param in params:
        out_all = sentiment(f"{param}: {text}")[0] 
        weighted_sum = sum(_label_map[d['label']] * d['score'] for d in out_all)
        aspect_scores[param] = weighted_sum

        total += weighted_sum
        count += 1

    aspect_scores['Geral'] = (total / count) if count else 0.0
    print(aspect_scores)
    return aspect_scores

def find_country(text: str):
    text = text.lower()
    for code, names in spell_map.items():
        for name in names:
            if name.lower() in text:
                return code

    return None

def analyze_text(comment: str, score_map: map, country: str | None, score, permalink, user):
    code = find_country(comment)

    if (code is None and country is None):
        code = 'None'

    sentiment_scores = collect_sentiment(comment)

    key = code if code else country

    print(f'related country is {key}')

    if key not in score_map:
        score_map[key] = []

    score_map[key].append({
        'text': comment,
        'score': score,
        'country': key,
        'permalink': permalink,
        'user': user,
        'sentiment': sentiment_scores,
    })

    return key

def analyze_comment(comment, score_map: map, country: str | None):
    key = analyze_text(comment['body'], score_map, country, comment['score'], comment['permalink'], comment['author'])

    if ('replies' in comment):
        for reply in comment['replies']:
            analyze_comment(reply, score_map, key)    


def analyze_data():
    with open(os.path.join(base_path, 'data.json'), 'r') as f:
        data = json.load(f)
        score_map = {}
        count = 0
        length = len(data)

        for post in data:
            print(f'Analyzing post {count + 1} of {length}')

            full_text = f'{post["title"]} {post["selftext"]}'
            country = find_country(full_text)

            analyze_text(full_text, score_map, country, post['score'], post['permalink'], post['author'])
            
            if ('comments' in post):
                c_count = 0
                c_length = len(post['comments']) 

                for comment in post['comments']:
                    print(f'Analyzing comment {c_count + 1} of {c_length}')
                    analyze_comment(comment, score_map, country)
                    c_count += 1
            
            count += 1
        
        return score_map
    
full_data = analyze_data()

output_path = os.path.join(base_path, 'scored.json')

with open(output_path, 'w') as outfile:
    json.dump(full_data, outfile, indent=4, ensure_ascii=False)
