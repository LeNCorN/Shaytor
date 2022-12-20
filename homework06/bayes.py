from collections import Counter
from math import log as ln


class NaiveBayesClassifier:
    def __init__(self, for_education):
        self.for_education = for_education
        self.probability_dict = None
        self.p_positive = None
        self.p_negative = None
        self.education()

    def education(self) -> None:
        for_education = self.for_education
        positive_count = Counter(for_education.values())[True]
        negative_count = Counter(for_education.values())[False]
        total_count = positive_count + negative_count
        p_positive = positive_count / total_count
        p_negative = negative_count / total_count

        positive_dict = Counter(
            sum([i for i in (key.split(" ") for key, value in for_education.items() if value)], [])
        )
        negative_dict = Counter(
            sum(
                [i for i in (key.split(" ") for key, value in for_education.items() if not value)],
                [],
            )
        )
        total_dict = {
            i: None for i in sum((key.split(" ") for key in for_education.keys()), [])
        }

        result = {}
        for word in total_dict:
            positive_formula = (positive_dict[word] + 1) / (
                sum(positive_dict.values()) + len(total_dict)
            )
            negative_formula = (negative_dict[word] + 1) / (
                sum(positive_dict.values()) + len(total_dict)
            )
            result[word] = (positive_formula, negative_formula)
        self.probability_dict = result
        self.p_positive = p_positive
        self.p_negative = p_negative
        return None

    def prediction(self, test):
        probability_dict = self.probability_dict
        result = {}
        p_word_host = (ln(self.p_positive), ln(self.p_negative))
        for i in test:
            p_positive_word = p_word_host[0]
            p_negative_word = p_word_host[1]
            for word in i.split(" "):
                try:
                    p_positive_word += ln(probability_dict[word][0])
                    p_negative_word += ln(probability_dict[word][1])
                except KeyError:
                    continue
            if p_positive_word > p_negative_word:
                result[i] = True
            elif p_positive_word < p_negative_word:
                result[i] = False
            else:
                result[i] = None
        return result