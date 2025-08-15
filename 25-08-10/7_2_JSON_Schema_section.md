# 7.2 JSON Schema in a nutshell

7.2 JSON Schema in a nutshell 143
7.3 Schema flexibility and strictness 149
7.4 Schema composition 154
7.5 Details about data validation failures 158
8 Advanced concurrency control 163
8.1 The complexity of locks 164
8.2 Thread-safe counter with atoms 165
8.3 Thread-safe cache with atoms 170
8.4 State management with atoms 172
9 Persistent data structures 175
9.1 The need for persistent data structures 175
9.2 The efficiency of persistent data structures 178
9.3 Persistent data structures libraries 184
Persistent data structures in Java 184■Persistent data structures 
in JavaScript 186
9.4 Persistent data structures in action 188
Writing queries with persistent data structures 188■Writing 
mutations with persistent data structures 191■Serialization and 
deserialization 192■Structural diff 193
10 Database operations 197
10.1 Fetching data from the database 198
10.2 Storing data in the database 204
10.3 Simple data manipulation 207
10.4 Advanced data manipulation 211
11 Web services 220
11.1 Another feature request 221
11.2 Building the insides like the outsides 222
11.3 Representing a client request as a map 225
CONTENTS xi
11.4 Representing a server response as a map 227
11.5 Passing information forward 231
11.6 Search result enrichment in action 234
PART 3M AINTAINABILITY ............................................245
12 Advanced data validation 247
12.1 Function arguments validation 248
12.2 Return value validation 255
12.3 Advanced data validation 257
12.4 Automatic generation of data model diagrams 260
12.5 Automatic generation of schema-based unit tests 262
12.6 A new gift 269
13 Polymorphism 272
13.1 The essence of polymorphism 273
13.2 Multimethods with single dispatch 277
13.3 Multimethods with multiple dispatch 281
13.4 Multimethods with dynamic dispatch 286
13.5 Integrating multimethods in a production system 289
14 Advanced data manipulation 295
14.1 Updating a value in a map with eloquence 296
14.2 Manipulating nested data 299
14.3 Using the best tool for the job 301
14.4 Unwinding at ease 305
15 Debugging 311
15.1 Determinism in programming 312
15.2 Reproducibility with numbers and strings 314
15.3 Reproducibility with any data 318
15.4 Unit tests 321
15.5 Dealing with external data sources 329
CONTENTS xii
appendix A Principles of data-oriented programming 333
appendix B Generic data access in statically-typed languages 364
appendix C Data-oriented programming: A link in the chain of programming 
paradigms 381
appendix D Lodash reference 387
index 391
xiiiforewords
Every programming principle, every design method, every architecture style, and even
most language features are about organizing complexity while allowing adaptation.
Two characteristics—immutable data and turning parts of the program into data
inside the program itself—drew me to Clojure in 2009 and more recently to Yehona-
than Sharvit’s Data-Oriented Programming .
 In 2005, I worked on one of my favorite projects with some of my favorite people.
It was a Java project, but we did two things that were not common practice in the Java
world at that time. First, we made our core data values immutable. It wasn’t easy but it
worked extraordinarily well. We hand-rolled clone  and deepClone  methods in many
classes. The payoff was huge. Just as one example, suppose you need template docu-
ments for users to instantiate. When you can make copies of entire object trees, the
objects themselves don’t need to “know” whether they are template data or instance
data. That decision is up to whatever object holds the reference. Another big benefit
came from comparison: when values are immutable, equality of identity indicates
equality of value. This can make for very fast equality checks.
 Our second technique was to take advantage of generic data—though not to the
extent Yehonathan will show you in this book. Where one layer had a hierarchy of
classes, its adjoining layer would represent those as instances of a more general class.
What would be a member variable in one layer would be described by a field in a map
in another layer. I am certain this style was influenced by the several small talkers on
our team. It also paid off immediately, as we were able to compose and recompose
objects in different configurations.
FOREWORDS xiv
 Data-oriented programming, as you will see, promises to reduce accidental complex-
ity, and raise the level of abstraction you work at. You will start to see repeated behavior
in your programs as artificial, a result of carving generic functions into classes, which act
like little namespaces that operate only on a subset of your program’s values (their
instances). We can “fold together” almost all of those values into maps and lists. We can
turn member names (data available only with difficulty via reflective APIs) into map
keys. As we do that, code simply melts away. This is the first level of enlightenment.
 At this point, you might object that the compiler uses those member names at
compile time for correctness checking. Indeed it does. But have faith, for Yehonathan
will guide you to the next level of enlightenment: that those compile-time checks are a
small subset of possible correctness checks on values. We can make the correctness
checks themselves  into data, too! We can make schemas into values inside our programs.
What’s more, we can enforce criteria that researchers on the forefront of type systems
are still trying to figure out. This is the second level of enlightenment.
 Data-oriented programming especially shines when working with web APIs. There is
no type of system on the wire, so attempting to map a request payload directly into a
domain class guarantees a brittle, complex implementation. If we let data be data, we get
simpler code and far fewer dependencies on hundred-megabyte framework libraries.
 So, whatever happened to the OOP virtues of encapsulation, inheritance, and
polymorphism? It turns out we can decomplect these and get each of them à la carte.
(In my opinion, inheritance of implementations is the least important of these, even
though it is often the first one taught. I now prefer inheritance of interfaces  via proto-
cols and shared function signatures.) Data-oriented programming offers polymor-
phism of the “traditional” kind: dispatch to one of many functions based on the type
of the first argument (in an OO language, this  is a disguise for the method’s first
argument. It just happens it goes before the “ .”). However, as with schema checking,
DOP allows more dynamism. Imagine dispatching based on the types of the first two
arguments. Or based on whether the argument has a “birthday” field with today’s date
in it! This is the third level of enlightenment.
 And as for encapsulation, we must still apply it to the organizing logic of our
program. We encapsulate subsystems, not values. This encapsulation embodies the
decision-hiding of David Parnas. Inside a subsystem, we can stop walling off our data
into the disjointed namespaces that classes impose. In the words of Alan Perlis, “It is
better to have one hundred functions operate on one data structure than ten func-
tions on ten data structures.”
 In our unending battle with entropy, we can use data-oriented programming to
both reduce the volume of code to keep up and raise the level of abstraction to make
our program’s logic and meaning precise and evident. Enjoy the journey and pause at
each new plateau to enjoy the view and say to yourself, “It’s just data!”
—M ICHAEL  T. N YGARD
 author of Release It!: Design and
Deploy Production-Ready Software
FOREWORDS xv
This book hit me at just the right time. I had been building web apps for nearly 20
years in an object-oriented framework. I never considered myself an expert program-
mer, but I knew my tools well enough to look at a typical business problem, sketch out
a data model, and build an MVC-style app to get the job done.
 Projects were thrilling at the start. I loved the feeling of plugging pieces together
and seeing the app come to life. But once I got it working, I ran into problems. I
couldn’t change one part without keeping all the other models in mind. I knew I
should write tests, but I had to set up so much state to test things that it didn’t feel
worth it—I didn’t want to write more code that would be hard to change. Even run-
ning bits of code in the console was tedious because I had to create database state to
call the method. I thought I was probably doing it wrong, but the solutions I knew
about, such as sophisticated testing frameworks, seemed to add to the complexity
instead of making things easier.
 Then one day, I saw a talk on YouTube by Rich Hickey, the creator of Clojure. He
was explaining functional programming and contrasting it with OO, which he deri-
sively called “place-oriented programming.” I wasn’t sure if he was right, but I heard a
hidden message that intrigued me: “It’s not you, it’s your language.” I watched all the
videos I could find and started to think Clojure might be the answer.
 Years went by. I kept watching Clojure videos and trying to apply functional princi-
ples when I could. But whenever it was time to start on a new project, I fell back on my
familiar framework. Changing to another language with a totally different ecosystem
of libraries was too big of a leap.
 Then, just as I was about to start work on a new product, I found this book. The
words “Data-Oriented” in the title rang a bell. I heard programmers in those Clojure
videos use the words before, but I hadn’t really understood what they meant. Some-
thing about how it’s easier to build systems that manipulate data literals (like maps
and arrays) instead of custom objects. The languages I knew had good support for
data literals, so I thought I might learn something to hold me over until that magical
day when I might switch to Clojure.
 My first a-ha moment came right in the introduction. In the first few pages, Yehona-
than explains that, though he’s written Clojure for 10 years, the book isn’t language-
specific, and the examples will be in JavaScript. Wait!—I thought. Could it really be
that I don’t have to change languages to deeply improve the way I write programs?
 I was so excited by this prospect that I devoured the book in one sitting. My eyes
opened to something that had been right in front of me all along. Of course my code
was hard to test! Because of the ORM I used, all my functionality was written in objects
that assumed a bunch of database state! When I saw it spelled out with examples in the
book, I couldn’t unsee it. I didn’t need a new language, I just needed to approach pro-
gramming differently!
 The designers I consider great all point to the same thing: good design is about
pulling things apart. It’s not just about getting the code to work, no matter how ugly.
FOREWORDS xvi
It’s about untangling the parts from each other so you can change one thing without
breaking everything else.
 This book pulls apart code and data, with surprising and exciting results. For me, it
also went further. It pulled apart a way of programming  from a specific language . I might
never make that switch to Clojure, and I don’t feel like I have to anymore. Data-
Oriented Programming  helped me see new possibilities in the languages I know and the
multitude of new frameworks appearing every day.
—R YAN SINGER
 author of Shape Up: Stop Running
in Circles and Ship Work that Matters
xviipreface
I have been a software engineer since 2000. For me, there is clearly a “before” and an
“after” 2012. Why 2012? Because 2012 is the year I discovered Clojure. Before Clojure,
programming was my job. After Clojure, programming has been my passion.
 A few years ago, I wondered what features of Clojure made this programming lan-
guage such a great source of pleasure for me. I shared my questions with other mem-
bers of the Clojure community who have the same passion for it that I do. Together,
we discovered that what was so special about Clojure was not features, but principles.
 When we set out to distill the core principles of Clojure, we realized that they were,
in fact, applicable to other programming languages. It was then that the idea for this
book began to emerge. I wanted to share what I like so much about Clojure with the
global community of developers. For that, I would need a means of clearly expressing
ideas that are mostly unfamiliar to developers who do not know Clojure.
 I’ve always loved inventing stories, but would my invented dialogues be taken seri-
ously by programmers? Certainly, Plato had invented stories with his “Socratic Dia-
logues” to transmit the teachings of his teacher. Likewise, Rabbi Judah Halevi had
invented the story of the king of the Khazars to explain the foundations of Judaism.
But these two works are in the realm of thought, not practice!
 I then remembered a management book I had read a few years ago, called The Goal
(North River Press, 2014). In this book, Eliyahu Goldratt invents the story of a plant
manager who manages to save his factory thanks to the principles coming from the
theory of constraints. Plato, Judah Halevi, and Eliyahu Goldratt legitimized my crazy
desire to write a story to share ideas.
xviiiacknowledgments
First and foremost, I want to thank my beloved, Karine. You believed in me since the
beginning of this project. You always manage to see the light, even when it hides
behind several layers of darkness. To my wonderful children, Odaya, Orel, Advah,
Nehoray, and Yair, who were the first audience for the stories I invented when I was a
young daddy. You are the most beautiful story I ever wrote!
 There are numerous other folks to whom I want to also extend my thanks, includ-
ing Joel Klein, for all the fascinating and enriching discussions on the art and the soul;
to Meir Armon for helping me clarify what content should not be included in the
book; to Rich Hickey for inventing Clojure, such a beautiful language, which embraced
data-oriented programming before it even had a name; to Christophe Grand, whose
precious advice helped me to distill the first three principles of data-oriented pro-
gramming; to Mark Champine, for reviewing the manuscript so carefully and provid-
ing many valuable suggestions; to Eric Normand, for your encouragement and, in
particular, your advice on the application of data-oriented programming in Java; to
Bert Bates, for teaching me the secrets of writing a good book; and to Ben Button, for
reviewing the chapters that deal with JSON Schema.
 My thanks to all the folks at Manning Publications, especially Mike Stephens, for
agreeing to continue working with me despite the failure of my first book; Elesha
Hyde, for your availability and your attention to the smallest details; Marius Butuc, for
your enthusiastic positive feedback from reading the first chapter; Linda Kotlyarsky,
for formulating the chapter descriptions in such a fun way; and to Frances Buran for
improving the clarity of the text and the flow of the story.
ACKNOWLEDGMENTS xix
 To all the reviewers, Alex Gout, Allen Ding, Andreas Schabus, Andrew Jennings,
Andy Kirsch, Anne Epstein, Berthold Frank, Christian Kreutzer-Beck, Christopher
Kardell, Dane Balia, Dr. Davide Cadamuro, Elias Ilmari Liinamaa, Ezra Simeloff,
George Thomas, Giri S., Giuliano Araujo Bertoti, Gregor Rayman, J. M. Borovina
Josko, Jerome Meyer, Jesús A. Juárez Guerrero, John D. Lewis, Jon Guenther, Kelum
Prabath Senanayake, Kelvin Johnson, Kent R. Spillner, Kim Gabrielsen, Konstantin
Eremin, Marcus Geselle, Mark Elston, Matthew Proctor, Maurizio Tomasi, Michael
Aydinbas, Milorad Imbra, Özay Duman, Raffaella Ventaglio, Ramanan Nararajan,
Rambabu Posa, Saurabh Singh, Seth MacPherson, Shiloh Morris, Victor Durán,
Vincent Theron, William E. Wheeler, Yogesh Shetty, and Yvan Phelizot, your sugges-
tions helped make this a better book. 
 Finally, I’d like to mention my cousin Nissim, whom a band of barbarians did not
allow to flourish.
xxabout this book
Data-Oriented Programming  was written to help developers reduce the complexity of the
systems they build. The ideas in this book are mostly applicable to systems that manip-
ulate information—systems like frontend applications, backend web servers, or web
services.
Who should read this book?
Data-Oriented Programming  is for frontend, backend, and full stack developers with a
couple of years of experience in a high-level programming language like Java, C#,
C++, Ruby, or Python. For object-oriented programming developers, some ideas pre-
sented in this book might take them out of their comfort zone and require them to
unlearn some of the programming paradigms they feel so much at ease with. For func-
tional programming developers, this book will be a little easier to digest but should
deliver some nice surprises as well.
How this book is organized: A road map
This book tells a story that illustrates the value of data-oriented programming (DOP)
and how to apply its principles in real-life production systems. My suggestion is to fol-
low the story and read the chapters in order. However, if some chapters trigger your
curiosity more than the others, be aware that the material in part 1 and in chapter 7
are required to understand part 2 and part 3.
 Throughout the book, we use Lodash ( https:/ /lodash.com/ ) to illustrate how to
manipulate data with generic functions. In case you are reading a code snippet that
ABOUT THIS BOOK xxi
uses a Lodash function that you are unfamiliar with, you can refer to appendix D to
understand the behavior of the function.
 Part 1, Flexibility , contains six chapters and shines a spotlight on the challenges of
traditional object-oriented programming (OOP) and puts data-oriented program-
ming (DOP) center stage, revealing how to build flexible systems by using DOP’s basic
principles. The chapters line up this way:
In chapter 1, Complexity of object-oriented programming , we look at the complexity
of OOP. Then, our DOP saga begins! Listen in on a conversation between
Theo, a senior developer, and his up-and-coming colleague, Dave. Feel empa-
thy for Theo struggling with OOP complexity and discover an excellent rea-
son for trying a different programming paradigm.
Chapter 2, Separation between code and data , finds our friend Theo searching for a
solution that will reduce complexity and increase the flexibility of systems. His
job is on the line. Enter Joe, an experienced developer who has an answer for
him—DOP. Discover how DOP Principle #1 helps to reduce complexity of
information systems.
Chapter 3, Basic data manipulation , explores how we can liberate our data from
its encapsulation in class rigidity and manipulate it freely with generic functions
by applying DOP Principle #2. Vive la révolution!
Chapter 4, State management , explores state management with a multiversion
approach that lets us go back in time by restoring the system to a previous state
because, in DOP, state is nothing more than data. Time travel is real—in DOP!
Chapter 5, Basic concurrency control , helps us to get high throughput of reads and
writes in a concurrent system by applying an optimistic concurrency control
strategy. No rose-colored glasses required!
Chapter 6, Unit tests , offers a cup of joe . . . with Joe! Our friend Joe proves that
unit testing data-oriented code is so easy you can tackle it in a coffee shop. Grab
a cuppa and learn why it’s so straightforward—even for mutations!—as you
write a DOP unit test hands-on with Joe. It’s cool beans!
Part 2, Scalability , illustrates how to build a DOP system at scale with a focus on data val-
idation, multi-threaded environments, large data collections, and database access and
web services. Need to supersize your system? No problem!
Chapter 7, Basic data validation , teaches us how to ensure that data going in and
out of our systems is valid, just in case . . . because, as Joe says, you are not
forced to validate data in DOP, but you can when you need to. To validate or
not to validate, that is the question!
Chapter 8, Advanced concurrency control , discusses how, after our friend Joe breaks
down the implementation details of the atom mechanism, we’ll learn to man-
age the whole system state in a thread-safe way without using any locks. You
won’t know complexity from atom—up and atom!
ABOUT THIS BOOK xxii
Chapter 9, Persistent data structures , moves to a more academic setting where our
friend Joe unveils the internal details of a safer and more scalable way to pre-
serve data immutability as well as how to implement it efficiently, no matter the
data size. Class is now in session!
Chapter 10, Database operations , teaches us how to represent, access, and manip-
ulate data from the database in a way that offers added flexibility, and—you
guessed it!—less complexity.
Chapter 11, Web services , lets us discover the simplicity of communicating with
web services. We’ll learn what Joe means when he says, “We should build the
insides of our systems like we build the outsides.”
Part 3, Maintainability , levels up to the DOP techniques of advanced data validation,
polymorphism, eloquent code, and debugging techniques, which are vital when
you’re working in a team. Welcome to the team!
Chapter 12, Advanced data validation , allows us to discover the shape of things to
come. Here, you’ll learn how to validate data when it flows inside the system,
allowing you to ease development by defining the expected shape of function
arguments and return values.
Chapter 13, Polymorphism , takes us along with Theo and Dave for a class in the
countryside—a fitting place to play with animals and learn about polymorphism
without objects via multimethods.
Chapter 14, Advanced data manipulation , lets us see how Dave and Theo apply
Joe’s sage advice to turn tedious code into eloquent code as they create their own
data manipulation tools. “Put the cart before the horse.”—another gem from Joe!
Chapter 15, Debugging , takes Dave and Theo to the museum for one last “hur-
rah” as they create an innovative solution for reproducing and fixing bugs.
This book also has four appendices:
Appendix A, Principles of data-oriented programming , summarizes each of the four
DOP principles that are covered in detail in part 1 and illustrates how each
principle can be applied to both FP and OOP languages. It also describes the
benefits of each principle and the costs of adherence to each.
Appendix B, Generic data access in statically-typed languages , presents various ways
to provide generic data access in statically-typed programming languages like
Java and C#.
Appendix C, Data-oriented programming: A link in the chain of programming para-
digms , explores the ideas and trends that have inspired DOP. We look at the dis-
coveries that make it applicable in production systems at scale.
Appendix D, Lodash reference , summarizes the Lodash functions that we use
throughout the book to illustrate how to manipulate data with generic func-
tions without mutating it.
ABOUT THIS BOOK xxiii
About the code
Most of the code snippets in this book are in JavaScript. We chose JavaScript for two
reasons:
JavaScript supports both functional programming and object-oriented program-
ming styles.
The syntax of JavaScript is easy to read in the sense that, even if you are not
familiar with JavaScript, you can read a piece of JavaScript code at a high level
as though it were pseudocode.
To make it easy for readers from any programming language to read the code snip-
pets, we have limited ourselves to basic JavaScript syntax and have avoided the use of
advanced language features like arrow functions and async notation. Where there was
a conceptual challenge in applying an idea to a statically-typed language, we have
added code snippets in Java.
 Code appears throughout the text and as separate code snippets in a fixed-width
font  like  this.  In many cases, the original source code has been reformatted. We’ve
added line breaks and reworked indentation to accommodate the available page space
in the book. Code annotations also accompany some of the listings, highlighting import-
ant concepts.
 You can get executable snippets of code from the liveBook (online) version of this
book at https:/ /livebook.manning.com/book/data-oriented-programming , or from
the book’s Github link here: https:/ /github.com/viebel/data-oriented-programming .
liveBook discussion forum
Purchase of Data-Oriented Programming includes free access to liveBook, Manning’s
online reading platform. Using liveBook’s exclusive discussion features, you can
attach comments to the book globally or to specific sections or paragraphs. It’s a snap
to make notes for yourself, ask and answer technical questions, and receive help from
the author and other users. To access the forum, go to https:/ /livebook.manning.com/
book/data-oriented-programming/discussion . You can also learn more about Man-
ning’s forums and the rules of conduct at https:/ /livebook.manning.com/discussion .
 Manning’s commitment to our readers is to provide a venue where a meaningful
dialogue between individual readers and between readers and the author can take
place. It is not a commitment to any specific amount of participation on the part of
the author, whose contribution to the forum remains voluntary (and unpaid). We sug-
gest you try asking the author some challenging questions lest his interest stray! The
forum and the archives of previous discussions will be accessible from the publisher’s
website as long as the book is in print.
xxivabout the author
YEHONATHAN  SHARVIT  has over 20 years of experience as a soft-
ware engineer, programming with C++, Java, Ruby, JavaScript,
Clojure, and ClojureScript, both in the backend and the front-
e n d .  A t  t h e  t i m e  o f  w r i t i n g  t h i s  b o o k ,  h e  w o r k s  a s  a  s o f t w a r e
architect at Cycognito, building software infrastructures for
high-scale data pipelines. He shares his passion about program-
ming on his blog ( https:/ /blog.klipse.tech/ ) and at tech confer-
ences. You can follow him on Twitter ( https:/ /twitter.com/viebel ).

xxvabout the cover illustration
The figure on the cover of Data-Oriented Programming  is “Fille de l’Isle Santorin,” or
“Girl from the island of Santorini,” taken from a collection by Jacques Grasset de
Saint-Sauveur, published in 1797. Each illustration is finely drawn and colored by hand. 
 In those days, it was easy to identify where people lived and what their trade or sta-
tion in life was just by their dress. Manning celebrates the inventiveness and initiative
of the computer business with book covers based on the rich diversity of regional cul-
ture centuries ago, brought back to life by pictures from collections such as this one.
xxvidramatis personae
 THEO, senior developer
 NANCY, entrepreneur
 MONICA, manager, Theo’s boss
 DAVE, junior developer, Theo’s colleague
 JOE, independent programmer
 KAY, therapist, Joe’s wife
 JANE, Theo’s wife
 NERIAH, Joe’s son
 AURELIA, Joe’s daughter
The story takes place in San Francisco.
Part 1
Flexibility
It’s Monday morning. Theodore is sitting with Nancy on the terrace of La Vita è
Bella, an Italian coffee shop near the San Francisco Zoo. Nancy is an entrepreneur
looking for a development agency for her startup company, Klafim. Theo works for
Albatross, a software development agency that seeks to regain the trust of startups.
Nancy and her business partner have raised seed money for Klafim, a social net-
work for books. Klafim’s unique value proposition is to combine the online world
with the physical world by allowing users to borrow books from local libraries and
then to meet online to discuss the books. Most parts of the product rely on the inte-
gration of already existing online services. The only piece that requires software
development is what Nancy calls a Global Library Management System. Their discus-
sion is momentarily interrupted by the waiter who brings Theo his tight espresso and
Nancy her Americano with milk on the side.
Theo In your mind, what’s a Global Library Management System?
Nancy It’s a software system that handles the basic housekeeping functions of a
library, mainly around the book catalog and the library members.
Theo Could you be a little bit more specific?
Nancy Sure. For the moment, we need a quick prototype. If the market response
to Klafim is positive, we will move forward with a big project.
Theo What features do you need for the prototype phase?
Nancy grabs the napkin under her coffee mug and writes down a couple of bulleted
points on the napkin.
 
 
2 PART 1 Flexibility
Theo Well, that’s pretty clear.
Nancy How much time would it take for your company to deliver the prototype?
Theo I think we should be able to deliver within a month. Let’s say Wednesday the
30th.
Nancy That’s too long. We need it in two weeks!
Theo That’s tough! Can you cut a feature or two?
Nancy Unfortunately, we cannot cut any feature, but if you like, you can make the
search very basic.
(Theo really doesn’t want to lose this contract, so he’s willing to work hard and sleep later.)
Theo I think it should be doable by Wednesday the 16th.
Nancy Perfect!The requirements for the Klafim prototype
Two kinds of library users are members and librarians.
Users log in to the system via email and password.
Members can borrow books.
Members and librarians can search books by title or by author.
Librarians can block and unblock members (e.g., when they are late in return-
ing a book).
Librarians can list the books currently lent to a member.
There could be several copies of a book.
The book belongs to a physical library.
3Complexity of object-
oriented programming
A capricious entrepreneur
In this chapter, we’ll explore why object-oriented programming  (OOP) systems tend to
be complex. This complexity is not related to the syntax or the semantics of a specific
OOP language. It is something that is inherent to OOP’s fundamental insight—
programs should be composed from objects, which consist of some state, together
with methods for accessing and manipulating that state.
 Over the years, OOP ecosystems have alleviated this complexity by adding new
features to the language (e.g., anonymous classes and anonymous functions) and
by developing frameworks that hide some of this complexity, providing a simpler
interface for developers (e.g., Spring and Jackson in Java). Internally, the frame-
works rely on the advanced features of the language such as reflection and custom
annotations.
 This chapter covers
The tendency of OOP to increase system 
complexity
What makes OOP systems hard to understand
The cost of mixing code and data together into 
objects
 This chapter is not meant to be read as a critical analysis of OOP. Its purpose is to
raise your awareness of the tendency towards OOP’s increased complexity as a pro-
gramming paradigm. Hopefully, it will motivate you to discover a different program-
ming paradigm, where system complexity tends to be reduced. This paradigm is
known as data-oriented programming  (DOP). 
1.1 OOP design: Classic or classical?
 NOTE Theo, Nancy, and their new project were introduced in the opener for part 1.
Take a moment to read the opener if you missed it.
Theo gets back to the office with Nancy’s napkin in his pocket and a lot of anxiety in his
heart because he knows he has committed to a tough deadline. But he had no choice! Last
week, Monica, his boss, told him quite clearly that he had to close the deal with Nancy no
matter what.
Albatross, where Theo works, is a software consulting company with customers all over
the world. It originally had lots of customers among startups. Over the last year, however,
many projects were badly managed, and the Startup department lost the trust of its cus-
tomers. That’s why management moved Theo from the Enterprise department to the
Startup department as a Senior Tech lead. His job is to close deals and to deliver on time.
1.1.1 The design phase
Before rushing to his laptop to code the system, Theo grabs a sheet of paper, much big-
ger than a napkin, and starts to draw a UML class diagram of the system that will imple-
ment the Klafim prototype. Theo is an object-oriented programmer. For him, there is no
question—every business entity is represented by an object, and every object is made
from a class.
Theo spends some time thinking about the organization of the system. He identifies the
main classes for the Klafim Global Library Management System.The requirements for the Klafim prototype
There are two kinds of users: library members and librarians.
Users log in to the system via email and password.
Members can borrow books.
Members and librarians can search books by title or by author.
Librarians can block and unblock members (e.g., when they are late in return-
ing a book).
Librarians can list the books currently lent to a member.
There can be several copies of a book.
A book belongs to a physical library.
5 1.1 OOP design: Classic or classical?
That was the easy part. Now comes the difficult part: the relations between the classes.
After two hours or so, Theo comes up with a first draft of a design for the Global Library
Management System. It looks like the diagram in figure 1.1.
 NOTE The design presented here doesn’t pretend to be the smartest OOP design:
experienced OOP developers would probably use a couple of design patterns to sug-
gest a much better design. This design is meant to be naive and by no means covers all
the features of the system. It serves two purposes:
For Theo, the developer , it is rich enough to start coding.
For me, the author of the book , it is rich enough to illustrate the complexity of a
typical OOP system.
Theo feels proud of himself and of the design diagram he just produced. He definitely
deserves a cup of coffee!
Near the coffee machine, Theo meets Dave, a junior software developer who joined
Albatross a couple of weeks ago. Theo and Dave appreciate each other, as Dave’s curiosity
leads him to ask challenging questions. Meetings near the coffee machine often turn into
interesting discussions about programming.
Theo Hey Dave! How’s it going?
 Dave Today? Not great. I’m trying to fix a bug in my code! I can’t understand why
the state of my objects always changes. I’ll figure it out though, I’m sure. How’s
your day going?
Theo I just finished the design of a system for a new customer.
Dave Cool! Would it be OK for me to see it? I’m trying to improve my design skills.
Theo Sure! I have the diagram on my desk. We can take a look now if you like. The main classes of the library management system
Library —The central part of the system design.
Book—A book.
BookItem —A book can have multiple copies, and each copy is considered as
a book item.
BookLending —When a book is lent, a book lending object is created.
Member —A member of the library.
Librarian —A librarian.
User—A base class for Librarian  and Member .
Catalog —Contains a list of books.
Author —A book author.
1.1.2 UML 101
Latte in hand, Dave follows Theo to his desk. Theo proudly shows Dave his piece of art: the
UML diagram for the Library Management System (figure 1.1). Dave seems really excited.
Dave Wow! Such a detailed class diagram.
Theo Yeah. I’m pretty happy with it.LibrarianC
blockMember(member: Member) : Bool
unblockMember(member: Member) : Bool
addBookItem(bookItem: BookItem) : BookItem
getBookLendingsOfMember(member: Member) : List<BookLending>
MemberC
isBlocked() : Bool
block() : Bool
unblock() : Bool
returnBook(bookLending: BookLending) : Bool
checkout(bookItem: BookItem) : BookLendingCatalogC
search(searchCriteria, queryStr) : List<Book>
addBookItem(librarian: Librarian, bookItem: BookItem) : BookItemLibraryC
name : String
address : String
BookC
id : String
title : String
AuthorC
id : String
fullName: String
BookItemC
id : String
libId: String
checkout(member: Member) : BookLending
BookLendingC
id : String
lendingDate : date
dueDate : date
isLate() : Bool
returnBook() : BoolUserC
id : String
email : String
password : String
login() : Bool*
*
**
*
*
*
Figure 1.1 A class diagram for Klafim’s Global Library Management System
7 1.1 OOP design: Classic or classical?
Dave The thing is that I can never remember the meaning of the different arrows.
Theo There are four types of arrows in my class diagram: composition , association ,
inheritance , and usage .
Dave What’s the difference between composition and association?
 NOTE Don’t worry if you’re not familiar with OOP jargon. We’re going to leave it
aside in the next chapter.
Theo It’s all about whether the objects can live without each other. With composi-
tion, when one object dies, the other one dies too. While in an association rela-
tion, each object has an independent life.
TIP In a composition relation, when one object dies, the other one also dies. While
in an association relation, each object has an independent life cycle.
In the class diagram, there are two kinds of composition symbolized by an arrow with
a plain diamond at one edge and an optional star at the other edge. Figure 1.2 shows
the relation between:
A Library  that owns a Catalog —A one-to-one composition. If a Library  object
dies, then its Catalog  object dies with it.
A Library  that owns many Member s—A one-to-many composition. If a Library
object dies, then all its Member  objects die with it.
TIP A composition relation is represented by a plain diamond at one edge and an
optional star at the other edge.
Dave Do you have association relations in your diagram?
Theo Take a look at the arrow between Book  and Author . It has an empty diamond
and a star at both edges, so it’s a many-to-many association relation.
A book can be written by multiple authors, and an author can write multiple books.
Moreover, Book  and Author  objects can live independently. The relation between
books and authors is a many-to-many association (figure 1.3).CatalogC
List<Book> search(searchCriteria, queryStr)
BookItem addBookItem(librarian: Librarian, bookItem: BookItem)LibraryC
name : String
address : StringMemberC *
Figure 1.2 The two kinds of 
composition: one-to-one and 
one-to-many. In both cases, 
when an object dies, the 
composed object dies with it.
TIP A many-to-many  association relation is represented by an empty diamond and a
star at both edges.
Dave I also see a bunch of dashed arrows in your diagram.
Theo Dashed arrows are for usage relations: when a class uses a method of another
class. Consider, for example, the Librarian::blockMember  method. It calls
Member::block .
TIP Dashed arrows indicate usage  relations (figure 1.4), for instance, when a class
uses a method of another class.
Dave I see. And I guess a plain arrow with an empty triangle, like the one between
Member  and User , represents inheritance.
Theo Absolutely!
TIP Plain arrows with empty triangles represent class inheritance  (figure 1.5), where
the arrow points towards the superclass. BookC
id : String
title : String
AuthorC
id : String
fullName: String*
*
Figure 1.3 Many-to-many association relation: 
each object lives independently.
CCLibrarian
Bool isBlocked()
Bool block()
Bool unblock()
Bool returnBook(bookLending: BookLending)
BookLending checkout(bookItem: BookItem)CMemberBool blockMember(member: Member)
Bool unblockMember(member: Member)
BookItem addBookItem(bookItem: BookItem)
List<BookLending> getBookLendingsOfMember(member: Member)
Figure 1.4 Usage relation: a class 
uses a method of another class.
9 1.1 OOP design: Classic or classical?
1.1.3 Explaining each piece of the class diagram
Dave Thanks for the UML refresher! Now I think I can remember what the different
arrows mean.
Theo My pleasure. Want to see how it all fits together?
Dave What class should we look at first?
Theo I think we should start with Library .
THE LIBRARY  CLASS
The Library  is the root class of the library system. Figure 1.6 shows the system structure.CCMember
isBlocked() : Bool
block() : Bool
unblock() : Bool
checkout(bookItem: BookItem) : BookLendingreturnBook(bookLending : BookLending) : Bool
UserC
id : String
email : String
password : String
login() : BoolFigure 1.5 Inheritance relation: a class 
derives from another class.
**name : String
address : StringCCLibrary
CMember
Bool isBlocked()
Bool block()
Bool unblock()
Bool returnBook(bookLending: BookLending)
BookLending checkout(bookItem: BookItem)CCatalog
List<Book> search(searchCriteria, queryStr)
BookItem addBookItem(librarian: Librarian,
bookItem: BookItem)
CCLibrarian
Bool blockMember(member: Member)
Bool unblockMember(member: Member)
BookItem addBookItem(bookItem: BookItem)
List<BookLending> getBookLendingsOfMember
(member: Member)
Figure 1.6 The Library  class
In terms of code (behavior), a Library  object does nothing on its own. It delegates
everything to the objects it owns. In terms of data, a Library  object owns
Multiple Member  objects
Multiple Librarian  objects
A single Catalog  object
 NOTE In this book, we use the terms code and behavior  interchangeably. 
LIBRARIAN , MEMBER , AND USER CLASSES
Librarian  and Member  both derive from User . Figure 1.7 shows this relation.
The User  class represents a user of the library:
In terms of data members, it sticks to the bare minimum: it has an id, email ,
and password  (with no security and encryption for now).
In terms of code, it can log in via login .
The Member  class represents a member of the library:
It inherits from User .
In terms of data members, it has nothing more than User .
In terms of code, it can
– Check out a book via checkout .
– Return a book via returnBook .
– Block itself via block .
– Unblock itself via unblock .
– Answer if it is blocked via isBlocked .
It owns multiple BookLending  objects.
It uses BookItem  in order to implement checkout .CMember
isBlocked() : Bool
block() : Bool
unblock() : Bool
returnBook(bookLending : BookLending) : Bool
checkout(bookItem: BookItem) : BookLendingCLibrarian
blockMember(member: Member) :  Bool
unblockMember(member: Member) : Bool
addBookItem(bookItem: BookItem) : BookItem
: Member) :
CCUser
id : String
email : String
password : String
login() : Bool
Figure 1.7 Librarian  and Member  derive from User .
11 1.1 OOP design: Classic or classical?
The Librarian  class represents a librarian:
It derives from User .
In terms of data members, it has nothing more than User .
In terms of code, it can
– Block and unblock a Member .
– List the member’s book lendings via getBookLendings .
– Add book items to the library via addBookItem .
It uses Member  to implement blockMember , unblockMember , and getBook-
Lendings .
It uses BookItem  to implement checkout .
It uses BookLending  to implement getBookLendings . 
THE CATALOG  CLASS
The Catalog  class is responsible for the management of the books. Figure 1.8 shows
the relation among the Catalog , Librarian , and Book  classes. In terms of code, a
Catalog  object can
Search books via search .
Add book items to the library via addBookItem .
A Catalog  object uses Librarian  in order to implement addBookItem . In terms of
data, a Catalog  owns multiple Book  objects. 
THE BOOK CLASS
Figure 1.9 presents the Book  class. In terms of data, a Book  object
Should have as its bare minimum an id and a title .
Is associated with multiple Author  objects (a book might have multiple authors).
Owns multiple BookItem  objects, one for each copy of the book. *
Bool blockMember(member: Member)
Bool unblockMember(member: Member)CLibrarian
BookItem addBookItem(bookItem: BookItem)
List<BookLending> getBookLendingsOfMember (member: Member)CCatalog
List<Book> search(searchCriteria, queryStr)
BookItem addBookItem(librarian: Librarian, bookItem: BookItem)
BookC
id : String
title : String
Figure 1.8 The Catalog  class
THE BOOKITEM CLASS
The BookItem  class represents a book copy, and a book could have many copies. In
terms of data, a BookItem  object
Should have as its bare minimum data for members: an id and a libId  (for its
physical library ID).
Owns multiple BookLending  objects, one for each time the book is lent.
In terms of code, a BookItem  object can be checked out via checkout . 
1.1.4 The implementation phase
After this detailed investigation of Theo’s diagrams, Dave lets it sink in as he slowly sips his
coffee. He then expresses his admiration to Theo.
Dave Wow! That’s amazing!
Theo Thank you.
Dave I didn’t realize people were really spending the time to write down their design
in such detail before coding.
Theo I always do that. It saves me lot of time during the coding phase.
Dave When will you start coding?
Theo When I finish my latte.
Theo grabs his coffee mug and notices that his hot latte has become an iced latte. He was
so excited to show his class diagram to Dave that he forgot to drink it!* **BookC
id : String
title : String
AuthorC
id : String
fullName: StringBookItemC
id : String
Iibld: String
BookLending checkout(member: Member)
BookLendingC
id : String
lendingDate : date
dueDate : date
Bool isLate()
Bool returnBook() Figure 1.9 The Book  class
13 1.2 Sources of complexity
1.2 Sources of complexity
While Theo is getting himself another cup of coffee (a cappuccino this time), I
would like to challenge his design. It might look beautiful and clear on the paper,
but I claim that this design makes the system hard to understand. It’s not that Theo
picked the wrong classes or that he misunderstood the relations among the classes.
It goes much deeper:
It’s about the programming paradigm he chose to implement the system.
It’s about the object-oriented paradigm.
It’s about the tendency of OOP to increase the complexity of a system.
TIP OOP has a tendency to create complex systems.
Throughout this book, the type of complexity  I refer to is that which makes systems
hard to understand as defined in the paper, “Out of the Tar Pit,” by Ben Moseley
and Peter Marks (2006), available at http:/ /mng.bz/enzq . It has nothing to do with
the type of complexity that deals with the amount of resources consumed by a pro-
gram. Similarly, when I refer to simplicity , I mean not complex (in other words, easy
to understand).
 Keep in mind that complexity and simplicity (like hard and easy) are not absolute
but relative concepts. We can compare the complexity of two systems and determine
whether system A is more complex (or simpler) than system B.
 NOTE Complexity in the context of this book means hard to understand .
As mentioned in the introduction of this chapter, there are many ways in OOP to
alleviate complexity. The purpose of this book is not be critical of OOP, but rather
to present a programming paradigm called data-oriented programming  (DOP) that
tends to build systems that are less complex. In fact, the DOP paradigm is compati-
ble with OOP.
 If one chooses to build an OOP system that adheres to DOP principles, the system
will be less complex. According to DOP, the main sources of complexity in Theo’s sys-
tem (and of many traditional OOP systems) are that
Code and data are mixed.
Objects are mutable.
Data is locked in objects as members.
Code is locked into classes as methods.
This analysis is similar to what functional programming (FP) thinks about traditional
OOP. However, as we will see throughout the book, the data approach that DOP takes
in order to reduce system complexity differs from the FP approach. In appendix A, we
illustrate how to apply DOP principles both in OOP and in FP styles.
TIP DOP is compatible both with OOP and FP.
In the remaining sections of this chapter, we will illustrate each of the previous
aspects, summarized in table 1.1. We’ll look at this in the context of the Klafim project
and explain in what sense these aspects are a source of complexity.
1.2.1 Many relations between classes
One way to assess the complexity of a class diagram is to look only at the entities and
their relations, ignoring members and methods, as in figure 1.10. When we design a
system, we have to define the relations between different pieces of code and data.
That’s unavoidable.
TIP In OOP, code and data are mixed together in classes: data as members  and code as
methods .Table 1.1 Aspects of OOP and their impact on system complexity
Aspect Impact on complexity
Code and data are mixed. Classes tend to be involved in many relations.
Objects are mutable. Extra thinking is needed when reading code.
Objects are mutable. Explicit synchronization is required on multi-threaded environments.
Data is locked in objects. Data serialization is not trivial.
Code is locked in classes. Class hierarchies are complex.
* *
***
*LibrarianC BookC
AuthorC
BookItemCCatalogC
BookLendingCLibraryC
MemberC
UserC
Figure 1.10 A class 
diagram overview for 
Klafim’s Library 
Management System
15 1.2 Sources of complexity
From a system analysis perspective, the fact that code and data are mixed together
makes the system complex in the sense that entities tend to be involved in many rela-
tions. In figure 1.11, we take a closer look at the Member  class. Member  is involved in five
relations: two data relations and three code relations.
Data relations:
–Library  has many Member s.
–Member  has many BookLending s.
Code relations:
–Member  extends User .
–Librarian  uses Member .
–Member  uses BookItem .
Imagine for a moment that we were able, somehow, to split the Member  class into two
separate entities:
MemberCode  for the code
MemberData  for the data
Instead of a Member  class with five relations, we would have the diagram shown in fig-
ure 1.12 with:
A MemberCode  entity and three relations.
A MemberData  entity and two relations.LibraryCLibrarianC
BookItemC BookLendingC UserCMemberC*
*
Figure 1.11 The class Member  is 
involved in five relations.
LibrarianC
BookItemC UserCMemberCodeCLibraryC
BookLendingCMemberDataC*
*
Figure 1.12 A class diagram where Member  
is split into code and data entities
The class diagram where Member  is split into MemberCode  and MemberData  is made of
two independent parts. Each part is easier to understand than the original diagram.
 Let’s split every class of our original class diagram into code and data entities.
Figure 1.13 shows the resulting diagram. Now the system is made of two indepen-
dent parts:
A part that involves only data entities.
A part that involves only code entities.
TIP A system where every class is split into two independent parts, code and data, is
simpler than a system where code and data are mixed.
The resulting system, made up of two independent subsystems, is easier to understand
than the original system. The fact that the two subsystems are independent means that
each subsystem can be understood separately and in any order. The resulting system
not simpler by accident ; it is a logical consequence  of separating code from data.
TIP A system made of multiple simple independent parts is less complex than a sys-
tem made of a single complex part. 
1.2.2 Unpredictable code behavior
You might be a bit tired after the system-level analysis that we presented in the previ-
ous section. Let’s get refreshed and look at some code.
 Take a look at the code in listing 1.1, where we get the blocked status of a member
and display it twice. If I tell you that when I called displayBlockedStatusTwice , the
program displayed true  on the first console.log  call, can you tell me what the pro-
gram displayed on the second console.log  call?AuthorDataCLibrarianDataC CatalogCodeC
LibrarianCodeC
MemberCodeC
UserCodeC BookItemCBookItemCodeC*
*
*
*
***BookDataC
BookItemDataC
BookLendingDataCBookLendingCodeCLibraryDataC
CatalogDataC MemberDataC
Figure 1.13 A class diagram where every class is split into code and data entities
17 1.2 Sources of complexity
class Member {
  isBlocked;
  displayBlockedStatusTwice() {
    var isBlocked = this.isBlocked;
    console.log(isBlocked);
    console.log(isBlocked);
  }
}
member.displayBlockedStatusTwice();
“Of course, it displayed true  again,” you say. And you are right!
 Now, take a look at a slightly different pseudocode as shown in listing 1.2. Here we
display, twice, the blocked status of a member without assigning a variable. Same ques-
tion as before: if I tell you that when I called displayBlockedStatusTwice , the pro-
gram displayed true  on the first console.log  call, can you tell me what the program
displayed on the second console.log  call?
class Member {
  isBlocked;
  displayBlockedStatusTwice() {
    console.log(this.isBlocked);
    console.log(this.isBlocked);
  }
}
member.displayBlockedStatusTwice();
The correct answer is . . . in a single-threaded environment, it displays true , while in a
multi-threaded environment, it’s unpredictable. Indeed, in a multi-threaded environ-
ment between the two console.log  calls, there could be a context switch that changes
the state of the object (e.g., a librarian unblocked the member). In fact, with a slight
modification, the same kind of code unpredictability could occur even in a single-
threaded environment like JavaScript, when data is modified via asynchronous code
(see the section about Principle #3 in appendix A). The difference between the two
code snippets is that
In the first listing (listing 1.1), we access a Boolean value twice , which is a prim-
itive value.
In the second listing (listing 1.2), we access a member of an object twice.
TIP When data is mutable, code is unpredictable.Listing 1.1 Really simple code
Listing 1.2 Apparently simple code
This unpredictable behavior of the second listing is one of the annoying conse-
quences of OOP. Unlike primitive types, which are usually immutable, object mem-
bers are mutable. One way to solve this problem in OOP is to protect sensitive code
with concurrency safety mechanisms like mutexes, but that introduces issues like a
performance hit and a risk of deadlocks.
 We will see later in the book that DOP treats every piece of data in the same way:
both primitive types and collection types are immutable values. This value treatment for
all citizens  brings serenity to DOP developers’ minds, and more brain cells are avail-
able to handle the interesting pieces of the applications they build.
TIP Data immutability brings serenity to DOP developers’ minds. 
1.2.3 Not trivial data serialization
Theo is really tired, and he falls asleep at his desk. He’s having dream. In his dream, Nancy
asks him to make Klafim’s Library Management System accessible via a REST API using
JSON as a transport layer. Theo has to implement a /search  endpoint that receives a
query in JSON format and returns the results in JSON format. Listing 1.3 shows an input
example of the /search  endpoint, and listing 1.4 shows an output example of the /search
endpoint.
{
  "searchCriteria": "author",
  "query": "albert"
}
[
  {
    "title": "The world as I see it",
    "authors": [
      {
        "fullName": "Albert Einstein"
      }
    ]
  },
  {
    "title": "The Stranger",
    "authors": [
      {
        "fullName": "Albert Camus"
      }
    ]
  }
]Listing 1.3 A JSON input of the /search  endpoint
Listing 1.4 A JSON output of the /search  endpoint
19 1.2 Sources of complexity
Theo would probably implement the /search  endpoint by creating three classes simi-
larly to what is shown in the following list and in figure 1.14. (Not surprisingly, every-
thing in OOP has to be wrapped in a class. Right?)
SearchController  is responsible for handling the query.
SearchQuery  converts the JSON query string into data.
SearchResult  converts the search result data into a JSON string.
The SearchController  (see figure 1.14) would have a single handle  method with the
following flow:
Creates a SearchQuery  object from the JSON query string.
Retrieves searchCriteria  and queryStr  from the SearchQuery  object.
Calls the search  method of the catalog:Catalog  with searchCriteria  and
queryStr  and receives books:List<Book> .
Creates a SearchResult  object with books .
Converts the SearchResult  object to a JSON  string.
What about other endpoints, for instance, those allowing librarians to add book items
through /add-book-item ? Theo would have to repeat the exact same process and cre-
ate three classes:
AddBookItemController  to handle the query
BookItemQuery  to convert the JSON query string into data
BookItemResult  to convert the search result data into a JSON string
The code that deals with JSON deserialization that Theo wrote previously in Search-
Query  would have to be rewritten in BookItemQuery . Same thing for the code that
deals with JSON serialization he wrote previously in SearchResult ; it would have to be
rewritten in BookItemResult .List<Book> search(searchCriteria, queryStr)CCatalogCSearchController
String handle(searchQuery: String)
**
BookC
id : String
title : StringCSearchResult
SearchResult(books: List<Book>)
String toJSON()CSearchQuery
searchCriteria: String
query: String
SearchQuery(jsonString: String)
Figure 1.14 The class diagram for SearchController
 The bad news is that Theo would have to repeat the same process for every end-
point of the system. Each time he encounters a new kind of JSON input or output,
he would have to create a new class and write code. Theo’s dream is turning into a
nightmare!
Suddenly, his phone rings, next to where he was resting his head on the desk. As Theo
wakes up, he realizes that Nancy never asked for JSON. It was all a dream . . . a really bad
dream!
TIP In OOP, data serialization is difficult.
It’s quite frustrating that handling JSON serialization and deserialization in OOP
requires the addition of so many classes and writing so much code—again and again!
The frustration grows when you consider that serializing a search query, a book item
query, or any query is quite similar. It comes down to
Going over data fields.
Concatenating the name of the data fields and the value of the data fields, sepa-
rated by a comma.
Why is such a simple thing so hard to achieve in OOP? In OOP, data has to follow a
rigid shape defined in classes, which means that data is locked in members. There is
no simple way to access data generically.
TIP In OOP, data is locked in classes as members.
We will refine later what we mean by generic access to the data, and we will see how
DOP provides a generic way to handle JSON serialization and deserialization. Until
then, you will have to continue suffering. But at least you are starting to become aware
of this suffering, and you know that it is avoidable.
 NOTE Most OOP programming languages alleviate a bit of the difficulty involved
in the conversion from and to JSON. It either involves reflection, which is definitely a
complex thing, or code verbosity. 
1.2.4 Complex class hierarchies
One way to avoid writing the same code twice in OOP involves class inheritance. Indeed,
when every requirement of the system is known up front, you design your class hier-
archy is such a way that classes with common behavior derive from a base class.
 Figure 1.15 shows an example of this pattern that focuses on the part of our class
diagram that deals with members and librarians. Both Librarian s and Member s need
the ability to log in, and they inherit this ability from the User  class.
So far, so good, but when new requirements are introduced after the system is imple-
mented, it’s a completely different story. Fast forward to Monday, March 29th, at 11:00 AM,
where two days are left before the deadline (Wednesday at midnight).
21 1.2 Sources of complexity
Nancy calls Theo with an urgent request. Theo is not sure if it’s a dream or reality. He
pinches himself and he can feel the jolt. It’s definitely reality!
Nancy How is the project doing?
Theo Fine, Nancy. We’re on schedule to meet the deadline. We’re running our last
round of regression tests now.
Nancy Fantastic! It means we have time for adding a tiny feature to the system, right?
Theo Depends what you mean by “tiny.”
Nancy We need to add VIP members to the system.
Theo What do you mean by VIP members?
Nancy VIP members are allowed to add book items to the library by themselves.
Theo H m m...
Nancy What?
Theo That’s not a tiny change!
Nancy Why?
I’ll ask you the same question Nancy asked Theo: why is adding VIP members to our
system not a tiny task? After all, Theo has already written the code that allows librari-
ans to add book items to the library (it’s in Librarian::addBookItem ). What prevents
him from reusing this code for VIP members? The reason is that, in OOP, the code is
locked into classes as methods.
TIP In OOP, code is locked into classes.
VIP members are members that are allowed to add book items to the library by them-
selves. Theo decomposes the customer requirements into two pieces:CCMember
isBlocked() : Bool
checkout(bookItem: BookItem) : BookLendingreturnBook(bookLending : BookLending) : Bool
UserC
id : String
email : String
password : String
login() : BoolCLibrarian
blockMember(member: Member) : Bool
unblockMember(member: Member) : Bool
addBookItem(bookItem: BookItem) : BookItem
getBookLendingsOfMember(member: Member) : List<BookLending>
Figure 1.15 The part of the 
class diagram that deals with 
members and librarians
VIP members are library members.
VIP members are allowed to add book items to the library by themselves.
Theo then decides that he needs a new class, VIPMember . For the first requirement
(VIP members are library members), it seems reasonable to make VIPMember  derive
from Member . However, handling the second requirement (VIP members are allowed
to add book items) is more complex. He cannot make a VIPMember  derive from
Librarian  because the relation between VIPMember  and Librarian  is not linear:
On one hand, VIP members are like librarians in that they are allowed to add
book items.
On the other hand, VIP members are not l ike  li b rari ans  in t hat  th ey ar e n ot
allowed to block members or list the books lent to a member.
The problem is that the code that adds book items is locked in the Librarian  class.
There is no way for the VIPMember  class to use this code.
 Figure 1.16 shows one possible solution that makes the code of Librarian::add-
BookItem  available to both Librarian  and VIPMember  classes. Here are the changes to
the previous class diagram:
A base class UserWithBookItemRight  extends User .
addBookItem  moves from Librarian  to UserWithBookItemRight .
Both VIPMember  and Librarian  extend UserWithBookItemRight .
It wasn’t easy, but Theo manages to handle the change on time, thanks to an all nighter
coding on his laptop. He was even able to add new tests to the system and run the regres-
sion tests again. However, he was so excited that he didn’t pay attention to the diamondCCMember
isBlocked() : Bool
checkout(bookItem: BookItem) : BookLendingreturnBook(bookLending : BookLending) : BoolCCUserWithBookItemRight
addBookItem(bookItem: BookItem) : BookItem
UserC
id : String
email : String
password : String
login() : BoolCLibrarian
blockMember(member: Member) : Bool
unblockMember(member: Member) : Bool
getBookLendingsOfMember(member: Member) : List<BookLending>VIPMemberC
Figure 1.16 A class diagram for a system with VIP members
23 1.2 Sources of complexity
problem VIPMember  introduced in his class diagram due to multiple inheritance: VIPMember
extends both Member  and UserWithBookItemRight , which both extend User .
Wednesday, March 31, at 10:00 AM (14 hours before the deadline), Theo calls Nancy to
tell her the good news.
Theo We were able to add VIP members to the system on time, Nancy.
Nancy Fantastic! I told you it was a tiny feature.
Theo Yeah, well . . .
Nancy Look, I was going to call you anyway. I just finished a meeting with my business
partner, and we realized that we need another tiny feature before the launch.
Will you be able to handle it before the deadline?
Theo Again, it depends what you mean by “tiny.”
Nancy We need to add Super members to the system.
Theo What do you mean by Super members?
Nancy Super members are allowed to list the books lent to other members.
Theo E r r...
Nancy What?
Theo That’s not a tiny change!
Nancy Why?
As with VIP members, adding Super members to the system requires changes to Theo’s
class hierarchy. Figure 1.17 shows the solution Theo has in mind.
The addition of Super members has made the system really complex. Theo suddenly
notices that he has three diamonds in his class diagram—not gemstones but three “DeadlyUserC
id : String
email : String
password : String
login() : BoolCCMember
isBlocked() : Bool
checkout(bookItem: BookItem) : BookLendingreturnBook(bookLending : BookLending) : BoolCCUserWithBlockMemberRight
blockMember(member: Member) : Bool
unblockMember(member: Member) : BoolCCUserWithBookItemRight
addBookItem(bookItem: BookItem) : BookItemCLibrarian
getBookLendingsOfMember(member: Member) : List<BookLending>VIPMemberC SuperMemberC
Figure 1.17 A class diagram for a system with Super and VIP members
Diamonds of Death” as OOP developers sometimes name the ambiguity that arises when a
class D inherits from two classes B and C, where both inherit from class A!
He tries to avoid the diamonds by transforming the User  class into an interface and
using the composition over inheritance design pattern. But with the stress of the deadline
looming, he isn’t able to use all of his brain cells. In fact, the system has become so com-
plex, he’s unable to deliver the system by the deadline. Theo tells himself that he should
have used composition instead of class inheritance. But, it’s too late now.
TIP In OOP, prefer composition over class inheritance.
At 10:00 PM, two hours before the deadline, Theo calls Nancy to explain the situation.
Theo Look Nancy, we really did our best, but we won’t be able to add Super mem-
bers to the system before the deadline.
Nancy No worries, my business partner and I decided to omit this feature for now.
We’ll add it later.
With mixed feelings of anger and relief, Theo stops pacing around his office. He realizes
he will be spending tonight in his own bed, rather than plowing away on his computer at
the office. That should make his wife happy.
Theo I guess that means we’re ready for the launch tomorrow morning.
Nancy Yes. We’ll offer this new product for a month or so, and if we get good market
traction, we’ll move forward with a bigger project.
Theo Cool. Let’s be in touch in a month then. Good luck on the launch!
Summary
Complexity in the context of this book means hard to understand .
We use the terms code and behavior  interchangeably.
DOP stands for data-oriented programming.
OOP stands for object-oriented programming.
FP stands for functional programming.
In a composition relation , when one object dies, the other one also dies.
A composition relation is represented by a plain diamond at one edge and an
optional star at the other edge.
In an association relation , each object has an independent life cycle.
A many-to-many association relation  is represented by an empty diamond and a
star at both edges.
Dashed arrows indicate a usage relation ; for instance, when a class uses a method
of another class.
Plain arrows with empty triangles represent class inheritance , where the arrow
points towards the superclass.
The design presented in this chapter doesn’t pretend to be the smartest OOP
design. Experienced OOP developers would probably use a couple of design
patterns and suggest a much better diagram.
25 Summary
Traditional OOP systems tend to increase system complexity, in the sense that
OOP systems are hard to understand.
In traditional OOP, code and data are mixed together in classes: data as mem-
bers and code as methods.
In traditional OOP, data is mutable.
The root cause of the increase in complexity is related to the mixing of code
and data together into objects.
When code and data are mixed, classes tend to be involved in many relations.
When objects are mutable, extra thinking is required in order to understand
how the code behaves.
When objects are mutable, explicit synchronization mechanisms are required
on multi-threaded environments.
When data is locked in objects, data serialization  is not trivial.
When code is locked in classes, class hierarchies tend to be complex.
A system where every class is split into two independent parts, code and data, is
simpler than a system where code and data are mixed.
A system made of multiple simple independent parts is less complex than a sys-
tem made of a single complex part.
When data is mutable, code is unpredictable.
A strategic use of design patterns can help mitigate complexity in traditional
OOP to some degree.
Data immutability brings serenity to DOP developers’ minds.
Most OOP programming languages alleviate slightly the difficulty involved the
conversion from and to JSON. It either involves reflection , which is definitely a
complex thing, or code verbosity.
In traditional OOP, data serialization  is difficult.
In traditional OOP, data is locked in classes as members.
In traditional OOP, code is locked into classes.
DOP reduces complexity by rethinking data.
DOP is compatible both with OOP and FP.
26Separation between
code and data
A whole new world
The first insight of DOP is that we can decrease the complexity of our systems by
separating code from data. Indeed, when code is separated from data, our systems
are made of two main pieces that can be thought about separately: data entities and
code modules. This chapter is a deep dive in the first principle of DOP (summa-
rized in figure 2.1).This chapter covers
The benefits of separating code from data
Designing a system where code and data are 
separate
Implementing a system that respects the 
separation between code and data
PRINCIPLE #1 Separate code from data such that the code resides in functions,
whose behavior doesn’t depend on data that is somehow encapsulated in the func-
tion’s context.
27 2.1 The two parts of a DOP system
In this chapter, we’ll illustrate the separation between code and data in the context of
Klafim’s Library Management System that we introduced in chapter 1. We’ll also unveil
the benefits that this separation brings to the system:
The system is simple.  It is easy to understand.
The system is flexible and extensible.  Quite often, it requires no design changes to
adapt to changing requirements.
This chapter focuses on the design of the code in a system where code and data are
separate. In the next chapter, we’ll focus on the design of the data. As we progress in
the book, we’ll discover other benefits of separating code from data. 
2.1 The two parts of a DOP system
While Theo is driving home after delivering the prototype, he asks himself whether the
Klafim project was a success or not. Sure, he was able to satisfy the customer, but it was
more luck than brains. He wouldn’t have made it on time if Nancy had decided to keep
the Super members feature. Why was it so complicated to add tiny features to the system?
Why was the system he built so complex? He thought there should be a way to build more
flexible systems!
The next morning, Theo asks on Hacker News and on Reddit for ways to reduce system
complexity and build flexible systems. Some folks mention using different programming
languages, while others talk about advanced design patterns. Finally, Theo’s attention gets
captured by a comment from a user named Joe. He mentions data-oriented programming  and
claims that its main goal is to reduce system complexity. Theo has never heard this term
before. Out of curiosity, he decides to contact Joe by email. What a coincidence! Joe lives
in San Francisco too. Theo invites him to a meeting in his office.
Joe is a 40-year-old developer. He was a Java developer for nearly a decade before adopt-
ing Clojure around 7 years ago. When Theo tells Joe about the Library Management SystemSeparate code from dataCode modulesFunctionsStateless (static)
Data as ﬁrst argument
RelationsUsage
No inheritance
Data entitiesOnly members
No code
RelationsAssociation
Composition
Figure 2.1 DOP principle #1 summarized: Separate code from data.
he designed and built, and about his struggles to adapt to changing requirements, Joe is
not surprised.
Joe tells Theo that the systems that he and his team have built in Clojure over the last 7
years are less complex and more flexible than the systems he used to build in Java. Accord-
ing to Joe, the systems they build now tend to be much simpler because they follow the
principles of DOP.
Theo I’ve never heard of data-oriented programming. Is it a new concept?
Joe Yes and no. Most of the foundational ideas of data-oriented programming, or
DOP as we like to call it, are well known to programmers as best practices. The
n o v e l t y  o f  D O P ,  h o w e v e r ,  i s  t h a t  i t  c o m b i n e s  b e s t  p r a c t i c e s  i n t o  a  c o h e s i v e
whole.
Theo That’s a bit abstract for me. Can you give me an example?
Joe Sure! Take, for instance, the first insight of DOP. It’s about the relations between
code and data.
Theo You mean the encapsulation of data in objects?
Joe Actually, DOP is against data encapsulation.
Theo Why is that? I thought data encapsulation was a positive programming paradigm.
Joe Data encapsulation has both merits and drawbacks. Think about the way you
designed the Library Management System. According to DOP, the main cause
of complexity and inflexibility in systems is that code and data are mixed
together in objects.
TIP DOP is against  data encapsulation.
Theo It sounds similar to what I’ve heard about functional programming. So, if I
want to adopt DOP, do I need to get rid of object-oriented programming and
learn functional programming?
Joe No, DOP principles are language-agnostic. They can be applied in both object-
oriented and functional programming languages.
Theo That’s a relief! I was afraid that you were going to teach me about monads,
algebraic data types, and higher order functions.
Joe No, none of that is required in DOP.
TIP DOP principles are language-agnostic .
Theo What does the separation between code and data look like in DOP then?
Joe Data is represented by data entities that only hold members. Code is aggre-
gated into modules where all functions are stateless.
Theo What do you mean by stateless functions?
Joe Instead of having the state encapsulated in the object, the data entity is passed
as an argument.
Theo I don’t get that.
Joe Here, let’s make it visual.
29 2.2 Data entities
Joe steps up to a whiteboard and quickly draws a diagram to illustrate his comment. Fig-
ure 2.2 shows Joe’s drawing.
Theo It’s still not clear.
Joe It will become clearer when I show you how it looks in the context of your
Library Management System.
Theo OK. Shall we start with code or with data?
Joe Well, it’s data-oriented programming, so let’s start with data. 
2.2 Data entities
In DOP, we start the design process by discovering the data entities  of our system.
Here’s what Joe and Theo have to say about data entities.
Joe What are the data entities of your system?
Theo What do you mean by data entities?
Joe I mean the parts of your system that hold information.
 NOTE Data entities are the parts of your system that hold information.
Theo Well, it’s a Library Management System, so we have books and members.
Joe Of course, but there are more. One way to discover the data entities of a system
is to look for nouns and noun phrases in the requirements of the system.
Theo looks at Nancy’s requirement napkin. He highlights the nouns and noun phrases
that seem to represent data entities.
Highlighting terms in the requirements that correspond to data entities
There are two kinds of users: library members  and librarians .
Users  log in to the system via email and password.
Members  can borrow books .
Members  and librarians  can search books  by title or by author .
Librarians  can block and unblock members  (e.g., when they are late in return-
ing a book).
Librarians  can list the books currently lent  to a member.
There could be several copies of a book .Separate code from dataCode modules Stateless functions
Data entities Only members
Figure 2.2 The separation between code and data
Joe Excellent. Can you see a natural way to group these entities?
Theo Not sure, but it seems to me that users, members, and librarians form one
group, whereas books, authors, and book copies form another group.
Joe Sounds good to me. What would you call each group?
Theo Probably user management for the first group and catalog for the second
group.
Theo I’m not sure about the relations between books and authors. Should it be asso-
ciation or composition?
Joe Don’t worry too much about the details for the moment. We’ll refine our data
entity design later. For now, let’s visualize the two groups in a mind map.
Theo and Joe confer for a bit. Figure 2.3 shows the mind map they come up with.The data entities of the system organized in a nested list
The catalog data
–Data about books
–Data about authors
–Data about book items
–Data about book lendings
The user management data
–Data about users
–Data about members
–Data about librarians
Library dataCatalogBooks
Authors
Book items
Book lendings
User managementUsers
Members
Librarians Figure 2.3 The data entities of the 
system organized in a mind map
31 2.3 Code modules
The most precise way to visualize the data entities of a DOP system is to draw a data
entity diagram with different arrows for association and composition. We will come
back to data entity diagrams later.
TIP Discover the data entities of your system and then sort them into high-level
groups, either as a nested list or as a mind map.
We will dive deeper into the design and representation of data entities in the next
chapter. For now, let’s simplify things and say that the data of our library system is
made of two high-level groups: user management and catalog. 
2.3 Code modules
The second step of the design process in DOP is to define the code modules. Let’s lis-
ten in on Joe and Theo again.
Joe Now that you have identified the data entities of your system and have
arranged them into high-level groups, it’s time to think about the code part of
your system.
Theo What do you mean by the code part?
Joe One way to think about that is to identity the functionality of your system.
Theo looks again at Nancy’s requirements. This time he highlights the verb phrases that
represent functionality.
In addition, it’s obvious to Theo that members can also return a book. Moreover, there
should be a way to detect whether a user is a librarian or not. He adds those to the require-
ments and then lists the functionality of the system.Highlighting terms in the requirements that correspond to functionality
There are two kinds of users: library members and librarians.
Users log in to the system  via email and password.
Members can borrow books .
Members and librarians can search books  by title or by author.
Librarians can block  and unblock members  (e.g., when they are late in return-
ing a book).
Librarians can list the books currently lent to a member .
There could be several copies of a book.
The functionality of the library system
Search for a book.
Add a book item.
Block a member.
Joe Excellent! Now, tell me what functionality needs to be exposed to the outside
world?
Theo What do you mean by exposed to the outside world?
Joe Imagine that the Library Management System exposes an API over HTTP.
What functionality would be exposed by the HTTP endpoints?
Theo Well, all system functionality would be exposed except checking to see if a user
is a librarian.
Joe OK. Now give each exposed function a short name and gather them together
in a module box called Library .
That takes Theo less than a minute. Figure 2.4 shows the module that contains the
exposed functions of the library devised by Theo.
TIP The first step in designing the code part of a DOP system is to aggregate the
exposed functions into a single module.
Joe Beautiful! You just created your first code module.
Theo To me it looks like a class. What’s the difference between a module and a class?
Joe A module is an aggregation of functions. In OOP, a module is represented
by a class, but in other programming languages, it might be a package or a
namespace.
Theo I see.
Joe The important thing about DOP code modules is that they contain only state-
less functions.
Theo You mean like static methods in Java?
Joe Yes, and the classes of these static methods should not have any data members.(continued)
Unblock a member.
Log a user into the system.
List the books currently lent to a member.
Borrow a book.
Return a book.
Check whether a user is a librarian.
searchBook()
addBookItem()
blockMember()
unblockMember()
getBookLendings()
checkoutBook()
returnBook()CLibrary
Figure 2.4 The Library  module 
contains the exposed functions of the 
Library Management System.
33 2.3 Code modules
Theo So, how do the functions know what piece of information they operate on?
Joe Easy. We pass that as the first argument to the function.
Theo OK. Can you give me an example?
Joe, biting his nails, takes a look at the list of functions of the Library  module in figure 2.4.
He spots a likely candidate.
Joe Let’s take, for example, getBookLendings . In classic OOP, what would its
arguments be?
Theo A librarian ID and a member ID.
Joe So, in traditional OOP, getBookLendings  would be a method of a Library
class that receives two arguments: librarianId  and memberId .
Theo Yep.
Joe Now comes the subtle part. In DOP, getBookLendings  is part of the Library
module, and it receives the LibraryData  as an argument.
Theo Could you show me what you mean?
Joe Sure.
Joe goes over to Theo’s keyboard and starts typing. He enters an example of what a class
method looks like in OOP:
class Library {
  catalog 
  userManagement
  getBookLendings(userId, memberId) {
    // accesses library state via this.catalog and this.userManagement
  }
}
Theo Right! The method accesses the state of the object (in our case, the library
data) via this .
Joe Would you say that the object’s state is an argument of the object’s methods?
Theo I’d say that the object’s state is an implicit argument to the object’s methods.
TIP In traditional OOP, the state of the object is an implicit argument to the meth-
ods of the object.
Joe Well, in DOP, we pass data as an explicit argument. The signature of getBook-
Lendings  would look like this.
class Library {
  static getBookLendings(libraryData, userId, memberId) {
  }
}Listing 2.1 The signature of getBookLendings
Joe The state of the library is stored in libraryData , and libraryData  is passed
to the getBookLendings  static method as an explicit argument.
Theo Is that a general rule?
Joe Absolutely! The same rule applies to the other functions of the Library  mod-
ule and to other modules as well. All of the modules are stateless—they receive
the library data that they manipulate as an argument.
TIP In DOP, functions of a code module are stateless. They receive the data that they
manipulate as an explicit argument, which is usually the first argument.
 NOTE A module is an aggregation of functions. In DOP, the module functions are
stateless.
Theo It reminds me of Python and the way the self  argument appears in method
signatures. Here, let me show you an example.
class Library:
  catalog = {}
  userManagement = {}
  def getBookLendings(self, userId, memberId):
  # accesses library state via self.catalog and self.userManagement
Joe Indeed, but the difference I’m talking about is much deeper than a syntax
change. It’s about the fact that data lives outside the modules.
Theo I got that. As you said, module functions are stateless.
Joe Exactly! Would you like to try and apply this principle across the whole
Library  module?
Theo Sure.
Theo refines the design of the Library  module by including the details about the func-
tions’ arguments. He presents the diagram in figure 2.5 to Joe.
Joe Perfect. Now, we’re ready to tackle the high-level design of our system.
Theo What’s a high-level design in DOP?Listing 2.2 A Python object as an explicit argument in method signatures
CLibrary
searchBook(libraryData, searchQuery)
addBookItem(libraryData, bookItemInfo)
blockMember(libraryData, memberId)
unblockMember(libraryData, memberId)
login(libraryData, loginInfo)
getBookLendings(libraryData, userId)
checkoutBook(libraryData, userId, bookItemId)
returnBook(libraryData, userId, bookItemId)Figure 2.5 The Library  module 
with the functions’ arguments
35 2.3 Code modules
Joe A high-level design in DOP is the definition of modules and the interaction
between them.
Theo I see. Are there any guidelines to help me define the modules?
Joe Definitely. The high-level modules of the system correspond to the high-level
data entities.
Theo You mean the data entities that appear in the data mind map?
Joe Exactly!
Theo looks again at the data mind map (figure 2.6). He focuses on the high-level data enti-
ties library, catalog, and user management. This means that in the system, besides the
Library  module, we have two high-level modules:
The Catalog  module deals with catalog data.
The UserManagement  module deals with user management data.
Theo then draws the high-level design of the Library Management System with the Catalog
and UserManagement  modules. Figure 2.7 shows the addition of these modules, where:
Functions of Catalog  receive catalogData  as their first argument.
Functions of UserManagement  receive userManagementData  as their first argument.Library dataCatalog
User managementFigure 2.6 A mind map of the high-
level data entities of the Library 
Management System
CUserManagementCCatalog
searchBook(catalogData, searchQuery)
addBookItem(catalogData, bookItemInfo)
checkoutBook(catalogData, bookItemId)
returnBook(catalogData, bookItemId)
getBookLendings(catalogData, userId)CLibrary
searchBook(libraryData, searchQuery)
addBookItem(libraryData, bookItemInfo)
blockMember(libraryData, memberId)
unblockMember(libraryData, memberId)
login(libraryData, loginInfo)
getBookLendings(libraryData, userId)
checkoutBook(libraryData, userId, bookItemId)
returnBook(libraryData, userId, bookItemId)
blockMember(userManagementData, memberId)
unblockMember(userManagementData, memberId)
login(userManagementData, loginInfo)
isLibrarian(userManagementData, userId)
Figure 2.7 The modules of the Library Management System with their functions’ arguments
It’s not 100% clear for Theo at this point how the data entities get passed between mod-
ules. For the moment, he thinks of libraryData  as a class with two members:
catalog  holds the catalog data.
userManagement  holds the user management data.
Theo also sees that the functions of Library  share a common pattern. (Later on in this
chapter, we’ll see the code for some functions of the Library  module.)
They receive libraryData  as an argument.
They pass libraryData.catalog  to the functions of Catalog .
They pass libraryData.userManagement  to the functions of UserManagement .
TIP The high-level modules of a DOP system correspond to the high-level data enti-
ties. 
2.4 DOP systems are easy to understand
Theo takes a look at the two diagrams that represent the high-level design of his system:
The data entities in the data mind map in figure 2.8
The code modules in the module diagram in figure 2.9
A bit perplexed, Theo asks Joe:
Theo I’m not sure that this system is better than a traditional OOP system where
objects encapsulate data.
Joe The main benefit of a DOP system over a traditional OOP system is that it’s eas-
ier to understand.
Theo What makes it easier to understand?
Joe The fact that the system is split cleanly into code modules and data entities.
Theo How does that help?
Joe When you try to understand the data entities of the system, you don’t have to
think about the details of the code that manipulates the data entities.
Theo So, when I look at the data mind map of my Library Management System, I can
understand it on its own?
Joe Exactly, and similarly, when you try to understand the code modules of the sys-
tem, you don’t have to think about the details of the data entities manipulated
by the code. There is a clear separation of concerns between the code and the
data.
Theo looks again at the data mind map in figure 2.8. He has kind of an Aha! moment:
Data lives on its own!
 NOTE A DOP system is easier to understand because the system is split into two
parts: data entities and code modules.
37 2.4 DOP systems are easy to understand
Now, Theo looks at the module diagram in figure 2.9. He feels a bit confused and asks Joe
for clarification:
On one hand, the module diagram looks similar to the class diagrams from classic
OOP, boxes for classes and arrows for relations between classes.
On the other hand, the code module diagram looks much simpler than the class
diagrams from classic OOP, but he cannot explain why.
Theo The module diagram seems much simpler than the class diagrams I am used to
in OOP. I feel it, but I can’t put it into words.
Joe The reason is that module diagrams have constraints.Library dataCatalogBooks
Authors
Book items
Book lendings
User managementUsers
Members
LibrariansFigure 2.8 A data mind map of the 
Library Management System
CUserManagementCCatalog
searchBook(catalogData, searchQuery)
addBookItem(catalogData, bookItemInfo)
checkoutBook(catalogData, bookItemId)
returnBook(catalogData, bookItemId)
getBookLendings(catalogData, userId)CLibrary
searchBook(libraryData, searchQuery)
addBookItem(libraryData, bookItemInfo)
blockMember(libraryData, memberId)
unblockMember(libraryData, memberId)
login(libraryData, loginInfo)
getBookLendings(libraryData, userId)
checkoutBook(libraryData, userId, bookItemId)
returnBook(libraryData, userId, bookItemId)
blockMember(userManagementData, memberId)
unblockMember(userManagementData, memberId)
login(userManagementData, loginInfo)
isLibrarian(userManagementData, userId)
Figure 2.9 The modules of the Library Management System with the function arguments
Theo What kind of constraints?
Joe Constraints on the functions we saw before. All the functions are static (or
stateless), but there’s also constraints on the relations between the modules.
TIP All the functions in a DOP module are stateless .
Theo In what way are the relations between modules constrained?
Joe There is a single kind of relation between DOP modules—the usage relation. A
module uses code from another module. There’s no association, no composi-
tion, and no inheritance between modules. That’s what makes a DOP module
diagram easy to understand.
Theo I understand why there is no association and no composition between DOP
modules. After all, association and composition are data relations. But why no
inheritance relation? Does that mean that DOP is against polymorphism?
Joe That’s a great question! The quick answer is that in DOP, we achieve polymor-
phism with a different mechanism than class inheritance. We will talk about it
some day.
 NOTE For a discussion of polymorphism in DOP, see chapter 13.
Theo Now, you’ve piqued my curiosity. I thought inheritance was the only way to
achieve polymorphism.
Theo looks again at the module diagram in figure 2.9. Now he not only feels that this dia-
gram is simpler than traditional OOP class diagrams, he understands why it’s simpler: all
the functions are static, and all the relations between modules are of type usage. Table 2.1
summarizes Theo’s perception.
TIP The only kind of relation between DOP modules is the usage relation.
TIP Each part of a DOP system is easy to understand because it provides constraints. 
2.5 DOP systems are flexible
Theo I see how a sharp separation between code and data makes DOP systems easier
to understand than classic OOP systems. But what about adapting to changes
in requirements?
Joe Another benefit of DOP systems is that it is easy to extend them and to adapt to
changing requirements.Table 2.1 What makes each part of a DOP system easy to understand
System part Constraint on entities Constraints on relations
Data entities Members only (no code) Association and composition
Code modules Stateless functions (no members) Usage (no inheritance)
39 2.5 DOP systems are flexible
Theo I remember that, when Nancy asked me to add Super members and VIP mem-
bers to the system, it was hard to adapt my OOP system. I had to introduce a
few base classes, and the class hierarchy became really complex.
Joe I know exactly what you mean. I’ve experienced the same kind of struggle so
many times. Describe the changes in the requirements for Super members and
VIP members, and I’m quite sure that you’ll see how easy it would be to extend
your DOP system.
Theo opens his IDE and starts to code the getBookLendings  function of the Library
module (see listing 2.3), first without addressing the requirements for Super members.
Theo remembers what Joe told him about module functions in DOP:
Functions are stateless.
Functions receive the data they manipulate as their first argument.
In terms of functionality, getBookLendings  has two parts:
Checks that the user is a librarian.
Retrieves the book lendings from the catalog.
Basically, the code of getBookLendings  has two parts as well:
Calls the isLibrarian  function from the UserManagement  module and passes it
the UserManagementData .
Calls the getBookLendings  function from the Catalog  module and passes it the
CatalogData .
class Library {
  static getBookLendings(libraryData, userId, memberId) {
    if(UserManagement.isLibrarian(libraryData.userManagement, userId)) {
      return Catalog.getBookLendings(libraryData.catalog, memberId);
    } else {
      throw "Not allowed to get book lendings";    
    }
  }
}
class UserManagement {
  static isLibrarian(userManagementData, userId) {
    // will be implemented later     
  }
}The requirements for Super members and VIP members
Super members are members that are allowed to list the book lendings to
other members.
VIP members are members that are allowed to add book items to the library.
Listing 2.3 Getting the book lendings of a member
There are other 
ways to manage 
errors.
In chapter 3, we will see how 
to manage permissions with 
generic data collections.
class Catalog {
  static getBookLendings(catalogData, memberId) {
    // will be implemented later    
  }
}
It’s Theo’s first piece of DOP code and passing around all those data objects— library-
Data , libraryData.userManagement , and libraryData.catalog —feels a bit awkward.
But he did it! Joe looks at Theo’s code and seems satisfied.
Joe Now, how would you adapt your code to Super members?
Theo I would add a function isSuperMember  to the UserManagement  module and
call it from Library.getBookLendings .
Joe Exactly! It’s as simple as that.
Theo types the code on his laptop so that he can show it to Joe. Here’s how Theo adapts
his code for Super members.
class Library {
  static getBookLendings(libraryData, userId, memberId) {
    if(Usermanagement.isLibrarian(libraryData.userManagement, userId) ||
      Usermanagement.isSuperMember(libraryData.userManagement, userId)) {
      return Catalog.getBookLendings(libraryData.catalog, memberId);
    } else {
      throw "Not allowed to get book lendings";  
    }
  }
}
class UserManagement {
  static isLibrarian(userManagementData, userId) {
    // will be implemented later                    
  }
  static isSuperMember(userManagementData, userId) {
    // will be implemented later                    
  }
}
class Catalog {
  static getBookLendings(catalogData, memberId) {
    // will be implemented later    
  }
}
Now, the awkward feeling caused by passing around all those data objects is dominated by
a feeling of relief. Adapting to this change in requirements takes only a few lines of code
and requires no changes in the system design. Once again, Joe seems satisfied.
TIP DOP systems are flexible. Quite often they adapt to changing requirements with-
out changing the system design.Listing 2.4 Allowing Super members to get the book lendings of a memberIn chapter 3, we will see how 
to query data with generic 
data collections.
There are other 
ways to manage 
errors.
In chapter 3, we will see how 
to manage permissions with 
generic data collections.
In chapter 3, we will see how 
to query data with generic 
data collections.
41 2.5 DOP systems are flexible
Theo starts coding addBookItem . He looks at the signature of Library.addBookItem ,
and the meaning of the third argument bookItemInfo  isn’t clear to him. He asks Joe for
clarification.
class Library {
  static addBookItem(libraryData, userId, bookItemInfo) {
  }
}
Theo What is bookItemInfo ?
Joe Let’s call it the book item information. Imagine we have a way to represent this
information in a data entity named bookItemInfo .
Theo You mean an object?
Joe For now, it’s OK to think about bookItemInfo  as an object. Later on, I will
show you how to we represent data in DOP.
Besides this subtlety about how the book item information is represented by book-
ItemInfo , the code for Library.addBookItem  in listing 2.6 is quite similar to the code
Theo wrote for Library.getBookLendings  in listing 2.4. Once again, Theo is amazed by
the fact that adding support for VIP members requires no design change.
class Library {
  static addBookItem(libraryData, userId, bookItemInfo) {
    if(UserManagement.isLibrarian(libraryData.userManagement, userId) ||
      UserManagement.isVIPMember(libraryData.userManagement, userId)) {
      return Catalog.addBookItem(libraryData.catalog, bookItemInfo);
    } else {
      throw "Not allowed to add a book item";   
    }
  }
}
class UserManagement {
  static isLibrarian(userManagementData, userId) {
    // will be implemented later                     
  }
  static isVIPMember(userManagementData, userId) {
    // will be implemented later                     
  }
}
class Catalog {
  static addBookItem(catalogData, memberId) {
    // will be implemented later    
  }
}Listing 2.5 The signature of Library.addBookItem
Listing 2.6 Allowing VIP members to add a book item to the library
There are other 
ways to manage 
errors.
In chapter 3, we will see how 
to manage permissions with 
generic data collections.
In chapter 4, we will see how 
to manage state of the system 
with immutable data.
Theo It takes a big mindset shift to learn how to separate code from data!
Joe What was the most challenging thing to accept?
Theo The fact that data is not encapsulated in objects.
Joe It was the same for me when I switched from OOP to DOP.
Now it’s time to eat! Theo takes Joe for lunch at Simple, a nice, small restaurant near the
office. 
Summary
DOP principles are language-agnostic .
DOP principle #1 is to separate code from data.
The separation between code and data in DOP systems makes them simpler
(easier to understand) than traditional OOP systems.
Data entities  are the parts of your system that hold information.
DOP is against data encapsulation .
The more flexible a system is, the easier it is to adapt to changing requirements.
The separation between code and data in DOP systems makes them more flexi-
ble than traditional OOP systems.
When code is separated from data, we have the freedom to design code and
data in isolation.
We represent data as data entities .
We discover the data entities of our system and sort them into high-level groups,
either as a nested list or as a mind map.
A DOP system is easier to understand than a traditional OOP system because
the system is split into two parts: data entities  and code modules .
In DOP, a code module  is an aggregation of stateless functions.
DOP systems are flexible. Quite often they adapt to changing requirements
without changing the system design.
In traditional OOP, the state of the object is an implicit argument to the meth-
ods of the object.
Stateless functions receive data they manipulate as an explicit argument.
The high-level modules of a DOP system correspond to high-level data entities.
The only kind of relation between code modules  is the usage relation .
The only kinds of relation between data entities  are the association  and the compo-
sition  relation.
For a discussion of polymorphism  in DOP, see chapter 13.
43Basic data manipulation
Meditation and programming
After learning why and how to separate code from data in the previous chapter,
let’s talk about data on its own. In contrast to traditional OOP, where system design
tends to involve a rigid class hierarchy, DOP prescribes that we represent our data
model as a flexible combination of maps and arrays (or lists), where we can access
each piece of information via an information path. This chapter is a deep dive into
the second principle of DOP.This chapter covers
Representing records with string maps to improve 
flexibility
Manipulating data with generic functions
Accessing each piece of information via its 
information path
Gaining JSON serialization for free
PRINCIPLE #2 Represent data entities with generic data structures.
We increase system flexibility when we represent records as string maps and not as
objects instantiated from classes. This liberates data from the rigidity of a class-based sys-
tem. Data becomes a first-class citizen powered by generic functions to add, remove, or
rename fields.
 NOTE We refer to maps that have strings as keys as string maps .
The dependency between the code that manipulates data and the data is a weak
dependency. The code only needs to know the keys of specific fields in the record it
wants to manipulate. The code doesn’t even need to know about all the keys in the
record, only the ones relevant to it. In this chapter, we’ll deal only with data query.
We’ll discuss managing changes in system state in the next chapter. 
3.1 Designing a data model
During lunch at Simple, Theo and Joe don’t talk about programming. Instead, they start
getting to know each other on a personal level. Theo discovers that Joe is married to Kay,
who has just opened her creative therapy practice after many years of studying various
fields related to well-being. Neriah, their 14-year-old son, is passionate about drones, whereas
Aurelia, their 12-year-old daughter, plays the transverse flute.
Joe tells Theo that he’s been practicing meditation for 10 years. Meditation, he says, has
taught him how to break away from being continually lost in a “storm thought” (especially
negative thoughts, which can be the source of great suffering) to achieve a more direct
relationship with reality. The more he learns to experience reality as it is, the calmer his
mind. When he first started to practice meditation, it was sometimes difficult and even
weird, but by persevering, he has increased his feeling of well-being with each passing year.
When they’re back at the office, Joe tells Theo that his next step in their DOP journey
will be about data models. This includes data representation.
Joe When we design the data part of our system, we’re free to do it in isolation.
Theo What do you mean by isolation?
Joe I mean that you don’t have to bother with code, only data.
Theo Oh, right. I remember you telling me how that makes a DOP system simpler
than OOP. Separation of concerns is a design principle I’m used to in OOP.
Joe Indeed.
Theo And, when we think about data, the only relations we have to think about are
association and composition.
Joe Correct.
Theo Will the data model design be significantly different than the data model I’m
used to designing as an OOP developer?
Joe Not so much.
Theo OK. Let me see if I can draw a DOP-style data entity diagram.
Theo takes a look at the data mind map that he drew earlier in the morning. He then
draws the diagram in figure 3.1.
He refines the details of the fields of each data entity and the kind of relations between
entities. Figure 3.2 shows the result of this redefined data entity diagram.
45 3.1 Designing a data model
Library dataCatalogBooks
Authors
Book items
Book lendings
User managementUsers
Members
Librarians Figure 3.1 A data mind map of 
the Library Management System
*
*
** *name: String
address: StringCCLibrary
**
CCAuthor
name: StringCCBookLending
lendingDate: String
CCBookItem
libld: String
purchaseDate: StringCCCatalog CCUserManagement
CCLibrarian
email: String
password: StringCCMember
email: String
password: StringCCBook
title : String
publicationYear: Number
ISBN: String
publisher: String
Figure 3.2 A data model of the Library Management System
Joe The next step is to be more explicit about the relations between entities.
Theo What do you mean?
Joe For example, in your entity diagram, Book  and Author  are connected by a
many-to-many association relation. How is this relation going to be repre-
sented in your program?
Theo In the Book  entity, there will be a collection of author IDs, and in the Author
entity, there will be a collection of book IDs.
Joe Sounds good. And what will the book ID be?
Theo The book ISBN.
 NOTE The International Standard Book Number (ISBN) is a numeric commercial
book identifier that is intended to be unique.
Joe And where will you hold the index that enables you to retrieve a Book  from its
ISBN?
Theo In the Catalog  because the catalog holds a bookByISBN  index.
Joe What about author ID?
Theo Author ID is the author name in lowercase and with dashes instead of white
spaces (assuming that we don’t have two authors with the same name).
Joe And I guess that you also hold the author index in the Catalog ?
Theo Exactly!
Joe Excellent. You’ve been 100% explicit about the relation between Book  and
Author . I’ll ask you to do the same with the other relations of the system.
It’s quite easy for Theo to do, as he has done that so many times as an OOP developer. Fig-
ure 3.3 provides the detailed entity diagram of Theo’s system.
 NOTE By positional collection , we mean a collection where the elements are in order
(like a list or an array). By index , we mean a collection where the elements are accessi-
ble via a key (like a hash map or a dictionary).
The Catalog  entity contains two indexes:
booksByIsbn —The keys are book ISBNs, and the values are Book  entities. Its type is
noted as {Book} .
authorsById —The keys are author IDs, and the values are Author  entities. Its type
is noted as {Author} .
Inside a Book  entity, we have authors , which is a positional collection of author IDs of type
[String] . Inside an Author  entity, we have books , which is a collection of book IDs of
type [String] .
 NOTE For the notation for collections and index types, a positional collection of
String s is noted as [String] . An index of Book s is noted as {Book} . In the context of
a data model, the index keys are always strings.
47 3.1 Designing a data model
There is a dashed line between Book  and Author , which means that the relation between
Book  and Author  is indirect. To access the collection of Author  entities from a Book  entity,
we’ll use the authorById  index defined in the Catalog  entity.
Joe I like your data entity diagram.
Theo Thank you.
Joe Can you tell me what the three kinds of data aggregations are in your diagram
(and, in fact, in any data entity diagram)?
Theo Let’s see . . . we have positional collections like authors  in Book . We have
indexes like booksByIsbn  in Catalog . I can’t find the third one.
Joe The third kind of data aggregation is what we’ve called, until now, an “entity”
(like Library , Catalog , Book , etc.), and the common term for entity in com-
puter science is record.CCAuthor
id: String
bookIsbns: [String]name: String
CCBookLending
lendingDate: String
bookIsbn: StringbookItemId: StringCCLibrary
name: String
address: String
catalog: Catalog
userManagement: UserManagement
CCMember
email: String
encryptedPassword: String
isBlocked: Boolean
bookLendings: [BookLending]
CCBookItem
id: String
libId: String
purchaseDate: String
isLent: BooleanCCBook
title : String
publicationYear: Number
isbn: String
authorIds: [String]
bookItems: [BookItem]CCUserManagement
librariansByEmail: {Librarian}
membersByEmail: {Member}CCCatalog
booksByIsbn: {Book}
authorsById: {Author}
CCLibrarian
email: String
encryptedPassword: String**
*
*
**
*
*
Figure 3.3 Library management relation model. Dashed lines (e.g., between Book  and Author ) denote 
indirect relations, [String]  denotes a positional collection of strings, and {Book}  denotes an index of 
Book s.
 NOTE A record  is a data structure that groups together related data items. It’s a col-
lection of fields, possibly of different data types.
Theo Is it correct to say that a data entity diagram consists only of records, positional
collections, and indexes?
Joe That’s correct. Can you make a similar statement about the relations between
entities?
Theo The relations in a data entity diagram are either composition (solid line with a
full diamond) or association (dashed line with an empty diamond). Both types
of relations can be either one-to-one, one-to-many, or many-to-many.
Joe Excellent!
TIP A data entity diagram consists of records whose values are either primitives, posi-
tional collections, or indexes. The relation between records is either composition or
association. 
3.2 Representing records as maps
So far, we’ve illustrated the benefits we gain from the separation between code and
data at a high-system level. There’s a separation of concerns between code and data,
and each part has clear constraints:
Code consists of static functions that receive data as an explicit argument.
Data entities are modeled as records, and the relations between records are
represented by positional collections and indexes.
Now comes the question of the representation of the data. DOP has nothing special
to say about collections and indexes. However, it’s strongly opinionated about the
representation of records: records should be represented by generic data structures
such as maps.
 This applies to both OOP and FP languages. In dynamically-typed languages like
JavaScript, Python, and Ruby, data representation feels natural. While in statically-
typed languages like Java and C#, it is a bit more cumbersome.
Theo I’m really curious to know how we represent positional collections, indexes,
and records in DOP.
Joe Let’s start with positional collections. DOP has nothing special to say about the
representation of collections. They can be linked lists, arrays, vectors, sets, or
other collections best suited for the use case.
Theo It’s like in OOP.
Joe Right! For now, to keep things simple, we’ll use arrays to represent positional
collections.
Theo What about indexes?
Joe Indexes are represented as homogeneous string maps.
Theo What do you mean by a homogeneous map?
49 3.2 Representing records as maps
Joe I mean that all the values of the map are of the same kind. For example, in a
Book  index, all the values are Book , and in an author index, all the values are
Author , and so forth.
Theo Again, it’s like in OOP.
 NOTE A homogeneous map  is a map where all the values are of the same type. A hetero-
geneous map  is a map where the values are of different types.
Joe Now, here’s the big surprise. In DOP, records are represented as maps, more
precisely, heterogeneous string maps.
Joe goes to the whiteboard and begins to draw. When he’s finished, he shows Theo the dia-
gram in figure 3.4.
Theo stays silent for a while. He is shocked to hear that the data entities of a system can be
represented as a generic data structure, where the field names and value types are not
specified in a class. Then, Theo asks Joe:
Theo What are the benefits of this folly?
Joe Flexibility and genericity.
Theo Could you explain, please?
Joe I’ll explain in a moment, but before that, I’d like to show you what an instance
of a record in a DOP system looks like.
Theo OK.
Joe Let’s take as an example, Watchmen , by Alan Moore and Dave Gibbons, which is
my favorite graphic novel. This masterpiece was published in 1987. I’m going
to assume that, in a physical library, there are two copies of this book, whose ID
is nyc-central-lib , and that one of the two copies is currently out. Here’s
how I’d represent the Book  record for Watchmen  in DOP.
Joe comes closer to Theo’s laptop. He opens a text editor (not an IDE!) and types the Book
record for Theo.Data representationHeterogeneous map Record
Array
CollectionLinked list
Set
Vector
Index Homogeneous mapFigure 3.4 The building blocks 
of data representation
{
  "isbn": "978-1779501127",
  "title": "Watchmen",
  "publicationYear": 1987,
  "authors": ["alan-moore", "dave-gibbons"],
  "bookItems": [
    {
      "id": "book-item-1",
      "libId": "nyc-central-lib",
      "isLent": true
    },
    {
      "id": "book-item-2",
      "libId": "nyc-central-lib",
      "isLent": false
    }
  ]
}
Theo looks at the laptop screen. He has a question.
Theo How am I supposed to instantiate the Book  record for Watchmen  programmat-
ically?
Joe It depends on the facilities that your programming language offers to instantiate
maps. With dynamic languages like JavaScript, Ruby, or Python, it’s straight-
forward, because we can use literals for maps and arrays. Here, let me show
you how.
Joe jots down the JavaScript code that creates an instance of a Book  record, which rep-
resents as a map in JavaScript. He shows the code to Theo.
var watchmenBook = {
  "isbn": "978-1779501127",
  "title": "Watchmen",
  "publicationYear": 1987,
  "authors": ["alan-moore", "dave-gibbons"],
  "bookItems": [
    {
      "id": "book-item-1",
      "libId": "nyc-central-lib",
      "isLent": true
    },
    {
      "id": "book-item-2",
      "libId": "nyc-central-lib",
      "isLent": false
    }
  ]
}Listing 3.1 An instance of a Book  record represented as a map
Listing 3.2 A Book  record represented as a map in JavaScript
51 3.2 Representing records as maps
Theo And, if I’m in Java?
Joe It’s a bit more tedious, but still doable with the immutable Map and List  static
factory methods.
 NOTE See “Creating Immutable Lists, Sets, and Maps” at http:/ /mng.bz/voGm  for
more information on this Java core library.
Joe types the Java code to create an instance of a Book  record represented as a map. He
shows Theo the Java code.
Map watchmen = Map.of(
  "isbn", "978-1779501127",
  "title", "Watchmen",
  "publicationYear", 1987,
  "authors", List.of("alan-moore", "dave-gibbons"),
  "bookItems", List.of(
    Map.of(
      "id", "book-item-1",
      "libId", "nyc-central-lib",
      "isLent", true
    ),
    Map.of (
      "id", "book-item-2",
      "libId", "nyc-central-lib",
      "isLent", false
    )
  )
);
TIP In DOP, we represent a record as a heterogeneous string map.
Theo I’d definitely prefer to create a Book  record using a Book  class and a BookItem
class.
Theo opens his IDE. He types the JavaScript code to represent a Book  record as an instance
of a Book  class.
class Book {
  isbn;
  title;
  publicationYear;
  authors;
  bookItems;
  constructor(isbn, title, publicationYear, authors, bookItems) {
    this.isbn = isbn;
    this.title = title;
    this.publicationYear = publicationYear;
    this.authors = authors;
    this.bookItems = bookItems;Listing 3.3 A Book  record represented as a map in Java
Listing 3.4 A Book  record as an instance of a Book  class in JavaScript
  }
}
class BookItem {
  id;
  libId;
  isLent;
  constructor(id, libId, isLent) {
    this.id = id;
    this.libId = libId;
    this.isLent = isLent;
  }
}
var watchmenBook = new Book("978-1779501127",
  "Watchmen",
  1987,
  ["alan-moore", "dave-gibbons"],
  [new BookItem("book-item-1", "nyc-central-lib", true),
    new BookItem("book-item-2", "nyc-central-lib", false)]);
Joe Theo, why do you prefer classes over maps for representing records?
Theo It makes the data shape of the record part of my program. As a result, the IDE
can auto-complete field names, and errors are caught at compile time.
Joe Fair enough. Can I show you some drawbacks for this approach?
Theo Sure.
Joe Imagine that you want to display the information about a book in the context
of search results. In that case, instead of author IDs, you want to display
author names, and you don’t need the book item information. How would
you handle that?
Theo I’d create a class BookInSearchResults  without a bookItems  member and
with an authorNames  member instead of the authorIds  member of the Book
class. Also, I would need to write a copy constructor that receives a Book  object.
Joe In classic OOP, the fact that data is instantiated only via classes brings safety.
But this safety comes at the cost of flexibility.
TIP There’s a tradeoff between flexibility and safety in a data model.
Theo So, how can it be different?
Joe In the DOP approach, where records are represented as maps, we don’t need
to create a class for each variation of the data. We’re free to add, remove, and
rename record fields dynamically. Our data model is flexible.
Theo Interesting!
TIP In DOP, the data model is flexible. We’re free to add, remove, and rename
record fields dynamically at run time.
Joe Now, let me talk about genericity. How would you serialize the content of a
Book  object to JSON?
53 3.2 Representing records as maps
TIP In DOP, records are manipulated with generic functions.
Theo Oh no! I remember that while working on the Klafim prototype, I had a night-
mare about JSON serialization when I was developing the first version of the
Library Management System.
Joe Well, in DOP, serializing a record to JSON is super easy.
Theo Does it require the usage of reflection in order to go over the fields of the
record like the Gson Java library does?
 NOTE See https:/ /github.com/google/gson  for more information on Gson.
Joe Not at all! Remember that in DOP, a record is nothing more than data. We can
write a generic JSON serialization function that works with any record. It can
be a Book , an Author , a BookItem , or anything else.
Theo Amazing!
TIP In DOP, you get JSON serialization for free.
Joe Actually, as I’ll show you in a moment, lots of data manipulation stuff can be
done using generic functions.
Theo Are the generic functions part of the language?
Joe It depends on the functions and on the language. For example, JavaScript pro-
vides a JSON serialization function called JSON.stringify  out of the box, but
none for omitting multiple keys or for renaming keys.
Theo That’s annoying.
Joe Not so much; there are third-party libraries that provide data-manipulation facil-
ities. A popular data manipulation library in the JavaScript ecosystem is Lodash.
 NOTE See https:/ /lodash.com/  to find out more about Lodash.
Theo What about other languages?
Joe Lodash has been ported to Java, C#, Python, and Ruby. Let me bookmark some
sites for you.
Joe bookmarks these sites for Theo:
https:/ /javalibs.com/artifact/com.github.javadev/underscore-lodash  for Java
https:/ /www.nuget.org/packages/lodash/  for C#
https:/ /github.com/dgilland/pydash  for Python
https:/ /rudash-website.now.sh/  for Ruby
 NOTE Throughout the book, we use Lodash to show how to manipulate data with
generic functions, but there is nothing special about Lodash. The exact same approach
could be implemented via other data manipulation libraries or custom code.
Theo Cool!
Joe Actually, Lodash and its rich set of data manipulation functions can be ported
to any language. That’s why it’s so beneficial to represent records as maps.
TIP DOP compromises on data safety to gain flexibility and genericity.
At the whiteboard, Joe quickly sketches the tradeoffs (see table 3.1).
3.3 Manipulating data with generic functions
Joe Now let me show you how to manipulate data in DOP with generic functions.
Theo Yes, I’m quite curious to see how you’ll implement the search functionality of
the Library Management System.
Joe OK. First, let’s instantiate a Catalog  record for the catalog data of a library,
where we have a single book, Watchmen .
Joe instantiates a Catalog  record according to Theo’s data model in figure 3.3. Here’s
what Joe shows to Theo.
var catalogData = {
  "booksByIsbn": {
    "978-1779501127": {
      "isbn": "978-1779501127",
      "title": "Watchmen",
      "publicationYear": 1987,
      "authorIds": ["alan-moore", "dave-gibbons"],
      "bookItems": [
        {
          "id": "book-item-1",
          "libId": "nyc-central-lib",
          "isLent": true
        },
        {
          "id": "book-item-2",
          "libId": "nyc-central-lib",
          "isLent": false
        }
      ]
    }
  },
  "authorsById": {
    "alan-moore": {
      "name": "Alan Moore",
      "bookIsbns": ["978-1779501127"]
    },Table 3.1 The tradeoff among safety, flexibility, and genericity
OOP DOP
Safety High Low
Flexibility Low High
Genericity Low High 
Listing 3.5 A Catalog  record
55 3.3 Manipulating data with generic functions
    "dave-gibbons": {
      "name": "Dave Gibbons",
      "bookIsbns": ["978-1779501127"]
    }
  }
}
Theo I see the two indexes we talked about, booksByIsbn  and authorsById . How
do you differentiate a record from an index in DOP?
Joe In an entity diagram, there’s a clear distinction between records and indexes.
But in our code, both are plain data.
Theo I guess that’s why this approach is called data-oriented programming.
Joe See how straightforward it is to visualize any part of the system data inside a
program? The reason is that data is represented as data!
TIP In DOP, data is represented as data.
Theo That sounds like a lapalissade.1
Joe Oh, does it? I’m not so sure! In OOP, data is usually represented by objects,
which makes it more challenging to visualize data inside a program.
TIP In DOP, we can visualize any part of the system data.
Theo How would you retrieve the title of a specific book from the catalog data?
Joe Great question! In fact, in a DOP system, every piece of information has an
information path from which we can retrieve the information.
Theo Information path?
Joe For example, the information path to the title of the Watchmen  book in the
catalog is ["booksByIsbn",  "978-1779501127",  "title"] .
Theo Ah, I see. So, is an information path sort of like a file path, but that names in
an information path correspond to nested entities?
Joe You’re exactly right. And once we have the path of a piece of information, we
can retrieve the information with Lodash’s _.get  function.
Joe types a few characters on Theo’s laptop. Theo is amazed at how little code is needed to
get the book title.
_.get(catalogData, ["booksByIsbn", "978-1779501127", "title"])
// → "Watchmen"
Theo Neat. I wonder how hard it would be to implement a function like _.get
myself.
1A lapalissade is an obvious truth—a truism or tautology—that produces a comical effect.Listing 3.6 Retrieving the title of a book from its information path
After a few minutes of trial and error, Theo is able to produce his implementation. He
shows Joe the code.
function get(m, path) {
  var res = m;
  for(var i = 0; i < path.length; i++) {  
    var key = path[i];
    res = res[key];
  }
  return res;
}
After testing Theo’s implementation of get, Joe compliments Theo. He’s grateful that
Theo is catching on so quickly.
get(catalogData, ["booksByIsbn", "978-1779501127", "title"]);
// → "Watchmen"
Joe Well done!
Theo I wonder if a function like _.get  works smoothly in a statically-typed language
like Java?
Joe It depends on whether you only need to pass the value around or to access the
value concretely.
Theo I don’t follow.
Joe Imagine that once you get the title of a book, you want to convert the string
into an uppercase string. You need to do a static cast to String , right? Here,
let me show you an example that casts a field value to a string, then we can
manipulate it as a string.
((String)watchmen.get("title")).toUpperCase()
Theo That makes sense. The values of the map are of different types, so the compiler
declares it as a Map<String,Object> . The information of the type of the field
is lost.
Joe It’s a bit annoying, but quite often our code just passes the data around. In that
case, we don’t have to deal with static casting. Moreover, in a language like C#,
when using the dynamic  data type, type casting can be avoided.2,3Listing 3.7 Custom implementation of get
Listing 3.8 Testing the custom implementation of get
Listing 3.9 Casting a field value to a string
2See http:/ /mng.bz/4jo5  for the C# documentation on the built-in reference to dynamic types.
3See appendix A for details about dynamic fields and type casting in C#.We could use 
forEach instead 
of a for loop.
57 3.3 Manipulating data with generic functions
TIP In statically-typed languages, we sometimes need to statically cast the field values.
Theo What about performance?
Joe In most programming languages, maps are quite efficient. Accessing a field
in a map is slightly slower than accessing a class member. Usually, it’s not
significant.
TIP There’s no significant performance hit for accessing a field in a map instead of as
a class member.
Theo Let’s get back to this idea of information path. It works in OOP too. I could
access the title of the Watchmen  book with catalogData.booksByIsbn["978-
1779501127"].title . I’d use class members for record fields and strings for
index keys.
Joe There’s a fundamental difference, though. When records are represented as
maps, the information can be retrieved via its information path using a generic
function like _.get . But when records are represented as objects, you need to
write specific code for each type of information path.
Theo What do you mean by specific code? What’s specific in catalogData.books-
ByIsbn["978-1779501127"].title ?
Joe In a statically-typed language like Java, you’d need to import the class defini-
tions for Catalog  and Book .
Theo And, in a dynamically-typed language like JavaScript . . . ?
Joe Even in JavaScript, when you represent records with objects instantiated from
classes, you can’t easily write a function that receives a path as an argument
and display the information that corresponds to this path. You would have to
write specific code for each kind of path. You’d access class members with dot
notation and map fields with bracket notation.
Theo Would you say that in DOP, the information path is a first-class citizen?
Joe Absolutely! The information path can be stored in a variable and passed as an
argument to a function.
TIP In DOP, you can retrieve every piece of information via a path and a generic
function.
Joe goes to the whiteboard. He draws a diagram like that in figure 3.5, which shows the
catalog data as a tree.
Joe You see, Theo, each piece of information is accessible via a path made of
strings and integers. For example, the path of Alan Moore’s first book is
["catalog",  "authorsById",  "alan-moore",  "bookIsbns",  0]. 
 
 
3.4 Calculating search results
Theo Interesting. I’m starting to feel the power of expression of DOP!
Joe Wait, that’s just the beginning. Let me show you how simple it is to write code
that retrieves book information and displays it in search results. Can you tell
me exactly what information has to appear in the search results?
Theo Searching for book information should return isbn , title , and author-
Names .
Joe And what would a BookInfo  record look like for Watchmen ?
Theo quickly enters the code on his laptop. He then shows it to Joe.
{
  "title": "Watchmen",
  "isbn": "978-1779501127",
  "authorNames": [
    "Alan Moore",
    "Dave Gibbons",
  ]
}Listing 3.10 A BookInfo  record for Watchmen  in the context of search resultcatalog
booksByIsbn
978-1779501127
title
authorIds

dave-gibbons0
alan-mooreisbn
978-1779501127
publicationYearWatchmen

bookItems

book-item-2
libId
la-central-lib
isLent
false0
book-item-1
libIdid id
nyc-cental-lib
isLent
trueauthorsById
alan-moore
name
Alan Moore
bookIsbns

978-1779501127
dave-gibbons
name
Dave Gibbons
bookIsbns

978-1779501127
Figure 3.5 The catalog data as a tree
59 3.4 Calculating search results
Joe Now I’ll show you step by step how to write a function that returns search
results matching a title in JSON format. I’ll use generic data manipulation
functions from Lodash.
Theo I’m ready!
Joe Let’s start with an authorNames  function that calculates the author names of a
Book  record by looking at the authorsById  index. Could you tell me what’s
the information path for the name of an author whose ID is authorId ?
Theo It’s ["authorsById",  authorId,  "name"] .
Joe Now, let me show you how to retrieve the name of several authors using _.map .
Joe types the code to map the author IDs to the author names. Theo nonchalantly peeks
over Joe’s shoulder.
_.map(["alan-moore", "dave-gibbons"], 
  function(authorId) {
    return _.get(catalogData, ["authorsById", authorId, "name"]);
  }); 
// → [ "Alan Moore", "Dave Gibbons"]
Theo What’s this _.map  function? It smells like functional programming! You said I
wouldn’t have to learn FP to implement DOP!
Joe No need to learn functional programming in order to use _.map , which is a
function that transforms the values of a collection. You can implement it with
a simple for loop.
Theo spends a couple of minutes in front of his computer figuring out how to implement
_.map . Now he’s got it!
function map(coll, f) {
  var res = [];
  for(var i = 0; i < coll.length; i++) {   
    res[i] = f(coll[i]);
  }
  return res;
}
After testing Theo’s implementation of map, Joe shows Theo the test. Joe again compli-
ments Theo.
map(["alan-moore", "dave-gibbons"], 
  function(authorId) {
    return _.get(catalogData, ["authorsById", authorId, "name"]);
  }); 
// → [ "Alan Moore", "Dave Gibbons"]Listing 3.11 Mapping author IDs to author names
Listing 3.12 Custom implementation of map
Listing 3.13 Testing the custom implementation of mapWe could use 
forEach instead 
of a for loop.
Joe Well done!
Theo You were right! It wasn’t hard.
Joe Now, let’s implement authorNames  using _.map .
It takes a few minutes for Theo to come up with the implementation of authorNames .
When he’s finished, he turns his laptop to Joe.
function authorNames(catalogData, book) {
  var authorIds = _.get(book, "authorIds");
  var names = _.map(authorIds, function(authorId) { 
    return _.get(catalogData, ["authorsById", authorId, "name"]);
  });
  return names;
}
Joe We also need a bookInfo  function that converts a Book  record into a Book-
Info  record. Let me show you the code for that.
function bookInfo(catalogData, book) {
  var bookInfo =  {
    "title": _.get(book, "title"),
    "isbn": _.get(book, "isbn"),
    "authorNames": authorNames(catalogData, book)
  };
  return bookInfo;  
}
Theo Looking at the code, I see that a BookInfo  record has three fields: title ,
isbn , and authorNames . Is there a way to get this information without looking
at the code?
Joe You can either add it to the data entity diagram or write it in the documenta-
tion of the bookInfo  function, or both.
Theo I have to get used to the idea that in DOP, the record field information is not
part of the program.
Joe Indeed, it’s not part of the program, but it gives us a lot of flexibility.
Theo Is there any way for me to have my cake and eat it too?
Joe Yes, and someday I’ll show you how to make record field information part of a
DOP program (see chapters 7 and 12).
Theo Sounds intriguing!
Joe Now that we have all the pieces in place, we can write our searchBooksBy-
Title  function, which returns the book information about the books that
match the query. First, we find the Book  records that match the query with
_.filter  and then we transform each Book  record into a BookInfo  record
with _.map  and bookInfo .Listing 3.14 Calculating the author names of a book
Listing 3.15 Converting a Book  record into a BookInfo  record
There’s no need to create 
a class for bookInfo.
61 3.4 Calculating search results
function searchBooksByTitle(catalogData, query) {
  var allBooks = _.values(_.get(catalogData, "booksByIsbn"));
  var matchingBooks = _.filter(allBooks, function(book) { 
    return _.get(book, "title").includes(query);     
  });
  var bookInfos = _.map(matchingBooks, function(book) { 
    return bookInfo(catalogData, book);
  });
  return bookInfos;
}
Theo You’re using Lodash functions without any explanation again!
Joe Sorry about that. I am so used to basic data manipulation functions that I con-
sider them as part of the language. What functions are new to you?
Theo_.values  and _.filter
Joe Well, _.values  returns a collection made of the values of a map, and _.filter
returns a collection made of the values that satisfy a predicate.
Theo_.values  seems trivial. Let me try to implement _.filter .
The implementation of _.filter  takes a bit more time. Eventually, Theo manages to get
it right, then he is able to test it.
function filter(coll, f) {
  var res = [];
  for(var i = 0; i < coll.length; i++) {   
    if(f(coll[i])) {
      res.push(coll[i]);
    }
  }
  return res;
}
filter(["Watchmen", "Batman"], function (title) {
  return title.includes("Watch");
});
// → ["Watchmen"]
Theo To me, it’s a bit weird that to access the title of a book record, I need to write
_.get(book,  "title") . I’d expect it to be book.title  in dot notation or
book["title"]  in bracket notation.
Joe Remember that book  is a record that’s not represented as an object. It’s a map.
Indeed, in JavaScript, you can write _.get(book,  "title") , book.title , or
book["title"] . But I prefer to use Lodash’s _.get  function. In some lan-
guages, the dot and the bracket notations might not work on maps.Listing 3.16 Searching books that match a query
Listing 3.17 Custom implementation of filter
Listing 3.18 Testing the custom implementation of filterThe includes JavaScript 
function checks whether 
a string includes a string 
as a substring.
We could use 
forEach instead 
of a for loop.
Theo Being language-agnostic has a price!
Joe Right, would you like to test searchBooksByTitle ?
Theo Absolutely! Let me call searchBooksByTitle  to search the books whose title
contain the string Watch .
searchBooksByTitle(catalogData, "Wat");
//[
//  {
//    "authorNames": [
//      "Alan Moore",
//      "Dave Gibbons"
//    ],
//    "isbn": "978-1779501127",
//    "title": "Watchmen"
//  }
//]
Theo It seems to work! Are we done with the search implementation?
Joe Almost. The searchBooksByTitle  function we wrote is going to be part of the
Catalog  m o d u l e ,  a n d  i t  r e t u r n s  a  c o l l e c t i o n  o f  r e c o r d s .  W e  h a v e  t o  w r i t e  a
function that’s part of the Library  module, and that returns a JSON string.
Theo You told me earlier that JSON serialization was straightforward in DOP.
Joe Correct. The code for searchBooksByTitleJSON  retrieves the Catalog  record,
passes it to searchBooksByTitle , and converts the results to JSON with
JSON.stringify . That’s part of JavaScript. Here, let me show you.
function searchBooksByTitleJSON(libraryData, query) {
  var results = searchBooksByTitle(_.get(libraryData, "catalog"), query);
  var resultsJSON = JSON.stringify(results);
  return resultsJSON;
}
Joe In order to test our code, we need to create a Library  record that contains our
Catalog  record. Could you do that for me, please?
Theo Should the Library  record contain all the Library  fields (name , address ,
and UserManagement )?
Joe That’s not necessary. For now, we only need the catalog  field, then the test
for searching books.
var libraryData = {
  "catalog": {
    "booksByIsbn": {
      "978-1779501127": {
        "isbn": "978-1779501127",
        "title": "Watchmen",Listing 3.19 Testing searchBooksByTitle
Listing 3.20 Implementation of searching books in a library as JSON
Listing 3.21 A Library  record
63 3.4 Calculating search results
        "publicationYear": 1987,
        "authorIds": ["alan-moore",
          "dave-gibbons"],
        "bookItems": [
          {
            "id": "book-item-1",
            "libId": "nyc-central-lib",
            "isLent": true
          },
          {
            "id": "book-item-2",
            "libId": "nyc-central-lib",
            "isLent": false
          }
        ]
      }
    },
    "authorsById": {
      "alan-moore": {
        "name": "Alan Moore",
        "bookIsbns": ["978-1779501127"]
      },
      "dave-gibbons": {
        "name": "Dave Gibbons",
        "bookIsbns": ["978-1779501127"]
      }
    }
  }
};
searchBooksByTitleJSON(libraryData, "Wat");
Theo How are we going to combine the four functions that we’ve written so far?
Joe The functions authorNames , bookInfo , and searchBooksByTitle  go into
the Catalog  module, and searchBooksByTitleJSON  goes into the Library
module.
Theo looks at the resulting code of the two modules, Library  and Catalog . He’s quite
amazed by its conciseness.
class Catalog {
  static authorNames(catalogData, book) {
    var authorIds = _.get(book, "authorIds");
    var names = _.map(authorIds, function(authorId) { 
      return _.get(catalogData, ["authorsById", authorId, "name"]);
    });
    return names;
  }Listing 3.22 Test for searching books in a library as JSON
Listing 3.23 Calculating search results for Library  and Catalog
  static bookInfo(catalogData, book) {
    var bookInfo =  {
      "title": _.get(book, "title"),
      "isbn": _.get(book, "isbn"),
      "authorNames": Catalog.authorNames(catalogData, book)
    };         
    return bookInfo;
  }
  static searchBooksByTitle(catalogData, query) {
    var allBooks = _.get(catalogData, "booksByIsbn");
    var matchingBooks = _.filter(allBooks, 
      function(book) {                            
        return _.get(book, "title").includes(query);
    });
    var bookInfos = _.map(matchingBooks, function(book) { 
      return Catalog.bookInfo(catalogData, book);
    });
    return bookInfos;
  }
}
class Library {
  static searchBooksByTitleJSON(libraryData, query) {
    var catalogData = _.get(libraryData, "catalog");
    var results = Catalog.searchBooksByTitle(catalogData, query);
    var resultsJSON = JSON.stringify(results);   
    return resultsJSON;
  }
}
After testing the final code in listing 3.24, Theo looks again at the source code from list-
ing 3.23. After a few seconds, he feels like he’s having another Aha! moment.
Library.searchBooksByTitleJSON(libraryData, "Watchmen");
// → "[{\"title\":\"Watchmen\",\"isbn\":\"978-1779501127\",
// → \"authorNames\":[\"Alan Moore\",\"Dave Gibbons\"]}]"
Theo The important thing is not that the code is concise, but that the code contains
no abstractions. It’s just data manipulation!
Joe responds with a smile that says, “You got it, my friend!”
Joe It reminds me of what my first meditation teacher told me 10 years ago:
meditation guides the mind to grasp the reality as it is without the abstractions
created by our thoughts.
TIP In DOP, many parts of our code base tend to be just about data manipulation
with no abstractions. Listing 3.24 Search results in JSONThere’s no need 
to create a class 
for bookInfo.
When _.filter is 
passed a map, it 
goes over the values 
of the map.
Converts data 
to JSON (part 
of JavaScript)
65 3.5 Handling records of different types
3.5 Handling records of different types
We’ve seen how DOP enables us to treat records as first-class citizens that can be
manipulated in a flexible way using generic functions. But if a record is nothing more
than an aggregation of fields, how do we know what the type of the record is? DOP has
a surprising answer to this question.
Theo I have a question. If a record is nothing more than a map, how do you know
the type of the record?
Joe That’s a great question with a surprising answer.
Theo I’m curious.
Joe Most of the time, there’s no need to know the record type.
Theo What! What do you mean?
Joe I mean that what matters most are the values of the fields. For example, take a
look at the Catalog.authorNames  source code. It operates on a Book  record,
but the only thing that matters is the value of the authorIds  field.
Doubtful, Theo looks at the source code for Catalog.authorNames . This is what Theo sees.
function authorNames(catalogData, book) {
  var authorIds = _.get(book, "authorIds");
  var names = _.map(authorIds, function(authorId) { 
    return _.get(catalogData, ["authorsById", authorId, "name"]);
  });
  return names;
}
Theo What about differentiating between various user types like Member  versus
Librarian ? I mean, they both have email  and encryptedPassword . How do
you know if a record represents a Member  or a Librarian ?
Joe Simple. You check to see if the record is found in the librariansByEmail
index or in the membersByEmail  index of the Catalog .
Theo Could you be more specific?
Joe Sure! Let me write what the user management data of our tiny library might
look like, assuming we have one librarian and one member. To keep things
simple, I’m encrypting passwords through naive base-64 encoding for the User-
Management  record.
var userManagementData = {
  "librariansByEmail": {
    "franck@gmail.com" : {
      "email": "franck@gmail.com",
      "encryptedPassword": "bXlwYXNzd29yZA=="    
    }
  },Listing 3.25 Calculating the author names of a book
Listing 3.26 A UserManagement  record
The base-64 
encoding of 
"mypassword"
  "membersByEmail": {
    "samantha@gmail.com": {
      "email": "samantha@gmail.com",
      "encryptedPassword": "c2VjcmV0",  
      "isBlocked": false,
      "bookLendings": [
        {
          "bookItemId": "book-item-1",
          "bookIsbn": "978-1779501127",
          "lendingDate": "2020-04-23"
        }
      ]
    }
  }
}
TIP Most of the time, there’s no need to know the record type.
Theo This morning, you told me you’d show me the code for UserManagement
.isLibrarian  function this afternoon.
Joe So, here we are. It’s afternoon, and I’m going to fulfill my promise.
Joe implements isLibrarian . With a slight pause, he then issues the test for isLibrarian .
function isLibrarian(userManagement, email) {
  return _.has(_.get(userManagement, "librariansByEmail"), email);
}
isLibrarian(userManagementData, "franck@gmail.com");
// → true
Theo I’m assuming that _.has  is a function that checks whether a key exists in a
map. Right?
Joe Correct.
Theo OK. You simply check whether the librariansByEmail  map contains the
email  field.
Joe Yep.
Theo Would you use the same pattern to check whether a member is a Super mem-
ber or a VIP member?
Joe Sure. We could have SuperMembersByEmail  and VIPMembersByEmail  indexes.
But there’s a better way.
Theo How?
Joe When a member is a VIP member, we add a field, isVIP , with the value true  to
its record. To check if a member is a VIP member, we check whether the
isVIP  field is set to true  in the member record. Here’s how I would code
isVIPMember .Listing 3.27 Checking if a user is a librarian
Listing 3.28 Testing isLibrarianThe base-64 
encoding of 
"secret"
67 3.5 Handling records of different types
function isVIPMember(userManagement, email) {
  return _.get(userManagement, ["membersByEmail", email, "isVIP"]) == true;
}
Theo I see that you access the isVIP  field via its information path, ["membersBy-
Email",  email,  "isVIP"] .
Joe Yes, I think it makes the code crystal clear.
Theo I agree. I guess we can do the same for isSuperMember  and set an isSuper
field to true  when a member is a Super member?
Joe Yes, just like this.
Joe assembles all the pieces in a UserManagement  class. He then shows the code to Theo.
class UserManagement {
  isLibrarian(userManagement, email) {
    return _.has(_.get(userManagement, "librariansByEmail"), email);
  }
  isVIPMember(userManagement, email) {
    return _.get(userManagement, 
      ["membersByEmail", email, "isVIP"]) == true;
  }
  isSuperMember(userManagement, email) {
    return _.get(userManagement, 
      ["membersByEmail", email, "isSuper"]) == true;
  }
}
Theo looks at the UserManagement  module code for a couple of seconds. Suddenly, an
idea comes to his mind.
Theo Why not have a type  field in member record whose value would be either VIP
or Super ?
Joe I assume that, according to the product requirements, a member can be both a
VIP and a Super member.
Theo Hmm . . . then the types  field could be a collection containing VIP or Super
or both.
Joe In some situations, having a types  field is helpful, but I find it simpler to have
a Boolean field for each feature that the record supports.
Theo Is there a name for fields like isVIP  and isSuper ?
Joe I call them feature fields .
TIP Instead of maintaining type information about a record, use a feature field (e.g.,
isVIP ).Listing 3.29 Checking whether a member is a VIP member
Listing 3.30 The code of UserManagement  module
Theo Can we use feature fields to differentiate between librarians and members?
Joe You mean having an isLibrarian  and an isMember  field?
Theo Yes, and having a common User  record type for both librarians and members.
Joe We can, but I think it’s simpler to have different record types for librarians and
members: Librarian  for librarians and Member  for members.
Theo Why?
Joe Because there’s a clear distinction between librarians and members in terms of
data. For example, members can have book lendings but librarians don’t.
Theo I agree. Now, we need to mention the two Member  feature fields in our entity
diagram.
With that, Theo adds these fields to his diagram on the whiteboard. When he’s finished, he
shows Joe his additions (figure 3.6).
Joe Do you like the data model that we have designed together?
Theo I find it quite simple and clear.CCAuthor
id: String
bookIsbns: [String]name: String
CCBookLending
lendingDate: String
bookIsbn: StringbookItemId: StringCCLibrary
name: String
address: String
catalog: Catalog
userManagement: Catalog
CCMember
email: String
encryptedPassword: String
isBlocked: Boolean
bookLendings: [BookLending]
isVIP: Boolean
isSuper: Boolean
CCBookItem
id: String
libId: String
purchaseDate: String
isLent: BooleanCCBook
title : String
publicationYear: Number
isbn: String
authorIds: [String]
bookItems: [BookItem]CCUserManagement
librariansByEmail: {Librarian}
membersByEmail: {Member}CCCatalog
booksByIsbn: {Book}
authorsById: {Author}
CCLibrarian
email: String
encryptedPassword: String**
*
*
**
*
*
Figure 3.6 A library management data model with the Member  feature fields isVIP  and isSuper
69 Summary
Joe That’s the main goal of DOP.
Theo Also, I’m pleasantly surprised how easy it is to adapt to changing requirements,
both in terms of code and the data model.
Joe I suppose you’re also happy to get rid of complex class hierarchy diagrams.
Theo Absolutely! Also, I think I’ve found an interesting connection between DOP
and meditation.
Joe Really?
Theo When we were eating at Simple, you told me that meditation helped you expe-
rience reality as it is without the filter of your thoughts.
Joe Right.
Theo From what you taught me today, I understand that in DOP, we are encouraged
to treat data as data without the filter of our classes.
Joe Clever! I never noticed that connection between those two disciplines that are
so important for me. I guess you’d like to continue your journey in the realm
of DOP.
Theo Definitely. Let’s meet again tomorrow.
Joe Unfortunately, tomorrow I’m taking my family to the beach to celebrate the
twelfth birthday of my eldest daughter, Aurelia.
Theo Happy birthday, Aurelia!
Joe We could meet again next Monday, if that’s OK with you.
Theo With pleasure!
Summary
DOP principle #2 is to represent data entities with generic data structures.
We refer to maps that have strings as keys as string maps .
Representing data as data means representing records with string maps.
By positional collection , we mean a collection where the elements are in order
(like a list or an array).
A positional collection of String s is noted as [String] .
By index , we mean a collection where the elements are accessible via a key (like
a hash map or a dictionary).
An index of Book s is noted as {Book} .
In the context of a data model, the index keys are always strings.
A record  is a data structure that groups together related data items. It’s a collec-
tion of fields, possibly of different data types.
A homogeneous map  is a map where all the values are of the same type.
A heterogeneous map  is a map where the values are of different types.
In DOP, we represent a record as a heterogeneous string map.
A data entity diagram  consists of records whose values are either primitives, posi-
tional collections, or indexes.
The relation between records in a data entity diagram is either composition  or
association .
T h e  d a t a  p a r t  o f  a  D O P  s y s t e m  i s  f l e x i b l e ,  a n d  e a c h  p i e c e  o f  i n f o r m a t i o n  i s
accessible via its information path.
There is a tradeoff  between flexibility and safety in a data model.
DOP compromises on data safety to gain flexibility and genericity.
In DOP, the data model is flexible. We’re free to add, remove, and rename
record fields dynamically at run time.
We manipulate data with generic functions.
Generic functions are provided either by the language itself or by third-party
libraries like Lodash.
JSON serialization  is implemented in terms of a generic function.
On the one hand, we’ve lost the safety of accessing record fields via members
defined at compile time. On the other hand, we’ve liberated data from the lim-
itation of classes and objects. Data is represented as data!
The weak dependency between code and data makes it is easier to adapt to
changing requirements.
When data is represented as data, it is straightforward to visualize system data.
Usually, we do not need to maintain type information about a record.
We can visualize any part of the system data.
In statically-typed languages, we sometimes need to statically cast the field values.
Instead of maintaining type information about a record, we use a feature field .
There is no significant performance hit for accessing a field in a map instead of
a class member.
In DOP, you can retrieve every piece of information via an information path  and
a generic function.
In DOP, many parts of our code base tend to be just about data manipulation
with no abstractions.
Lodash functions introduced in this chapter
Function Description
get(map,  path) Gets the value of map at path
has(map,  path) Checks if map has a field at path
merge(mapA,  mapB) Creates a map resulting from the recursive merges between mapA  and mapB
values(map) Creates an array of values of map
filter(coll,  pred) Iterates over elements of coll , returning an array of all elements for which 
pred  returns true
map(coll,  f) Creates an array of values by running each element in coll  through f
71State management
Time travel
So far, we have seen how DOP handles queries via generic functions that access sys-
tem data, which is represented as a hash map. In this chapter, we illustrate how
DOP deals with mutations  (requests that change the system state). Instead of updat-
ing the state in place, we maintain multiple versions of the system data. At a specific
point in time, the system state  refers to a specific version of the system data. This
chapter is a deep dive in the third principle of DOP.
The maintenance of multiple versions of the system data requires the data to be
immutable. This is made efficient both in terms of computation and memory via aThis chapter covers
A multi-version approach to state management
The calculation phase of a mutation
The commit phase of a mutation
Keeping a history of previous state versions
PRINCIPLE #3 Data is immutable.
technique called structural sharing , where parts of the data that are common between
two versions are shared instead of being copied. In DOP, a mutation is split into two
distinct phases:
In the calculation phase, we compute the next version of the system data.
In the commit phase, we move the system state forward so that it refers to the
version of the system data computed by the calculation phase.
This distinction between calculation and commit phases allows us to reduce the part
of our system that is stateful to its bare minimum. Only the code of the commit phase
is stateful, while the code in the calculation phase of a mutation is stateless and is
made of generic functions similar to the code of a query. The implementation of the
commit phase is common to all mutations. As a consequence, inside the commit
phase, we have the ability to ensure that the state always refers to a valid version of the
system data.
 Another benefit of this state management approach is that we can keep track of
the history of previous versions of the system data. Restoring the system to a previous
state (if needed) becomes straightforward. Table 4.1 shows the two phases.
In this chapter, we assume that no mutations occur concurrently in our system. In the
next chapter, we will deal with concurrency control. 
4.1 Multiple versions of the system data
When Joe comes in to the office on Monday, he tells Theo that he needs to exercise before
starting to work with his mind. Theo and Joe go for a walk around the block, and the dis-
cussion turns toward version control systems. They discuss how Git keeps track of the
whole commit history and how easy and fast it is to restore the code to a previous state.
When Theo tells Joe that Git’s ability to “time travel” reminds him one of his favorite mov-
ies, Back to the Future , Joe shares that a month ago he watched the Back to the Future  trilogy
with Neriah, his 14-year-old son.
Their walk complete, they arrive back at Theo’s office. Theo and Joe partake of the
espresso machine in the kitchen before they begin today’s lesson.
Joe So far, we’ve seen how we manage queries that retrieve information from the
system in DOP. Now I’m going to show you how we manage mutations. By a
mutation, I mean an operation that changes the state of the system.
 NOTE A mutation  is an operation that changes the state of the system.Table 4.1 The two phases of a mutation
Phase Responsibility State Implementation
Calculation Computes the next version of system data Stateless Specific
Commit Moves the system state forward Stateful Common
73 4.1 Multiple versions of the system data
Theo Is there a fundamental difference between queries and mutations in DOP?
After all, the whole state of the system is represented as a hash map. I could
easily write code that modifies part of the hash map, and it would be similar to
the code that retrieves information from the hash map.
Joe You could mutate the data in place, but then it would be challenging to ensure
that the code of a mutation doesn’t put the system into an invalid date. You
would also lose the ability to track previous versions of the system state.
Theo I see. So, how do you handle mutations in DOP?
Joe We adopt a multi-version state approach, similar to what a version control sys-
tem like Git does; we manage different versions of the system data. At a specific
point in time, the state of the system refers to a version of the system data. After
a mutation is executed, we move the reference forward.
Theo I’m confused. Is the system state mutable or immutable?
Joe The data is immutable, but the state reference is mutable.
TIP The data is immutable, but the state reference is mutable.
Noticing the look of confusion on Theo’s face, Joe draws a quick diagram on the white-
board. He then shows Theo figure 4.1, hoping that it will clear up Theo’s perplexity.
Theo Does that mean that before the code of a mutation runs, we make a copy of the
system data?
Joe No, that would be inefficient, as we would have to do a deep copy of the data.After mutation B After mutation C
Mutation A
Mutation BData V10
Data V11
Data V12Mutation A
Mutation B
Mutation CData V10
Data V11
Data V12
Data V13System State
System State
Figure 4.1 After mutation  B is executed, the system state refers to Data  V12. After 
mutation  C is executed, the system state refers to Data  V13.
Theo How does it work then?
Joe It works by using a technique called structural sharing, where most of the data
between subsequent versions of the state is shared instead of being copied.
This technique efficiently creates new versions of the system data, both in
terms of memory and computation.
Theo I’m intrigued.
TIP With structural sharing, it’s efficient (in terms of memory and computation) to
create new versions of data.
Joe I’ll explain in detail how structural sharing works in a moment.
Theo takes another look at the diagram in figure 4.1, which illustrates how the system state
refers to a version of the system data. Suddenly, a question emerges.
Theo Are the previous versions of the system data kept?
Joe In a simple application, previous versions are automatically removed by the
garbage collector. But, in some cases, we maintain historical references to pre-
vious versions of the data.
Theo What kind of cases?
Joe For example, if we want to support time travel in our system, as in Git, we can
move the system back to a previous version of the state easily.
Theo Now I understand what you mean by data is immutable, but the state reference
is mutable!
4.2 Structural sharing
As mentioned in the previous section, structural sharing  enables the efficient cre-
ation of new versions of immutable data. In DOP, we use structural sharing in the
calculation phase of a mutation to compute the next state of the system based on
the current state of the system. Inside the calculation phase, we don’t have to deal
with state management; that is delayed to the commit phase. As a consequence, the
code involved in the calculation phase of a mutation is stateless and is as simple as
the code of a query.
Theo I’m really intrigued by this more efficient way to create new versions of data.
How does it work?
Joe Let’s take a simple example from our library system. Imagine that you want to
modify the value of a field in a book in the catalog; for instance, the publica-
tion year of Watchmen . Can you tell me the information path for Watchmen ’s
publication year?
Theo takes a quick look at the catalog data in figure 4.2. Then he answers Joe’s question.
75 4.2 Structural sharing
Theo The information path for Watchmen ’s publication year is ["catalog",  "books-
ByIsbn",  "978-1779501127",  "publicationYear"] .
Joe Now, let me show how you to use the immutable function _.set  that Lodash
also provides.
Theo Wait! What do you mean by an immutable function? When I looked at the
Lodash documentation for _.set  on their website, it said that it mutates the
object.
Joe You’re right, but the default Lodash functions are not immutable. In order to
use an immutable version of the functions, we need to use the Lodash FP mod-
ule as explained in the Lodash FP guide.
 NOTE See https:/ /lodash.com/docs/4.17.15#set  to view Lodash’s documentation
for _.set , and see https:/ /github.com/lodash/lodash/wiki/FP-Guide  to view the
Lodash FP guide.
Theo Do the immutable functions have the same signature as the mutable functions?
Joe By default, the order of the arguments in immutable functions is shuffled.
The Lodash FP guide explains how to resolve this. With this piece of code,catalog
booksByIsbn
978-1779501127
title
authorIds

dave-gibbons0
alan-mooreisbn
978-1779501127
publicationYearWatchmen

bookItems

book-item-2
libId
la-central-lib
isLent
false0
book-item-1
libIdid id
nyc-cental-lib
isLent
trueauthorsById
alan-moore
name
Alan Moore
bookIsbns

978-1779501127
dave-gibbons
name
Dave Gibbons
bookIsbns

978-1779501127
Figure 4.2 Visualization of the catalog data. The nodes in the information path to Watchmen ’s publication 
year are marked with a dotted border.
the signature of the immutable functions is exactly the same as the mutable
functions.
_ = fp.convert({
  "cap": false,
  "curry": false,
  "fixed": false,
  "immutable": true,
  "rearg": false
});
TIP In order to use Lodash immutable functions, we use Lodash’s FP module, and
we configure it so that the signature of the immutable functions is the same as in the
Lodash documentation web site.
Theo So basically, I can still rely on Lodash documentation when using immutable
versions of the functions.
Joe Except for the piece in the documentation that says the function mutates the
object.
Theo Of course!
Joe Now I’ll show you how to write code that creates a version of the library data
with the immutable function _.set .
Joe’s fingers fly across Theo’s keyboard. Theo then looks at Joe’s code, which creates a ver-
sion of the library data where the Watchmen  publication year is set to 1986.
var nextLibraryData = _.set(libraryData, 
  ["catalog", "booksByIsbn",
    "978-1779501127", "publicationYear"],
  1986);
 NOTE A function is said to be immutable  when, instead of mutating the data, it cre-
ates a new version of the data without changing the data it receives.
Theo You told me earlier that structural sharing allowed immutable functions to be
efficient in terms of memory and computation. Can you tell me what makes
them efficient?
Joe With pleasure, but before that, you have to answer a series of questions. Are
you ready?
Theo Yes, sure . . .
Joe What part of the library data is impacted by updating the Watchmen  publication
year: the UserManagement  or the Catalog ?Listing 4.1 Configuring Lodash so immutable and mutable functions have same signature
Listing 4.2 Using _.set  as an immutable function
77 4.2 Structural sharing
Theo Only the Catalog .
Joe What part of the Catalog ?
Theo Only the booksByIsbn  index.
Joe What part of the booksByIsbn  index?
Theo Only the Book  record that holds the information about Watchmen .
Joe What part of the Book  record?
Theo Only the publicationYear  field.
Joe Perfect! Now, suppose that the current version of the library data looks like
this.
Joe goes to the whiteboard and draws a diagram. Figure 4.3 shows the result.
Theo So far, so good . . .
Joe Next, let me show you what an immutable function does when you use it to cre-
ate a new version of Library , where the publication year of Watchmen  is set to
1986 instead of 1987.
Joe updates his diagram on the whiteboard. It now looks like figure 4.4....
...
...Library
Catalog UserManagement
booksBylsbn
watchmen
publicationYear:1987 authorlds title:WatchmenauthorsByld
Figure 4.3 High-level visualization of the current version of Library
Theo Could you explain?
Joe The immutable function creates a fresh Library  hash map, which recursively
uses the parts of the current Library  that are common between the two ver-
sions instead of deeply copying them.
Theo It’s a bit abstract for me.
Joe The next version of Library  uses the same UserManagement  hash map as the
old one. The Catalog  inside the next Library  uses the same authorsById  as
the current Catalog . The Watchmen  Book  record inside the next Catalog  uses
all the fields of the current Book  except for the publicationYear  field.
Theo So, in fact, most parts of the data are shared between the two versions. Right?
Joe Exactly! That’s why this technique is called structural sharing .
TIP Structural sharing provides an efficient way (both in terms of memory and com-
putation) to create a new version of the data by recursively sharing the parts that don’t
need to change.
Theo That’s very cool!
Joe Indeed. Now let’s look at how to write a mutation for adding a member using
immutable functions.Library
booksByIsbn
watchmen
authorlds title:Watchmen publicationYear:1987authorsById ...
...
...«Next»
Catalog
«Next»
booksByIsbn
«Next»
watchmen
«Next»
publicationYear:1986«Next»
Library
UserManagement Catalog
Figure 4.4 Structural sharing provides an efficient way to create a new version of the data. 
Next  Library  is recursively made of nodes that use the parts of Library  that are 
common between the two.
79 4.2 Structural sharing
Once again, Joe goes to the whiteboard. Figure 4.5 shows the diagram that Joe draws to
illustrate how structural sharing looks when we add a member.
Theo Awesome! The Catalog  and the librarians  hash maps don’t have to be copied!
Joe Now, in terms of code, we have to write a Library.addMember  function that
delegates to UserManagement.addMember .
Theo I guess it’s going to be similar to the code we wrote earlier to implement the
search books query, where Library.searchBooksByTitleJSON  delegates to
Catalog.searchBooksByTitle .
Joe Similar in the sense that all the functions are static, and they receive the data
they manipulate as an argument. But there are two differences. First, a muta-
tion could fail, for instance, if the member to be added already exists. Second,
the code for Library.addMember  is a bit more elaborate than the code for
Library.searchBooksByTitleJSON  because we have to create a new version
of Library  that refers to the new version of UserManagement . Here, let me
show you an example.
UserManagement.addMember = function(userManagement, member) {
  var email = _.get(member, "email");
  var infoPath = ["membersByEmail", email];
  if(_.has(userManagement, infoPath)) {    
    throw "Member already exists.";
  }
  var nextUserManagement =  _.set(
    userManagement,     
    infoPath,
    member);
  return nextUserManagement;
};Listing 4.3 The code for the mutation that adds a memberLibrary
UserManagement Catalog
librarians
member0 member1members ...
...«Next»
Library
«Next»
userManagement
«Next»
members
Figure 4.5 Adding a member 
with structural sharing. Most of 
the data is shared between the 
two versions.
Checks if a member with 
the same email address 
already exists
Creates a new version of 
userManagement that 
includes the member
Library.addMember = function(library, member) {
  var currentUserManagement = _.get(library, "userManagement");
  var nextUserManagement = UserManagement.addMember(
    currentUserManagement,
    member);
  var nextLibrary = _.set(library, 
    "userManagement", 
    nextUserManagement);   
  return nextLibrary;
};
Theo To me, it’s a bit weird that immutable functions return an updated version of
the data instead of changing it in place.
Joe It was also weird for me when I first encountered immutable data in Clojure
seven years ago.
Theo How long did it take you to get used to it?
Joe A couple of weeks. 
4.3 Implementing structural sharing
When Joe leaves the office, Theo meets Dave near the coffee machine. Dave looks perplexed.
Dave Who’s the guy that just left the office?
Theo It’s Joe. My DOP mentor.
Dave What’s DOP?
Theo DOP refers to data-oriented programming.
Dave I never heard that term before.
Theo It’s not well-known by programmers yet, but it’s quite a powerful programming
paradigm. From what I’ve seen so far, it makes programming much simpler.
Dave Can you give me an example?
Theo I just learned about structural sharing and how it makes it possible to create
new versions of data, effectively without copying.
Dave How does that work?
Theo takes Dave to his office and shows him Joe’s diagram on the whiteboard (see figure 4.6).
It takes Theo a few minutes to explain to Dave what it does exactly, but in the end, Dave
gets it.
Dave What does the implementation of structural sharing look like?
Theo I don’t know. I used the _.set  function from Lodash.
Dave It sounds like an interesting challenge.
Theo Take the challenge if you want. Right now, I’m too tired for this recursive algo-
rithmic stuff.Creates a new version of 
library that contains the new 
version of userManagement
81 4.3 Implementing structural sharing
The next day, Theo stops by Dave’s cubicle before heading to his office. Dave, with a touch
of pride, shows Theo his implementation of structural sharing. Theo is amazed by the fact
that it’s only 11 lines of JavaScript code!
function setImmutable(map, path, v) {
  var modifiedNode = v;
  var k = path[0];
  var restOfPath = path.slice(1);
  if (restOfPath.length > 0) {
    modifiedNode = setImmutable(map[k], restOfPath, v);
  }
  var res = Object.assign({}, map);   
  res[k] = modifiedNode;
  return res;
}
Theo Dave, you’re brilliant!
Dave (smiling) Aw, shucks.
Theo Oops, I have to go. I’m already late for my session with Joe! Joe is probably wait-
ing in my office, biting his nails. Listing 4.4 The implementation of structural sharingLibrary
booksByIsbn
watchmen
authorlds title:Watchmen publicationYear:1987authorsById ...
...
...«Next»
Catalog
«Next»
booksByIsbn
«Next»
watchmen
«Next»
publicationYear:1986«Next»
Library
UserManagement Catalog
Figure 4.6 Structural sharing in action
Shallow 
clones a map 
in JavaScript.
4.4 Data safety
Joe is about to start the day’s lesson. Theo asks him a question about yesterday’s material
instead.
Theo Something isn’t clear to me regarding this structural sharing stuff. What hap-
pens if we write code that modifies the data part that’s shared between the two
versions of the data? Does the change affect both versions?
Joe Could you please write a code snippet that illustrates your question?
Theo starts typing on his laptop. He comes up with this code to illustrate modifying a piece
of data shared between two versions.
var books = {
  "978-1779501127": {
    "isbn": "978-1779501127",
    "title": "Watchmen",
    "publicationYear": 1987,
    "authorIds": ["alan-moore",
      "dave-gibbons"]
  }
};
var nextBooks = _.set(books, ["978-1779501127", "publicationYear"], 1986)
console.log("Before:", nextBooks["978-1779501127"]["authorIds"][1]);
books["978-1779501127"]["authorIds"][1] = "dave-chester-gibbons";
console.log("After:", nextBooks["978-1779501127"]["authorIds"][1]); 
// → Before: dave-gibbons
// → After: dave-chester-gibbons
Theo My question is, what is the value of isBlocked  in updatedMember ?
Joe The answer is that mutating data via the native hash map setter is forbidden.
All the data manipulation must be done via immutable functions.
 NOTE All data manipulation must be done with immutable functions. It is forbid-
den to use the native hash map setter.
Theo When you say “forbidden,” you mean that it’s up to the developer to make sure
it doesn’t happen. Right?
Joe Exactly.
Theo Is there a way to protect our system from a developer’s mistake?
Joe Yes, there is a way to ensure the immutability of the data at the level of the data
structure. It’s called persistent data structures.
Theo Are persistent data structures also efficient in terms of memory and computation?
Joe Actually, the way data is organized inside persistent data structures make them
even more efficient than immutable functions.Listing 4.5 Modifying data that’s shared between two versions
83 4.5 The commit phase of a mutation
TIP Persistent data structures are immutable at the level of the data. There is no way
to mutate them, even by mistake.
Theo Are there libraries providing persistent data structures?
Joe Definitely. I just happen to have a list of those libraries on my computer.
Joe, being well-organized for a programmer, quickly brings up his list. He shows it to Theo:
Immutable.js in JavaScript at https:/ /immutable-js.com/
Paguro in Java at https:/ /github.com/GlenKPeterson/Paguro
Immutable Collections in C# at http:/ /mng.bz/y4Ke
Pyrsistent in Python at https:/ /github.com/tobgu/pyrsistent
Hamster in Ruby at https:/ /github.com/hamstergem/hamster
Theo Why not use persistent data structures instead of immutable functions?
Joe The drawback of persistent data structures is that they are not native. This
means that working with them requires conversion from native to persistent
and from persistent to native.
Theo What approach would you recommend?
Joe If you want to play around a bit, then start with immutable functions. But for a
production application, I’d recommend using persistent data structures.
Theo Too bad the native data structures aren’t persistent!
Joe That’s one of the reasons why I love Clojure—the native data structures of the
language are immutable!
4.5 The commit phase of a mutation
So far, we saw how to implement the calculation phase of a mutation. The calculation
phase is stateless in the sense that it doesn’t make any change to the system. Now, let’s
see how to update the state of the system inside the commit phase.
Theo takes another look at the code for Library.addMember . Something bothers him:
this function returns a new state of the library that contains an additional member, but it
doesn’t affect the current state of the library.
Library.addMember = function(library, member) {
  var currentUserManagement = _.get(library, "userManagement");
  var nextUserManagement = UserManagement.addMember(
    currentUserManagement,
    member);
  var nextLibrary = _.set(library, "userManagement", nextUserManagement);
  return nextLibrary;
};
Theo I see that Library.addMember  doesn’t change the state of the library. How
does the library state get updated?Listing 4.6 The commit phase moves the system state forward
Joe That’s an excellent question. Library.addMember  deals only with data calcula-
tion and is stateless. The state is updated in the commit phase by moving for-
ward the version of the state that the system state refers to.
Theo What do you mean by that?
Joe Here’s what happens when we add a member to the system. The calculation
phase creates a version of the state that has two members. Before the commit
phase, the system state refers to the version of the state with one member. The
responsibility of the commit phase is to move the system state forward so that it
refers to the version of the state with two members.
TIP The responsibility of the commit phase is to move the system state forward to the
version of the state returned by the calculation phase.
Joe draws another illustration on the whiteboard (figure 4.7). He hopes it helps to clear up
any misunderstanding Theo may have.
Theo How is this implemented?
Joe The code is made of two classes: System , a singleton stateful class that imple-
ments the mutations, and SystemState , a singleton stateful class that manages
the system state.
Theo It sounds to me like classic OOP.
Joe Right, and this part of the system being stateful is OOP-like.
Theo I’m happy to see that you still find some utility in OOP.
Joe Meditation taught me that every part of our universe has a role to play.
Theo Nice! Could you show me some code?
Joe Sure.
Joe thinks for a moment before starting to type. He wants to show the System  class and its
implementation of the addMember  mutation.
class System {
  addMember(member) {
    var previous = SystemState.get();Listing 4.7 The System  classSystem State
System StateaddMember addMemberState with one
memberState with one
member
State with two
membersState with two
membersBefore Commit After Commit
Figure 4.7 The commit phase moves the system state forward.
85 4.6 Ensuring system state integrity
    var next = Library.addMember(previous, member);
    SystemState.commit(previous, next);     
  }
}
Theo What does SystemState  look like?
Joe I had a feeling you were going to ask that. Here’s the code for the System-
State  class, which is a stateful class!
class SystemState {
  systemState;
  get() {
    return this.systemState;
  }
  commit(previous, next) {
    this.systemState = next;
  }
}
Theo I don’t get the point of SystemState . It’s a simple class with a getter and a
commit function, right?
Joe In a moment, we are going to enrich the code of the SystemState.commit
method so that it provides data validation and history tracking. For now, the
important thing to notice is that the code of the calculation phase is stateless
and is decoupled from the code of the commit phase, which is stateful.
TIP The calculation phase is stateless. The commit phase is stateful. 
4.6 Ensuring system state integrity
Theo Something still bothers me about the way functions manipulate immutable
data in the calculation phase. How do we preserve data integrity?
Joe What do you mean?
Theo In OOP, data is manipulated only by methods that belong to the same class as
the data. It prevents other classes from corrupting the inner state of the class.
Joe Could you give me an example of an invalid state of the library?
Theo For example, imagine that the code of a mutation adds a book item to the
book lendings of a member without marking the book item as lent in the cata-
log. Then the system data would be corrupted.
Joe In DOP, we have the privilege of ensuring data integrity at the level of the
whole system instead of scattering the validation among many classes.
Theo How does that work?
Joe The fact that the code for the commit phase is common to all the mutations
allows us to validate the system data in a central place. At the beginning of the
commit phase, there is a step that checks whether the version of the systemListing 4.8 The SystemState  classSystemState is covered 
in listing 4.8.
state to be committed is valid. If the data is invalid, the commit is rejected.
Here let me show you.
SystemState.commit = function(previous, next) {
  if(!SystemValidity.validate(previous, next)) { // not implemented for now
    throw "The system data to be committed is not valid!";
  };
  this.systemData = next;
};
Theo It sounds similar to a commit hook in Git.
Joe I like your analogy!
Theo Why are you passing the previous state in previous  and the next state in next
to SystemValidity.validate ?
Joe Because it allows SystemValidity.validate  to optimize the validation in
terms of computation. For example, we could validate just the data that has
changed.
TIP In DOP, we validate the system data as a whole. Data validation is decoupled
from data manipulation.
Theo What does the code of SystemValidity.validate  look like?
Joe Someday, I will show you how to define a data schema and to validate that a
piece of data conforms to a schema.
 NOTE See chapters 7 and 12 to see how Joe defines this data schema. 
4.7 Restoring previous states
Another advantage of the multi-version state approach with immutable data that is
manipulated via structural sharing is that we can keep track of the history of all the
versions of the data without exploding the memory of our program. It allows us, for
instance, to restore the system back to an earlier state easily.
Theo You told me earlier that it was easy to restore the system to a previous state.
Could you show me how?
Joe Happily, but before that, I’d like to make sure you understand why keeping
track of all the versions of the data is efficient in terms of memory.
Theo I think it’s related to the fact that immutable functions use structural sharing,
and most of the data between subsequent versions of the state is shared.
TIP Structural sharing allows us to keep many versions of the system state without
exploding memory use.
Joe Perfect! Now, I’ll show you how simple it is to undo a mutation. In order to
implement an undo mechanism, our SystemState  class needs to have twoListing 4.9 Data validation inside the commit phase
87 4.7 Restoring previous states
references to the system data: systemData  references the current state of the
system, and previousSystemData  references the previous state of the system.
Theo That makes sense.
Joe In the commit phase, we update both previousSystemData  and systemData .
Theo What does it take to implement an undo mechanism?
Joe The undo is achieved by having systemData  reference the same version of the
system data as previousSystemData .
Theo Could you walk me through an example?
Joe To make things simple, I am going to give a number to each version of the sys-
tem state. It starts at V0, and each time a mutation is committed, the version is
incremented: V1, V2, V3, and so forth.
Theo OK.
Joe Let’s say that currently our system state is at V12 (see figure 4.8). In the
SystemState  object, systemData  refers to V12, and previousSystemData
refers to V11.
Theo So far, so good . . .
Joe Now, when a mutation is committed (for instance, adding a member), both
references move forward: systemData  refers to V13, and previousSystem-
Data  refers to V12.
Joe erases the whiteboard to make room for another diagram (figure 4.9). When he’s
through with his drawing, he shows it to Theo.systemDatapreviousSystemData
Mutation A Mutation BData V10 Data V11 Data V12
Figure 4.8 When the system state is at V12, systemData  refers to V12, and 
previousSystemData  refers to V11.
previousSystemData
Mutation A Mutation B Mutation C
systemDataData V10 Data V11 Data V12 Data V13
Figure 4.9 When a mutation is committed, systemData  refers to V13, and 
previousSystemData  refers to V12.
Theo I suppose that when we undo the mutation, both references move backward.
Joe In theory, yes, but in practice, it’s necessary to maintain a stack of all the state
references. For now, to simplify things, we’ll maintain only a reference to the
previous version. As a consequence, when we undo the mutation, both refer-
ences refer to V12. Let me draw another diagram on the whiteboard that shows
this state (see figure 4.10).
Theo Could you show me how to implement this undo mechanism?
Joe Actually, it takes only a couple of changes to the SystemState  class. Pay atten-
tion to the changes in the commit  function. Inside systemDataBeforeUpdate ,
we keep a reference to the current state of the system. If the validation and
the conflict resolution succeed, we update both previousSystemData  and
systemData .
class SystemState {
  systemData;
  previousSystemData;
  get() {
    return this.systemData;
  }
  commit(previous, next) {
    var systemDataBeforeUpdate = this.systemData;
    if(!Consistency.validate(previous, next)) {
      throw "The system data to be committed is not valid!";
    }
    this.systemData = next;
    this.previousSystemData = systemDataBeforeUpdate;
  }
  undoLastMutation() {
    this.systemData = this.previousSystemData;
  }
}Listing 4.10 The SystemState  class with undo capabilitypreviousSystemData
Mutation A Mutation B Mutation C
systemDataData V10 Data V11 Data V12 Data V13
Figure 4.10 When a mutation is undone, both systemData  and previousSystemData  refer 
to V12.
89 Summary
Theo I see that implementing System.undoLastMutation  is simply a matter of hav-
ing systemData  refer the same value as previousSystemData .
Joe As I told you, if we need to allow multiple undos, the code would be a bit more
complicated, but you get the idea.
Theo I think so. Although Back to the Future  belongs to the realm of science fiction, in
DOP, time travel is real. 
Summary
DOP principle #3 states that data is immutable.
A mutation  is an operation that changes the state of the system.
In a multi-version approach to state management, mutations are split into cal-
culation and commit phases.
All data manipulation must be done via immutable functions. It is forbidden to
use the native hash map setter.
Structural sharing  allows us to create new versions of data efficiently (in terms of
memory and computation), where data that is common between the two ver-
sions is shared instead of being copied.
Structural sharing creates a new version of the data by recursively sharing the
parts that don’t need to change.
A mutation is split in two phases: calculation and commit.
A function is said to be immutable  when, instead of mutating the data, it creates
a new version of the data without changing the data it receives.
During the calculation phase , data is manipulated with immutable functions that
use structural sharing.
The calculation phase is stateless.
During the commit phase , we update the system state.
The responsibility of the commit phase is to move the system state forward to
the version of the state returned by the calculation phase.
The data is immutable, but the state reference is mutable.
The commit phase  is stateful.
We validate the system data as a whole. Data validation is decoupled from data
manipulation.
The fact that the code for the commit phase is common to all the mutations
allows us to validate the system state in a central place before we update the
state.
Keeping the history of the versions of the system data is memory efficient due to
structural sharing .
Restoring the system to one of its previous states is straightforward due to the
clear separation between the calculation phase and the commit phase.
In order to use Lodash immutable functions, we use the Lodash FP module
(https:/ /github.com/lodash/lodash/wiki/FP-Guide ).
Lodash functions introduced in this chapter
Function Description
set(map,  path,  value) Creates a map with the same fields as map with the addition of a 
<path,  value>  field
91Basic concurrency control
Conflicts at home
The changes required for system manage concurrency are only in the commit
phase. They involve a reconciliation algorithm that is universal, in the sense that it
can be used in any system where data is represented as an immutable hash map.
The implementation of the reconciliation algorithm is efficient because subse-
quent versions of the system state are created via structural sharing.
 In the previous chapter, we illustrated the multiversion approach to state man-
agement, where a mutation is split into two distinct phases: the calculation phase
that deals only with computation, and the commit phase that moves the state ref-
erence forward. Usually, in a production system, mutations occur concurrently.
Moving the state forward naively like we did in the previous chapter is not appro-
priate. In the present chapter, we are going to learn how to handle concurrent
mutations.This chapter covers
Managing concurrent mutations with a lock-free 
optimistic concurrency control strategy
Supporting high throughput of reads and writes
Reconciliation between concurrent mutations
 In DOP, because only the code of the commit phase is stateful, that allows us to use
an optimistic concurrency control  strategy that doesn’t involve any locking mechanism. As
a consequence, the throughput of reads and writes is high. The modifications to the
code are not trivial, as we have to implement an algorithm that reconciles concurrent
mutations. But the modifications impact only the commit phase. The code for the cal-
culation phase stays the same as in the previous chapter.
 NOTE This chapter requires more of an effort to grasp. The flow of the reconcilia-
tion algorithm is definitely not trivial, and the implementation involves a nontrivial
recursion. 
5.1 Optimistic concurrency control
This morning, before getting to work, Theo takes Joe to the fitness room in the office and,
while running on the step machine, the two men talk about their personal lives again. Joe
talks about a fight he had last night with Kay, who thinks that he pays more attention to his
work than to his family. Theo recounts the painful conflict he had with Jane, his wife,
about house budget management. They went to see a therapist, an expert in Imago Rela-
tionship Therapy. Imago allowed them to transform their conflict into an opportunity to
grow and heal.
Joe’s ears perk up when he hears the word conflict  because today’s lesson is going to be
about resolving conflicts and concurrent mutations. A different kind of conflict, though. . . .
After a shower and a healthy breakfast, Theo and Joe get down to work.
Joe Yesterday, I showed you how to manage state with immutable data, assuming
that no mutations occur concurrently. Today, I am going to show you how to
deal with concurrency control in DOP.
Theo I’m curious to discover what kind of lock mechanisms you use in DOP to syn-
chronize concurrent mutations.
Joe In fact, we don’t use any lock mechanism!
Theo Why not?
Joe Locks hit performance, and if you’re not careful, your system could get into a
deadlock.
Theo So, how do you handle possible conflicts between concurrent mutations in
DOP?
Joe In DOP, we use a lock-free strategy called optimistic concurrency control. It’s a
strategy that allows databases like Elasticsearch to be highly scalable.
 NOTE See https:/ /www.elastic.co/elasticsearch/  to find out more about Elastic-
search.
Theo You sound like my couples therapist and her anger-free, optimistic conflict
resolution strategy.
Joe Optimistic concurrency control and DOP fit together well. As you will see in a
moment, optimistic concurrency control is super efficient when the system
data is immutable.
93 5.1 Optimistic concurrency control
TIP Optimistic concurrency control with immutable data is super efficient.
Theo How does it work?
Joe Optimistic concurrency control occurs when we let mutations ask forgiveness
instead of permission.
TIP Optimistic concurrency control occurs when we let mutations ask forgiveness
instead of permission.
Theo What do you mean?
Joe The calculation phase does its calculation as if it were the only mutation run-
ning. The commit phase is responsible for reconciling concurrent mutations
when they don’t conflict or for aborting the mutation.
TIP The calculation phase  does its calculation as if it were the only mutation running.
The commit phase  is responsible for trying to reconcile concurrent mutations.
Theo That sounds quite challenging to implement.
Joe Dealing with state is never trivial. But the good news is that the code for the
reconciliation logic in the commit phase is universal.
Theo Does that mean that the same code for the commit phase can be used in any
DOP system?
Joe Definitely. The code that implements the commit phase assumes nothing
about the details of the system except that the system data is represented as an
immutable map.
TIP The implementation of the commit phase in optimistic concurrency control is
universal. It can be used in any system where the data is represented by an immutable
hash map.
Theo That’s awesome!
Joe Another cool thing is that handling concurrency doesn’t require any changes
to the code in the calculation phase. From the calculation phase perspective,
the next version of the system data is computed in isolation as if no other muta-
tions were running concurrently.
Joe stands up to illustrate what he means on the whiteboard. While Theo looks at the draw-
ing in figure 5.1, Joe summarizes the information in table 5.1.
Table 5.1 The two phases of a mutation with optimistic concurrency control
Phase Responsibility State Implementation
Calculation Compute next state in isolation Stateless Specific
Commit Reconcile and update system state Stateful Common 
5.2 Reconciliation between concurrent mutations
Theo Could you give me some examples of conflicting concurrent mutations?
Joe Sure. One example would be two members trying to borrow the same book
copy. Another example might be when two librarians update the publication
year of the same book.
Theo You mentioned that the code for the reconciliation logic in the commit phase
is universal. What do you mean exactly by reconciliation logic?
Joe It’s quite similar to what could happen in Git when you merge a branch back
into the main branch.
Theo I love it when the main branch stays the same.
Joe Yes, it’s nice when the merge has no conflicts and can be done automatically.
Do you remember how Git handles the merge in that case?
Theo Git does a fast-forward; it updates the main branch to be the same as the merge
branch.
Joe Right! And what happens when you discover that, meanwhile, another devel-
oper has committed their code to the main branch?
Theo Then Git does a three-way merge, trying to combine all the changes from the
two merge branches with the main branch.
Joe Does it always go smoothly?
Theo Usually, yes, but it’s possible that two developers have modified the same line
in the same file. I then have to manually resolve the conflict. I hate when that
happens!
TIP In a production system, multiple mutations run concurrently. Before updating
the state, we need to reconcile the conflicts between possible concurrent mutations.Calculation phase
Commit phaseCapture system state
Compute next version
Abort mutation Reconcile mutations
Update system stateUpdate system stateConcurrent mutations?Yes
Yes NoConﬂict?No
Figure 5.1 The logic flow 
of optimistic concurrency 
control
95 5.2 Reconciliation between concurrent mutations
Joe In DOP, the reconciliation algorithm in the commit phase is quite similar to a
merge in Git, except instead of a manual conflict resolution, we abort the
mutation. There are three possibilities to reconcile between possible concur-
rent mutations: fast-forward, three-way merge, or abort.
Joe goes to the whiteboard again. He draws the two diagrams shown in figures 5.2 and 5.3.
Theo Could you explain in more detail?
Joe When the commit phase of a mutation starts, we have three versions of the sys-
tem state: previous , which is the version on which the calculation phase based
its computation; current , which is the current version during the commit
phase; and next , which is the version returned by the calculation phase.
Theo Why would current  be different than previous ?
Joe It happens when other mutations have run concurrently with our mutation.
Theo I see.
Joe If we are in a situation where the current state is the same as the previous state,
it means that no mutations run concurrently. Therefore, as in Git, we can
safely fast-forward and update the state of the system with the next version.
Theo What if the state has not stayed the same?
Joe Then it means that mutations have run concurrently. We have to check for
conflicts in a way similar to the three-way merge used by Git. The difference is
that instead of comparing lines, we compare fields of the system hash map.
Theo Could you explain that?Yes No
Yes NoState has stayed the same
Fast forwardConcurrent mutations compatible?
Abort 3-way Merge
Figure 5.2 The 
reconciliation flow
previouscurrent
next
The base version
for the Calculation
phaseThe version during
the Commit phase
The version
returned by the
Calculation phaseFigure 5.3 When the commit phase 
starts, there are three versions of the 
system state.
Joe We calculate the diff between previous  and next  and between previous  and
current . If the two diffs have no fields in common, then there is no conflict
between the mutations that have run concurrently. We can safely apply the
changes from previous  to next  into current .
Joe makes his explanation visual with another diagram on the whiteboard. He then shows
figure 5.4 to Theo.
Theo What if there is a conflict?
Joe Then we abort the mutation.
Theo Aborting a user request seems unacceptable.
Joe In fact, in a user-facing system, conflicting concurrent mutations are fairly rare.
That’s why it’s OK to abort and let the user run the mutation again. Here, let
me draft a table to show you the differences between Git and DOP (table 5.2).
Table 5.2 The analogy between Git and data-oriented programming
Data-oriented programming Git
Concurrent mutations Different branches
A version of the system data A commit
State A reference
Calculation phase Branching
Validation Precommit hook
Reconciliation Merge
Fast-forward Fast-forward
Three-way merge Three-way merge
Abort Manual conflict resolution
Hash map Tree (folder)
Leaf node Blob (file)
Data field Line of codediﬀPreviousCurrent
diﬀPreviousNextdiffPreviousNext
nextcurrent
merged previous
Figure 5.4 In a three-way merge, we calculate the diff between previous  and 
next , and we apply it to current .
97 5.3 Reducing collections
Theo Great! That helps, but in cases where two mutations update the same field of
the same entity, I think it’s fair enough to let the user know that the request
can’t be processed.
TIP In a user-facing system, conflicting concurrent mutations are fairly rare. 
5.3 Reducing collections
Joe Are you ready to challenge your mind with the implementation of the diff
algorithm?
Theo Let’s take a short coffee break before, if you don’t mind. Then, I’ll be ready to
tackle anything.
After enjoying large mug of hot coffee and a few butter cookies, Theo and Joe are back to
work. Their discussion on the diff algorithm continues.
Joe In the implementation of the diff algorithm, we’re going to reduce collections.
Theo I heard about reducing collections in a talk about FP, but I don’t remember
the details. Could you remind me how this works?
Joe Imagine you want to calculate the sum of the elements in a collection of num-
bers. With Lodash’s _.reduce , it would look like this.
_.reduce([1, 2, 3], function(res, elem) {
  return res + elem;
}, 0);
// →  6
Theo I don’t understand.
Joe goes to the whiteboard and writes the description of _.reduce . Theo waits patiently
until Joe puts the pen down before looking at the description.Listing 5.1 Summing numbers with _.reduce
Description of _.reduce
_.reduce  receives three arguments:
coll—A collection of elements
f—A function that receives two arguments
initVal —A value
Logic flow:
1Initialize currentRes  with initVal .
2For each element x of coll, update currentRes  with f(currentRes,  x).
3Return currentRes .
Theo Would you mind if I manually expand the logic flow of that code you just wrote
for _.reduce ?
Joe I think it’s a great idea!
Theo In our case, initVal  is 0. It means that the first call to f will be f(0,  1). Then,
we’ll have f(f(0,  1), 2) and, finally, f(f(f(0,  1), 2), 3).
Joe I like your manual expansion, Theo! Let’s make it visual.
Now Theo goes to the whiteboard and draws a diagram. Figure 5.5 shows what that looks like.
Theo It’s much clearer now. I think that by implementing my custom version of
_.reduce , it will make things 100% clear.
It takes Theo much less time than he expected to implement reduce() . In no time at all,
he shows Joe the code.
function reduce(coll, f, initVal) {
  var currentRes = initVal;
  for (var i = 0; i < coll.length; i++) {  
    currentRes = f(currentRes, coll[i])
  }
  return currentRes;
}
After checking that Theo’s code works as expected (see listing 5.3), Joe is proud of Theo.
He seems to be catching on better than he anticipated.
reduce([1, 2, 3], function(res, elem) {
  return res + elem;
}, 0);
// →  6
Joe Well done!Listing 5.2 Custom implementation of _.reduce
Listing 5.3 Testing the custom implementation of reduce()f
f
fa2
a1
a0 initVal Figure 5.5 Visualization 
of _.reduce
We could use 
forEach instead 
of a for loop.
99 5.4 Structural difference
5.4 Structural difference
 NOTE This section deals with the implementation of a structural diff algorithm . Feel
free to skip this section if you don’t want to challenge your mind right now with the
details of a sophisticated use of recursion. It won’t prevent you from enjoying the rest
of the book. You can come back to this section later.
Theo How do you calculate the diff between various versions of the system state?
Joe That’s the most challenging part of the reconciliation algorithm. We need to
implement a structural diff algorithm for hash maps.
Theo In what sense is the diff structural?
Joe The structural diff algorithm looks at the structure of the hash maps and
ignores the order of the fields.
Theo Could you give me an example?
Joe Let’s start with maps without nested fields. Basically, there are three kinds of
diffs: field replacement, field addition, and field deletion. In order to make
things not too complicated, for now, we’ll deal only with replacement and
addition.
Joe once again goes to the whiteboard and draws table 5.3, representing the three kinds of
diffs. Theo is thinking the whiteboard is really starting to fill up today.
Theo I notice that the order of the maps matters a lot. What about nested fields?
Joe It’s the same idea, but the nesting makes it a bit more difficult to grasp.
Joe changes several of the columns in table 5.3. When he’s through, he shows Theo the
nested fields in table 5.4.Table 5.3 Kinds of structural differences between maps without nested fields
Kind First map Second map Diff
Replacement {"a": 1} {"a": 2} {"a": 2}
Addition {"a": 1} {"a": 1, "b": 2} {"b": 2}
Deletion {"a": 1, "b": 2} {"a": 1} Not supported
Table 5.4 Kinds of structural differences between maps with nested fields
Kind First map Second map Diff
Replacement {
  "a": {
    "x": 1
  }
}{
  "a": {
    "x": 2
  }
}{
  "a": {
    "x": 2
  }
}
 NOTE The version of the structural diff algorithm illustrated in this chapter does
not deal with deletions. Dealing with deletions is definitely possible, but it requires a
more complicated algorithm.
Theo As you said, it’s harder to grasp. What about arrays?
Joe We compare the elements of the arrays in order: if they are equal, the diff is
null ; if they differ, the diff has the value of the second array.
Joe summarizes the various kinds of diffs in another table on the whiteboard. Theo looks
at the result in table 5.5.
Theo This usage of null  is a bit weird but OK. Is it complicated to implement the
structural diff algorithm?
Joe Definitely! It took a good dose of mental gymnastics to come up with these 30
lines of code.
Joe downloads the code from one his personal repositories. Theo, with thumb and forefin-
gers touching his chin and his forehead slightly tilted, studies the code.
function diffObjects(data1, data2) {
  var emptyObject = _.isArray(data1) ? [] : {};   
  if(data1 == data2) {Addition {
  "a": {
    "x": 1
  }
}{
  "a": {
    "x": 1,
    "y": 2,
  }
}{
  "a": {
    "y": 2
  }
}
Deletion {
  "a": {
    "x": 1,
    "y": 2,
  }
}{
  "a": {
    "y": 2
  }
}Not supported
Table 5.5 Kinds of structural differences between arrays without nested elements
Kind First array Second array Diff
Replacement [1] [2] [2]
Addition [1] [1, 2] [null, 2]
Deletion [1, 2] [1] Not supported
Listing 5.4 The implementation of a structural diffTable 5.4 Kinds of structural differences between maps with nested fields  (continued)
Kind First map Second map Diff
_.isArray checks whether 
its argument is an array.
101 5.4 Structural difference
    return emptyObject;
  }
  var keys = _.union(_.keys(data1), _.keys(data2));    
  return _.reduce(keys,
    function (acc, k) {
      var res = diff(
        _.get(data1, k),
        _.get(data2, k));
      if((_.isObject(res) && _.isEmpty(res)) ||    
        (res == "no-diff")) {                
        return acc;
      }
      return _.set(acc, [k], res);
    },
    emptyObject);
}
function diff(data1, data2) {
  if(_.isObject(data1) && _.isObject(data2)) {   
    return diffObjects(data1, data2);
  }
  if(data1 !== data2) {
    return data2;
  }
  return "no-diff";                          
}
Theo Wow! It involves a recursion inside a reduce! I’m sure Dave will love this, but
I’m too tired to understand this code right now. Let’s focus on what it does
instead of how it does it.
In order familiarize himself with the structural diff algorithm, Theo runs the algorithm
with examples from the table that Joe drew on the whiteboard. While Theo occupies his
fingers with more and more complicated examples, his mind wanders in the realm of
performance.
var data1 = {
  "a": {
    "x": 1,
    "y": [2, 3],
    "z": 4
  }
};
var data2 = {
  "a": {
    "x": 2,
    "y": [2, 4],
    "z": 4
  }
}Listing 5.5 An example of usage of a structural diff_.union creates an 
array of unique 
values from two 
arrays (like union of 
two sets in Maths).
_.isObject checks 
whether its argument 
is a collection (either 
a map or an array).
_.isEmpty
checks
whether its
argument
is an empty
collection."no-diff" is how 
we mark that 
two values are 
the same.
diff(data1, data2);
//{
//  "a":  {
//    "x": 2,
//    "y":  [
//      undefined,
//      4
//    ]
//  }
//}
Theo What about the performance of the structural diff algorithm? It seems that the
algorithm goes over the leaves of both pieces of data?
Joe In the general case, that’s true. But, in the case of system data that’s manipu-
lated with structural sharing, the code is much more efficient.
Theo What do you mean?
Joe With structural sharing, most of the nested objects are shared between two ver-
sions of the system state. Therefore, most of the time, when the code enters
diffObjects , it will immediately return because data1  and data2  are the same.
TIP Calculating the diff between two versions of the state is efficient because two
hash maps created via structural sharing from the same hash map have most of their
nodes in common.
Theo Another benefit of immutable data . . . Let me see how the diff algorithm
behaves with concurrent mutations. I think I’ll start with a tiny library with no
users and a catalog with a single book, Watchmen .
var library = {
  "catalog": {
    "booksByIsbn": {
      "978-1779501127": {
        "isbn": "978-1779501127",
        "title": "Watchmen",
        "publicationYear": 1987,
        "authorIds": ["alan-moore", "dave-gibbons"]
      }
    },
    "authorsById": {
      "alan-moore": {
        "name": "Alan Moore",
        "bookIsbns": ["978-1779501127"]
      },
      "dave-gibbons": {
        "name": "Dave Gibbons",
        "bookIsbns": ["978-1779501127"]
      }
    }
  }
};Listing 5.6 The data for a tiny library
103 5.4 Structural difference
Joe I suggest that we start with nonconflicting mutations. What do you suggest?
Theo A mutation that updates the publication year of Watchmen  and a mutation that
updates both the title of Watchmen  and the name of the author of Watchmen .
On his laptop, Theo creates three versions of the library. He shows Joe his code, where one
mutation updates the publication year of Watchmen , and the other one updates the title of
Watchmen  and the author’s name.
var previous = library;
var next = _.set(
  library,
  ["catalog", "booksByIsbn", "978-1779501127", "publicationYear"],
  1986);
var libraryWithUpdatedTitle = _.set(
  library,
  ["catalog", "booksByIsbn", "978-1779501127", "title"],
  "The Watchmen");
var current = _.set(
  libraryWithUpdatedTitle,
  ["catalog", "authorsById", "dave-gibbons", "name"],
  "David Chester Gibbons");
Theo I’m curious to see what the diff between previous  and current  looks like.
Joe Run the code and you’ll see.
Theo runs the code snippets for the structural diff between previous  and next  and for
the structural diff between previous  and current . His curiosity satisfied, Theo finds it’s
all beginning to make sense.
diff(previous, next);
//{
//    "catalog": {
//        "booksByIsbn": {
//            "978-1779501127": {
//                "publicationYear": 1986
//            }
//        }
//    }
//}
diff(previous, current);
//{
//  "authorsById": {
//    "dave-gibbons": {
//      "name": "David Chester Gibbons",Listing 5.7 Two nonconflicting mutations
Listing 5.8 Structural diff between maps with a single difference
Listing 5.9 Structural diff between maps with two differences
//    }
//  },
//  "catalog": {
//    "booksByIsbn": {
//      "978-1779501127": {
//        "title": "The Watchmen"
//      }
//    }
//  }
//}
//
Joe Can you give me the information path of the single field in the structural diff
between previous  and next ?
Theo It’s ["catalog",  "booksByIsbn",  "978-1779501127",  "publicationYear"] .
Joe Right. And what are the information paths of the fields in the structural diff
between previous  and current ?
Theo It’s ["catalog",  "booksByIsbn",  "978-1779501127",  "title"]  for the book
title and ["authorsById",  "dave-gibbons",  "name"]  for the author’s name.
Joe Perfect! Now, can you figure out how to detect conflicting mutations by
inspecting the information paths of the structural diffs?
Theo We need to check if they have an information path in common or not.
Joe Exactly! If they have, it means the mutations are conflicting.
Theo But I have no idea how to write code that retrieves the information paths of a
nested map.
Joe Once again, it’s a nontrivial piece of code that involves a recursion inside a
reduce . Let me download another piece of code from my repository and show
it to you.
function informationPaths (obj, path = []) {
  return _.reduce(obj, 
    function(acc, v, k) {
      if (_.isObject(v)) {
        return _.concat(acc,
          informationPaths(v,
            _.concat(path, k)));
      }
      return _.concat(acc, [_.concat(path, k)]); 
    },
    []);
}
Theo Let me see if your code works as expected with the structural diffs of the
mutations.
Theo tests Joe’s code with two code snippets. The first shows the information paths of the
structural diff between previous  and next , and the second shows the information paths
of the structural diff between previous  and current .Listing 5.10 Calculating the information paths of a (nested) map
105 5.4 Structural difference
informationPaths(diff(previous, next)); 
// → ["catalog.booksByIsbn.978-1779501127.publicationYear"]
informationPaths(diff(previous, current));   
// [
//  [
//    "catalog",
//    "booksByIsbn",
//    "978-1779501127",
//    "title"
//  ],
//  [
//    "authorsById",
//    "dave-gibbons",
//    "name"
//  ]
//]
Theo Nice! I assume that Lodash has a function that checks whether two arrays have
an element in common.
Joe Almost. There is _.intersection , which returns an array of the unique values
that are in two given arrays. For our purpose, though, we need to check
whether the intersection is empty. Here, look at this example.
function havePathInCommon(diff1, diff2) {
  return !_.isEmpty(_.intersection(informationPaths(diff1),
    informationPaths(diff2)));
}
Theo You told me earlier that in the case of nonconflicting mutations, we can
safely patch the changes induced by the transition from previous  to next
into current . How do you implement that?
Joe We do a recursive merge between current  and the diff between previous  and
next .
Theo Does Lodash provide an immutable version of recursive merge?
Joe Yes, here’s another example. Take a look at this code.
_.merge(current, (diff(previous, next))); 
//{
// "authorsById": {
//   "dave-gibbons": {
//     "name": "David Chester Gibbons"
//   }
// },Listing 5.11 Fields that differ between previous  and next
Listing 5.12 Fields that differ between previous  and current
Listing 5.13 Checking whether two diff maps have a common information path
Listing 5.14 Applying a patch
// "catalog": {
//   "authorsById": {
//     "alan-moore": {
//       "bookIsbns": ["978-1779501127"]
//       "name": "Alan Moore"
//     },
//     "dave-gibbons": {
//       "bookIsbns": ["978-1779501127"],
//       "name": "Dave Gibbons"
//     },
//   },
//   "booksByIsbn": {
//     "978-1779501127": {
//       "authorIds": ["alan-moore", "dave-gibbons"],
//       "isbn": "978-1779501127",
//       "publicationYear": 1986,
//       "title": "The Watchmen"
//     }
//   }
// }
//}
Theo Could it be as simple as this?
Joe Indeed. 
5.5 Implementing the reconciliation algorithm
Joe All the pieces are now in place to implement our reconciliation algorithm.
Theo What kind of changes are required?
Joe It only requires changes in the code of SystemState.commit . Here, look at
this example on my laptop.
class SystemState {
  systemData;
  get() {
    return this.systemData;
  }
  set(_systemData) {
    this.systemData = _systemData;
  }
  commit(previous, next) {
    var nextSystemData = SystemConsistency.reconcile(
      this.systemData,       
      previous,
      next);
    if(!SystemValidity.validate(previous, nextSystemData)) {
      throw "The system data to be committed is not valid!";
    };Listing 5.15 The SystemState  class
SystemConsistency class is 
implemented in listing 5. 16.
107 5.5 Implementing the reconciliation algorithm
    this.systemData = nextSystemData;
  }
}
Theo How does SystemConsistency  do the reconciliation?
Joe The SystemConsistency  class starts the reconciliation process by comparing
previous  and current . If they are the same, then we fast-forward and return
next . Look at this code for SystemConsistency .
class SystemConsistency {
  static threeWayMerge(current, previous, next) {
    var previousToCurrent = diff(previous, current);         
    var previousToNext = diff(previous, next);
    if(havePathInCommon(previousToCurrent, previousToNext)) {
      return _.merge(current, previousToNext);
    }
    throw "Conflicting concurrent mutations.";
  }
  static reconcile(current, previous, next) {
    if(current == previous) {
      return next;                                           
    }
    return SystemConsistency.threeWayMerge(current,
      previous,
      next);
  }
}
Theo Wait a minute! Why do you compare previous  and current  by reference?
You should be comparing them by value, right? And, it would be quite expen-
sive to compare all the leaves of the two nested hash maps!
Joe That’s another benefit of immutable data. When the data is not mutated, it is
safe to compare references. If they are the same, we know for sure that the data
is the same.
TIP When data is immutable, it is safe to compare by reference, which is super fast.
When the references are the same, it means that the data is the same.
Theo What about the implementation of the three-way merge algorithm?
Joe When previous  differs from current , it means that concurrent mutations
have run. In order to determine whether there is a conflict, we calculate two
diffs: the diff between previous  and current  and the diff between previous
and next . If the intersection between the two diffs is empty, it means there is
no conflict. We can safely patch the changes between previous  to next  into
current .
Theo takes a closer look at the code for the SystemConsistency  class in listing 5.16. He
tries to figure out if the code is thread-safe or not.Listing 5.16 The reconciliation flow in action
When the system 
state is the same 
as the state used 
by the calculation 
phase, we fast-
forward.
Theo I think the code for SystemConsistency  class is not thread-safe! If there’s a
context switch between checking whether the system has changed in the
SystemConsistency  class and the updating of the state in SystemData  class, a
mutation might override the changes of a previous mutation.
Joe You are totally right! The code works fine in a single-threaded environment
like JavaScript, where concurrency is handled via an event loop. However, in a
multi-threaded environment, the code needs to be refined in order to be
thread-safe. I’ll show you some day.
 NOTE The SystemConsistency  class is not thread-safe. We will make it thread-safe
in chapter 8.
Theo I think I understand why you called it optimistic concurrency control. It’s
because we assume that conflicts don’t occur too often. Right?
Joe Correct! It makes me wonder what your therapist would say about conflicts that
cannot be resolved. Are there some cases where it’s not possible to reconcile
the couple?
Theo I don’t think she ever mentioned such a possibility.
Joe She must be a very optimistic person. 
Summary
Optimistic concurrency control  allows mutations to ask forgiveness instead of
permission.
Optimistic concurrency control is lock-free .
Managing concurrent mutations of our system state with optimistic concurrency
control allows our system to support a high throughput of reads and writes.
Optimistic concurrency control with immutable data is super efficient.
Before updating the state, we need to reconcile  the conflicts between possible con-
current mutations.
We reconcile between concurrent mutations in a way that is similar to how Git han-
dles a merge between two branches: either a fast-forward or a three-way merge.
The changes required to let our system manage concurrency are only in the
commit phase.
The calculation phase  does its calculation as if it were the only mutation running.
The commit phase  is responsible for trying to reconcile concurrent mutations.
The reconciliation algorithm  is universal in the sense that it can be used in any sys-
tem where the system data is represented as an immutable hash map.
The implementation of the reconciliation algorithm is efficient, as it leverages
the fact that subsequent versions of the system state are created via structural
sharing.
In a user-facing system, conflicting concurrent mutations are fairly rare.
When we cannot safely reconcile between concurrent mutations, we abort the
mutation and ask the user to try again.
109 Summary
Calculating the structural diff  between two versions of the state is efficient because
two hash maps created via structural sharing from the same hash map have most
of their nodes in common.
When data is immutable, it is safe to compare by reference, which is fast. When
the references are the same, it means that the data is the same.
There are three kinds of structural differences between two nested hash maps:
replacement, addition, and deletion.
Our structural diff algorithm supports replacements and additions but not
deletions.
Lodash functions introduced in this chapter
Function Description
concat(arrA,  arrB) Creates an new array, concatenating arrA  and arrB
intersection(arrA,  arrB) Creates an array of unique values both in arrA  and arrB
union(arrA,  arrB) Creates an array of unique values from arrA  and arrB
find(coll,  pred) Iterates over elements of coll , returning the first element for 
which pred  returns true
isEmpty(coll) Checks if coll  is empty
reduce(coll,  f, initVal) Reduces coll  to a value that is the accumulated result of running 
each element in coll  through f, where each successive invoca-
tion is supplied the return value of the previous
isArray(coll) Checks if coll  is an array
isObject(coll) Checks if coll  is a collection
110Unit tests
Programming at a coffee shop
In a data-oriented system, our code deals mainly with data manipulation: most of
our functions receive data and return data. As a consequence, it’s quite easy to
write unit tests to check whether our code behaves as expected. A unit test is made
of test cases that generate data input and compare the data output of the function
with the expected data output. In this chapter, we write unit tests for the queries
and mutations that we wrote in the previous chapters. 
6.1 The simplicity of data-oriented test cases
Theo and Joe are seated around a large wooden table in a corner of “La vie est belle,” a
nice little French coffee shop, located near the Golden Gate Bridge. Theo orders a café
au lait with a croissant, and Joe orders a tight espresso with a pain au chocolat. Instead
of the usual general discussions about programming and life when they’re out of theThis chapter covers
Generation of the minimal data input for a 
test case
Comparison of the output of a function with 
the expected output
Guidance about the quality and the quantity 
of the test cases
111 6.1 The simplicity of data-oriented test cases
office, Joe leads the discussion towards a very concrete topic—unit tests. Theo asks Joe for
an explanation.
Theo Are unit tests such a simple topic that we can tackle it here in a coffee shop?
Joe Unit tests in general, no. But unit tests for data-oriented code, yes!
Theo Why does that make a difference?
Joe The vast majority of the code base of a data-oriented system deals with data
manipulation.
Theo Yeah. I noticed that almost all the functions we wrote so far receive data and
return data.
TIP Most of the code in a data-oriented system deals with data manipulation.
Joe Writing a test case for functions that deal with data is only about generating
data input and expected output, and comparing the output of the function
with the expected output.
Theo That’s it?
Joe Yes. As you’ll see in a moment, in DOP, there’s usually no need for mock
functions.
Theo I understand how to compare primitive values like strings or numbers, but I’m
not sure how I would compare data collections like maps.
Joe You compare field by field.
Theo Recursively?
Joe Yes!
Theo Oh no! I’m not able to write any recursive code in a coffee shop. I need the
calm of my office for that kind of stuff.
Joe Don’t worry. In DOP, data is represented in a generic way. There is a generic
function in Lodash called _.isEqual  for recursive comparison of data collec-
tions. It works with both maps and arrays.
Joe opens his laptop. He is able to convince Theo by executing a few code snippets with
_.isEqual  to compare an equal data collection with a non-equal one.
_.isEqual({
  "name": "Alan Moore",
  "bookIsbns": ["978-1779501127"]The steps of a test case
1Generate data input: dataIn
2Generate expected output: dataOut
3Compare the output of the function with the expected output: f(dataIn)  and
dataOut
Listing 6.1 Comparing an equal data collection recursively
}, {
    "name": "Alan Moore",
    "bookIsbns": ["978-1779501127"]
  });
// → true
_.isEqual({
  "name": "Alan Moore",
  "bookIsbns": ["978-1779501127"]
}, {
    "name": "Alan Moore",
    "bookIsbns": ["bad-isbn"]
  });
// → false
Theo Nice!
Joe Most of the test cases in DOP follow this pattern.
Theo decides he wants to try this out. He fires up his laptop and types a few lines of
pseudocode.
var dataIn = {
  // input
};
var dataOut = {
  // expected output
};
_.isEqual(f(dataIn), dataOut);
TIP It’s straightforward to write unit tests for code that deals with data manipulation.
Theo Indeed, this looks like something we can tackle in a coffee shop!
6.2 Unit tests for data manipulation code
A waiter in an elegant bow tie brings Theo his croissant and Joe his pain au chocolat. The
two friends momentarily interrupt their discussion to savor their French pastries. When
they’re done, they ask the waiter to bring them their drinks. Meanwhile, they resume the
discussion.
Joe Do you remember the code flow of the implementation of the search query?
Theo Let me look again at the code that implements the search query.
Theo brings up the implementation of the search query on his laptop. Noticing that Joe is
chewing on his nails again, he quickly checks out the code.Listing 6.2 Comparing a non-equal data collection recursively
Listing 6.3 The general pattern of a data-oriented test case
113 6.2 Unit tests for data manipulation code
class Catalog {
  static authorNames(catalogData, authorIds) {
    return _.map(authorIds, function(authorId) {
      return _.get(catalogData, ["authorsById", authorId, "name"]);
    });
  }
  static bookInfo(catalogData, book) {
    var bookInfo =  {
      "title": _.get(book, "title"),
      "isbn": _.get(book, "isbn"),
      "authorNames": Catalog.authorNames(catalogData,
        _.get(book, "authorIds"))
    };
    return bookInfo;
  }
  static searchBooksByTitle(catalogData, query) {
    var allBooks = _.get(catalogData, "booksByIsbn");
    var matchingBooks = _.filter(allBooks, function(book) {
      return _.get(book, "title").includes(query);
    });
    var bookInfos = _.map(matchingBooks, function(book) {
      return Catalog.bookInfo(catalogData, book);
    });
    return bookInfos;
  }
}
class Library {
  static searchBooksByTitleJSON(libraryData, query) {
    var catalogData = _.get(libraryData, "catalog");
    var results = Catalog.searchBooksByTitle(catalogData, query);
    var resultsJSON = JSON.stringify(results);
    return resultsJSON;
  }
}
6.2.1 The tree of function calls
The waiter brings Theo his café au lait and Joe his tight espresso. They continue their dis-
cussion while enjoying their coffees.
Joe Before writing a unit test for a code flow, I find it useful to visualize the tree of
function calls of the code flow.
Theo What do you mean by a tree of function calls?
Joe Here, I’ll draw the tree of function calls for the Library.searchBooksBy-
TitleJSON  code flow.
Joe puts down his espresso and takes a napkin from the dispenser. He carefully places it
flat on the table and starts to draw. When he is done, he shows the illustration to Theo (see
figure 6.1).Listing 6.4 The code involved in the implementation of the search query
Theo Nice! Can you teach me how to draw a tree of function calls like that?
Joe Sure. The root of the tree is the name of the function for which you draw the
tree, in our case, Library.searchBooksByTitleJSON . The children of a
node in the tree are the names of the functions called by the function. For exam-
ple, if you look again at the code for Library.searchBooksByTitleJSON  (list-
ing 6.4), you’ll see that it calls Catalog.searchBooksByTitle , _.get , and
JSON.stringify .
Theo How long would I continue to recursively expand the tree?
Joe You continue until you reach a function that doesn’t belong to the code base
of your application. Those nodes are the leaves of our tree; for example, the
functions from Lodash : _.get , _.map , and so forth.
Theo What if the code of a function doesn’t call any other functions?
Joe A function that doesn’t call any other function would be a leaf in the tree.
Theo What about functions that are called inside anonymous functions like Catalog
.bookInfo ?
JoeCatalog.bookInfo  appears in the code of Catalog.searchBooksByTitle .
Therefore, it is considered to be a child node of Catalog.searchBooksBy-
Title . The fact that it is nested inside an anonymous function is not relevant
in the context of the tree of function calls.
 NOTE A tree of function calls for a function f is a tree where the root is f, and the
children of a node g in the tree are the functions called by g. The leaves of the tree are
functions that are not part of the code base of the application. These are functions
that don’t call any other functions.
Theo It’s very cool to visualize my code as a tree, but I don’t see how it relates to
unit tests.Library.searchBooksByTitleJSON
_.get JSON.stringify Catalog.searchBooksByTitle
_.get _.map _.ﬁlter Catalog.bookInfo
_.get Catalog.authorNames
_.get _.map
Figure 6.1 The tree of function calls for the search query code flow
115 6.2 Unit tests for data manipulation code
Joe The tree of function calls guides us about the quality and the quantity of test
cases we should write.
Theo How?
Joe You’ll see in a moment. 
6.2.2 Unit tests for functions down the tree
Joe Let’s start from the function that appears in the deepest node in our tree:
Catalog.authorNames .  T a k e  a  l o o k  a t  t h e  c o d e  f o r  Catalog.authorNames
and tell me what are the input and the output of Catalog.authorNames .
Joe turns his laptop so Theo can a closer look at the code. Theo takes a sip of his café au
lait as he looks over what’s on Joe’s laptop.
Catalog.authorNames = function (catalogData, authorIds) {
  return _.map(authorIds, function(authorId) {
    return _.get(catalogData, ["authorsById", authorId, "name"]);
  });
};
Theo The input of Catalog.authorNames  is catalogData  and authorIds . The
output is authorNames .
Joe Would you do me a favor and express it visually?
Theo Sure.
It’s Theo’s turn to grab a napkin. He draws a small rectangle with two inward arrows and
one outward arrow as in figure 6.2.
Joe Excellent! Now, how many combinations of input would you include in the
unit test for Catalog.authorNames ?
Theo Let me see.
Theo reaches for another napkin. This time he creates a table to gather his thoughts
(table 6.1).Listing 6.5 The code of Catalog.authorNames
Catalog.authorNames()catalogData authorIds
authorNamesFigure 6.2 Visualization of the input 
and output of Catalog.authorNames
Theo To begin with, I would have a catalogData  with two author IDs and call
Catalog.authorNames  with three arguments: an empty array, an array with a
single author ID, and an array with two author IDs.
Joe How would you generate the catalogData ?
Theo Exactly as we generated it before.
Turning to his laptop, Theo writes the code for catalogData . He shows it to Joe.
var catalogData = {
  "booksByIsbn": {
    "978-1779501127": {
      "isbn": "978-1779501127",
      "title": "Watchmen",
      "publicationYear": 1987,
      "authorIds": ["alan-moore", "dave-gibbons"],
      "bookItems": [
        {
          "id": "book-item-1",
          "libId": "nyc-central-lib",
          "isLent": true
        },
        {
          "id": "book-item-2",
          "libId": "nyc-central-lib",
          "isLent": false
        }
      ]
    }
  },
  "authorsById": {
    "alan-moore": {
      "name": "Alan Moore",
      "bookIsbns": ["978-1779501127"]
    },
    "dave-gibbons": {
      "name": "Dave Gibbons",
      "bookIsbns": ["978-1779501127"]
    }
  }
};Table 6.1 The table of test cases for Catalog.authorNames
catalogData authorIds authorNames
Catalog with two authors Empty array Empty array
Catalog with two authors Array with one author ID Array with one author name
Catalog with two authors Array with two author IDs Array with two author names
Listing 6.6 A complete catalogData  map
117 6.2 Unit tests for data manipulation code
Joe You could use your big catalogData  map for the unit test, but you could also
use a smaller map in the context of Catalog.authorNames . You can get rid of
the booksByIsbn  field of the catalogData  and the bookIsbns  fields of the
authors.
Joe deletes a few lines from catalogData  and gets a much smaller map. He shows the revi-
sion to Theo.
var catalogData = {
  "authorsById": {
    "alan-moore": {
      "name": "Alan Moore"
    },
    "dave-gibbons": {
      "name": "Dave Gibbons"
    }
  }
};
Theo Wait a minute! This catalogData  is not valid.
Joe In DOP, data validity depends on the context. In the context of Library
.searchBooksByTitleJSON  and Catalog.searchBooksByTitle , the mini-
mal version of catalogData  is indeed not valid. However, in the context of
Catalog.bookInfo  and Catalog.authorNames , it is perfectly valid. The reason
is that those two functions access only the authorsById  field of catalogData .
TIP The validity of the data depends on the context.
Theo Why is it better to use a minimal version of the data in a test case?
Joe For a very simple reason—the smaller the data, the easier it is to manipulate.
TIP The smaller the data, the easier it is to manipulate.
Theo I’ll appreciate that when I write the unit tests!
Joe Definitely! One last thing before we start coding: how would you check that the
output of Catalog.authorNames  is as expected?
Theo I would check that the value returned by Catalog.authorNames  is an array
with the expected author names.
Joe How would you handle the array comparison?
Theo Let me think. I want to compare by value, not by reference. I guess I’ll have to
check that the array is of the expected size and then check member by mem-
ber, recursively.
Joe That’s too much of a mental burden when you’re in a coffee shop. As I showed
you earlier (see listing 6.1), we can recursively compare two data collections by
value with _.isEqual  from Lodash.Listing 6.7 A minimal version of catalogData
TIP We can compare the output and the expected output of our functions with
_.isEqual .
Theo Sounds good! Let me write the test cases.
Theo starts typing on his laptop. After a few minutes, he has some test cases for Catalog
.authorNames , each made from a function call to Catalog.authorNames  wrapped in
_.isEqual .
var catalogData = {
  "authorsById": {
    "alan-moore": {
      "name": "Alan Moore"
    },
    "dave-gibbons": {
      "name": "Dave Gibbons"
    }
  }
};
_.isEqual(Catalog.authorNames(catalogData, []), []);
_.isEqual(Catalog.authorNames(
  catalogData, 
  ["alan-moore"]),
  ["Alan Moore"]);
_.isEqual(Catalog.authorNames(catalogData, ["alan-moore", "dave-gibbons"]),
  ["Alan Moore", "Dave Gibbons"]);
Joe Well done! Can you think of more test cases?
Theo Yes. There are test cases where the author ID doesn’t appear in the catalog
data, and test cases with empty catalog data. With minimal catalog data and
_.isEqual , it’s really easy to write lots of test cases!
Theo really enjoys this challenge. He creates a few more test cases to present to Joe.
_.isEqual(Catalog.authorNames({}, []), []);
_.isEqual(Catalog.authorNames({}, ["alan-moore"]), [undefined]);
_.isEqual(Catalog.authorNames(catalogData, ["alan-moore", 
  "albert-einstein"]), ["Alan Moore", undefined]);
_.isEqual(Catalog.authorNames(catalogData, []), []);
_.isEqual(Catalog.authorNames(catalogData, ["albert-einstein"]),
  [undefined]);
Theo How do I run these unit tests?
Joe You use your preferred test framework.Listing 6.8 Unit test for Catalog.authorNames
Listing 6.9 More test cases for Catalog.authorNames
119 6.2 Unit tests for data manipulation code
 NOTE We don’t deal here with test runners and test frameworks. We deal only with
the logic of the test cases. 
6.2.3 Unit tests for nodes in the tree
Theo I’m curious to see what unit tests for an upper node in the tree of function calls
look like.
Joe Sure. Let’s write a unit test for Catalog.bookInfo . How many test cases would
you have for Catalog.bookInfo ?
Catalog.bookInfo = function (catalogData, book) {
  return  {
    "title": _.get(book, "title"),
    "isbn": _.get(book, "isbn"),
    "authorNames": Catalog.authorNames(catalogData, 
      _.get(book, "authorIds"))
  };
};
Theo takes another look at the code for Catalog.bookInfo  on his laptop. Then, reaching
for another napkin, he draws a diagram of its input and output (see figure 6.3).
Theo I would have a similar number of test cases for Catalog.authorNames : a book
with a single author, with two authors, with existing authors, with non-existent
authors, with . . .
Joe Whoa! That’s not necessary. Given that we have already written unit tests for
Catalog.authorNames , we don’t need to check all the cases again. We simply
need to write a minimal test case to confirm that the code works.
TIP When we write a unit test for a function, we assume that the functions called by
this function are covered by unit tests and work as expected. It significantly reduces
the quantity of test cases in our unit tests.
Theo That makes sense.
Joe How would you write a minimal test case for Catalog.bookInfo ?
Theo once again takes a look at the code for Catalog.bookInfo  (see listing 6.10). Now he
can answer Joe’s question.Listing 6.10 The code of Catalog.bookInfo
Catalog.bookInfo()catalogData book
bookInfoFigure 6.3 Visualization of the input 
and output of Catalog.bookInfo
Theo I would use the same catalog data as for Catalog.authorNames  and a book
record. I’d test that the function behaves as expected by comparing its return
value with a book info record using _.isEqual . Here, let me show you.
It takes Theo a bit more time to write the unit test. The reason is that the input and the
output of Catalog.authorNames  are both records. Dealing with a record is more complex
than dealing with an array of strings (as it was the case for Catalog.authorNames ). Theo
appreciates the fact that _.isEqual  saves him from writing code that compares the two
maps property by property. When he’s through, he shows the result to Joe and takes a nap-
kin to wipe his forehead.
var catalogData = {
  "authorsById": {
    "alan-moore": {
      "name": "Alan Moore"
    },
    "dave-gibbons": {
      "name": "Dave Gibbons"
    }
  }
};
var book = {
  "isbn": "978-1779501127",
  "title": "Watchmen",
  "publicationYear": 1987,
  "authorIds": ["alan-moore", "dave-gibbons"]
};
var expectedResult = {
  "authorNames": ["Alan Moore", "Dave Gibbons"],
  "isbn": "978-1779501127",
  "title": "Watchmen",
};
var result = Catalog.bookInfo(catalogData, book);
_.isEqual(result, expectedResult);
Joe Perfect! Now, how would you compare the kind of unit tests for Catalog
.bookInfo  with the unit tests for Catalog.authorNames ?
Theo On one hand, there is only a single test case in the unit test for Catalog.book-
Info . On the other hand, the data involved in the test case is more complex
than the data involved in the test cases for Catalog.authorNames .
Joe Exactly! Functions that appear in a deep node in the tree of function calls tend
to require more test cases, but the data involved in the test cases is less complex.
TIP Functions that appear in a lower level in the tree of function calls tend to
involve less complex data than functions that appear in a higher level in the tree
(see table 6.2).Listing 6.11 Unit test for Catalog.bookInfo
121 6.3 Unit tests for queries
6.3 Unit tests for queries
In the previous section, we saw how to write unit tests for utility functions like Catalog
.bookInfo  and Catalog.authorNames . Now, we are going to see how to write unit tests
for the nodes of a query tree of function calls that are close to the root of the tree.
Joe Theo, how would you write a unit test for the code of the entry point of the
search query?
To recall the particulars, Theo checks the code for Library.searchBooksByTitleJSON .
Although Joe was right about today’s topic being easy enough to enjoy the ambience of a
coffee shop, he has been doing quite a lot of coding this morning.
Library.searchBooksByTitleJSON = function (libraryData, query) {
  var catalogData = _.get(libraryData, "catalog");
  var results = Catalog.searchBooksByTitle(catalogData, query);
  var resultsJSON = JSON.stringify(results);
  return resultsJSON;
};
He then takes a moment to think about how he’d write a unit test for that code. After
another Aha! moment, now he’s got it.
Theo The inputs of Library.searchBooksByTitleJSON  are library data and a
query string, and the output is a JSON string (see figure 6.4). So, I would cre-
ate a library data record with a single book and write tests with query strings
that match the name of the book and ones that don’t match.
Joe What about the expected results of the test cases?Table 6.2 The correlation between the depth of a function in the tree of function calls and the 
quality and quantity of the test cases
Depth in the tree Complexity of the data Number of test cases
Lower Higher Lower
Higher Lower Higher 
Listing 6.12 The code of Library.searchBooksByTitleJSON
query
Library.searchBooksByTitleJSON()libraryData
resultsJSONFigure 6.4 The input and output of 
Library.searchBooksByTitleJSON
Theo In cases where the query string matches, the expected result is a JSON string
with the book info. In cases where the query string doesn’t match, the
expected result is a JSON string with an empty array.
Joe H m m...
Theo What?
Joe I don’t like your answer.
Theo Why?
Joe Because your test case relies on a string comparison instead of a data comparison.
Theo What difference does it make? After all, the strings I’m comparing come from
the serialization of data.
Joe It’s inherently much more complex to compare JSON strings than it is to com-
pare data. For example, two different strings might be the serialization of the
same piece of data.
Theo Really? How?
Joe Take a look at these two strings. They are the serialization of the same data.
They’re different strings because the fields appear in a different order, but in
fact, they serialize the same data!
Joe turns his laptop to Theo. As Theo looks at the code, he realizes that, once again, Joe
is correct.
var stringA = "{\"title\":\"Watchmen\",\"publicationYear\":1987}";
var stringB = "{\"publicationYear\":1987,\"title\":\"Watchmen\"}";
TIP Avoid using a string comparison in unit tests for functions that deal with data.
Theo I see. . . . Well, what can I do instead?
Joe Instead of comparing the output of Library.searchBooksByTitleJSON  with
a string, you could deserialize the output and compare it to the expected data.
Theo What do you mean by deserialize a string?
Joe Deserializing a string s, for example, means to generate a piece of data whose
serialization is s.
Theo Is there a Lodash function for string deserialization?
Joe Actually, there is a native JavaScript function for string deserialization; it’s
called JSON.parse .
Joe retrieves his laptop and shows Theo an example of string deserialization. The code
illustrates a common usage of JSON.parse .
var myString = "{\"publicationYear\":1987,\"title\":\"Watchmen\"}";
var myData = JSON.parse(myString);Listing 6.13 Two different strings that serialize the same data
Listing 6.14 Example of string deserialization
123 6.3 Unit tests for queries
_.get(myData, "title");
// → "Watchmen"
Theo Cool! Let me try writing a unit test for Library.searchBooksByTitleJSON
using JSON.parse .
It doesn’t take Theo too much time to come up with a piece of code. Using his laptop, he
inputs the unit test.
var libraryData = {
  "catalog": {
    "booksByIsbn": {
      "978-1779501127": {
        "isbn": "978-1779501127",
        "title": "Watchmen",
        "publicationYear": 1987,
        "authorIds": ["alan-moore",
          "dave-gibbons"]
      }
    },
    "authorsById": {
      "alan-moore": {
        "name": "Alan Moore",
        "bookIsbns": ["978-1779501127"]
      },
      "dave-gibbons": {
        "name": "Dave Gibbons",
        "bookIsbns": ["978-1779501127"]
      }
    }
  }
};
var bookInfo = {
  "isbn": "978-1779501127",
  "title": "Watchmen",
  "authorNames": ["Alan Moore",
    "Dave Gibbons"]
};
_.isEqual(JSON.parse(Library.searchBooksByTitleJSON(libraryData,
  "Watchmen")),
  [bookInfo]);
_.isEqual(JSON.parse(Library.searchBooksByTitleJSON(libraryData,
  "Batman")),
  []);
Joe Well done! I think you’re ready to move on to the last piece of the puzzle and
write the unit test for Catalog.searchBooksByTitle .Listing 6.15 Unit test for Library.searchBooksByTitleJSON
Because Theo and Joe have been discussing unit tests for quite some time, he asks Joe if he
would like another espresso. They call the waiter and order, then Theo looks again at the
code for Catalog.searchBooksByTitle .
Catalog.searchBooksByTitle = function(catalogData, query) {
  var allBooks = _.get(catalogData, "booksByIsbn");
  var matchingBooks = _.filter(allBooks, function(book) {
    return _.get(book, "title").includes(query);
  });
  var bookInfos = _.map(matchingBooks, function(book) {
    return Catalog.bookInfo(catalogData, book);
  });
  return bookInfos;
};
Writing the unit test for Catalog.searchBooksByTitle  is a more pleasant experience for
Theo than writing the unit test for Library.searchBooksByTitleJSON . He appreciates
this for two reasons:
It’s not necessary to deserialize the output because the function returns data.
It’s not necessary to wrap the catalog data in a library data map.
var catalogData = {
  "booksByIsbn": {
    "978-1779501127": {
      "isbn": "978-1779501127",
      "title": "Watchmen",
      "publicationYear": 1987,
      "authorIds": ["alan-moore",
        "dave-gibbons"]
    }
  },
  "authorsById": {
    "alan-moore": {
      "name": "Alan Moore",
      "bookIsbns": ["978-1779501127"]
    },
    "dave-gibbons": {
      "name": "Dave Gibbons",
      "bookIsbns": ["978-1779501127"]
    }
  }
};
var bookInfo = {
  "isbn": "978-1779501127",
  "title": "Watchmen",
  "authorNames": ["Alan Moore",
    "Dave Gibbons"]
};Listing 6.16 The code of Catalog.searchBooksByTitle
Listing 6.17 Unit test for Catalog.searchBooksByTitle
125 6.3 Unit tests for queries
_.isEqual(Catalog.searchBooksByTitle(catalogData, "Watchmen"), [bookInfo]);
_.isEqual(Catalog.searchBooksByTitle(catalogData, "Batman"), []);
Joe That’s a good start!
Theo I thought I was done. What did I miss?
Joe You forgot to test cases where the query string is all lowercase.
Theo You’re right! Let me quickly add one more test case.
In less than a minute, Theo creates an additional test case and shows it to Joe. What a dis-
appointment when Theo discovers that the test case with "watchmen"  in lowercase fails!
_.isEqual(Catalog.searchBooksByTitle(catalogData, "watchmen"),
  [bookInfo]);
Joe Don’t be too upset, my friend. After all, the purpose of unit tests is to find bugs
in the code so that you can fix them. Can you fix the code of Catalog-
Data.searchBooksByTitle ?
Theo Sure. All I need to do is to lowercase both the query string and the book title
before comparing them. I’d probably do something like this.
Catalog.searchBooksByTitle = function(catalogData, query) {
  var allBooks = _.get(catalogData, "booksByIsbn");
  var queryLowerCased = query.toLowerCase();         
  var matchingBooks = _.filter(allBooks, function(book) {
    return _.get(book, "title")
      .toLowerCase()     
      .includes(queryLowerCased);
  });
  var bookInfos = _.map(matchingBooks, function(book) {
    return Catalog.bookInfo(catalogData, book);
  });
  return bookInfos;
};
After fixing the code of Catalog.searchBooksByTitle , Theo runs all the test cases
again. This time, all of them pass—what a relief!
_.isEqual(Catalog.searchBooksByTitle(catalogData, "watchmen"),
  [bookInfo]);
Joe It’s such good feeling when all the test cases pass.
Theo Sure is.
Joe I think we’ve written unit tests for all the search query code, so now we’re ready
to write unit tests for mutations. Thank goodness the waiter just brought our
coffee orders. Listing 6.18 Additional test case for Catalog.searchBooksByTitle
Listing 6.19 Fixed code of Catalog.searchBooksByTitle
Listing 6.20 Additional test case for Catalog.searchBooksByTitleConverts the query 
to lowercase
Converts the book 
title to lowercase
6.4 Unit tests for mutations
Joe Before writing unit tests for the add member mutation, let’s draw the tree of
function calls for System.addMember .
Theo I can do that.
Theo takes a look at the code for the functions involved in the add member mutation. He
notices the code is spread over three classes: System , Library , and UserManagement .
System.addMember = function(systemState, member) {
  var previous = systemState.get();
  var next = Library.addMember(previous, member);
  systemState.commit(previous, next);
};
Library.addMember = function(library, member) {
  var currentUserManagement = _.get(library, "userManagement");
  var nextUserManagement = UserManagement.addMember(
    currentUserManagement, member);
  var nextLibrary = _.set(library, "userManagement", nextUserManagement);
  return nextLibrary;
};
UserManagement.addMember = function(userManagement, member) {
  var email = _.get(member, "email");
  var infoPath = ["membersByEmail", email];
  if(_.has(userManagement, infoPath)) {
    throw "Member already exists.";
  }
  var nextUserManagement =  _.set(userManagement,
    infoPath,
    member);
  return nextUserManagement;
};
Theo grabs another napkin. Drawing the tree of function calls for System.addMember  is
now quite easy (see figure 6.5).Listing 6.21 The functions involved in the add member mutation
System.addMember
SystemState.get SystemState.commit Library.addMember
UserManagement.addMember _.get _.set
_.has _.set
Figure 6.5 The tree of function calls for System.addMember
127 6.4 Unit tests for mutations
Joe Excellent! So which functions of the tree should be unit tested for the add
member mutation?
Theo I think the functions we need to test are System.addMember , SystemState
.get , SystemState.commit , Library.addMember , and UserManagement
.addMember . That right?
Joe You’re totally right. Let’s defer writing unit tests for functions that belong to
SystemState  until later. Those are generic functions that should be tested
outside the context of a specific mutation. Let’s assume for now that we’ve
already written unit tests for the SystemState  class. We’re left with three func-
tions: System.addMember , Library.addMember , and UserManagement.add-
Member .
Theo In what order should we write the unit tests, bottom up or top down?
Joe Let’s start where the real meat is—in UserManagement.addMember . The two
other functions are just wrappers.
Theo OK.
Joe Writing a unit test for the main function of a mutation requires more effort
than writing the test for a query. The reason is that a query returns a response
based on the system data, whereas a mutation computes a new state of the system
based on the current state of the system and some arguments (see figure 6.6).
TIP Writing a unit test for the main function of a mutation requires more effort than
for a query.
Theo It means that in the test cases of UserManagement.addMember , both the input
and the expected output are maps that describe the state of the system.
Joe Exactly. Let’s start with the simplest case, where the initial state of the system
is empty.
Theo You mean that userManagementData  passed to UserManagement.addMember
is an empty map?
Joe Yes.
Once again, Theo places his hands over his laptop keyboard, thinks for a moment, and
begins typing. He reminds himself that the code needs to add a member to an empty userMutationSystemData Argument
QueryArgument SystemData
NextSystemData ResponseData
Figure 6.6 The output of a mutation is more complex than 
the output of a query.
management map and to check that the resulting map is as expected. When he’s finished,
he shows his code to Joe.
var member = {
  "email": "jessie@gmail.com",
  "password": "my-secret"
};
var userManagementStateBefore = {};
var expectedUserManagementStateAfter = {
  "membersByEmail": {
    "jessie@gmail.com": {
      "email": "jessie@gmail.com",
      "password": "my-secret"
    }
  }
};
var result = UserManagement.addMember(userManagementStateBefore, member);
_.isEqual(result, expectedUserManagementStateAfter);
Joe Very nice! Keep going and write a test case when the initial state is not empty.
Theo knows this requires a few more lines of code but nothing complicated. When he fin-
ishes, he once again shows the code to Joe.
var jessie = {
  "email": "jessie@gmail.com",
  "password": "my-secret"
};
var franck = {
  "email": "franck@gmail.com",
  "password": "my-top-secret"
};
var userManagementStateBefore = {
  "membersByEmail": {
    "franck@gmail.com": {
      "email": "franck@gmail.com",
      "password": "my-top-secret"
    }
  }
};
var expectedUserManagementStateAfter = {
  "membersByEmail": {
    "jessie@gmail.com": {
      "email": "jessie@gmail.com",Listing 6.22 Test case for Catalog.addMember  without members
Listing 6.23 Test case for Catalog.addMember  with existing members
129 6.4 Unit tests for mutations
      "password": "my-secret"
    },
    "franck@gmail.com": {
      "email": "franck@gmail.com",
      "password": "my-top-secret"
    }
  }
};
var result = UserManagement.addMember(userManagementStateBefore, jessie);
_.isEqual(result, expectedUserManagementStateAfter);
Joe Awesome! Can you think of other test cases for UserManagement.addMember ?
Theo No.
Joe What about cases where the mutation fails?
Theo Right! I always forget to think about negative test cases. I assume that relates to
the fact that I’m an optimistic person.
TIP Don’t forget to include negative test cases in your unit tests.
Joe Me too. The more I meditate, the more I’m able to focus on the positive side of
life. Anyway, how would you write a test case where the mutation fails?
Theo I would pass to UserManagement.addMember  a member that already exists in
userManagementStateBefore .
Joe And how would you check that the code behaves as expected in case of a failure?
Theo Let me see. When a member already exists, UserManagement.addMember
throws an exception. Therefore, what I need to do in my test case is to wrap the
code in a try/catch  block.
Joe Sounds good to me.
Once again, it doesn’t require too much of an effort for Theo to create a new test case.
When he’s finished, he eagerly turns his laptop to Joe.
var jessie = {
  "email": "jessie@gmail.com",
  "password": "my-secret"
};
var userManagementStateBefore = {
  "membersByEmail": {
    "jessie@gmail.com": {
      "email": "jessie@gmail.com",
      "password": "my-secret"
    }
  }
};Listing 6.24 Test case for UserManagement.addMember  if it’s expected to fail
var expectedException = "Member already exists.";
var exceptionInMutation;
try {
  UserManagement.addMember(userManagementStateBefore, jessie);
} catch (e) {
  exceptionInMutation = e;
}
_.isEqual(exceptionInMutation, expectedException);
Theo Now, I think I’m ready to move forward and write unit tests for Library.add-
Member  and System.addMember .
Joe I agree with you. Please start with Library.addMember .
TheoLibrary.addMember  is quite similar to UserManagement.addMember .  S o  I
guess I’ll write similar test cases.
Joe In fact, that won’t be required. As I told you when we wrote unit tests for a
query, when you write a unit test for a function, you can assume that the func-
tions down the tree work as expected.
Theo Right. So I’ll just write the test case for existing members.
Joe Go for it!
Theo starts with a copy-and-paste of the code from the UserManagement.addMember  test
case with the existing members in listing 6.23. After a few modifications, the unit test for
Library.addMember  is ready.
var jessie = {
  "email": "jessie@gmail.com",
  "password": "my-secret"
};
var franck = {
  "email": "franck@gmail.com",
  "password": "my-top-secret"
};
var libraryStateBefore = {
  "userManagement": {
    "membersByEmail": {
      "franck@gmail.com": {
        "email": "franck@gmail.com",
        "password": "my-top-secret"
      }
    }
  }
};
var expectedLibraryStateAfter = {
  "userManagement": {
    "membersByEmail": {Listing 6.25 Unit test for Library.addMember
131 6.4 Unit tests for mutations
      "jessie@gmail.com": {
        "email": "jessie@gmail.com",
        "password": "my-secret"
      },
      "franck@gmail.com": {
        "email": "franck@gmail.com",
        "password": "my-top-secret"
      }
    }
  }
};
var result = Library.addMember(libraryStateBefore, jessie);
_.isEqual(result, expectedLibraryStateAfter);
Joe Beautiful! Now, we’re ready for the last piece. Write a unit test for System
.addMember . Before you start, could you please describe the input and the out-
put of System.addMember ?
Theo takes another look at the code for System.addMember  and hesitates; he’s a bit con-
fused. The function doesn’t seem to return anything!
System.addMember = function(systemState, member) {
  var previous = systemState.get();
  var next = Library.addMember(previous, member);
  systemState.commit(previous, next);
};
Theo The input of System.addMember  is a system state instance and a member. But,
I’m not sure what the output of System.addMember  is.
Joe In fact, System.addMember  doesn’t have any output. It belongs to this stateful
part of our code that doesn’t deal with data manipulation. Although DOP
allows us to reduce the size of the stateful part of our code, it still exists. Here is
how I visualize it.
Joe calls the waiter to see if he can get more napkins. With that problem resolved, he draws
the diagram in figure 6.7.Listing 6.26 The code of System.addMember
Change system state MutationSystemData Member
NothingFigure 6.7 System.addMember  
doesn’t return data—it changes the 
system state!
Theo Then how do we validate that the code works as expected?
Joe We’ll retrieve the system state after the code is executed and compare it to the
expected value of the state.
Theo OK. I’ll try to write the unit test.
Joe Writing unit tests for stateful code is more complicated than for data manipula-
tion code. It requires the calm of the office.
Theo Then let’s go back to the office. Waiter! Check, please.
Theo picks up the tab, and he and Joe take the cable car back to Albatross. When they’re
back at the office, Theo starts coding the unit test for Library.addMember .
Theo Can we use _.isEqual  with system state?
Joe Definitely. The system state is a map like any other map.
TIP The system state is a map. Therefore, in the context of a test case, we can com-
pare the system state after a mutation is executed to the expected system state using
_.isEqual
Theo copies and pastes the code for Library.addMember  (listing 6.21), which initializes
the data for the test. Then, he passes a SystemState  object that is initialized with
libraryStateBefore  to System.addMember . Finally, to complete the test, he compares
the system state after the mutation is executed with the expected value of the state.
class SystemState {
  systemState;
  get() {
    return this.systemState;
  }
  commit(previous, next) {
    this.systemState = next;
  }
}
window.SystemState = SystemState;
var jessie = {
  "email": "jessie@gmail.com",
  "password": "my-secret"
};
var franck = {
  "email": "franck@gmail.com",
  "password": "my-top-secret"
};
var libraryStateBefore = {
  "userManagement": {
    "membersByEmail": {Listing 6.27 Unit test for System.addMember
133 6.4 Unit tests for mutations
      "franck@gmail.com": {
        "email": "franck@gmail.com",
        "password": "my-top-secret"
      }
    }
  }
};
var expectedLibraryStateAfter = {
  "userManagement": {
    "membersByEmail": {
      "jessie@gmail.com": {
        "email": "jessie@gmail.com",
        "password": "my-secret"
      },
      "franck@gmail.com": {
        "email": "franck@gmail.com",
        "password": "my-top-secret"
      }
    }
  }
};
var systemState = new SystemState();    
systemState.commit(null, libraryStateBefore);   
System.addMember(systemState, jessie);     
_.isEqual(systemState.get(),
  expectedLibraryStateAfter);  
Joe Wow, I’m impressed; you did it! Congratulations!
Theo Thank you. I’m so glad that in DOP most of our code deals with data manipu-
lation. It’s definitely more pleasant to write unit tests for stateless code that
only deals with data manipulation.
Joe Now that you know the basics of DOP, would you like to refactor the code of
your Klafim prototype according to DOP principles?
Theo Definitely. Nancy told me yesterday that Klafim is getting nice market traction.
I’m supposed to have a meeting with her in a week or so about the next steps.
Hopefully, she’ll be willing to work with Albatross for the long term.
Joe Exciting! Do you know what might influence Nancy’s decision?
Theo Our cost estimate, certainly, but I know she’s in touch with other software com-
panies. If we come up with a competitive proposal, I think we’ll get the deal.
Joe I’m quite sure that after refactoring to DOP, features will take much less time
to implement. That means you should be able to quote Nancy a lower total cost
than the competition, right?
Theo I’ll keep my fingers crossed!Creates an empty 
SystemState object 
(see chapter 4)
Initializes the system 
state with the library 
data before the 
mutation
Executes the 
mutation on the 
SystemState object
Validates the state after the 
mutation is executed
Moving forward
The meeting with Nancy went well. Albatross got the deal, Monica (Theo’s boss) is
pleased, and it’s going to be a long-term project with a nice budget. They’ll need to hire a
team of developers in order to meet the tough deadlines. While driving back to the office,
Theo gets a phone call from Joe.
Joe How was your meeting with Nancy?
Theo We got the deal!
Joe Awesome! I told you that with DOP the cost estimation would be lower.
Theo In fact, we are not going to use DOP for this project.
Joe Why?
Theo After refactoring the Library Management System prototype to DOP, I did a
deep analysis with my engineers. We came to the conclusion that DOP might
be a good fit for the prototype phase, but it won’t work well at scale.
Joe Could you share the details of your analysis?
Theo I can’t right now. I’m driving.
Joe Could we meet in your office later today?
Theo I’m quite busy with the new project and the tough deadlines.
Joe Let’s meet at least in order to have a proper farewell.
Theo OK. Let’s meet at 4 PM, then.
 NOTE The story continues in the opener of part 2.
Summary
Most of the code in a data-oriented system deals with data manipulation.
It’s straightforward to write unit tests for code that deals with data manipulation.
Test cases follow the same simple general pattern:
aGenerate data input 
bGenerate expected data output 
cCompare the output of the function with the expected data output
In order to compare the output of a function with the expected data output, we
need to recursively compare the two pieces of data.
The recursive comparison  of two pieces of data is implemented via a generic
function.
When a function returns a JSON string, we parse the string back to data so that
we deal with data comparison instead of string comparison.
A tree of function calls  for a function f is a tree where the root is f, and the chil-
dren of a node g in the tree are the functions called by g.
The leaves of the tree are functions that are not part of the code base of the
application and are functions that don’t call any other functions.
The tree of function calls visualization guides us regarding the quality and
quantity of the test cases in a unit test.
135 Summary
Functions that appear in a lower level in the tree of function calls tend to involve
less complex data than functions that appear in a higher level in the tree.
Functions that appear in a lower level in the tree of function calls usually need
to be covered with more test cases than functions that appear in a higher level
in the tree.
Unit tests for mutations focus on the calculation phase of the mutation.
The validity of the data depends on the context.
The smaller the data, the easier it is to manipulate.
We compare the output and the expected output of our functions with a generic
function that recursively compares two pieces of data (e.g., _.isEqual ).
When we write a unit test for a function, we assume that the functions called by
this function are covered by the unit tests and work as expected. This signifi-
cantly reduces the quantity of test cases in our unit tests.
We avoid using string comparison in unit tests for functions that deal with data.
Writing a unit test for the main function of a mutation requires more effort
than for a query.
Remember to include negative test cases in your unit tests.
The system state is a map. Therefore, in the context of a test case, we can com-
pare the system state after a mutation is executed to the expected system state
using a generic function like _.isEqual .
 
Part 2
Scalability
T heo feels a bit uncomfortable about the meeting with Joe. He was so enthusias-
tic about DOP, and he was very good at teaching it. Every meeting with him was an
opportunity to learn new things. Theo feels lot of gratitude for the time Joe spent
with him. He doesn’t want to hurt him in any fashion. Surprisingly, Joe enters the
office with the same relaxed attitude as usual, and he is even smiling.
Joe I’m really glad that you got the deal with Nancy.
Theo Yeah. There’s lot of excitement about it here in the office, and a bit of
stress too.
Joe What kind of stress?
Theo You know. . . .  We need to hire a team of developers, and the deadlines
are quite tight.
Joe But you told me that you won’t use DOP. I assume that you gave regular
deadlines?
Theo No, my boss Monica really wanted to close the deal. She feels that success
with this project is strategically important for Albatross, so it’s worthwhile
to accept some risk by giving what she calls an “optimistic” time estima-
tion. I told her that it was really an unrealistic time estimation, but Mon-
ica insists that if we make smart decisions and bring in more developers,
we can do it.
Joe I see. Now I understand why you told me over the phone that you were
very busy. Anyway, would you please share the reasons that made you
think DOP wouldn’t be a good fit at scale?
138 PART 2Scalability
Theo First of all, let me tell you that I feel lot of gratitude for all the teaching you
shared with me. Reimplementing the Klafim prototype with DOP was really
fun and productive due to the flexibility this paradigm offers.
Joe I’m happy that you found it valuable.
Theo But, as I told you over the phone, now we’re scaling up into a long-term project
with several developers working on a large code base. We came to the conclu-
sion that DOP will not be a good fit at scale.
Joe Could you share the reasons behind your conclusion?
Theo There are many of them. First of all, as DOP deals only with generic data struc-
tures, it’s hard to know what kind of data we have in hand, while in OOP, we
know the type of every piece of data. For the prototype, it was kind of OK. But
as the code base grows and more developers are involved in the project, it
would be too painful.
Joe I hear you. What else, my friend?
Theo Our system is going to run on a multi-threaded environment. I reviewed the
concurrency control strategy that you presented, and it’s not thread-safe.
Joe I hear you. What else, my friend?
Theo I have been doing a bit of research about implementing immutable data struc-
tures with structural sharing. I discovered that when the size of the data
structures grows, there is a significant performance hit.
Joe I hear you. What else?
Theo As our system grows, we will use a database to store the application data and
external services to enrich book information, and in what you have showed me
so far, data lives in memory.
Joe I hear you. What else, my friend?
Theo Don’t you think I have shared enough reasons to abandon DOP?
Joe I think that your concerns about DOP at scale totally make sense. However, it
doesn’t mean that you should abandon DOP.
Theo What do you mean?
Joe With the help of meditation, I learned not be attached to the objections that
flow in my mind while I’m practicing. Sometimes all that is needed to quiet our
minds is to keep breathing; sometimes, a deeper level of practice is needed.
Theo I don’t see how breathing would convince me to give DOP a second chance.
Joe Breathing might not be enough in this case, but a deeper knowledge of DOP
could be helpful. Until now, I have shared with you only the material that was
needed in order to refactor your prototype. In order to use DOP in a big proj-
ect, a few more lessons are necessary.
Theo But I don’t have time for more lessons. I need to work.
Joe Have you heard the story about the young woodcutter and the old man?
Theo No.
Joe It goes like this.
139 PART 2Scalability
Theo takes a moment to meditate on the story. He wonders if he needs to take the time to
sharpen his saw and commit to a deeper level of practice.
Theo Do you really think that with DOP, it will take much less time to deliver the
project?
Joe I know so!
Theo But if we miss the deadline, I will probably get fired. I’m the one that needs to
take the risk, not you.
Joe Let’s make a deal. If you miss the deadline and get fired, I will hire you at my
company for double the salary you make at Albatross.
Theo And what if we meet the deadline?
Joe If you meet the deadline, you will probably get promoted. In that case, I will
ask you to buy a gift for my son Neriah and my daughter Aurelia.
Theo Deal! When will I get my first lesson about going deeper into DOP?
Joe Why not start right now?
Theo Let me reschedule my meetings.The young woodcutter and the old man
A young woodcutter strained to saw down a tree. An old man who was watching near-
by asked, “What are you doing?”
“Are you blind?” the woodcutter replied. “I’m cutting down this tree.”
The old man replied, “You look exhausted! Take a break. Sharpen your saw.”
The young woodcutter explained to the old man that he had been sawing for hours
and did not have time to take a break.
The old man pushed back, “If you sharpen the saw, you would cut down the tree much
faster.”
The woodcutter said, “I don’t have time to sharpen the saw. Don’t you see, I’m too
busy!”

141Basic data validation
A solemn gift
At first glance, it may seem that embracing DOP means accessing data without validat-
ing it and engaging in wishful thinking, where data is always valid. In fact, data valida-
tion is not only possible but recommended when we follow data-oriented principles.
 This chapter illustrates how to validate data when data is represented with
generic data structures. It focuses on data validation occurring at the boundaries of
the system, while in part 3, we will deal with validating data as it flows through the
system. This chapter is a deep dive into the fourth principle of DOP.This chapter covers
The importance of validating data at system 
boundaries
Validating data using the JSON Schema language
Integrating data validation into an existing code 
base
Getting detailed information about data validation 
failures
PRINCIPLE #4 Separate data schema from data representation. 
7.1 Data validation in DOP
Theo has rescheduled his meetings. With such an imposing deadline, he’s still not sure if
he’s made a big mistake giving DOP a second chance.
 NOTE The reason why Theo rescheduled his meetings is explained in the opener
for part 2. Take a moment to read the opener if you missed it.
Joe What aspect of OOP do you think you will miss the most in your big project?
Theo Data validation.
Joe Can you elaborate a bit?
Theo In OOP, I have this strong guarantee that when a class is instantiated, its mem-
ber fields have the proper names and proper types. But with DOP, it’s so easy
to have small mistakes in field names and field types.
Joe Well, I have good news for you! There is a way to validate data in DOP.
Theo How does it work? I thought DOP and data validation were two contradictory
concepts!
Joe Not at all. It’s true that DOP doesn’t force you to validate data, but it doesn’t
prevent you from doing so. In DOP, the data schema is separate from the data
representation.
Theo I don’t get how that would eliminate data consistency issues.
Joe According to DOP, the most important data to validate is data that crosses the
boundaries of the system.
Theo Which boundaries are you referring to?
Joe In the case of a web server, it would be the areas where the web server commu-
nicates with its clients and with its data sources.
Theo A diagram might help me see it better.
Joe goes to the whiteboard and picks up the pen. He then draws a diagram like the one in
figure 7.1.
Data
DataClient (e.g., web browser)
Web server
Web service DatabaseData
Figure 7.1 High-level architecture of 
a modern web server
143 7.2 JSON Schema in a nutshell
Joe This architectural diagram defines what we call the boundaries of the system in
terms of data exchange. Can you tell me what the three boundaries of the sys-
tem are?
 NOTE The boundaries  of a system are defined as the areas where the system exchanges
data.
Theo Let me see. The first one is the client boundary, then we have the database
boundary, and finally, the web service boundary.
Joe Exactly! It’s important to identify the boundaries of a system because, in
DOP, we differentiate between two kinds of data validation: validation that
occurs at the boundaries of the system and validation that occurs inside the
system. Today, we’re going to focus on validation that occurs at the boundar-
ies of the system.
Theo Does that mean data validation at the boundaries of the system is more
important?
Joe Absolutely! Once you’ve ensured that data going into and out of the system is
valid, the odds for an unexpected piece of data inside the system are pretty low.
TIP When data at system boundaries is validated, it’s not critical to validate data
again inside the system.
Theo Why do we need data validation inside the system then?
Joe It has to do with making it easier to code your system as your code base grows.
Theo And, what’s the main purpose of data validation at the boundaries?
Joe To prevent invalid data from going in and out of the system, and to display
informative errors when we encounter invalid data. Let me draw a table on the
whiteboard so you can see the distinction (table 7.1).
Theo When will you teach me about data validation inside the system?
Joe Later, when the code base is bigger. 
7.2 JSON Schema in a nutshell
Theo For now, the Library Management System is an application that runs in mem-
ory, with no database and no HTTP clients connected to it. But Nancy will
probably want me to make the system into a real web server with clients, data-
base, and external services.
Joe OK. Let’s imagine how a client request for searching books would look.Table 7.1 Two kinds of data validation
Kind of data validation Purpose Environment
Boundaries Guardian Production
Inside Ease of development Dev
Theo Basically, a search request is made of a string and the fields you’d like to
retrieve for the books whose title contains the string. So the request has two
fields: title , which is a string, and fields , which is an array of strings.
Theo quickly writes on the whiteboard. When he finishes, he steps aside to let Joe view his
code for a search request.
{
"title": "habit",
"fields": ["title", "weight", "number_of_pages"]
}
Joe I see. Let me show you how to express the schema of a search request sepa-
rately from the representation of the search request data.
Theo What do you mean exactly by “separately?”
Joe Data representation stands on its own, and the data schema stands on its own.
You are free to validate that a piece of data conforms with a data schema as you
will and when you will.
TIP In DOP, the data schema is separate from the data representation.
Theo It’s a bit abstract for me.
Joe I know. It will become much clearer in a moment. For now, I am going to show
you how to build the data schema for the search request in a schema language
called JSON Schema.
Theo I love JSON!
 NOTE Information on the JSON Schema language can be found at https:/ /json
-schema.org . The schemas in this book use JSON Schema version 2020-12.
Joe First, we have to express the data type of the request. What’s the data type in
the case of a book search request?
Theo It’s a map.
Joe In JSON Schema, the data type for maps is called object . Look at this basic
skeleton of a map. It’s a map with two fields: type  and properties .
Joe goes to the whiteboard. He quickly writes the code for the map with its two fields.
{
"type": "object",
"properties": {...}
}Listing 7.1 An example of a search request
Listing 7.2 Basic schema skeleton of a map
145 7.2 JSON Schema in a nutshell
Joe The value of type  is "object" , and the value of properties  is a map with the
schema for the map fields.
Theo I assume that, inside properties, we are going to express the schema of the map
fields as JSON Schema.
Joe Correct.
Theo I am starting to feel the dizziness of recursion.
Joe In JSON Schema, a schema is usually a JSON object with a field called type ,
which specifies the data type. For example, the type for the title  field is
string  a n d...
Theo . . . the type for the fields  field is array .
Joe Yes!
Now it’s Theo’s turn to go to the whiteboard. He fills the holes in the search request
schema with the information about the fields.
{
"type": "object",
"properties": {
"title": {"type": "string"},
"fields": {"type": "array"}
}
}
On Theo’s way back from the whiteboard to his desk, Joe makes a sign with his right hand
that says, “Stay near the whiteboard, please.” Theo turns and goes back to the whiteboard.
Joe We can be a little more precise about the fields  property by providing infor-
mation about the type of the elements in the array. In JSON Schema, an array
schema has a property called items , whose value is the schema for the array
elements.
Without any hesitation, Theo adds this information on the whiteboard. Stepping aside, he
shows Joe the result.
{
"type": "object",
"properties": {
"title": {"type": "string"},
"fields": {
"type": "array",
"items": {"type": "string"}
}
}
}Listing 7.3 Schema skeleton for search request
Listing 7.4 Schema for search request with information about array elements
Before going back to his desk, Theo asks Joe:
Theo Are we done now?
Joe Not yet. We can be more precise about the fields  field in the search request.
I assume that the fields in the request should be part of a closed list of fields.
Therefore, instead of allowing any string, we could have a list of allowed values.
Theo Like an enumeration value?
Joe Exactly! In fact, JSON Schema supports enumeration values with the enum  key-
word. Instead of {"type": "string"} , you need to have {"enum": […]}  and
replace the dots with the supported fields.
Once again, Theo turns to the whiteboard. He replaces the dots with the information Joe
requests.
{
"type": "object",
"properties": {
"title": {"type": "string"},
"fields": {
"type": "array",
"items": {
"enum": [
"publishers",
"number_of_pages",
"weight",
"physical_format",
"subjects",
"publish_date",
"physical_dimensions"
]
}
}
}
}
Theo Are we done, now?
Joe Almost. We need to decide whether the fields of our search request are optional
or required. In our case, both title  and fields  are required.
Theo How do we express this information in JSON Schema?
Joe There is a field called required  whose value is an array made of the names of
the required fields in the map.
After adding the required  field, Theo looks at Joe. This time he makes a move with his
right hand that says, “Now you can go back to your desk.”
var searchBooksRequestSchema = {
"type": "object",Listing 7.5 Schema for the search request with enumeration values
Listing 7.6 Schema of a search request
147 7.2 JSON Schema in a nutshell
"properties": {
"title": {"type": "string"},
"fields": {
"type": "array",
"items": {
"enum": [
"publishers",
"number_of_pages",
"weight",
"physical_format",
"subjects",
"publish_date",
"physical_dimensions"
]
}
}
},
"required": ["title", "fields"]
};
Joe Now I’ll show you how to validate a piece of data according to a schema.
Theo What do you mean, validate?
Joe Validating data according to a schema means checking whether data conforms
to the schema. In our case, it means checking whether a piece of data is a valid
search books request.
TIP Data validation in DOP means checking whether a piece of data conforms to a
schema.
Theo I see.
Joe There are a couple of libraries that provide JSON Schema validation. They
have a validate  function that receives a schema and a piece of data and
returns true  when the data is valid and false  when the data is not valid. I just
happen to have a file in my laptop that provides a table with a list of schema
validation libraries (table 7.2). We can print it out if you like.
Theo turns on the printer as Joe scans through his laptop for the table. When he has it up,
he checks with Theo and presses Print.
Table 7.2 Libraries for JSON Schema validation
Language Library URL
JavaScript Ajv https:/ /github.com/ajv-validator/ajv
Java Snow https:/ /github.com/ssilverman/snowy-json
C# JSON.net Schema https:/ /www.newtonsoft.com/jsonschema
Python jschon https:/ /github.com/marksparkza/jschon
Ruby JSONSchemer https:/ /github.com/davishmcclurg/json_schemer
Theo So, if I call validate  with this search request and that schema, it will return
true ?
Theo indicates the search request example from listing 7.7 and the schema from listing 7.6.
{
"title": "habit",
"fields": ["title", "weight", "number_of_pages"]
}
Joe Give it a try, and you’ll see.
Indeed! When Theo executes the code to validate the search request, it returns true .
var searchBooksRequestSchema = {
"type": "object",
"properties": {
"title": {"type": "string"},
"fields": {
"type": "array",
"items": {"type": "string"}
}
},
"required": ["title", "fields"]
};
var searchBooksRequest = {
"title": "habit",
"fields": ["title", "weight", "number_of_pages"]
};
validate(searchBooksRequestSchema, searchBooksRequest);
//→true
Joe Now, please try an invalid request.
Theo Let me think about what kind of invalidity to try. I know, I’ll make a typo in the
title  field and call it tilte  with the l before the t.
As expected, the code with the type returns false . Theo is not surprised, and Joe is smil-
ing from ear to ear.
var invalidSearchBooksRequest = {
"tilte": "habit",
"fields": ["title", "weight", "number_of_pages"]
};Listing 7.7 An example of a search request
Listing 7.8 Validating the search request
Listing 7.9 Validating an invalid search request