# 속성
---
process_status: false
source: 2022_Data-Oriented Programming_Manning.pdf
source_type: book
source_language: english
structure_type: component
content_processing: unified
title: Data-Oriented Programming
folder_name: 
created_at: 2025-08-28T11:43:31.980838

# 추출
---

# 내용
---
## Summary

Summary
 DOP Principle #4 is to separate data schema and data representation.
 The boundaries of a system are defined to be the areas where the system
exchanges data.
 Some examples of data validation at the boundaries of the system are validation
of client requests and responses, and validation of data that comes from exter-
nal sources.
 Data validation in DOP means checking whether a piece of data conforms to a
schema.
 When a piece of data is not valid, we get information about the validation fail-
ures and send this information back to the client in a human readable format.
 When data at system boundaries is valid, it's not critical to validate data again
inside the system.
 JSON Schema is a language that allows us to separate data validation from data
representation.
 JSON Schema syntax is a bit verbose.
 The expressive power of JSON Schema is high.
 JSON Schemas are just maps and, as so, we are free to manipulate them like any
other maps in our programs.
 We can store a schema definition in a variable and use this variable in another
schema.
 In JSON Schema, map fields are optional by default.
 It's good practice to validate data that comes from an external data source.

=== 페이지 190 ===
162 CHAPTER 7 Basic data validation
 It's good practice to be strict regarding data that you send and to be flexible
regarding data that you receive.
 Ajv is a JSON Schema library in JavaScript.
 By default, Ajv catches only the first validation failure.
 Advanced validation is covered in chapter 12.

# 구성
---
없음 (리프 노드)
