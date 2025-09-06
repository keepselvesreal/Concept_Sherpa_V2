# 목차
# - 생성 시간: 2025-08-07 20:10:30 KST
# - 핵심 내용: Chapter 1 리프노드 자동 추출 스크립트
# - 상세 내용: 
#   - chapter1_leafnodes/: 개별 리프노드 파일들이 저장될 디렉토리
#   - extract_leaf_nodes(): 제공된 텍스트를 파싱하여 각 섹션별로 파일 생성
# - 상태: 활성
# - 주소: chapter1_leaf_extractor
# - 참조: 없음

#!/usr/bin/env python3
import os
import re

def extract_leaf_nodes():
    """Chapter 1의 모든 리프노드를 개별 파일로 추출"""
    
    # 출력 디렉토리 생성
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/chapter1_leafnodes"
    os.makedirs(output_dir, exist_ok=True)
    
    # Chapter 1 전체 텍스트 (사용자 제공)
    chapter1_text = """Complexity of object-oriented programming
A capricious entrepreneur
This chapter covers
 The tendency of OOP to increase system complexity
 What makes OOP systems hard to understand
 The cost of mixing code and data together into objects
In this chapter, we'll explore why object-oriented programming (OOP) systems tend to
be complex. This complexity is not related to the syntax or the semantics of a specific
OOP language. It is something that is inherent to OOP's fundamental insight—
programs should be composed from objects, which consist of some state, together
with methods for accessing and manipulating that state.
Over the years, OOP ecosystems have alleviated this complexity by adding new
features to the language (e.g., anonymous classes and anonymous functions) and
by developing frameworks that hide some of this complexity, providing a simpler
interface for developers (e.g., Spring and Jackson in Java). Internally, the frame-
works rely on the advanced features of the language such as reflection and custom
annotations.
This chapter is not meant to be read as a critical analysis of OOP. Its purpose is to
raise your awareness of the tendency towards OOP's increased complexity as a pro-
gramming paradigm. Hopefully, it will motivate you to discover a different program-
ming paradigm, where system complexity tends to be reduced. This paradigm is
known as data-oriented programming (DOP).
1.1 OOP design: Classic or classical?
 NOTE Theo, Nancy, and their new project were introduced in the opener for part 1.
Take a moment to read the opener if you missed it.
Theo gets back to the office with Nancy's napkin in his pocket and a lot of anxiety in his
heart because he knows he has committed to a tough deadline. But he had no choice! Last
week, Monica, his boss, told him quite clearly that he had to close the deal with Nancy no
matter what.
Albatross, where Theo works, is a software consulting company with customers all over
the world. It originally had lots of customers among startups. Over the last year, however,
many projects were badly managed, and the Startup department lost the trust of its cus-
tomers. That's why management moved Theo from the Enterprise department to the
Startup department as a Senior Tech lead. His job is to close deals and to deliver on time.
1.1.1 The design phase
Before rushing to his laptop to code the system, Theo grabs a sheet of paper, much big-
ger than a napkin, and starts to draw a UML class diagram of the system that will imple-
ment the Klafim prototype. Theo is an object-oriented programmer. For him, there is no
question—every business entity is represented by an object, and every object is made
from a class.
The requirements for the Klafim prototype
 There are two kinds of users: library members and librarians.
 Users log in to the system via email and password.
 Members can borrow books.
 Members and librarians can search books by title or by author.
 Librarians can block and unblock members (e.g., when they are late in return-
ing a book).
 Librarians can list the books currently lent to a member.
 There can be several copies of a book.
 A book belongs to a physical library.
Theo spends some time thinking about the organization of the system. He identifies the
main classes for the Klafim Global Library Management System.
The main classes of the library management system
 Library—The central part of the system design.
 Book—A book.
 BookItem—A book can have multiple copies, and each copy is considered as
a book item.
 BookLending—When a book is lent, a book lending object is created.
 Member—A member of the library.
 Librarian—A librarian.
 User—A base class for Librarian and Member.
 Catalog—Contains a list of books.
 Author—A book author.
That was the easy part. Now comes the difficult part: the relations between the classes.
After two hours or so, Theo comes up with a first draft of a design for the Global Library
Management System. It looks like the diagram in figure 1.1.
 NOTE The design presented here doesn't pretend to be the smartest OOP design:
experienced OOP developers would probably use a couple of design patterns to sug-
gest a much better design. This design is meant to be naive and by no means covers all
the features of the system. It serves two purposes:
 For Theo, the developer, it is rich enough to start coding.
 For me, the author of the book, it is rich enough to illustrate the complexity of a
typical OOP system.
Theo feels proud of himself and of the design diagram he just produced. He definitely
deserves a cup of coffee!
Near the coffee machine, Theo meets Dave, a junior software developer who joined
Albatross a couple of weeks ago. Theo and Dave appreciate each other, as Dave's curiosity
leads him to ask challenging questions. Meetings near the coffee machine often turn into
interesting discussions about programming.
Theo Hey Dave! How's it going?
Dave Today? Not great. I'm trying to fix a bug in my code! I can't understand why
the state of my objects always changes. I'll figure it out though, I'm sure. How's
your day going?
Theo I just finished the design of a system for a new customer.
Dave Cool! Would it be OK for me to see it? I'm trying to improve my design skills.
Theo Sure! I have the diagram on my desk. We can take a look now if you like.
1.1.2 UML 101
Latte in hand, Dave follows Theo to his desk. Theo proudly shows Dave his piece of art: the
UML diagram for the Library Management System (figure 1.1). Dave seems really excited.
Dave Wow! Such a detailed class diagram.
Theo Yeah. I'm pretty happy with it.
Dave The thing is that I can never remember the meaning of the different arrows.
Theo There are four types of arrows in my class diagram: composition, association,
inheritance, and usage.
Dave What's the difference between composition and association?
 NOTE Don't worry if you're not familiar with OOP jargon. We're going to leave it
aside in the next chapter.
Theo It's all about whether the objects can live without each other. With composi-
tion, when one object dies, the other one dies too. While in an association rela-
tion, each object has an independent life.
TIP In a composition relation, when one object dies, the other one also dies. While
in an association relation, each object has an independent life cycle.
In the class diagram, there are two kinds of composition symbolized by an arrow with
a plain diamond at one edge and an optional star at the other edge. Figure 1.2 shows
the relation between:
 A Library that owns a Catalog—A one-to-one composition. If a Library object
dies, then its Catalog object dies with it.
 A Library that owns many Members—A one-to-many composition. If a Library
object dies, then all its Member objects die with it.
TIP A composition relation is represented by a plain diamond at one edge and an
optional star at the other edge.
Dave Do you have association relations in your diagram?
Theo Take a look at the arrow between Book and Author. It has an empty diamond
and a star at both edges, so it's a many-to-many association relation.
A book can be written by multiple authors, and an author can write multiple books.
Moreover, Book and Author objects can live independently. The relation between
books and authors is a many-to-many association (figure 1.3).
TIP A many-to-many association relation is represented by an empty diamond and a
star at both edges.
Dave I also see a bunch of dashed arrows in your diagram.
Theo Dashed arrows are for usage relations: when a class uses a method of another
class. Consider, for example, the Librarian::blockMember method. It calls
Member::block.
TIP Dashed arrows indicate usage relations (figure 1.4), for instance, when a class
uses a method of another class.
Dave I see. And I guess a plain arrow with an empty triangle, like the one between
Member and User, represents inheritance.
Theo Absolutely!
TIP Plain arrows with empty triangles represent class inheritance (figure 1.5), where
the arrow points towards the superclass.
1.1.3 Explaining each piece of the class diagram
Dave Thanks for the UML refresher! Now I think I can remember what the different
arrows mean.
Theo My pleasure. Want to see how it all fits together?
Dave What class should we look at first?
Theo I think we should start with Library.
THE LIBRARY CLASS
The Library is the root class of the library system. Figure 1.6 shows the system structure.
In terms of code (behavior), a Library object does nothing on its own. It delegates
everything to the objects it owns. In terms of data, a Library object owns
 Multiple Member objects
 Multiple Librarian objects
 A single Catalog object
 NOTE In this book, we use the terms code and behavior interchangeably.
LIBRARIAN, MEMBER, AND USER CLASSES
Librarian and Member both derive from User. Figure 1.7 shows this relation.
The User class represents a user of the library:
 In terms of data members, it sticks to the bare minimum: it has an id, email,
and password (with no security and encryption for now).
 In terms of code, it can log in via login.
The Member class represents a member of the library:
 It inherits from User.
 In terms of data members, it has nothing more than User.
 In terms of code, it can
– Check out a book via checkout.
– Return a book via returnBook.
– Block itself via block.
– Unblock itself via unblock.
– Answer if it is blocked via isBlocked.
 It owns multiple BookLending objects.
 It uses BookItem in order to implement checkout.
The Librarian class represents a librarian:
 It derives from User.
 In terms of data members, it has nothing more than User.
 In terms of code, it can
– Block and unblock a Member.
– List the member's book lendings via getBookLendings.
– Add book items to the library via addBookItem.
 It uses Member to implement blockMember, unblockMember, and getBook-
Lendings.
 It uses BookItem to implement checkout.
 It uses BookLending to implement getBookLendings.
THE CATALOG CLASS
The Catalog class is responsible for the management of the books. Figure 1.8 shows
the relation among the Catalog, Librarian, and Book classes. In terms of code, a
Catalog object can
 Search books via search.
 Add book items to the library via addBookItem.
A Catalog object uses Librarian in order to implement addBookItem. In terms of
data, a Catalog owns multiple Book objects.
THE BOOK CLASS
Figure 1.9 presents the Book class. In terms of data, a Book object
 Should have as its bare minimum an id and a title.
 Is associated with multiple Author objects (a book might have multiple authors).
 Owns multiple BookItem objects, one for each copy of the book.
THE BOOKITEM CLASS
The BookItem class represents a book copy, and a book could have many copies. In
terms of data, a BookItem object
 Should have as its bare minimum data for members: an id and a libId (for its
physical library ID).
 Owns multiple BookLending objects, one for each time the book is lent.
In terms of code, a BookItem object can be checked out via checkout.
1.1.4 The implementation phase
After this detailed investigation of Theo's diagrams, Dave lets it sink in as he slowly sips his
coffee. He then expresses his admiration to Theo.
Dave Wow! That's amazing!
Theo Thank you.
Dave I didn't realize people were really spending the time to write down their design
in such detail before coding.
Theo I always do that. It saves me lot of time during the coding phase.
Dave When will you start coding?
Theo When I finish my latte.
Theo grabs his coffee mug and notices that his hot latte has become an iced latte. He was
so excited to show his class diagram to Dave that he forgot to drink it!
1.2 Sources of complexity
While Theo is getting himself another cup of coffee (a cappuccino this time), I
would like to challenge his design. It might look beautiful and clear on the paper,
but I claim that this design makes the system hard to understand. It's not that Theo
picked the wrong classes or that he misunderstood the relations among the classes.
It goes much deeper:
 It's about the programming paradigm he chose to implement the system.
 It's about the object-oriented paradigm.
 It's about the tendency of OOP to increase the complexity of a system.
TIP OOP has a tendency to create complex systems.
Throughout this book, the type of complexity I refer to is that which makes systems
hard to understand as defined in the paper, "Out of the Tar Pit," by Ben Moseley
and Peter Marks (2006), available at http://mng.bz/enzq. It has nothing to do with
the type of complexity that deals with the amount of resources consumed by a pro-
gram. Similarly, when I refer to simplicity, I mean not complex (in other words, easy
to understand).
Keep in mind that complexity and simplicity (like hard and easy) are not absolute
but relative concepts. We can compare the complexity of two systems and determine
whether system A is more complex (or simpler) than system B.
 NOTE Complexity in the context of this book means hard to understand.
As mentioned in the introduction of this chapter, there are many ways in OOP to
alleviate complexity. The purpose of this book is not be critical of OOP, but rather
to present a programming paradigm called data-oriented programming (DOP) that
tends to build systems that are less complex. In fact, the DOP paradigm is compati-
ble with OOP.
If one chooses to build an OOP system that adheres to DOP principles, the system
will be less complex. According to DOP, the main sources of complexity in Theo's sys-
tem (and of many traditional OOP systems) are that
 Code and data are mixed.
 Objects are mutable.
 Data is locked in objects as members.
 Code is locked into classes as methods.
This analysis is similar to what functional programming (FP) thinks about traditional
OOP. However, as we will see throughout the book, the data approach that DOP takes
in order to reduce system complexity differs from the FP approach. In appendix A, we
illustrate how to apply DOP principles both in OOP and in FP styles.
TIP DOP is compatible both with OOP and FP.
In the remaining sections of this chapter, we will illustrate each of the previous
aspects, summarized in table 1.1. We'll look at this in the context of the Klafim project
and explain in what sense these aspects are a source of complexity.
Table 1.1 Aspects of OOP and their impact on system complexity
Aspect Impact on complexity
Code and data are mixed. Classes tend to be involved in many relations.
Objects are mutable. Extra thinking is needed when reading code.
Objects are mutable. Explicit synchronization is required on multi-threaded environments.
Data is locked in objects. Data serialization is not trivial.
Code is locked in classes. Class hierarchies are complex.
1.2.1 Many relations between classes
One way to assess the complexity of a class diagram is to look only at the entities and
their relations, ignoring members and methods, as in figure 1.10. When we design a
system, we have to define the relations between different pieces of code and data.
That's unavoidable.
TIP In OOP, code and data are mixed together in classes: data as members and code as
methods.
From a system analysis perspective, the fact that code and data are mixed together
makes the system complex in the sense that entities tend to be involved in many rela-
tions. In figure 1.11, we take a closer look at the Member class. Member is involved in five
relations: two data relations and three code relations.
 Data relations:
– Library has many Members.
– Member has many BookLendings.
 Code relations:
– Member extends User.
– Librarian uses Member.
– Member uses BookItem.
Imagine for a moment that we were able, somehow, to split the Member class into two
separate entities:
 MemberCode for the code
 MemberData for the data
Instead of a Member class with five relations, we would have the diagram shown in fig-
ure 1.12 with:
 A MemberCode entity and three relations.
 A MemberData entity and two relations.
The class diagram where Member is split into MemberCode and MemberData is made of
two independent parts. Each part is easier to understand than the original diagram.
Let's split every class of our original class diagram into code and data entities.
Figure 1.13 shows the resulting diagram. Now the system is made of two indepen-
dent parts:
 A part that involves only data entities.
 A part that involves only code entities.
TIP A system where every class is split into two independent parts, code and data, is
simpler than a system where code and data are mixed.
The resulting system, made up of two independent subsystems, is easier to understand
than the original system. The fact that the two subsystems are independent means that
each subsystem can be understood separately and in any order. The resulting system
not simpler by accident; it is a logical consequence of separating code from data.
TIP A system made of multiple simple independent parts is less complex than a sys-
tem made of a single complex part.
1.2.2 Unpredictable code behavior
You might be a bit tired after the system-level analysis that we presented in the previ-
ous section. Let's get refreshed and look at some code.
Take a look at the code in listing 1.1, where we get the blocked status of a member
and display it twice. If I tell you that when I called displayBlockedStatusTwice, the
program displayed true on the first console.log call, can you tell me what the pro-
gram displayed on the second console.log call?
"Of course, it displayed true again," you say. And you are right!
Now, take a look at a slightly different pseudocode as shown in listing 1.2. Here we
display, twice, the blocked status of a member without assigning a variable. Same ques-
tion as before: if I tell you that when I called displayBlockedStatusTwice, the pro-
gram displayed true on the first console.log call, can you tell me what the program
displayed on the second console.log call?
The correct answer is...in a single-threaded environment, it displays true, while in a
multi-threaded environment, it's unpredictable. Indeed, in a multi-threaded environ-
ment between the two console.log calls, there could be a context switch that changes
the state of the object (e.g., a librarian unblocked the member). In fact, with a slight
modification, the same kind of code unpredictability could occur even in a single-
threaded environment like JavaScript, when data is modified via asynchronous code
(see the section about Principle #3 in appendix A). The difference between the two
code snippets is that
 In the first listing (listing 1.1), we access a Boolean value twice , which is a prim-
itive value.
 In the second listing (listing 1.2), we access a member of an object twice.
TIP When data is mutable, code is unpredictable.
This unpredictable behavior of the second listing is one of the annoying conse-
quences of OOP. Unlike primitive types, which are usually immutable, object mem-
bers are mutable. One way to solve this problem in OOP is to protect sensitive code
with concurrency safety mechanisms like mutexes, but that introduces issues like a
performance hit and a risk of deadlocks.
We will see later in the book that DOP treats every piece of data in the same way:
both primitive types and collection types are immutable values. This value treatment for
all citizens brings serenity to DOP developers' minds, and more brain cells are avail-
able to handle the interesting pieces of the applications they build.
TIP Data immutability brings serenity to DOP developers' minds.
1.2.3 Not trivial data serialization
Theo is really tired, and he falls asleep at his desk. He's having dream. In his dream, Nancy
asks him to make Klafim's Library Management System accessible via a REST API using
JSON as a transport layer. Theo has to implement a /search endpoint that receives a
query in JSON format and returns the results in JSON format. Listing 1.3 shows an input
example of the /search endpoint, and listing 1.4 shows an output example of the /search
endpoint.
Theo would probably implement the /search endpoint by creating three classes simi-
larly to what is shown in the following list and in figure 1.14. (Not surprisingly, every-
thing in OOP has to be wrapped in a class. Right?)
 SearchController is responsible for handling the query.
 SearchQuery converts the JSON query string into data.
 SearchResult converts the search result data into a JSON string.
The SearchController (see figure 1.14) would have a single handle method with the
following flow:
 Creates a SearchQuery object from the JSON query string.
 Retrieves searchCriteria and queryStr from the SearchQuery object.
 Calls the search method of the catalog:Catalog with searchCriteria and
queryStr and receives books:List<Book>.
 Creates a SearchResult object with books.
 Converts the SearchResult object to a JSON string.
What about other endpoints, for instance, those allowing librarians to add book items
through /add-book-item? Theo would have to repeat the exact same process and cre-
ate three classes:
 AddBookItemController to handle the query
 BookItemQuery to convert the JSON query string into data
 BookItemResult to convert the search result data into a JSON string
The code that deals with JSON deserialization that Theo wrote previously in Search-
Query would have to be rewritten in BookItemQuery. Same thing for the code that
deals with JSON serialization he wrote previously in SearchResult; it would have to be
rewritten in BookItemResult.
The bad news is that Theo would have to repeat the same process for every end-
point of the system. Each time he encounters a new kind of JSON input or output,
he would have to create a new class and write code. Theo's dream is turning into a
nightmare!
Suddenly, his phone rings, next to where he was resting his head on the desk. As Theo
wakes up, he realizes that Nancy never asked for JSON. It was all a dream...a really bad
dream!
TIP In OOP, data serialization is difficult.
It's quite frustrating that handling JSON serialization and deserialization in OOP
requires the addition of so many classes and writing so much code—again and again!
The frustration grows when you consider that serializing a search query, a book item
query, or any query is quite similar. It comes down to
 Going over data fields.
 Concatenating the name of the data fields and the value of the data fields, sepa-
rated by a comma.
Why is such a simple thing so hard to achieve in OOP? In OOP, data has to follow a
rigid shape defined in classes, which means that data is locked in members. There is
no simple way to access data generically.
TIP In OOP, data is locked in classes as members.
We will refine later what we mean by generic access to the data, and we will see how
DOP provides a generic way to handle JSON serialization and deserialization. Until
then, you will have to continue suffering. But at least you are starting to become aware
of this suffering, and you know that it is avoidable.
 NOTE Most OOP programming languages alleviate a bit of the difficulty involved
in the conversion from and to JSON. It either involves reflection, which is definitely a
complex thing, or code verbosity.
1.2.4 Complex class hierarchies
One way to avoid writing the same code twice in OOP involves class inheritance. Indeed,
when every requirement of the system is known up front, you design your class hier-
archy is such a way that classes with common behavior derive from a base class.
Figure 1.15 shows an example of this pattern that focuses on the part of our class
diagram that deals with members and librarians. Both Librarians and Members need
the ability to log in, and they inherit this ability from the User class.
So far, so good, but when new requirements are introduced after the system is imple-
mented, it's a completely different story. Fast forward to Monday, March 29th, at 11:00 AM,
where two days are left before the deadline (Wednesday at midnight).
Nancy calls Theo with an urgent request. Theo is not sure if it's a dream or reality. He
pinches himself and he can feel the jolt. It's definitely reality!
Nancy How is the project doing?
Theo Fine, Nancy. We're on schedule to meet the deadline. We're running our last
round of regression tests now.
Nancy Fantastic! It means we have time for adding a tiny feature to the system, right?
Theo Depends what you mean by "tiny."
Nancy We need to add VIP members to the system.
Theo What do you mean by VIP members?
Nancy VIP members are allowed to add book items to the library by themselves.
Theo Hmm...
Nancy What?
Theo That's not a tiny change!
Nancy Why?
I'll ask you the same question Nancy asked Theo: why is adding VIP members to our
system not a tiny task? After all, Theo has already written the code that allows librari-
ans to add book items to the library (it's in Librarian::addBookItem). What prevents
him from reusing this code for VIP members? The reason is that, in OOP, the code is
locked into classes as methods.
TIP In OOP, code is locked into classes.
VIP members are members that are allowed to add book items to the library by them-
selves. Theo decomposes the customer requirements into two pieces:
 VIP members are library members.
 VIP members are allowed to add book items to the library by themselves.
Theo then decides that he needs a new class, VIPMember. For the first requirement
(VIP members are library members), it seems reasonable to make VIPMember derive
from Member. However, handling the second requirement (VIP members are allowed
to add book items) is more complex. He cannot make a VIPMember derive from
Librarian because the relation between VIPMember and Librarian is not linear:
 On one hand, VIP members are like librarians in that they are allowed to add
book items.
 On the other hand, VIP members are not like librarians in that they are not
allowed to block members or list the books lent to a member.
The problem is that the code that adds book items is locked in the Librarian class.
There is no way for the VIPMember class to use this code.
Figure 1.16 shows one possible solution that makes the code of Librarian::add-
BookItem available to both Librarian and VIPMember classes. Here are the changes to
the previous class diagram:
 A base class UserWithBookItemRight extends User.
 addBookItem moves from Librarian to UserWithBookItemRight.
 Both VIPMember and Librarian extend UserWithBookItemRight.
It wasn't easy, but Theo manages to handle the change on time, thanks to an all nighter
coding on his laptop. He was even able to add new tests to the system and run the regres-
sion tests again. However, he was so excited that he didn't pay attention to the diamond
problem VIPMember introduced in his class diagram due to multiple inheritance: VIPMember
extends both Member and UserWithBookItemRight, which both extend User.
Wednesday, March 31, at 10:00 AM (14 hours before the deadline), Theo calls Nancy to
tell her the good news.
Theo We were able to add VIP members to the system on time, Nancy.
Nancy Fantastic! I told you it was a tiny feature.
Theo Yeah, well...
Nancy Look, I was going to call you anyway. I just finished a meeting with my business
partner, and we realized that we need another tiny feature before the launch.
Will you be able to handle it before the deadline?
Theo Again, it depends what you mean by "tiny."
Nancy We need to add Super members to the system.
Theo What do you mean by Super members?
Nancy Super members are allowed to list the books lent to other members.
Theo Err...
Nancy What?
Theo That's not a tiny change!
Nancy Why?
As with VIP members, adding Super members to the system requires changes to Theo's
class hierarchy. Figure 1.17 shows the solution Theo has in mind.
The addition of Super members has made the system really complex. Theo suddenly
notices that he has three diamonds in his class diagram—not gemstones but three "Deadly
Diamonds of Death" as OOP developers sometimes name the ambiguity that arises when a
class D inherits from two classes B and C, where both inherit from class A!
He tries to avoid the diamonds by transforming the User class into an interface and
using the composition over inheritance design pattern. But with the stress of the deadline
looming, he isn't able to use all of his brain cells. In fact, the system has become so com-
plex, he's unable to deliver the system by the deadline. Theo tells himself that he should
have used composition instead of class inheritance. But, it's too late now.
TIP In OOP, prefer composition over class inheritance.
At 10:00 PM, two hours before the deadline, Theo calls Nancy to explain the situation.
Theo Look Nancy, we really did our best, but we won't be able to add Super mem-
bers to the system before the deadline.
Nancy No worries, my business partner and I decided to omit this feature for now.
We'll add it later.
With mixed feelings of anger and relief, Theo stops pacing around his office. He realizes
he will be spending tonight in his own bed, rather than plowing away on his computer at
the office. That should make his wife happy.
Theo I guess that means we're ready for the launch tomorrow morning.
Nancy Yes. We'll offer this new product for a month or so, and if we get good market
traction, we'll move forward with a bigger project.
Theo Cool. Let's be in touch in a month then. Good luck on the launch!
Summary
 Complexity in the context of this book means hard to understand.
 We use the terms code and behavior interchangeably.
 DOP stands for data-oriented programming.
 OOP stands for object-oriented programming.
 FP stands for functional programming.
 In a composition relation, when one object dies, the other one also dies.
 A composition relation is represented by a plain diamond at one edge and an
optional star at the other edge.
 In an association relation, each object has an independent life cycle.
 A many-to-many association relation is represented by an empty diamond and a
star at both edges.
 Dashed arrows indicate a usage relation; for instance, when a class uses a method
of another class.
 Plain arrows with empty triangles represent class inheritance, where the arrow
points towards the superclass.
 The design presented in this chapter doesn't pretend to be the smartest OOP
design. Experienced OOP developers would probably use a couple of design
patterns and suggest a much better diagram.
 Traditional OOP systems tend to increase system complexity, in the sense that
OOP systems are hard to understand.
 In traditional OOP, code and data are mixed together in classes: data as mem-
bers and code as methods.
 In traditional OOP, data is mutable.
 The root cause of the increase in complexity is related to the mixing of code
and data together into objects.
 When code and data are mixed, classes tend to be involved in many relations.
 When objects are mutable, extra thinking is required in order to understand
how the code behaves.
 When objects are mutable, explicit synchronization mechanisms are required
on multi-threaded environments.
 When data is locked in objects, data serialization is not trivial.
 When code is locked in classes, class hierarchies tend to be complex.
 A system where every class is split into two independent parts, code and data, is
simpler than a system where code and data are mixed.
 A system made of multiple simple independent parts is less complex than a sys-
tem made of a single complex part.
 When data is mutable, code is unpredictable.
 A strategic use of design patterns can help mitigate complexity in traditional
OOP to some degree.
 Data immutability brings serenity to DOP developers' minds.
 Most OOP programming languages alleviate slightly the difficulty involved the
conversion from and to JSON. It either involves reflection, which is definitely a
complex thing, or code verbosity.
 In traditional OOP, data serialization is difficult.
 In traditional OOP, data is locked in classes as members.
 In traditional OOP, code is locked into classes.
 DOP reduces complexity by rethinking data.
 DOP is compatible both with OOP and FP."""

    # 섹션별 분할 정의
    sections = [
        {
            "file": "1_0_introduction.md",
            "title": "# 1.0 Introduction (사용자 추가)",
            "start": "Complexity of object-oriented programming",
            "end": "known as data-oriented programming (DOP)."
        },
        {
            "file": "1_1_0_introduction.md", 
            "title": "# 1.1.0 Introduction (사용자 추가)",
            "start": " NOTE Theo, Nancy, and their new project",
            "end": "His job is to close deals and to deliver on time."
        },
        {
            "file": "1_1_1_design_phase.md",
            "title": "# 1.1.1 The design phase", 
            "start": "Before rushing to his laptop to code the system",
            "end": "We can take a look now if you like."
        },
        {
            "file": "1_1_2_uml_101.md",
            "title": "# 1.1.2 UML 101",
            "start": "Latte in hand, Dave follows Theo to his desk",
            "end": "the arrow points towards the superclass."
        },
        {
            "file": "1_1_3_explaining_class_diagram.md", 
            "title": "# 1.1.3 Explaining each piece of the class diagram",
            "start": "Dave Thanks for the UML refresher!",
            "end": "a BookItem object can be checked out via checkout."
        },
        {
            "file": "1_1_4_implementation_phase.md",
            "title": "# 1.1.4 The implementation phase",
            "start": "After this detailed investigation of Theo's diagrams",
            "end": "he forgot to drink it!"
        },
        {
            "file": "1_2_0_introduction.md",
            "title": "# 1.2.0 Introduction (사용자 추가)", 
            "start": "While Theo is getting himself another cup of coffee",
            "end": "source of complexity."
        },
        {
            "file": "1_2_1_many_relations.md",
            "title": "# 1.2.1 Many relations between classes",
            "start": "One way to assess the complexity of a class diagram",
            "end": "system made of a single complex part."
        },
        {
            "file": "1_2_2_unpredictable_behavior.md",
            "title": "# 1.2.2 Unpredictable code behavior", 
            "start": "You might be a bit tired after the system-level analysis",
            "end": "serenity to DOP developers' minds."
        },
        {
            "file": "1_2_3_data_serialization.md",
            "title": "# 1.2.3 Not trivial data serialization",
            "start": "Theo is really tired, and he falls asleep at his desk",
            "end": "code verbosity."
        },
        {
            "file": "1_2_4_complex_hierarchies.md", 
            "title": "# 1.2.4 Complex class hierarchies",
            "start": "One way to avoid writing the same code twice in OOP",
            "end": "Good luck on the launch!"
        },
        {
            "file": "summary.md",
            "title": "# Summary", 
            "start": "Summary",
            "end": "DOP is compatible both with OOP and FP."
        }
    ]
    
    # 각 섹션별로 파일 생성
    for section in sections:
        try:
            start_idx = chapter1_text.find(section["start"])
            end_idx = chapter1_text.find(section["end"]) + len(section["end"])
            
            if start_idx != -1 and end_idx != -1:
                content = chapter1_text[start_idx:end_idx]
                full_content = f"{section['title']}\n\n{content}"
                
                file_path = os.path.join(output_dir, section["file"])
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                
                print(f"✅ Created: {section['file']}")
            else:
                print(f"❌ Failed to find content for: {section['file']}")
                
        except Exception as e:
            print(f"❌ Error creating {section['file']}: {e}")
    
    print(f"\n🎯 Total files created in: {output_dir}")

if __name__ == "__main__":
    extract_leaf_nodes()