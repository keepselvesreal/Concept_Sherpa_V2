# 14.1 Updating a value in a map with eloquence

**메타데이터:**
- ID: 133
- 레벨: 2
- 페이지: 324-326
- 페이지 수: 3
- 부모 ID: 131
- 텍스트 길이: 5972 문자

---

value in a map with eloquence
Dave is more and more autonomous on the Klafim project. He can implement most fea-
tures on his own, typically turning to Theo only for code reviews. Dave’s code quality stan-
dards are quite high. Even when his code is functionally solid, he tends to be unsatisfied
with its readability. Today, he asks for Theo’s help in improving the readability of the code
that fixes a bug Theo introduced a long time ago.
Dave I think I have a found a bug in the code that returns book information from
the Open Library API.
Theo What bug?
Dave Sometimes, the API returns duplicate author names, and we pass the dupli-
cates through to the client.
Theo It doesn’t sound like a complicated bug to fix.
Dave Right, I fixed it, but I’m not satisfied with the readability of the code I wrote.
Theo Being critical of our own code is an important quality for a developer to prog-
ress. What is it exactly that you don’t like?
Dave Take a look at this code.
Listing14.1 Removing duplicates in a straightforward but tedious way
function removeAuthorDuplicates(book) {
var authors = _.get(book, "authors");
var uniqAuthors = _.uniq(authors);
return _.set(book,"authors", uniqAuthors);
}
Dave I’m using _.get to retrieve the array with the author names, then _.uniq to
create a duplicate-free version of the array, and finally, _.set to create a new
version of the book with no duplicate author names.
Theo The code is tedious because the next value of authorNames needs to be based
on its current value.
Dave But it’s a common use case! Isn’t there a simpler way to write this kind of code?
Theo Your astonishment definitely honors you as a developer, Dave. I agree with you
that there must be a simpler way. Let me phone Joe and see if he’s available for
a conference call.
Joe How’s it going, Theo?
Theo Great! Are you back from your tech conference?
Joe I just landed. I’m on my way home now in a taxi.
Theo How was your talk about DOP?
Joe Pretty good. At the beginning people were a bit suspicious, but when I told
them the story of Albatross and Klafim, it was quite convincing.
Theo Yeah, adults are like children in that way; they love stories.
Joe What about you? Did you manage to achieve polymorphism with multimethods?
Theo Yes! Dave even managed to implement a feature in Klafim with multimethods.
Joe Cool!

14.1 Updating a value in a map with eloquence 297
Theo Do you have time to help Dave with a question about programming?
Joe Sure.
Dave Hi Joe. How are you doing?
Joe Hello Dave. Not bad. What kind of help do you need?
Dave I’m wondering if there’s a simpler way to remove duplicates inside an array
value in a map. Using _.get, _.uniq, and _.set looks quite tedious.
Joe You should build your own data manipulation tools.
Dave What do you mean?
Joe You should write a generic update function that updates a value in a map,
applying a calculation based on its current value.1
Dave What would the arguments of update be in your opinion?
Joe Put the cart before the horse.
Dave What?!
Joe Rewrite your business logic as if update were already implemented, and you’ll
discover what the arguments of update should be.
Dave I see what you mean: the horse is the implementation of update, and the cart is
the usage of update.
Joe Exactly. But remember, it’s better if you keep your update function generic.
Dave How?
Joe By not limiting it to your specific use case.
Dave I see. The implementation of update should not deal with removing duplicate
elements. Instead, it should receive the updating function—in my case,
_.uniq—as an argument.
Joe Exactly! Uh, sorry Dave, I gotta go, I just got home. Good luck!
Dave Take care, Joe, and thanks!
Dave ends the conference call. Looking at Theo, he reiterates the conversation with Joe.
Dave Joe advised me to write my own update function. For that purpose, he told me
to start by rewriting removeAuthorDuplicates as if update were already
implemented. That will allow us to make sure we get the signature of update
right.
Theo Sounds like a plan.
Dave Joe called it “putting the cart before the horse.”
Theo Joe and his funny analogies...
TIP The best way to find the signature of a custom data manipulation function is to
think about the most convenient way to use it.
Dave Anyway, the way I’d like to use update inside removeAuthorDuplicates is
like this.
1 Lodash provides an implementation of update, but for the sake of teaching, we are writing our own imple-
mentation.

298 CHAPTER 14 Advanced data manipulation
Listing14.2 The code that removes duplicates in an elegant way
function removeAuthorDuplicates(book) {
return update(book, "authors", _.uniq);
}
Theo Looks good to me!
Dave Wow! Now the code with update is much more elegant than the code with
_.get and _.set!
Theo Before you implement update, I suggest that you write down in plain English
exactly what the function does.
Dave It’s quite easy: update receives a map called map, a path called path, and a
function called fun. It returns a new version of map, where path is associated
with fun(currentValue), and currentValue is the value associated with
path in map.
Thinking out loud, Dave simultaneously draws a diagram like that in figure 14.1. Theo is
becoming more and more impressed with his young protegé as he studies the figure.
{
"position" : "manager", "income"
"income" : 100000
} map fun path
update
{
"position" : "manager",
"income" : fun(100000)
res Figure 14.1 The
}
behavior of update
TIP Before implementing a custom data manipulation function, formulate in plain
English exactly what the function does.
Theo With such a clear definition, it’s going to be a piece of cake to implement
update!
After a few minutes, Dave comes up with the code. It doesn’t take long because the plain-
English diagram helps him to organize the code.
Listing14.3 A generic update function
function update(map, path, fun) {
var currentValue = _.get(map, path);
var nextValue = fun(currentValue);
return _.set(map, path, nextValue);
}