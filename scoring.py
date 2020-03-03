import json
from logzero import logger
from jinja2 import Template

# The maximum number of scores to show on the scoreboard
scoreboard_limit = 30


def load_scores():
    logger.debug("Loading scores...")
    score_file = "scores.json"
    try:
        with open(score_file) as in_file:
            text = in_file.read()
        scores = json.loads(text)
        return scores
    except FileNotFoundError:
        return []


def get_sorted_scores():
    scores = load_scores()

    # sort by score highest to lowest
    # and then sort by time lowest to highest
    scores.sort(key=lambda x: (-x["score"], x["time"]))
    return scores


def generate_web_page():
    logger.debug("Generating score web page...")
    # import webpage
    with open("skeleton.jinja2") as in_file:
        template = Template(in_file.read())

    scores = get_sorted_scores()[:scoreboard_limit]
    score_page = template.render(scores=scores)

    # save webpage
    with open("scoring_report.html", "w") as out_file:
        out_file.write(score_page)


def save_scores(new_scores):
    logger.debug("Saving scores...")
    score_file = "scores.json"
    text = json.dumps(new_scores)
    with open(score_file, "w") as out_file:
        out_file.write(text)
    generate_web_page()


def add_score(name, score, time, school):
    logger.debug("Adding score {} FROM {} - {} in {}s".format(name, school,
                                                              score, time))
    new_score = {
            "name": name,
            "score": score,
            "time": time,
            "school": school
        }
    current_scores = load_scores()
    current_scores.append(new_score)
    save_scores(current_scores)


if __name__ == "__main__":
    generate_web_page()
