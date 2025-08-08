# Chapter 13: Polymorphism

**부제목:** Playing with the animals in the countryside
**계획된 페이지:** 300-322
**실제 페이지:** 300-322

=== PAGE 300 ===
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

=== PAGE 301 ===
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

=== PAGE 302 ===
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

=== PAGE 303 ===
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

=== PAGE 304 ===
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

=== PAGE 305 ===
13.2 Multimethods with single dispatch 277
break;
};
}
Dave But what if you want to extend the functionality of greet and add a new animal?
Theo Now you got me. I admit that with a switch statement, I can’t add a new animal
without modifying the original code, whereas in OOP, I can add a new class
without having to modify the original code.
Dave Yeah, but you helped me to realize that the main benefit of polymorphism is
that it makes the code easily extensible.
TIP The main benefit of polymorphism is extensibility.
Theo I’m going to ask Joe if there’s a way to benefit from polymorphism without
objects.
Theo sends a message to Joe and asks him about polymorphism in DOP. Joe answers that
he doesn’t have time to get into a deep response because he is in a tech conference where
he is about to give a talk about DOP. The only thing he has time to tell Theo is that he
should take a look at multimethods.
Theo and Dave read some online material about multimethods. It doesn’t look too
complicated. They decide that after lunch they will give multimethods a try.
13.2 Multimethods with single dispatch
During lunch, Theo asks Dave how it feels to have grown up in the country. Dave starts
with an enthusiastic description about being in direct contact with nature and living a sim-
pler life than in the city. He’s grateful for the experience, but he admits that country life
can sometimes be hard without the conveniences of the city. But who said simple was easy?
After lunch, they decide to have coffee. Dave asks Theo if he’d like to grind the coffee
beans himself. Theo accepts with joy. Next, Dave explains how to use a French press coffee
maker to get the ideal tradeoff between bitterness and rich taste. While savoring their
French press coffee in the garden, Theo and Dave continue their exploration of polymor-
phism à la DOP.
Theo From what I read before lunch, it seems that multimethods are a software con-
struct that provide polymorphism without the need for objects.
Dave I don’t get how that’s possible.
Theo Multimethods have two parts: a dispatch function and a set of methods that
provide an implementation for each dispatched value.
Dave I’m not sure I’m clear on that. Is a dispatch function like an interface?
Theo It’s like an interface in the sense that it defines the way the function needs to
be called, but it goes beyond that. It also dispatches a value that differentiates
between the different implementations.
Dave That’s a bit abstract for me.
Theo I think I understand how to implement the animal greeting capabilities. If we
use a multimethod called greet, we need a dispatch function and three
methods. Let’s call the dispatch function greetDispatch. It dispatches the
animal type, either "dog", "cat", or "cow". Then, each dispatch value is

=== PAGE 306 ===
278 CHAPTER 13 Polymorphism
handled by a specific method: "dog" by greetDog, "cat" by greetCat, and
"cow" by greetCow.
Theo takes out his notebook and opens it to a blank piece of paper. He draws a diagram
like the one in figure 13.1.
"dog" greetDog
Greet as a dog
greetDispatch "cat" greetCat
Emit the animal type Greet as a cat
animal
type, name "cow" greetCow
Greet as a cow
Figure 13.1 The logic flow
of the greet multimethod
Dave Why is there an arrow between animal and the methods, in addition to the
arrows between animal and the dispatch functions?
Theo Because the arguments of a multimethod are passed to the dispatch function
and to the methods.
TIP The arguments of a multimethod are passed to the dispatch function and to the
methods.
Dave Arguments plural?... I see only a single argument.
Theo You’re right. Right now our multimethod only receives a single argument, but
soon it will receive several arguments.
Dave I see. Could you show me how to write the code for the greet multimethod?
Theo For that, we need a library. For instance, in JavaScript, the arrows/multi-
method library provides an implementation of multimethods. Basically, we call
multi to create a multimethod called method to add a method.
 NOTE See http://mng.bz/nY9v for examples and documentation about this library.
Dave Where should we start?
Theo We’ll start with multimethod initialization by creating a dispatch function
greetDispatch that defines the signature of the multimethod, validates the
arguments, and emits the type of the animal. Then we’ll pass greetDispatch
to multi in order to create the greet multimethod. Our dispatch function
would then look like this.
Listing13.6 The dispatch function for greet multimethod
function greetDispatch(animal) {
Signature definition
if(dev()) {

=== PAGE 307 ===
13.2 Multimethods with single dispatch 279
if(!ajv.validate(animalSchema, animal)) {
Argument validation
var errors = ajv.errorsText(ajv.errors);
throw ("greet called with invalid arguments: " + errors);
}
}
Dispatch value
return animal.type;
}
Multimethod
initialization
var greet = multi(greetDispatch);
TIP A multimethod dispatch function is responsible for three things: it defines the sig-
nature of the multimethod, it validates the arguments, and it emits a dispatch value.
Dave What’s next?
Theo Now we need to implement a method for each dispatched value. Let’s start
with the method that deals with dogs. We create a greetDog function that
receives an animal and then add a dog method to the greet multimethod
using the method function from the arrows/multimethod library. The method
function receives two arguments: the dispatched value and a function that cor-
responds to the dispatch value.
Listing13.7 Implementation of greet method for dogs
function greetDog(animal) {
Method
console.log("Woof woof! My name is " + animal.name);
implementation
}
greet = method("dog", greetDog)(greet);
Method declaration
Dave Does the method implementation have to be in the same module as the multi-
method initialization?
Theo No, not at all! Method declarations are decoupled from multimethod initializa-
tion exactly like class definitions are decoupled from the interface definition.
That’s what make multimethods extensible.
TIP Multimethods provides extensibility by decoupling between multimethod initial-
ization and method implementations.
Dave What about cats and cows?
Theo We add their method implementations like we did for dogs.
Theo takes a moment to envision the implementation. Then he codes up two more greet
methods for cats and cows.
Listing13.8 Implementation of greet method for cats
function greetCat(animal) {
console.log("Meow! I am " + animal.name);
}
greet = method("cat", greetCat)(greet);

=== PAGE 308 ===
280 CHAPTER 13 Polymorphism
Listing13.9 Implementation of greet method for cows
function greetCow(animal) {
console.log("Moo! Call me " + animal.name);
}
greet = method("cow", greetCow)(greet);
TIP In the context of multimethods, a method is a function that provides an imple-
mentation for a dispatch value.
Dave Are the names of dispatch functions and methods important?
Theo According to what I read, not really, but I like to follow a simple naming con-
vention: use the name of the multimethod (for example, greet) as a prefix for
the dispatch function (for example, greetDispatch) and the methods. Then
I’d have the Dispatch suffix for the dispatch function and a specific suffix for
each method (for example, greetDog, greetCat, and greetCow).
Dave How does the multimethod mechanism work under the hood?
Theo Internally, a multimethod maintains a hash map where the keys are the dis-
patched values, and the values are the methods. When we add a method, an
entry is added to the hash map, and when we call the multimethod, we query the
hash map to find the implementation that corresponds to the dispatched value.
Dave I don’t think you’ve told me yet how to call a multimethod.
Theo We call it as a regular function. Give me a minute, and I’ll show you an exam-
ple that calls a multimethod.
Listing13.10 Calling a multimethod like a regular function
greet(myDog);
// → "Woof woof! My name is Fido"
greet(myCat);
// → "Meow! I am Milo"
greet(myCow);
// → "Moo! Call me Clarabelle"
TIP Multimethods are called like regular functions.
Dave You told me earlier that in the dispatch function, we should validate the argu-
ments. Is that mandatory or is it a best practice?
Theo It’s a best practice.
Dave What happens if the dispatch function doesn’t validate the arguments, and we
pass an invalid argument?
Theo Like when an animal has no corresponding method?
Dave Exactly!
Theo In that case, you’ll get an error. For instance, the arrows/multimethods library
throws a NoMethodError exception.
Dave That’s annoying. Is there a way to provide a default implementation?

=== PAGE 309 ===
13.3 Multimethods with multiple dispatch 281
Theo Absolutely! In order to define a default implementation, you pass to method—
as a single argument—the function that provides the default implementation.
Theo writes the code and shows it to Dave. Dave then tests Theo’s code and seems satisfied
with the result.
Listing13.11 Defining a default implementation
function greetDefault(animal) {
console.log("My name is " + animal.name);
}
greet = method(greetDefault)(greet);
Listing13.12 Calling a multimethod when no method fits the dispatch value
var myHorse = {
"type": "horse",
"name": "Horace"
};
greet(myHorse);
// → "My name is Horace"
TIP Multimethods support default implementations that are called when no method
corresponds to the dispatch value.
Dave Cool!
13.3 Multimethods with multiple dispatch
Theo So far, we’ve mimicked OOP by having the type of the multimethod argument
as a dispatch value. But if you think again about the flow of a multimethod,
you’ll discover something interesting. Would you like to try and draw a dia-
gram that describes the flow of a multimethod in general?
Dave Let me get a fresh napkin. The one under my glass is a bit wet.
Theo Uh, Dave, you can use my notebook.
It takes Dave a few minutes to draw a diagram like the one in figure 13.2. He pushes the
notebook back to Theo.
Value1 Method1
Handle case 1
Dispatch function Value3 Method3
Emit a dispatch value Handle case 3
args
Value2 Method2
Handle case 2
Figure 13.2 The logic flow
of multimethods

=== PAGE 310 ===
282 CHAPTER 13 Polymorphism
Theo Excellent! I hope you see that the dispatch function can emit any value.
Dave Like what?
Theo Like emitting the type of two arguments!
Dave What do you mean?
Theo Imagine that our animals are polyglot.
Dave Poly what?
Theo Polyglot comes from the Greek polús, meaning much, and from glôssa, meaning
language. A polyglot is a person who can speak many languages.
Dave What languages would our animals speak?
Theo I don’t know. Let’s say English and French.
Dave OK, and how would we represent a language in our program?
Theo With a map, of course!
Dave What fields would we have in a language map?
Theo Let’s keep things simple and have two fields: type and name.
Dave Like an animal map?
Theo Not exactly. In a language map, the type field must be either fr for French or en
for English, whereas in the animal map, the type field is either dog, cat, or cow.
Dave Let me try to write the language map schema and the two language maps.
Theo gladly consents; his French press coffee is getting cold! Dave writes his implementa-
tion of the code and shows Theo.
Listing13.13 The schema of a language map
var languageSchema = {
"type": "object",
"properties": {
"name": {"type": "string"},
"type": {"type": "string"}
},
"required": ["name", "type"],
};
Listing13.14 Two language maps
var french = {
"type": "fr",
"name": "Français"
};
var english = {
"type": "en",
"name": "English"
};
Theo Excellent! Now, let’s write the code for the dispatch function and the methods
for our polyglot animals. Let’s call our multimethod, greetLang. We have one
dispatch function and six methods.

=== PAGE 311 ===
13.3 Multimethods with multiple dispatch 283
Dave Right, three animals (dog, cat, and cow) times two languages (en and fr).
Before the implementation, I’d like to draw a flow diagram. It will help me to
make things crystal clear.
Theo You need my notebook again?
Not waiting for Dave to respond, Theo pushes his notebook across the table to Dave. Dave
draws a diagram like the one in figure 13.3 and slides the notebook back to Theo.
["dog", "en"] greetLangDogEn
Greet as a dog in English
["cat", "en"] greetLangCatEn
Greet as a cat in English
["cow", "en"] greetLangCowEn
Greet as a cow in English
args greetLangDispatch
animal, language Emit the animal and the language types
["dog", "fr"] greetLangDogFr
Greet as a dog in French
["cat", "fr"] greetLangCatFr
Greet as a cat in French
["cow", "fr"] greetLangCowFr
Greet as a cow in French
Figure 13.3 The logic flow of the greetLang multimethod
Theo Why did you omit the arrow between the arguments and the methods?
Dave In order to keep the diagram readable. Otherwise, there would be too many
arrows.
Theo OK, I see. Are you ready for coding?
Dave Yes!
Theo The dispatch function needs to validate its arguments and return an array with
two elements: the type of animal and the type of language.
Dave types for a bit on his laptop. He initializes the multimethod with a dispatch function
that returns the type of its arguments and then shows the code to Theo.
Listing13.15 Initializing a multimethod with a dispatch function
var greetLangArgsSchema = {
"type": "array",
"prefixItems": [animalSchema, languageSchema]
};
function greetLangDispatch(animal, language) {
if(dev()) {

=== PAGE 312 ===
284 CHAPTER 13 Polymorphism
if(!ajv.validate(greetLangArgsSchema, [animal, language])) {
throw ("greetLang called with invalid arguments: " +
ajv.errorsText(ajv.errors));
}
}
return [animal.type, language.type];
};
var greetLang = multi(greetLangDispatch);
Dave Does the order of the elements in the array matter?
Theo It doesn’t matter, but it needs to be consistent with the wiring of the methods.
The implementation of greetLang would therefore look like this.
Listing13.16 The implementation of greetLang methods
function greetLangDogEn(animal, language) {
console.log("Woof woof! My name is " +
animal.name +
" and I speak " +
language.name);
}
greetLang = method(["dog", "en"], greetLangDogEn)(greetLang);
function greetLangDogFr(animal, language) {
console.log("Ouaf Ouaf! Je m'appelle " +
animal.name +
" et je parle " +
language.name);
}
greetLang = method(["dog", "fr"], greetLangDogFr)(greetLang);
function greetLangCatEn(animal, language) {
console.log("Meow! I am " +
animal.name +
" and I speak " +
language.name);
}
greetLang = method(["cat", "en"], greetLangCatEn)(greetLang);
function greetLangCatFr(animal, language) {
console.log("Miaou! Je m'appelle " +
animal.name +
" et je parle " +
language.name);
}
greetLang = method(["cat", "fr"], greetLangCatFr)(greetLang);
function greetLangCowEn(animal, language) {
console.log("Moo! Call me " +
animal.name +
" and I speak " +

=== PAGE 313 ===
13.3 Multimethods with multiple dispatch 285
language.name);
}
greetLang = method(["cow", "en"], greetLangCowEn)(greetLang);
function greetLangCowFr(animal, language) {
console.log("Meuh! Appelle moi " +
animal.name +
" et je parle " +
language.name);
}
greetLang = method(["cow", "fr"], greetLangCowFr)(greetLang);
Dave looks at the code for the methods that deal with French. He is surprised to see Ouaf
Ouaf instead of Woof Woof for dogs, Miaou instead of Meow for cats, and Meuh instead of
Moo for cows.
Dave I didn’t know that animal onomatopoeia were different in French than in
English!
Theo Ono what?
Dave Onomatopoeia, from the Greek ónoma that means name and poiéo– that means to
produce. It is the property of words that sound like what they represent; for
instance, Woof, Meow, and Moo.
Theo Yeah, for some reason in French, dogs Ouaf, cats Miaou, and cows Meuh.
Dave I see that in the array the animal type is always before the language type.
Theo Right! As I told you before, in a multimethod that features multiple dispatch,
the order doesn’t really matter, but it has to be consistent.
TIP Multiple dispatch is when a dispatch function emits a value that depends on more
than one argument. In a multimethod that features multiple dispatch, the order of
the elements in the array emitted by the dispatch function has to be consistent with
the order of the elements in the wiring of the methods.
Dave Now let me see if I can figure out how to use a multimethod that features mul-
tiple dispatch.
Dave remembers that Theo told him earlier that multimethods are used like regular func-
tions. With that in mind, he comes up with the code for a multimethod that features multi-
ple dispatch.
Listing13.17 Calling a multimethod that features multiple dispatch
greetLang(myDog, french);
// → "Ouaf Ouaf! Je m\'appelle Fido et je parle Français"
greetLang(myDog, english);
// → "Woof woof! My name is Fido and I speak English"
greetLang(myCat, french);
// → "Miaou! Je m\'appelle Milo et je parle Français"

=== PAGE 314 ===
286 CHAPTER 13 Polymorphism
greetLang(myCat, english);
// → "Meow! I am Milo and I speak English"
greetLang(myCow, french);
// → "Meuh! Appelle moi Clarabelle et je parle Français"
greetLang(myCow, english);
// → "Moo! Call me Clarabelle and I speak English"
Theo Now do you agree that multimethods with multiple dispatch offer a more pow-
erful polymorphism that OOP polymorphism?
Dave Indeed, I do.
Theo Let me show you an even more powerful polymorphism called dynamic dis-
patch. But first, let’s get some more of that wonderful French press coffee.
Dave Great idea! While we’re in the kitchen, I think my mom made an orange Bundt
cake using the oranges from the grove.
13.4 Multimethods with dynamic dispatch
Dave refills their coffee cups as Theo takes two slices from the cake and dishes them up.
They take their coffee and cake outside to enjoy more of the fresh country air before
resuming their conversation.
Dave What is dynamic dispatch?
Theo It’s when the dispatch function of a multimethod returns a value that goes
beyond the static type of its arguments.
Dave Like what, for example?
Theo Like a number or a Boolean, for instance.
Dave Why would such a thing be useful?
Theo Imagine that instead of being polyglot, our animals would suffer from
dysmakrylexia.
Dave Suffering from what?
Theo Dysmakrylexia. It comes from the Greek dus, expressing the idea of difficulty,
makrýs meaning long, and léxis meaning diction. Therefore, dysmakrylexia is dif-
ficulty pronouncing long words.
Dave I’ve never heard of that.
Theo That’s because I just invented it.
Dave Funny. What’s considered a long word for our animals?
Theo Let’s say that when their name has more than five letters, they’re not able to
say it.
Dave A bit weird, but OK.
Theo Let’s call our multimethod dysGreet. Its dispatch function returns an array
with two elements: the animal type and a Boolean about whether the name is
long or not. Take a look at this multimethod initialization.

=== PAGE 315 ===
13.4 Multimethods with dynamic dispatch 287
Listing13.18 A multimethod using a dispatch function with dynamic dispatch
function dysGreetDispatch(animal) {
if(dev()) {
if(!ajv.validate(animalSchema, animal)) {
var errors = ajv.errorsText(ajv.errors);
throw ("dysGreet called with invalid arguments: " + errors);
}
}
var hasLongName = animal.name.length > 5;
return [animal.type, hasLongName];
};
var dysGreet = multi(dysGreetDispatch);
Dave Writing the dysGreet methods doesn’t seem too complicated.
As Theo reaches over to pass Dave his notebook, he accidently hits his coffee cup. Now Theo’s
notebook is completely wet, and all the diagrams are soggy! Fortunately, Dave brought an
extra napkin from the kitchen, and it’s still clean. He draws a flow diagram as in figure 13.4
and then grabs his laptop and writes the implementation of the dysGreet methods.
["dog", true] dysGreetDogLong
Greet as a dog mentioning name
["cat", true] dysGreetCatLong
Greet as a cat mentioning name
["cow", true] dysGreetCowLong
Greet as a cow mentioning name
args dysGreetLangDispatch
animal, language Emit the animal and the language types
["dog", false] dysGreetDogShort
Greet as a dog omitting name
["cat", false] dysGreetCatShort
Greet as a cat omitting name
["cow", false] dysGreetCowShort
Greet as a cow omitting name
Figure 13.4 The logic flow of the dysGreet multimethod
Listing13.19 The dysGreet methods
function dysGreetDogLong(animal) {
console.log("Woof woof! My name is " + animal.name);
}
dysGreet = method(["dog", true], dysGreetDogLong)(dysGreet);

=== PAGE 316 ===
288 CHAPTER 13 Polymorphism
function dysGreetDogShort(animal) {
console.log("Woof woof!");
}
dysGreet = method(["dog", false], dysGreetDogShort)(dysGreet);
function dysGreetCatLong(animal) {
console.log("Meow! I am " + animal.name);
}
dysGreet = method(["cat", true], dysGreetCatLong)(dysGreet);
function dysGreetCatShort(animal) {
console.log("Meow!");
}
dysGreet = method(["cat", false], dysGreetCatShort)(dysGreet);
function dysGreetCowLong(animal) {
console.log("Moo! Call me " + animal.name);
}
dysGreet = method(["cow", true], dysGreetCowLong)(dysGreet);
function dysGreetCowShort(animal) {
console.log("Moo!");
}
dysGreet = method(["cow", false], dysGreetCowShort)(dysGreet);
Theo checks that the code works as expected. He compliments Dave, not only on the
method implementation but also for having the foresight to grab an extra napkin.
Listing13.20 Testing dysGreet
dysGreet(myDog);
dysGreet(myCow);
dysGreet(myCat);
//"Woof woof!"
//"Moo! Call me Clarabelle"
//"Meow!"
Theo Well done, my friend! Our exploration of multimethods has come to an end. I
think it’s time for me to drive back if I want to get home before dark and beat
the rush hour traffic.
Dave Before you leave, let’s check if multimethods are available in programming
languages other than JavaScript.
Theo That’s a question for Joe.
Dave Do you think it’s OK if I call him now?
Theo I think it’s probably better if you send him an email. He’s in a tech conference,
and I’m not sure if it’s all day. Thank you for this beautiful day in the country
and the wonderful refreshments.
Dave I enjoyed it, also, especially our discussions about etymology. I think there are
some oranges for you to take home and enjoy later.
Theo Great! I can’t wait until my wife tries one.

=== PAGE 317 ===
13.5 Integrating multimethods in a production system 289
After Theo leaves, Dave sends Joe an email. A few minutes later, Dave receives an email
from Joe with the subject, “Support for multimethods in different languages.”
Support for multimethods in different languages
Python has a library called multimethods (https://github.com/weissjeffm/multimeth-
ods), and Ruby has one called Ruby multimethods (https://github.com/psantacl/
ruby-multimethods). Both seem to work quite like the JavaScript arrows/multi-
method library.
In Java, there is the Java Multimethod Framework (http://igm.univ-mlv.fr/~forax/
works/jmmf/), and C# supports multimethods natively via the dynamic keyword.
However, in both Java and C#, multimethods work only with static data types and not
with generic data structures.
Generic data structure
Language URL
support
JavaScript https://github.com/caderek/arrows/tree/master/ Yes
packages/multimethod
Java http://igm.univ-mlv.fr/~forax/works/jmmf/ No
C# Native support No
Python https://github.com/weissjeffm/multimethods Yes
Ruby https://github.com/psantacl/ruby-multimethods Yes
13.5 Integrating multimethods in a production system
While Theo is driving back home, his thoughts take him back to the fresh air of the coun-
try. This pleasant moment is interrupted by a phone call from Nancy at Klafim.
Nancy How are you doing?
Theo Fine. I’m driving back from the countryside.
Nancy Cool. Are you available to talk about work?
Theo Sure.
Nancy I’d like to add a tiny feature to the catalog.
In the past, when Nancy qualified a feature as tiny, it scared Theo because tiny turned into
huge. What seemed easy to her always took him a surprising amount of time to develop.
But after refactoring the system according to DOP principles, now what seems tiny to
Nancy is usually quite easy to implement.
Theo What feature?
Nancy I’d like to allow librarians to view the list of authors, ordered by last name, in
two formats: HTML and Markdown.

=== PAGE 318 ===
290 CHAPTER 13 Polymorphism
Theo It doesn’t sound too complicated.
Nancy Also, I need a bit of text formatting.
Theo What kind of text formatting?
Nancy Depending on the number of books an author has written, their name should
be in bold and italic fonts.
Theo Could you send me an email with all the details. I’ll take a look at it tomorrow
morning.
Nancy Perfect. Have a safe drive!
Before going to bed, Theo reflects about today’s etymology lessons. He realizes that he
never looked for the etymology of the word etymology itself! He searches for the term etymol-
ogy online and learns that the word etymology derives from the Greek étumon, meaning true
sense, and the suffix logia, denoting the study of. During the night, Theo dreams of dogs,
cats, and cows programming on their laptops in a field of grass.
When Theo arrives at the office the next day, he opens Nancy’s email with the details
about the text formatting feature. The details are summarized in table 13.1.
Table 13.1 Text formatting for author names according to the number of books
they have written
Number of books Italic Bold
10 or fewer Yes No
Between 11 and 50 No Yes
51 or more Yes Yes
Theo forwards Nancy’s email to Dave and asks him to take care of this task. Delegating
responsibility, after all, is the trait of a great manager.
Dave thinks the most difficult part of the feature lies in implementing an Author
.myName(author, format) function that receives two arguments: the author data and the
text format. He asks himself whether he can implement this function as a multimethod
and use what he learned yesterday with Theo at his parents’ home in the country. It seems
that this feature is quite similar to the one that dealt with dysmakrylexia. Instead of check-
ing the length of a string, he needs to check the length of an array.
First, Dave needs a data schema for the text format. He could represent a format as a
map with a type field like Theo did yesterday for languages, but at the moment, it seems
simpler to represent a format as a string that could be either markdown or html. He comes
up with the text format schema in listing 13.21. He already wrote the author schema with
Theo last week. It’s in listing 13.22.
Listing13.21 The text format schema
var textFormatSchema = {
"name": {"type": "string"},
"type": {"enum": ["markdown", "html"]}
};

=== PAGE 319 ===
13.5 Integrating multimethods in a production system 291
Listing13.22 The author schema
var authorSchema = {
"type": "object",
"required": ["name", "bookIsbns"],
"properties": {
"name": {"type": "string"},
"bookIsbns": {
"type": "array",
"items": {"type": "string"}
}
}
};
Now, Dave needs to write a dispatch function and initialize the multimethod. Remember-
ing that Theo had no qualms about creating the word dysmakrylexia, he decides that he
prefers his own neologism, prolificity, over the existing nominal form prolificness. He finds it
useful to have an Author.prolificityLevel helper function that returns the level of
prolificity of the author: either low, medium, or high. Now he’s ready to code the author-
NameDispatch function.
Listing13.23 Author.myName multimethod initialization
Author.prolificityLevel = function(author) {
var books = _.size(_.get(author, "bookIsbns"));
if (books <= 10) {
return "low";
};
if (books >= 51) {
return "high";
}
return "medium";
};
var authorNameArgsSchema = {
"type": "array",
"prefixItems": [
authorSchema,
{"enum": ["markdown", "html"]}
]
};
function authorNameDispatch(author, format) {
if(dev()) {
if(!ajv.validate(authorNameArgsSchema, [author, format])) {
throw ("Author.myName called with invalid arguments: " +
ajv.errorsText(ajv.errors));
}
}
return [Author.prolificityLevel(author), format];
};
Author.myName = multi(authorNameDispatch);

=== PAGE 320 ===
292 CHAPTER 13 Polymorphism
Then Dave works on the methods: first, the HTML format methods. In HTML, bold text is
wrapped inside a <b> tag, and italic text is wrapped in a <i> tag. For instance, in HTML,
three authors with different levels of prolificity would be written like this.
Listing13.24 Examples of bold and italic in HTML
Italic formatting for Bold formatting for
minimally prolific authors moderately prolific authors
<i>Yehonathan Sharvit<i>
Bold and italic formatting
<b>Stephen Covey</b>
for highly prolific authors
<b><i>Isaac Asimov</i></b>
With this information in hand, Dave writes the three methods that deal with HTML for-
matting. Easy!
Listing13.25 The methods that deal with HTML formatting
function authorNameLowHtml(author, format) {
return "<i>" + _.get(author, "name") + "</i>";
}
Author.myName = method(["low", "html"], authorNameLowHtml)(Author.myName);
function authorNameMediumHtml(author, format) {
return "<b>" + _.get(author, "name") + "</b>";
}
Author.myName =
method(["medium", "html"], authorNameMediumHtml)(Author.myName);
function authorNameHighHtml(author, format) {
return "<b><i>" + _.get(author, "name") + "</i></b>";
}
Author.myName =
method(["high", "html"], authorNameHighHtml)(Author.myName);
Then, Dave moves on to the three methods that deal with Markdown formatting. In
Markdown, bold text is wrapped in two asterisks, and italic text is wrapped in a single
asterisk. For instance, in Markdown, three authors with different levels of prolificity
would be written like the code in listing 13.26. The code for the Markdown methods is in
listing 13.27.
Listing13.26 Examples of bold and italic in Markdown
Italic formatting for Bold formatting for
minimally prolific authors moderately prolific authors
*Yehonathan Sharvit*
Bold and italic formatting
**Stephen Covey**
for highly prolific authors
***Isaac Asimov***

=== PAGE 321 ===
13.5 Integrating multimethods in a production system 293
Listing13.27 The methods that deal with Markdown formatting
function authorNameLowMarkdown(author, format) {
return "*" + _.get(author, "name") + "*";
}
Author.myName =
method(["low", "markdown"], authorNameLowMarkdown)(Author.myName);
function authorNameMediumMarkdown(author, format) {
return "**" + _.get(author, "name") + "**";
}
Author.myName =
method(["medium", "markdown"], authorNameMediumMarkdown)(Author.myName);
function authorNameHighMarkdown(author, format) {
return "***" + _.get(author, "name") + "***";
}
Author.myName =
method(["high", "markdown"], authorNameHighMarkdown)(Author.myName);
Dave decides to test his code by involving a mysterious author. Listing 13.28 and listing 13.29
show the tests.
Listing13.28 Testing HTML formatting
var yehonathan = {
"name": "Yehonathan Sharvit",
"bookIsbns": ["9781617298578"]
};
Author.myName(yehonathan, "html");
// → "<i>Yehonathan Sharvit</i>"
Listing13.29 Testing Markdown formatting
Author.myName(yehonathan, "markdown");
// → "*Yehonathan Sharvit*"
Theo shows up at Dave’s desk and asks to review Dave’s implementation of the list of
authors feature. Curious, Theo asks Dave about the author that appears in the test of
Author.myName.
Theo Who is Yehonathan Sharvit?
Dave I don’t really know. The name appeared when I googled “data-oriented pro-
gramming” yesterday. He wrote a book on the topic. I thought it would be cool
to use its ISBN in my test.

=== PAGE 322 ===
294 CHAPTER 13 Polymorphism
Summary
 The main benefit of polymorphism is extensibility.
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