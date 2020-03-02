import json


def load_scores():
    score_file = "scores.json"
    with open(score_file) as in_file:
        text = in_file.read()
    scores = json.loads(text)
    return scores


def save_scores(new_scores):
    score_file = "scores.json"
    text = json.dumps(new_scores)
    with open(score_file, "w") as out_file:
        out_file.write(text)


def add_score(name, score, time, school):
    new_score = [name, score, time, school]
    current_scores = load_scores()
    current_scores.append(new_score)
    save_scores(current_scores)


def get_sorted_scores():
    scores = load_scores()

    # sort by score highest to lowest
    # and then sort by time lowest to highest
    scores.sort(key=lambda x: (-x[1], x[2]))
    return scores


def generate_web_page():
    # import webpage
    with open("skeleton.html") as in_file:
        web_page = in_file.read()

    scores = get_sorted_scores()
    row_format = "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>"
    table = ""
    for user in scores:
        text_score = row_format.format(*user)
        table += text_score

    score_page = web_page.format(table)

    # save webpage
    with open("scoring_report.html", "w") as out_file:
        out_file.write(score_page)


if __name__ == "__main__":
    add_score("Ambruh", 50, 34, "The Chad")
    generate_web_page()
