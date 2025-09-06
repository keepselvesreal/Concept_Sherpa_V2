# 13 Introduction

**메타데이터:**
- ID: 124
- 레벨: 2
- 페이지: 300-301
- 페이지 수: 2
- 부모 ID: 123
- 텍스트 길이: 5771 문자

---

=== Page 299 ===
Summary 271
 Unlike data validation at system boundaries, data validation inside the system is
supposed to run only at development time and should be disabled in production.
 We visualize a data schema by generating a data model diagram out of a JSON
Schema.
 For functions that have data schemas for their arguments and return values, we
can automatically generate schema-based unit tests.
 Data validation is executed at run time.
 We can define advanced data validation conditions that go beyond static types,
like checking whether a number is within a range or if a string matches a regu-
lar expression.
 Data validation inside the system should be disabled in production.
 Records are represented as heterogeneous maps, and indexes are represented as
homogeneous maps.
 When you define a complex data schema, it is advised to store nested schemas
in variables to make the schemas easier to read.
 We treat data validation like unit tests.

=== Page 300 ===
Polymorphism
Playing with the animals
in the countryside
This chapter covers
 Mimicking objects with multimethods (single
dispatch)
 Implementing multimethod on several argument
types (multiple dispatch)
 Implementing multimethods dynamically on
several arguments (dynamic dispatch)
OOP is well-known for allowing different classes to be called with the same inter-
face via a mechanism called polymorphism. It may seem that the only way to have
polymorphism in a program is with objects. In fact, in this chapter, we are going to
see that it is possible to have polymorphism without objects, thanks to multimeth-
ods. Moreover, multimethods provide a more advanced polymorphism than OOP
polymorphism because they support cases where the chosen implementation
depends on several argument types (multiple dispatch) and even on the dynamic
value of the arguments (dynamic dispatch).
272

=== Page 301 ===
13.1 The essence of polymorphism 273
13.1 The essence of polymorphism
For today’s session, Dave has invited Theo to come and visit him at his parents’ house in
the countryside. As Theo’s drive across the Golden Gate Bridge takes him from the freeway
to increasingly rural country roads, he lets himself be carried away by the beauty of the
landscape, the smell of fresh earth, and the sounds of animals in nature. This “nature
bath” puts him in an excellent mood. What a way to start the week!
Dave receives Theo in jeans and a T-shirt, a marked contrast with the elegant clothes he
wears at the office. A straw hat completes his country look. Theo says hello to Dave’s par-
ents, now retired. Dave suggests that they go pick a few oranges in the field to squeeze for
juice. After drinking a much more flavorful orange juice than they are used to in San Fran-
cisco, Theo and Dave get to work.
Dave When I was waiting for you this morning, I thought of another thing I miss
from OOP.
Theo What’s that?
Dave Polymorphism.
Theo What kind of polymorphism?
Dave You know, you define an interface, and different classes implement the same
interface in different ways.
Theo I see. And why do you think polymorphism is valuable?
Dave Because it allows us to decouple an interface from its implementations.
Theo Would you mind illustrating that with a concrete example?
Dave Sure. Because we’re in the country, I’ll use the classic OOP polymorphism
example with animals.
Theo Good idea!
Dave Let’s say that each animal has its own greeting by making a sound and saying
its name.
Theo Oh cool, like in anthropomorphic comics books.
Dave Anthro what?
Theo You know, comics books where animals can walk, speak, and so forth—like
Mickey Mouse.
Dave Of course, but I don’t know that term. Where does it come from?
Theo Anthropomorphism comes from the Greek ánthro–pos, which means human, and
morphe–, which means form.
Dave I see. So an anthropomorphic book is a book where animals have human traits.
The word sounds related to polymorphism.
Theo Absolutely. Polymorphism comes from the Greek polús, which means many, and
morphe–, which, again, means form.
Dave That makes sense. Polymorphism is the ability of different objects to imple-
ment the same method in different ways. That brings me back to my animal
example. In OOP, I’d define an IAnimal interface with a greet method, and
each animal class would implement greet in its own way. Here, I happen to
have an example.

=== Page 302 ===
274 CHAPTER 13 Polymorphism
Listing13.1 OOP polymorphism illustrated with animals
interface IAnimal {
public void greet();
}
class Dog implements IAnimal {
private String name;
public void greet() {
System.out.println("Woof woof! My name is " + animal.name);
}
}
class Cat implements IAnimal {
private String name;
public void greet() {
System.out.println("Meow! I am " + animal.name);
}
}
class Cow implements IAnimal {
private String name;
public void greet() {
System.out.println("Moo! Call me " + animal.name);
}
}
Theo Let me challenge you a bit. What is the fundamental difference between OOP
polymorphism and a switch statement?
Dave What do you mean?
Theo I could, for instance, represent an animal with a map having two fields, name
and type, and call a different piece of code, depending on the value of type.
Theo pulls his laptop from its bag and fires it up. While the laptop is booting up, he enjoys
another taste of that wonderful orange juice. When the laptop is ready, he quickly types in
the example switch case. Meanwhile, Dave has finished his glass of orange juice.
Listing13.2 A switch case where behavior depends on type
function greet(animal) {
switch (animal.type) {
case "dog":
console.log("Woof Woof! My name is: " + animal.name);
break;
case "cat":
console.log("Meow! I am: " + animal.name);
break;
case "cow":
console.log("Moo! Call me " + animal.name);
break;
};
}