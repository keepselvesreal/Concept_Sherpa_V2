# 13.1 The essence of polymorphism

**메타데이터:**
- ID: 125
- 레벨: 2
- 페이지: 301-304
- 페이지 수: 4
- 부모 ID: 123
- 텍스트 길이: 6432 문자

---

of polymorphism 273
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

13.1 The essence of polymorphism 275
Dave How would animal look, exactly?
Theo Like I just said, a map with two fields: name and type. Let me input that for you.
Listing13.3 Representing animals with maps
var myDog = {
"type": "dog",
"name": "Fido"
};
var myCat = {
"type": "cat",
"name": "Milo"
};
var myCow = {
"type": "cow",
"name": "Clarabelle"
};
Dave Could you have given another name to the field that holds the animal type?
Theo Absolutely. It could be anything.
Dave I see. You’re asking me the fundamental difference between your code with a
switch statement and my code with an interface and three classes?
Theo Exactly.
Dave First of all, if you pass an invalid map to your greet function, bad things will
happen.
Theo You’re right. Let me fix that and validate input data.
Listing13.4 Data validation
var animalSchema = {
"type": "object",
"properties": {
"name": {"type": "string"},
"type": {"type": "string"}
},
"required": ["name", "type"],
};
See chapter 12 about
data validation for
function greet(animal) {
details.
if(dev()) {
if(!ajv.validate(animalSchema, animal)) {
var errors = ajv.errorsText(ajv.errors);
throw ("greet called with invalid arguments: " + errors);
}
}
switch (animal.type) {
case "dog":

276 CHAPTER 13 Polymorphism
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
 NOTE You should not use switch statements like this in your production code.
We use them here for didactic purposes only as a step towards distilling the essence of
polymorphism.
Dave Another drawback of your approach is that when you want to modify the
implementation of greet for a specific animal, you have to change the code
that deals with all the animals, while in my approach, you would change only a
specific animal class.
Theo I agree, and I could also fix that by having a separate function for each animal,
something like this.
Listing13.5 Different implementations in different functions
function greetDog(animal) {
console.log("Woof Woof! My name is: " + animal.name);
}
function greetCat(animal) {
console.log("Meow! I am: " + animal.name);
}
function greetCow(animal) {
console.log("Moo! Call me " + animal.name);
}
function greet(animal) {
if(dev()) {
if(!ajv.validate(animalSchema, animal)) {
var errors = ajv.errorsText(ajv.errors);
throw ("greet called with invalid arguments: " + errors);
}
}
switch (animal.type) {
case "dog":
greetDog(animal);
break;
case "cat":
greetCat(animal);
break;
case "cow":
greetCow(animal);