# 13.2 Multimethods with single dispatch

**메타데이터:**
- ID: 126
- 레벨: 2
- 페이지: 305-308
- 페이지 수: 4
- 부모 ID: 123
- 텍스트 길이: 8551 문자

---

s with single dispatch 277
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