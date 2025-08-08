# Summary

**메타데이터:**
- ID: 130
- 레벨: 2
- 페이지: 322-322
- 페이지 수: 1
- 부모 ID: 123
- 텍스트 길이: 1754 문자

---

in benefit of polymorphism is extensibility.
 Multimethods make it possible to benefit from polymorphism when data is repre-
sented with generic maps.
 A multimethod is made of a dispatch function and multiple methods.
 The dispatch function of a multimethod emits a dispatch value.
 Each of the methods used in a multimethod provides an implementation for a
specific dispatch value.
 Multimethods can mimic OOP class inheritance via single dispatch.
 In single dispatch, a multimethod receives a single map that contains a type field,
and the dispatch function of the multimethod emits the value of the type field.
 In addition to single dispatch, multimethods provide two kinds of advanced
polymorphisms: multiple dispatch and dynamic dispatch.
 Multiple dispatch is used when the behavior of the multimethod depends on
multiple arguments.
 Dynamic dispatch is used when the behavior of the multimethod depends on run-
time arguments.
 The arguments of a multimethod are passed to the dispatch function and to the
methods.
 A multimethod dispatch function is responsible for
– Defining the signature.
– Validating the arguments.
– Emitting a dispatch value.
 Multimethods provides extensibility by decoupling between multimethod ini-
tialization and method implementations.
 Multimethods are called like regular functions.
 Multimethods support default implementations that are called when no method
corresponds to the dispatch value.
 In a multimethod that features multiple dispatch, the order of the elements in
the array emitted by the dispatch function has to be consistent with the order of
the elements in the wiring of the methods.
Lodash functions introduced in this chapter
Function Description
size(coll) Gets the size of coll