# 13.4 Multimethods with dynamic dispatch

**메타데이터:**
- ID: 128
- 레벨: 2
- 페이지: 314-316
- 페이지 수: 3
- 부모 ID: 123
- 텍스트 길이: 4564 문자

---

s with dynamic dispatch
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