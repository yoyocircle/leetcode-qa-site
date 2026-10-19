"""## Task

Support posting tweets, following and unfollowing users, and fetching the ten newest tweets
posted by a user or their current followees.

## Hints

1. Assign each post a monotonically increasing timestamp.
2. A feed is a merge of already time-ordered per-user streams.

## Approach

### Heap merge of user timelines

Append timestamped posts to each user's list. Seed a heap with the newest post of every followed
user plus self, and advance that user's stream after each extraction.

### Scan global timeline

Keep one global append-only post list. Scan it backward and retain posts by self or a current
followee until ten are found.

## Why it works

### Heap merge of user timelines

Each heap entry is the newest unreported tweet from one eligible timeline. Its maximum timestamp
is the global newest available tweet, so ten extractions produce the required feed.

### Scan global timeline

Reverse insertion order is reverse chronological order. Filtering by current visibility
preserves that order, so the first ten retained tweets form exactly the feed.

## Walkthrough

User 1 posts 10, user 2 posts 20, then 1 follows 2. Feed 1 is [20,10]. After unfollowing 2 it
becomes [10].

## Cost and pitfalls

Heap merge of user timelines: O(1) post/follow/unfollow expected; O(f + 10 log(f+1)) feed time;
O(T+F) stored; O(f) query space.
Scan global timeline: O(1) post/follow/unfollow expected; O(T) feed time; O(T+F) space.
Objects own their state; query methods do not mutate caller data. A user always sees their own
posts, even after a self-unfollow. Follow sets suppress duplicate relationships. T is total
tweets and F total follow relations.
"""

from collections import defaultdict
from heapq import heapify, heappop, heappush


class Twitter:
    """Approach: Heap merge of user timelines
    Time: O(1) post/follow/unfollow expected; O(f + 10 log(f+1)) feed
    Space: O(T+F) stored; O(f) query
    """

    def __init__(self):
        self.clock = 0
        self.posts = defaultdict(list)
        self.following = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.posts[userId].append((self.clock, tweetId))
        self.clock += 1

    def getNewsFeed(self, userId: int) -> list[int]:
        heap = []
        for user in self.following.get(userId, set()) | {userId}:
            posts = self.posts.get(user)
            if posts:
                index = len(posts) - 1
                heap.append((-posts[index][0], user, index))
        heapify(heap)
        result = []
        while heap and len(result) < 10:
            _, user, index = heappop(heap)
            result.append(self.posts[user][index][1])
            if index:
                heappush(heap, (-self.posts[user][index - 1][0], user, index - 1))
        return result

    def follow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        followees = self.following.get(followerId)
        if followees is not None:
            followees.discard(followeeId)
            if not followees:
                del self.following[followerId]


class TimelineTwitter:
    """Approach: Scan global timeline
    Time: O(1) post/follow/unfollow expected; O(T) feed
    Space: O(T+F)
    """

    def __init__(self):
        self.timeline = []
        self.following = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.timeline.append((userId, tweetId))

    def getNewsFeed(self, userId: int) -> list[int]:
        visible = self.following.get(userId, set()) | {userId}
        result = []
        for user, tweet in reversed(self.timeline):
            if user in visible:
                result.append(tweet)
                if len(result) == 10:
                    break
        return result

    def follow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        followees = self.following.get(followerId)
        if followees is not None:
            followees.discard(followeeId)
            if not followees:
                del self.following[followerId]
