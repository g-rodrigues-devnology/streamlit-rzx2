from dataclasses import dataclass


@dataclass
class SentimentScore:
    safety: float
    culture: float
    carreer: float
    life_cost: float
    average: float

    @staticmethod
    def from_json(data: dict) -> 'SentimentScore':
        return SentimentScore(
            safety=data['Segurança'],
            culture=data['Cultura'],
            carreer=data['Carreira'],
            life_cost=data['Custo de Vida'],
            average=data['Geral']
        )

@dataclass
class Comment:
    permalink: str
    karma: float
    scores: SentimentScore
    body: str

    @staticmethod
    def from_json(data: dict) -> 'Comment':
        return Comment(
            permalink=data['permalink'],
            karma=data['score'],
            scores=SentimentScore.from_json(data['sentiment']),
            body=data['text']
        )

@dataclass
class CountryData:
    scores: SentimentScore
    name: str
    code: str
    flag: str
    data_count: int
    comments: list[Comment]

    most_disliked: Comment | None = None
    most_liked: Comment | None = None
    most_positive: Comment | None = None
    most_negative: Comment | None = None

    def __str__(self) -> str:
        return (
            f"Country: {self.name} ({self.code})\n"
            f"Flag: {self.flag}\n"
            f"Data Count: {self.data_count}\n"
            f"Scores:\n"
            f"  Safety: {self.scores.safety}\n"
            f"  Culture: {self.scores.culture}\n"
            f"  Career: {self.scores.carreer}\n"
            f"  Life Cost: {self.scores.life_cost}\n"
            f"  Average: {self.scores.average}"
        )