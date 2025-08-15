"""
생성 시간: 2025-08-10 22:28:30 KST
핵심 내용: 스키마 유연성과 엄격성 (7.3절) - 옵션 필드와 추가 속성 제어
상세 내용:
    - 검색 응답 예제 (344-371행): 두 권의 책 정보를 포함한 검색 응답 구조
    - 필드 옵션/필수 구분 (372-404행): title, available 필드는 필수, 나머지는 옵션
    - 스키마 리팩터링 (405-441행): bookInfoSchema 분리를 통한 가독성 개선
    - 데이터베이스 응답 스키마 (442-478행): 필수 필드만 포함하는 간단한 구조
    - additionalProperties 설정 (479-541행): 스키마에 명시되지 않은 추가 속성 허용/불허 제어
    - robustness principle (532-541행): 보내는 데이터는 엄격하게, 받는 데이터는 유연하게
상태: 활성
주소: chapter7_03_schema_flexibility_strictness
참조: 원본 파일 /home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md  
"""

# 7.3 Schema flexibility and strictness

7.3 Schema flexibility and strictness
Joe Can you give me an example of what a book search response would look like?
Theo Take a look at this example. It's a search response with information about two
books: 7 Habits of Highly Effective People and The Power of Habit.
Listing7.10 An example of a search response
[
{
"title": "7 Habits of Highly Effective People",
"available": true,
"isbn": "978-0812981605",
"subtitle": "Powerful Lessons in Personal Change",
"number_of_pages": 432
},

=== 페이지 178 ===
150 CHAPTER 7 Basic data validation
{
"title": "The Power of Habit",
"available": false,
"isbn_13": "978-1982137274",
"subtitle": "Why We Do What We Do in Life and Business",
"subjects": [
"Social aspects",
"Habit",
"Change (Psychology)"
]
}
]
Joe It's funny that you mention The Power of Habit. I'm reading this book in order
to get rid of my habit of biting my nails. Anyway, what fields are required and
what fields are optional in a book search response?
Theo In book information, the title and available fields are required. The other
fields are optional.
Joe As I told you when we built the schema for the book search request, fields in a
map are optional by default. In order to make a field mandatory, we have to
include it in the required array. I'd probably implement it with something
like this.
Listing7.11 Schema of a search response
var searchBooksResponseSchema = {
"type": "array",
"items": {
"type": "object",
"required": ["title", "available"],
"properties": {
"title": {"type": "string"},
"available": {"type": "boolean"},
"subtitle": {"type": "string"},
"number_of_pages": {"type": "integer"},
"subjects": {
"type": "array",
"items": {"type": "string"}
},
"isbn": {"type": "string"},
"isbn_13": {"type": "string"}
}
}
};
TIP In JSON Schema, map fields are optional by default.
Theo I must admit that specifying a list of required fields is much simpler than hav-
ing to specify that a member in a class in nullable!
Joe Agreed!
Theo On the other hand, I find the nesting of the book information schema in the
search response schema a bit hard to read.

=== 페이지 179 ===
7.3 Schema flexibility and strictness 151
Joe Nothing prevents you from separating the book information schema from the
search response schema.
Theo How?
Joe It's just JSON, my friend. It means, you are free to manipulate the schema as
any other map in your program. For instance, you could have the book infor-
mation schema in a variable named bookInfoSchema and use it in the search
books response schema. Let me refactor the schema to show you what I mean.
Listing7.12 Schema of a search response refactored
var bookInfoSchema = {
"type": "object",
"required": ["title", "available"],
"properties": {
"title": {"type": "string"},
"available": {"type": "boolean"},
"subtitle": {"type": "string"},
"number_of_pages": {"type": "integer"},
"subjects": {
"type": "array",
"items": {"type": "string"}
},
"isbn": {"type": "string"},
"isbn_13": {"type": "string"}
}
};
var searchBooksResponseSchema = {
"type": "array",
"items": bookInfoSchema
};
Theo Once again, I have to admit that JSON Schemas are more composable than
class definitions.
TIP JSON Schemas are just maps. We are free to compose and manipulate them like
any other map.
Joe Let's move on to validating data received from external data sources.
Theo Is that different?
Joe Not really, but I'll take it as an opportunity to show you some other features of
JSON Schema.
Theo I'm curious to learn how data validation is used when we access data from the
database.
Joe Each time we access data from the outside, it's a good practice to validate it.
Can you show me an example of how a database response for a search query
would look?
TIP It's a good practice to validate data that comes from an external data source.

=== 페이지 180 ===
152 CHAPTER 7 Basic data validation
Theo When we query books from the database, we expect to receive an array of
books with three fields: title, isbn, and available. The first two values should
be strings, and the third one should be a Boolean.
Joe Are those fields optional or required?
Theo What do you mean?
Joe Could there be books for which some of the fields are not defined?
Theo No.
Joe In that case, the schema is quite simple. Would you like to try writing the
schema for the database response?
Theo Let me see. It's an array of objects where each object has three properties, so
something like this?
Listing7.13 Schema of a database response
{
"type": "array",
"items": {
"type": "object",
"required": ["title", "isbn", "available"],
"properties": {
"title": {"type": "string"},
"available": {"type": "boolean"},
"isbn": {"type": "string"}
}
}
}
Joe Well done, my friend! Now, I want to tell you about the additionalProperties
field in JSON Schema.
Theo What's that?
Joe Take a look at this array.
Listing7.14 A book array with an additional property
[
{
"title": "7 Habits of Highly Effective People",
"available": true,
"isbn": "978-0812981605",
"dummy_property": 42
},
{
"title": "The Power of Habit",
"available": false,
"isbn": "978-1982137274",
"dummy_property": 45
}
]

=== 페이지 181 ===
7.3 Schema flexibility and strictness 153
Joe Is it a valid database response?
Theo No. A database response should not have a dummy_property field. It should
have only the three required fields specified in the schema.
Joe It might be surprising but, by default, fields not specified in the schema of an
object are allowed in JSON Schema. In order to disallow them, one has to set
additionalProperties to false like this.
Listing7.15 Disallowing properties not mentioned in the schema
var booksFromDBSchema = {
"type": "array",
"items": {
"type": "object",
"required": ["title", "isbn", "available"],
"additionalProperties": false,
"properties": {
"title": {"type": "string"},
"available": {"type": "boolean"},
"isbn": {"type": "string"}
}
}
};
TIP In JSON Schema, by default, fields not specified in the schema of a map are
allowed.
Theo Why is that?
Joe The reason is that usually having additional fields in a map doesn't cause
trouble. If your code doesn't care about a field, it simply ignores it. But some-
times we want to be as strict as possible, and we set additionalProperties
to false.
Theo What about the search request and response schema from the previous discus-
sions? Should we set additionalProperties to false?
Joe That's an excellent question. I'd say it's a matter of taste. Personally, I like to
allow additional fields in requests and disallow them in responses.
Theo What's the advantage?
Joe Well, the web server is responsible for the responses it sends to its clients. It
makes sense then to be as strict as possible. However, the requests are created
by the clients, and I prefer to do my best to serve my clients even when they are
not as strict as they should be.
Theo Naturally. "The client is always right."
Joe Actually, I prefer the way Jon Postel formulated his robustness principle: "Be
conservative in what you send, be liberal in what you accept."
TIP It's a good practice to be strict with the data that you send and to be flexible with
the data that you receive.

=== 페이지 182 ===
154 CHAPTER 7 Basic data validation