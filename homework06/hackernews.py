import sqlalchemy.exc
from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import get_news


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    label = request.GET.get("label", None)
    id = request.GET.get("id", None)
    row = s.query(News).filter(News.id == id).one()
    row.label = label
    s.add(row)
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    update = get_news("https://news.ycombinator.com/")
    for i in update:
        try:
            s.query(News).filter(News.title == i["title"]).one()
        except sqlalchemy.exc.NoResultFound:
            s.add(News(**i))
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    redirect("/recommendations")


@route("/recommendations")
def recommendations():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    already_classified_news = s.query(News).filter(News.label != None).all()
    already_dict: dict[str, bool] = dict()
    rows_list = []
    for row in already_classified_news:
        host_label: bool = True if row.label == "good" else None
        host_label: bool = False if row.label == "never" else host_label
        host: dict = {row.title: host_label}
        already_dict.update(host)
    for row in rows:
        rows_list.append(row.title)
    Bayes = NaiveBayesClassifier(already_dict)
    predicted = Bayes.prediction(rows_list)
    for news in predicted:
        s.query(News).filter(News.title == news).one().label = predicted[news]
    s.commit()
    classified_news = s.query(News).filter(News.label == "good").all()
    return template("news_template", rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)