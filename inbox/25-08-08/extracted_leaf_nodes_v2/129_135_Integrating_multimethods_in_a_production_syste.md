# 13.5 Integrating multimethods in a production system

**메타데이터:**
- ID: 129
- 레벨: 2
- 페이지: 317-321
- 페이지 수: 5
- 부모 ID: 123
- 텍스트 길이: 9052 문자

---

multimethods in a production system 289
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

294 CHAPTER 13 Polymorphism