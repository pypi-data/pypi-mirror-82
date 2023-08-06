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

from .request import get_filters, get_filter_data
from .helpers import tags, api_key, join_params, set_limit, validate_filter

__all__ = [
  "Filters",
  "Filter"
]

system_filters = {
  "default": 1,
  "everything": 2,
  "pony": 6,
  "wholesome": 9,
  "eu": 8,
  "not imported": 113,
  "fim species": 113,
}

class Filters(object):
  def __init__(self, q=set(), key="", filters_id="", limit=50, perpage=25, page=1,
               url_domain="https://twibooru.org", proxies={}):
    self.proxies = proxies
    self.url_domain = url_domain
    self._params = {
      "q": tags(q),
      "key": api_key(key),
      "perpage": set_limit(perpage),
      "page": set_limit(page)
    }

    if filters_id not in {"system", "user"}:
      if key:
        filters_id = "user"
      else:
        filters_id = "system"
      
    self._limit = set_limit(limit)
    self._search = get_filters(filters_id, self._params, 
                               self._limit, url_domain=self.url_domain, proxies=self.proxies)
  
  def __iter__(self):
    """
    Make Filters() iterable so that new search results can be lazily generated
    for performance reasons.
    """
    return self

  @property
  def parameters(self):
    """
    Returns a list of available parameters; useful for passing state to new
    instances of Filters().
    """
    return self._params

  @property
  def url(self):
    """
    Returns a standart URL of avaliable filters list
    """
    return f"{self.url_domain}/filters"

  def query(self, *q):
    """
    Takes one or more strings for searching.
    """
    params = join_params(self.parameters, {"q": q,
                                           "limit": self._limit,
                                           "url_domain": self.url_domain,
                                           "proxies": self.proxies}
                        )

    return self.__class__(**params)

  def key(self, key=""):
    """
    Takes a user's API key string which applies content settings. API keys can
    be found at <https://twibooru.org/users/edit>.
    """
    params = join_params(self.parameters, {"key": key,
                                           "limit": self._limit,
                                           "url_domain": self.url_domain,
                                           "proxies": self.proxies}
                        )

    return self.__class__(**params)

  def limit(self, limit):
    """
    Set absolute limit on number of filters to return, or set to None to return
    as many results as needed; default 50 filters. This limit on app-level.
    """
    params = join_params(self.parameters, {"limit": limit,
                                           "url_domain": self.url_domain,
                                           "proxies": self.proxies})

    return self.__class__(**params)

  def get_page(self,page):
    """
    Set page for gets result of search.
    """
    params = join_params(self.parameters, {"page": set_limit(page),
                                           "limit": self._limit,
                                           "url_domain": self.url_domain,
                                           "proxies": self.proxies}
                        )

    return self.__class__(**params)

  def perpage(self,limit):
    """
    Set absolute limit on number of filters to get, or set to None to return
    defaulting 25 posts; max 50 filters. This limit on API-level.
    """
    params = join_params(self.parameters, {"perpage": set_limit(limit),
                                           "limit": self._limit,
                                           "url_domain": self.url_domain,
                                           "proxies": self.proxies}
                        )

    return self.__class__(**params)

  def __next__(self):
    """
    Returns a result wrapped in a new instance of Filter().
    """
    return Filter(None, data=next(self._search), url_domain=self.url_domain, proxies=self.proxies)

class Filter(object):
  """
  This class provides a thin wrapper around JSON data, mapping each value to
  its own property. Once instantiated the data is immutable so as to reflect
  the stateless nature of a REST API.
  """
  def __init__(self, filter_id, data=None, url_domain="https://twibooru.org", proxies={}):
    self.proxies = proxies
    self.url_domain = url_domain

    if filter_id is None and data:
      self._data = data
    else:
      norm_str_filter_id = f"{filter_id}".lower()
      if norm_str_filter_id in system_filters:
        filter_id = system_filters[norm_str_filter_id]
      self._data = data = get_filter_data(validate_filter(filter_id),
                                          url_domain=url_domain, proxies=proxies)

    for field, body in data.items():
      if not hasattr(self, field):
        setattr(self, field, body) 

  def __str__(self):
    return f"Filter({self.name})"

  @property
  def data(self):
    return self._data

  def update(self):
    data = get_image_data(self.id, proxies=self.proxies)

    if data:
      self._data = data