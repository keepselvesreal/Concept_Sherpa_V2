# 9.3.0 Introduction (사용자 추가)

On their way back to the office, Theo and Joe don’t talk too much. Theo’s thoughts take
him back to what he learned in the university classroom. He feels a lot of respect for Phil
Bagwell, who discovered how to manipulate persistent data structures efficiently, and for
Rich Hickey, who created a programming language incorporating that discovery as a core
feature and making it available to the world. Immediately after lunch, Theo asks Joe to
show him what it looks like to manipulate persistent data structures for real in a program-
ming language.
Theo Are persistent data structures available in all programming languages?
Joe A few programming languages like Clojure, Scala, and C# provide them as part
of the language. In most programming languages, though, you need a third-
party library.
Theo Could you give me a few references?
Joe Sure.
Using Theo’s laptop, Joe bookmarks some sites. He knows exactly which URLs to look for.
Then, while Theo is looking over the bookmarked sites, Joe goes to the whiteboard and
jots down the specific libraries in table 9.1.
 Immutable.js for JavaScript at https://immutable-js.com/
 Paguro for Java at https://github.com/GlenKPeterson/Paguro
 Immutable Collections for C# at http://mng.bz/QW51
 Pyrsistent for Python at https://github.com/tobgu/pyrsistent
 Hamster for Ruby at https://github.com/hamstergem/hamster
Table 9.1 Persistent data structure libraries
Language Library
JavaScript Immutable.js
Java Paguro
C# Provided by the language
Python Pyrsistent
Ruby Hamster
Theo What does it take to integrate persistent data structures provided by a third-
party library into your code?