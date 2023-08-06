# -*- coding: utf-8 -*-

# Copyright (c) 2014, Joshua Stone
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__all__ = [
  "query"
]

class Query_Field(object):
  def __init__(self, name, is_neg=False):
    self.name = name
    self.is_neg = is_neg

  def __neg__(self):
    return self.__class__(self.name, is_neg=True)

class Equal(Query_Field):
  def __eq__(self, value):
    if value:
      return f"{'-' if self.is_neg else ''}{self.name}:{value}"
    else:
      raise ValueError(value)

  def __gt__(self, value):
    raise AttributeError("gt")

  def __lt__(self, value):
    raise AttributeError("lt")

  def __ge__(self, value):
    raise AttributeError("ge")

  def __le__(self, value):
    raise AttributeError("le")

 
class Comparable(Query_Field):
  def op(self, op, value):
    try:
      float(value)
      return f"{'-' if self.is_neg else ''}{self.name}.{op}:{value}"
    except:
      raise ValueError(value)
 
  def __eq__(self, value):
    return self.op("eq", value)
 
  def __gt__(self, value):
    return self.op("gt", value)
 
  def __lt__(self, value):
    return self.op("lt", value)
 
  def __ge__(self, value):
    return self.op("gte", value)
 
  def __le__(self, value):
    return self.op("lte", value) 


class Query(object):
  def __init__(self):
    for field in self.equal:
      setattr(self, field, Equal(field))

    for field in self.comparable:
      setattr(self, field, Comparable(field))

  def __neg__(self):
    return self.__class__()

  # literal, ngram
  @property
  def equal(self):
    return {"alias_of", "aliased", "aliases", "analyzed_name", "author", "body",
            "category", "description", "faved_by", "forum_id", "gallery_id", "image_ids",
            "implied_by", "implies", "my", "name", "name_in_namespace", "namespace",
            "original_format", "short_description", "slug", "source_url", "subject",
            "orig_sha512_hash", "sha512_hash", "topic_id", "uploader", "watcher_ids"}

  # int, float, date
  @property
  def comparable(self):
    return {"aspect_ratio", "comment_count", "created_at", "downvotes", "faved_by_id",
            "faves", "first_seen_at", "height", "id", "image_count", "image_id",
            "images", "score", "tag_count", "updated_at", "uploader_id", "upvotes",
            "user_id", "watcher_count", "width", "wilson_score"}

  @property
  def images_attr(self):
    return ("aspect_ratio", "comment_count", "created_at", "description", "downvotes",
            "faved_by", "faved_by_id", "faves", "first_seen_at", "gallery_id", "height",
            "id", "my", "source_url", "orig_sha512_hash", "original_format", "score",
            "sha512_hash", "tag_count", "updated_at", "uploader", "uploader_id",
            "upvotes", "width", "wilson_score")

  @property
  def comments_attr(self):
    return ("author", "body", "created_at", "id", "image_id", "my", "user_id")

  @property
  def tags_attr(self):
    return ("alias_of", "aliased", "aliases", "analyzed_name", "category",
            "description", "id", "images", "implied_by", "implies", "name",
            "name_in_namespace", "namespace", "short_description", "slug")

  @property
  def galleries_attr(self):
    return ("created_at", "description", "id", "image_count", "image_ids", "title",
            "updated_at", "user", "watcher_count", "watcher_ids")

  @property
  def posts_attr(self):
    return ("author", "body", "created_at", "forum_id", "id", "my",
            "subject", "topic_id", "updated_at", "user_id")

query = Query()
