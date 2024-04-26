import time
import requests
from cachetools import cached, TTLCache

#handles caching and GitHub API requests

def setup_cache():
    # Create a cache with a time-to-live (TTL) of 60 seconds
    return TTLCache(maxsize=100, ttl=60)

@cached(setup_cache())
def get_github_data(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    
    if response.status_code == 429:  # Rate limit exceeded
        reset_time = int(response.headers['X-RateLimit-Reset'])
        wait_time = reset_time - time.time()
        time.sleep(max(0, wait_time))  # Ensure wait time is non-negative
        return get_github_data(username)  # Retry the request
    elif response.status_code == 200:  # Success
        return response.json()
    else:
        return {"error": f"Failed to fetch data: {response.status_code}"}
