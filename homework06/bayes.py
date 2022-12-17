from collections import Counter
from math import log as ln


class NaiveBayesClassifier:
    def __init__(self, for_education: dict[str, bool]) -> None:
        self.for_education: dict[str, bool] = for_education
        self.probability_dict = None
        self.p_positive = None
        self.p_negative = None
        self.education()

    def education(self) -> None:
        for_education: dict[str, bool] = self.for_education
        positive_count: int = Counter(for_education.values())['good']
        negative_count: int = Counter(for_education.values())['never']
        total_count: int = positive_count + negative_count
        p_positive: float = positive_count / total_count
        p_negative: float = negative_count / total_count

        positive_dict: dict = Counter(
            sum([i for i in (key.split(" ") for key, value in for_education.items() if value)], [])
        )
        negative_dict: dict = Counter(
            sum(
                [i for i in (key.split(" ") for key, value in for_education.items() if not value)],
                [],
            )
        )
        total_dict: dict = {
            i: None for i in sum((key.split(" ") for key in for_education.keys()), [])
        }

        result: dict[str, tuple[float, float]] = {}
        for word in total_dict:
            positive_formula: float = (positive_dict[word] + 1) / (
                sum(positive_dict.values()) + len(total_dict)
            )
            negative_formula: float = (negative_dict[word] + 1) / (
                sum(positive_dict.values()) + len(total_dict)
            )
            result[word] = (positive_formula, negative_formula)
        self.probability_dict = result
        self.p_positive = p_positive
        self.p_negative = p_negative
        return None

    def prediction(self, test: list[str]) -> dict[str, bool]:
        probability_dict: dict[str, tuple[float, float]] = self.probability_dict
        result: dict[str, bool or int] = {}
        p_word_host: tuple[float, float] = (ln(self.p_positive), ln(self.p_negative))
        for i in test:
            p_positive_word: float = p_word_host[0]
            p_negative_word: float = p_word_host[1]
            for word in i.split(" "):
                try:
                    p_positive_word += ln(probability_dict[word][0])
                    p_negative_word += ln(probability_dict[word][1])
                except KeyError:
                    continue
            if p_positive_word > p_negative_word:
                result[i] = 'good'
            elif p_positive_word < p_negative_word:
                result[i] = 'never'
            else:
                result[i] = None
        return result