import redis
from googlesearch import search
from configurations import (REDIS_HOST, REDIS_PORT, GOOGLE_SEARCH_DOMAIN)


def get_redis_connection():
    redis_connection = None
    try:
        redis_connection = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    except redis.ConnectionError:
        print("Could not establish connection with Redis server")

    return redis_connection


def append_query_to_search_history(user_id, query):
    redis_connection = get_redis_connection()
    if redis_connection:
        redis_connection.lpush(user_id, query)
        print("{} added to the searches for the user_id - {}".format(query, user_id))


def get_recent_searches(user_id, query):
    redis_connection = get_redis_connection()
    matched_searches = []
    if redis_connection:
        history_length = redis_connection.llen(user_id)
        recent_searches = redis_connection.lrange(user_id, 0, history_length)

        for term in recent_searches:
            term = term.decode()
            if query in term:
                matched_searches.append(term)

    return matched_searches


def search_on_google(query):
    links = list(search(query, tld=GOOGLE_SEARCH_DOMAIN, num=5, stop=5))

    return links
