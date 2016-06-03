import yaml

from retrying import retry
from time import sleep
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator


with open("config.yaml") as f:
    auth_configs = yaml.load(f)

auth = Oauth1Authenticator(**auth_configs)

client = Client(auth)

# From https://www.yelp.com/developers/documentation/v2/all_category_list
categories = [
    "chinese",
    "japanese",
    "indpak",
    "greek",
    "french",
    "tradamerican",
    "newamerican",
    "australian",
    "beergarden",
    "brazilian",
    "british",
    "buffets",
    "burmese",
    "diners",
    "dumplings",
    "eastern_european",
    "irish",
    "italian",
    "korean",
    "raw_food",
    "mexican",
    "mideastern",
    "pizza",
    "salad",
    "sushi",
    "seafood",
    "vegetarian",
    "vegan",
    "wraps",
    "pita",
]

params = {
    "category_filter": "",
    "radius_filter": "2500",
    "sort": 2,
}

def max(a,b):
    if a>b:
        return a
    else:
        return b

@retry(wait_fixed=2000, stop_max_attempt_number=3)
def get_data(options):
    return client.search("Restaurants San Francisco", **options)

for category in categories:
    sleep(1)
    params["category_filter"] = category

    result = None
    try:
        result = get_data(params)
    except Exception:
        print "Failed the %s category" % category
        continue

    good_review = [business for business in result.businesses if business.rating >= 4.0]
    sorted_res = sorted(good_review, key=lambda x: x.review_count)

    print " "
    print category, ":"

    ran = range(-1, max(-len(sorted_res), -3)-1, -1)
    for i in ran:
        print "\t", sorted_res[i].name.encode("utf-8"), ":"
        print "\t\tRating:\t", sorted_res[i].rating
        print "\t\tReview count:\t", sorted_res[i].review_count
        print " "
