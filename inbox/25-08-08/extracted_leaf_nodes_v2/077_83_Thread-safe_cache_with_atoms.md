# 8.3 Thread-safe cache with atoms

**메타데이터:**
- ID: 77
- 레벨: 2
- 페이지: 198-199
- 페이지 수: 2
- 부모 ID: 73
- 텍스트 길이: 2562 문자

---

cache with atoms
Joe Are you familiar with the notion of in-memory cache?
Theo You mean memoization?

8.3 Thread-safe cache with atoms 171
Joe Kind of. Imagine that database queries don’t vary too much in your applica-
tion. It makes sense in that case to store the results of previous queries in mem-
ory in order to improve the response time.
Theo Yes, of course!
Joe What data structure would you use to store the in-memory cache?
Theo Probably a string map, where the keys are the queries, and the values are the
results from the database.
TIP It’s quite common to represent an in-memory cache as a string map.
Joe Excellent! Now can you write the code to cache database queries in a thread-
safe way using a lock?
Theo Let me see: I’m going to use an immutable string map. Therefore, I don’t
need to protect read access with a lock. Only the cache update needs to be
protected.
Joe You’re getting the hang of this!
Theo The code should be something like this.
Listing8.6 Thread-safe cache with locks
var mutex = new Mutex();
var cache = {};
function dbAccessCached(query) {
var resultFromCache = _.get(cache, query);
if (resultFromCache != nil) {
return resultFromCache;
}
var result = dbAccess(query);
mutex.lock();
cache = _.set(cache, query, result);
mutex.unlock();
return result;
}
Joe Nice! Now, let me show you how to write the same code using an atom instead
of a lock. Take a look at this code and let me know if it’s clear to you.
Listing8.7 Thread-safe cache with atoms
var cache = new Atom();
cache.set({});
function dbAccessCached(query) {
var resultFromCache = _.get(cache.get(), query);
if (resultFromCache != nil) {
return resultFromCache;
}
var result = dbAccess(query);
cache.swap(function(oldCache) {

172 CHAPTER 8 Advanced concurrency control
return _.set(oldCache, query, result);
});
return result;
}
Theo I don’t understand the function you’re passing to the swap method.
Joe The function passed to swap receives the current value of the cache, which is a
string map, and returns a new version of the string map with an additional key-
value pair.
Theo I see. But something bothers me with the performance of the swap method in
the case of a string map. How does the comparison work? I mean, comparing
two string maps might take some time.
Joe Not if you compare them by reference. As we discussed in the past, when data
is immutable, it is safe to compare by reference, and it’s super fast.
TIP When data is immutable, it is safe (and fast) to compare it by reference.
Theo Cool. So atoms play well with immutable data.
Joe Exactly!