# 11.1 Another feature request

**메타데이터:**
- ID: 104
- 레벨: 2
- 페이지: 249-249
- 페이지 수: 1
- 부모 ID: 102
- 텍스트 길이: 1977 문자

---

ture request 221
database and other web services, representing data, as with immutable data collec-
tions, leads to these benefits:
 Using generic data manipulation functions to manipulate data from multiple
data sources
 Passing data forward freely with no additional complexity
11.1 Another feature request
After having delivered the database milestone on time, Theo calls Nancy to share the good
news. Instead of celebrating Theo’s success, Nancy asks him about the ETA for the next
milestone, Book Information Enrichment with the Open Library Books API. Theo tells her
that he’ll get back to her with an ETA by the end of the day. When Joe arrives at the office,
Theo tells him about the discussion with Nancy.
Theo I just got a phone call from Nancy, and she is stressed about the next milestone.
Joe What’s in the next milestone?
Theo Do you remember the Open Library Books API that I told you about a few
weeks ago?
 NOTE You can find the Open Library Books API at https://openlibrary.org/dev/
docs/api/books.
Joe No.
Theo It’s a web service that provides detailed information about books.
Joe Cool!
Theo Nancy wants to enrich the book search results. Instead of fetching book infor-
mation from the database, we need to retrieve extended book information
from the Open Library Books API.
Joe What kind of book information?
Theo Everything! Number of pages, weight, physical format, topics, etc....
Joe What about the information from the database?
Theo Besides the information about the availability of the books, we don’t need it
anymore.
Joe Have you already looked at the Open Library Books API?
Theo It’s a nightmare! For some books, the information contains dozen of fields,
and for other books, it has only two or three fields.
Joe What’s the problem then?
Theo I have no idea how to represent data that is so sparse and unpredictable.
Joe When we represent data as data, that’s not an issue. Let’s have a coffee and I’ll
show you.

222 CHAPTER 11 Web services