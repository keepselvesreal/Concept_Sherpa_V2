# 15.5 Dealing with external data sources

**메타데이터:**
- ID: 144
- 레벨: 2
- 페이지: 357-357
- 페이지 수: 1
- 부모 ID: 138
- 텍스트 길이: 4262 문자

---

h external data sources 329
Dave What is _.every?
Theo It’s a Lodash function that receives a collection and a predicate and returns
true if the predicate returns true for every element of the collection.
Dave Nice!
Dave runs the unit tests and they pass. He then enjoys a sip of his espresso.
Dave Now, am I allowed to trigger the search endpoint with 7 Habit in order to con-
firm that the improved search works as expected?
Theo Of course. It’s only during the multiple iterations of code improvements that I
advise you not to trigger the system from the outside in order to benefit from a
shorter feedback loop. Once you’re done with the debugging and fixing, you
must then test the system from end to end.
Dave triggers the search endpoint with 7 Habit. It returns the details about 7 Habits of
Highly Effective People as expected.
15.5 Dealing with external data sources
Dave Can we also use reproducibility when the code involves fetching data from an
external data source like a database or an external service?
Theo Why not?
Dave The function context might be exactly the same, but the behavior might be dif-
ferent if the function fetches data from a data source that returns a different
response for the same query.
Theo Well, it depends on the data source. Some databases are immutable in the
sense that the same query always returns the same response.
Dave I have never heard about immutable databases.
Theo Sometimes, they are called functional databases or append-only databases.
Dave Never heard about them either. Did you mean read-only databases?
Theo Read-only databases are immutable for sure, but they are not useful for storing
the state of an application.
Dave How could a database be both writable and immutable?
Theo By embracing time.
Dave What does time have to do with immutability?
Theo In an immutable database, a record has an automatically generated timestamp,
and instead of updating a record, we create a new version of it with a new time-
stamp. Moreover, a query always has a time range in addition to the query
parameters.
Dave Why does that guarantee that the same query will always return the same
response?
Theo In an immutable database, queries don’t operate on the database itself. Instead,
they operate on a database snapshot, which never changes. Therefore, queries
with the same parameters are guaranteed to return the same response.

330 CHAPTER 15 Debugging
Dave Are there databases like that for real?
Theo Yes. For instance, the Datomic immutable database is used by some digital
banks.
 NOTE See https://www.datomic.com for more information on the Datomic transac-
tional database.
Dave But most databases don’t provide such a guarantee!
Theo Right, but in practice, when we’re debugging an issue in our local environ-
ment, data usually doesn’t change.
Dave What do you mean?
Theo Take, for instance, Klafim’s database. In theory, between the time you trigger
the search endpoint and the time you replay the search code from the REPL
with the same context, a book might have been borrowed, and its availability
state in the database has changed. This leads to a difference response to the
search query.
Dave Exactly.
Theo But in practice, you are the only one that interacts with the system in your local
environment. Therefore, it should not happen.
Dave I see. Because we are at the Museum of Science, would you allow me an anal-
ogy with science?
Theo Of course!
Dave In a sense, external data sources are like hidden variables in quantum physics.
In theory, they can alter the result of an experiment for no obvious reason. But
in practice, our physical world looks stable at the macro level.
With today’s discussion at an end, Theo searches his bag to find a parcel wrapped with gift
wrap from the museum’s souvenir shop, which he hands to Dave with a smile. Dave opens
the gift to find a T-shirt. On one side there is an Albert Einstein avatar and his famous
quote: “God does not play dice with the universe”; on the other side, an avatar of Alan Kay
and his quote: “The last thing you want to do is to mess with internal state.”
Dave thanks Theo for his gift. Theo can feel a touch of emotion at the back of his
throat. He’s really enjoyed playing the role of mentor with Dave, a rather skilled student.