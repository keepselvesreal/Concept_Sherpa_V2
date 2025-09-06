# Appendix B Introduction

**Level:** 1
**페이지 범위:** 392 - 393
**총 페이지 수:** 2
**ID:** 175

---

=== 페이지 392 ===
appendix B
Generic data access in
statically-typed languages
Representing data with generic data structures fits naturally in dynamically-typed
programming languages like JavaScript, Ruby, or Python. However, in statically-
typed programming languages like Java or C#, representing data as string maps
with values of an unspecified type is not natural for several reasons:
 Accessing map fields requires a type cast.
 Map field names are not validated at compile time.
 Autocompletion and other convenient IDE features are not available.
This appendix explores various ways to improve access to generic data in statically-
typed languages. We’ll look at:
 Value getters for maps to avoid type casting when accessing map fields
 Typed getters for maps to benefit from compile-time checks for map field
names
 Generic access for classes using reflection to benefit from autocompletion
and other convenient IDE features
B.1 Dynamic getters for string maps
Let’s start with a refresher about the approach we presented in part 1. Namely, we
represented records as string maps and accessed map fields with dynamic getters
and type casting.
 NOTE Most of the code snippets in this appendix use Java, but the approaches
illustrated can be applied to other object-oriented statically-typed languages like C#
or Go.
364

=== 페이지 393 ===
B.1 Dynamic getters for string maps 365
B.1.1 Accessing non-nested map fields with dynamic getters
Throughout this appendix, we will illustrate various ways to provide generic data access
using a book record. Our record is made of these parts:
 title (a string)
 isbn (a string)
 publicationYear (an integer)
Listing B.1 shows the representation of two books, Watchmen and Seven Habits of Highly
Effective People, in Java. These string maps contain values that are of type Object.
ListingB.1 Two books represented as maps
Map watchmenMap = Map.of(
"isbn", "978-1779501127",
"title", "Watchmen",
"publicationYear", 1987
);
Map sevenHabitsMap = Map.of(
"isbn", "978-1982137274",
"title", "7 Habits of Highly Effective People",
"publicationYear", 2020
);
The map fields can be accessed generically using a dynamic getter. The following list-
ing shows the implementation.
ListingB.2 The implementation of dynamic getter for map fields
class DynamicAccess {
static Object get(Map m, String k) {
return (m).get(k);
}
}
The drawback of dynamic getters is that a type cast is required to manipulate the value
of a map field. For instance, as shown in listing B.3, a cast to String is needed to call
the toUpperCase string method on the title field value.
ListingB.3 Accessing map fields with a dynamic getter and type casting
((String)DynamicAccess.get(watchmenMap, "title")).toUpperCase();
// → "WATCHMEN"
Dynamic getters provide generic data access in the sense that they do not require spe-
cific knowledge of the type of data the string map represents. As a consequence, the
name of the field can be received dynamically (e.g., from the user) as listing B.4
shows. This works because, in order to access a book data field in a string map, it is not
necessary to import the class that defines the book.
