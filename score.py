import json
from distance import levenshtein

default_not_json_score = 1000000


def is_json(obj):
    try:
        json.loads(obj)
        return True
    except:
        return False


def score_with_ref(obj, ref_obj, not_json_score=default_not_json_score):
    if not (is_json(obj)):
        return not_json_score
    return levenshtein(obj, ref_obj)


def score_without_ref(obj, not_json_score=default_not_json_score):
    if not (is_json(obj)):
        return not_json_score
    formatted_json = json.dumps(json.loads(obj), indent=4)
    return levenshtein(obj, formatted_json)
