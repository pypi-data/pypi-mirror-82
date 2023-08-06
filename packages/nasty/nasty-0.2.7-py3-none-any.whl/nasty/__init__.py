#
# Copyright 2019-2020 Lukas Schmelzeisen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__version__ = "dev"
try:
    from nasty._version import __version__  # type: ignore
except ImportError:
    pass

__version_info__ = tuple(
    (int(part) if part.isdigit() else part)
    for part in __version__.split(".", maxsplit=4)
)


import logging

from nasty.__main__ import main
from nasty.batch.batch import Batch
from nasty.batch.batch_entry import BatchEntry
from nasty.batch.batch_results import BatchResults
from nasty.request.conversation_request import ConversationRequest
from nasty.request.replies import Replies
from nasty.request.request import DEFAULT_BATCH_SIZE, DEFAULT_MAX_TWEETS, Request
from nasty.request.search import DEFAULT_FILTER, Search, SearchFilter
from nasty.request.thread import Thread
from nasty.tweet.conversation_tweet_stream import ConversationTweetStream
from nasty.tweet.tweet import Tweet, TweetId, User, UserId
from nasty.tweet.tweet_stream import TweetStream

__all__ = [
    "main",
    "Batch",
    "BatchEntry",
    "BatchResults",
    "ConversationRequest",
    "Replies",
    "DEFAULT_BATCH_SIZE",
    "DEFAULT_MAX_TWEETS",
    "Request",
    "DEFAULT_FILTER",
    "Search",
    "SearchFilter",
    "Thread",
    "ConversationTweetStream",
    "Tweet",
    "TweetId",
    "User",
    "UserId",
    "TweetStream",
]

# Don't show log messages in applications that don't configure logging.
# See https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger(__name__).addHandler(logging.NullHandler())
