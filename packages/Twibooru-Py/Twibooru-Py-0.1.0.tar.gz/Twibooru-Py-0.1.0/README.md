# Twibooru-Py

Python bindings for Twibooru's API

License: **Simplified BSD License**

Version: **0.1.0**

## Features

- High-level abstraction over Twibooru's REST API
- Parameter chaining for ease of manipulation
- Syntactic sugar for queries, e.g., "query.score >= 100" compiling to "score.gte:100"
- Design focusing on iterables and lazy generation for network efficiency

## Dependencies

- python3.6 or newer
- requests

## How to install

### Python 3.x

    $ pip3 install twibooru-py
 
## Checking documentation

### Python 3.x

    $ pydoc3 twibooru

## Typical usage

### Getting images currently on Twibooru's front page

```python
from twibooru import Search

for image in Search():
  id_number, score, tags = image.id, image.score, ", ".join(image.tags)
  print("#{} - score: {:>3} - {}".format(id_number, score, tags))
```

### Searching posts by tag

```python
from twibooru import Search

for image in Search().query("rarity", "twilight sparkle"):
  print(image.url)
```

### Getting images from other booru

```python
from twibooru import Search

for image in Search(url_domain='https:\\your.booru.example').query("rarity", "twilight sparkle"):
  print(image.url)
```

### Crawling Twibooru from first to last post

```python
from twibooru import Search

# This is only an example and shouldn't be used in practice as it abuses
# Twibooru's licensing terms
for image in Search().ascending().limit(None):
  id_number, score, tags = image.id, image.score, ", ".join(image.tags)
  print("#{} - score: {:>3} - {}".format(id_number, score, tags))
```

### Getting random posts

```python
from twibooru import Search, sort

for post in Search().sort_by(sort.RANDOM):
  print(post.url)
```

### Getting top 100 posts
```python
from twibooru import Search, sort

top_scoring = [post for post in Search().sort_by(sort.SCORE).limit(100)]
```

### Storing and passing new search parameters

```python
from twibooru import Search, sort

params = Search().sort_by(sort.SCORE).limit(100).parameters

top_scoring = Search(**params)
top_animated = top_scoring.query("animated")
```

### Filtering by metadata

```python
from twibooru import Search, query

q = {
  "wallpaper",
  query.width == 1920,
  query.height == 1080,
  query.score >= 100
}

wallpapers = [image for image in Search().query(*q)]
```
### Getting the latest images from a watchlist

```python

from twibooru import Search, user

key = "your_api_key"

for post in Search().key(key).watched(user.ONLY):
  id_number, score, tags = post.id, post.score, ", ".join(post.tags)
  print("#{} - score: {:>3} - {}".format(id_number, score, tags))
```

### Getting Image data by id:
```python
  i_want_ponies_ponified = Image(None,image_id=2)
  print(i_want_ponies_ponified.url)
```

### Posting images:
```python
  new_img = PostImage().key(API_KEY).image_url("https://pbs.twimg.com/media/EW4YtdmWAAEPaae.png:orig").description(description).tag_input("safe", "artist:dilarus", "ts", "pp").source_url("https://twitter.com/Dilarus/status/1255968549052583941")
  posted_img = new_img.post()
  id_number, score, tags = posted_img.id, posted_img.score, ", ".join(posted_img.tags)
```