# 1.2.3 Not trivial data serialization

**ID**: 14  
**Level**: 3  
**추출 시간**: 2025-08-09 10:09:52 KST

---

1.2.3 Not trivial data serialization
Theo is really tired, and he falls asleep at his desk. He’s having dream. In his dream, Nancy
asks him to make Klafim’s Library Management System accessible via a REST API using
JSON as a transport layer. Theo has to implement a /search endpoint that receives a
query in JSON format and returns the results in JSON format. Listing 1.3 shows an input
example of the /search endpoint, and listing 1.4 shows an output example of the /search
endpoint.
Listing1.3 A JSON input of the /search endpoint
{
"searchCriteria": "author",
"query": "albert"
}
Listing1.4 A JSON output of the /search endpoint
[
{
"title": "The world as I see it",
"authors": [
{
"fullName": "Albert Einstein"
}
]
},
{
"title": "The Stranger",
"authors": [
{
"fullName": "Albert Camus"
}
]
}
]

## 페이지 47

1.2 Sources of complexity 19
Theo would probably implement the /search endpoint by creating three classes simi-
larly to what is shown in the following list and in figure 1.14. (Not surprisingly, every-
thing in OOP has to be wrapped in a class. Right?)
 SearchController is responsible for handling the query.
 SearchQuery converts the JSON query string into data.
 SearchResult converts the search result data into a JSON string.
C SearchController
String handle(searchQuery: String)
C SearchQuery
C SearchResult
C Catalog
searchCriteria: String
SearchResult(books: List<Book>)
List<Book> search(searchCriteria, queryStr) query: String
String toJSON()
SearchQuery(jsonString: String)
* *
C Book
id : String
title : String
Figure 1.14 The class diagram for SearchController
The SearchController (see figure 1.14) would have a single handle method with the
following flow:
 Creates a SearchQuery object from the JSON query string.
 Retrieves searchCriteria and queryStr from the SearchQuery object.
 Calls the search method of the catalog:Catalog with searchCriteria and
queryStr and receives books:List<Book>.
 Creates a SearchResult object with books.
 Converts the SearchResult object to a JSON string.
What about other endpoints, for instance, those allowing librarians to add book items
through /add-book-item? Theo would have to repeat the exact same process and cre-
ate three classes:
 AddBookItemController to handle the query
 BookItemQuery to convert the JSON query string into data
 BookItemResult to convert the search result data into a JSON string
The code that deals with JSON deserialization that Theo wrote previously in Search-
Query would have to be rewritten in BookItemQuery. Same thing for the code that
deals with JSON serialization he wrote previously in SearchResult; it would have to be
rewritten in BookItemResult.

## 페이지 48

20 CHAPTER 1 Complexity of object-orientedprogramming
The bad news is that Theo would have to repeat the same process for every end-
point of the system. Each time he encounters a new kind of JSON input or output,
he would have to create a new class and write code. Theo’s dream is turning into a
nightmare!
Suddenly, his phone rings, next to where he was resting his head on the desk. As Theo
wakes up, he realizes that Nancy never asked for JSON. It was all a dream...a really bad
dream!
TIP In OOP, data serialization is difficult.
It’s quite frustrating that handling JSON serialization and deserialization in OOP
requires the addition of so many classes and writing so much code—again and again!
The frustration grows when you consider that serializing a search query, a book item
query, or any query is quite similar. It comes down to
 Going over data fields.
 Concatenating the name of the data fields and the value of the data fields, sepa-
rated by a comma.
Why is such a simple thing so hard to achieve in OOP? In OOP, data has to follow a
rigid shape defined in classes, which means that data is locked in members. There is
no simple way to access data generically.
TIP In OOP, data is locked in classes as members.
We will refine later what we mean by generic access to the data, and we will see how
DOP provides a generic way to handle JSON serialization and deserialization. Until
then, you will have to continue suffering. But at least you are starting to become aware
of this suffering, and you know that it is avoidable.
 NOTE Most OOP programming languages alleviate a bit of the difficulty involved
in the conversion from and to JSON. It either involves reflection, which is definitely a
complex thing, or code verbosity.
