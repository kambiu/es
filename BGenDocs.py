from elasticsearch import Elasticsearch
from random import randint, uniform
import datetime
import requests
import lxml.html as LH
import lxml.html.clean as clean
import re
import json

es = Elasticsearch(["localhost:9200"])


""" configuration """

grade = ["A+", "A", "B", "C", "D", "F"] #6
courses = ["Economics", "English Language", "Commerce", "French", "Geography",
           "History", "Phsics" , "Religious Studies", "Visual Arts", "Physical Education",
           "Biology"] #11

""" end configuration """


def get_page_text(url):
    ret_text = ""

    print("Url is {}".format(url))
    r = None
    try:
        r = requests.get(url)
    except Exception as e:
        print("Error opening website. Return no content")
        return "No Content"

    content = r.text

    pattern = "<title>(.+)<\/title>"
    titles_match = re.findall(pattern, content)
    ret_text += "title: " + " , ".join(titles_match) + " , "

    cleaner = clean.Cleaner()
    content = cleaner.clean_html(content)

    doc = LH.fromstring(content)

    ignore_tags = ('script', 'noscript', 'style')

    for elt in doc.iterdescendants():
        if elt.tag in ignore_tags: continue
        text = elt.text or ''
        tail = elt.tail or ''
        words = ' '.join((text, tail)).strip()
        if words:
            # words = words.decode('ascii', 'ignore').encode('utf-8')
            ret_text += " " + words

    ret_text = ret_text.replace("\n", " ").replace("\r", " ")

    return ret_text


def get_content(idx, url, x_path):
    print(idx)
    try:
        r = requests.get(url)
    except Exception as e:
        print("Error opening website. Return no content")
        return "No Content"
    fix_html = LH.fromstring(r.text)

    lst_url = []
    for elm_url in fix_html.xpath(x_path):
        lst_url.append(elm_url.get("href"))

    ret_idx = idx % len(lst_url)
    text = get_page_text(lst_url[ret_idx])
    return text


def get_larger_date(posix_time, format):
    time_diff = randint(43200, 15768000) # one day to one year
    new_time = posix_time + time_diff
    return datetime.datetime.utcfromtimestamp(new_time).strftime(format)


def gen_student(num):
    url = "https://www.studentnewsdaily.com/archive/daily-news-article/"
    xpath = "/html/body/div/div/div/p/a[@href]"
    for i in range(num):
        date_random = randint(946684800, 1483228800)

        yield {
            "date_created": date_random,
            "date_modified": get_larger_date(date_random, "%Y-%m-%d %H:%M:%S"),
            "age": randint(12, 20),
            "height": "{0:.2f}".format(uniform(1.5, 1.9)),
            "courses": courses[randint(0, 10)],
            "content": get_content(i, url, xpath),
            "active": randint(0, 1),
            "grade": grade[randint(0, 5)]
        }


def gen_teacher(num):
    url = "http://www.wsj.com/public/page/archive-2017-10-31.html"
    xpath = "/html/body/div/div/div/div/div/ul/li/h2/a[@href]"
    for i in range(num):
        date_random = randint(946684800, 1483228800)
        yield {
            "date_created": date_random,
            "date_modified": get_larger_date(date_random, "%d/%m/%Y %H:%M:%S"),
            "age": randint(25, 60),
            "height": "{0:.2f}".format(uniform(1.5, 1.9)),
            "courses": [courses[randint(0, 10)], courses[randint(0, 10)], courses[randint(0, 10)], courses[randint(0, 10)], courses[randint(0, 10)]],
            "content": get_content(i, url, xpath),
            "active": randint(0, 1)
        }
a = []
for i in range(0,5):
    a.append("{0:.2f}".format(uniform(10, 100)))

def gen_cake(num):
    url = "https://greatist.com/eat/dessert-recipes-for-one"
    xpath = "/html/body/div/div/div/div/article/div/div/h4/a[@href]"
    for i in range(num):
        date_random = randint(946684800, 1483228800)
        yield {
            "date_created": date_random,
            "date_expired": get_larger_date(date_random, "%Y/%m/%d"),
            "price": "{0:.1f}".format(uniform(250, 1000)),
            "weight": ["{0:.2f}".format(uniform(10, 100)) for i in range(0,5)],
            "grade": grade[randint(0, 5)],
            "content": get_content(i, url, xpath),
            "active": randint(0, 1)
        }


def write_file(index, type, data):
    filename = "{}_{}.txt".format(index, type)
    with open(filename, "w") as stream:
        for obj in data:
            stream.write('{"index": {"_index": "' + index + '", "_type": "' + type + '"}}\n')
            stream.write(json.dumps(obj) + "\n")


def main():
    # students = gen_student(108)
    # write_file("school", "student", students)

    # teachers = gen_teacher(152)
    # write_file("school", "staff", teachers)

    cakes = gen_cake(42)
    write_file("backery", "cake", cakes)

    print("Program end")


if __name__ == "__main__":
    main()