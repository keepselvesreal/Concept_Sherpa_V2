# 9.2 The efficiency of persistent data structures

Theo In what sense are those data structures persistent?
Joe Persistent data structures are so named because they always preserve their pre-
vious versions.
TIP Persistent data structures always preserve the previous version of themselves
when they are modified.
Joe Persistent data structures address the two main limitations of naive structural
sharing: safety and performance.

## 페이지 207

9.2 The efficiency of persistent data structures 179
Theo Let’s start with safety. How do persistent data structures prevent data from
being mutated accidentally?
Joe In a language like Java, they implement the mutation methods of the collec-
tion interfaces by throwing the run-time exception UnsupportedOperation-
Exception.
Theo And, in a language like JavaScript?
Joe In JavaScript, persistent data structures provide their own methods to access
data, and none of those methods mutate data.
Theo Does that mean that we can’t use the dot notation to access fields?
Joe Correct. Fields of persistent data structures are accessed via a specific API.
Theo What about efficiency? How do persistent data structures make it possible to
create a new version of a huge collection in an efficient way?
Joe Persistent data structures organize data in such a way that we can use structural
sharing at the level of the data structure.
Theo Could you explain?
Joe Certainly. Let’s start with the simplest data structure: a linked list. Imagine that
you have a linked list with 100,000 elements.
Theo OK.
Joe What would it take to prepend an element to the head of the list?
Theo You mean to create a new version of the list with an additional element?
Joe Exactly!
Theo Well, we could copy the list and then prepend an element to the list, but it
would be quite expensive.
Joe What if I tell you that the original linked list is guaranteed to be immutable?
Theo In that case, I could create a new list with a new head that points to the head of
the original list.
Theo goes to the classroom blackboard. He picks up a piece of chalk and draws the dia-
gram shown in figure 9.1.
New list Original list
Figure 9.1 Structural sharing
0 1 2 3 4 5 with linked lists
Joe Would the efficiency of this operation depend on the size of the list?
Theo No, it would be efficient, no matter the size of the list.
Joe That’s what I mean by structural sharing at the level of the data structure itself.
It relies on a simple but powerful insight—when data is immutable, it is safe to
share it.
TIP When data is immutable, it is safe to share it.

## 페이지 208

180 CHAPTER 9 Persistent data structures
Theo I understand how to use structural sharing at the level of the data structure for
linked lists and prepend operations, but how would it work with operations
like appending or modifying an element in a list?
Joe For that purpose, we need to be smarter and represent our list as a tree.
Theo How does that help?
Joe It helps because when a list is represented as a tree, most of the nodes in the
tree can be shared between two versions of the list.
Theo I am totally confused.
Joe Imagine that you take a list with 100,000 elements and split it into two lists of
50,000 elements each: elements 0 to 49,999 in list 1, and elements 50,000 to
99,999 in list 2. How many operations would you need to create a new version
of the list where a single element—let’s say, element at index 75,100—is
modified?
It’s hard for Theo to visualize this kind of stuff mentally. He goes back to the blackboard
and draws a diagram (see figure 9.2). Once Theo looks at the diagram, it’s easy for him to
answer Joe’s question.
List «Next»
List
List 1 List 2
«Next»
0...49,999 50,000...99,999
List 2
Figure 9.2 Structural sharing when
50,000...99,999
a list of 100,000 elements is split
Theo List 1 could be shared with one operation. I’d need to create a new version of
list 2, where element 75,100 is modified. It would take 50,000 operations, so it’s
one operation of sharing and one operation of copying 50,000 elements. Over-
all, it’s 50,001 operations.
Joe Correct. You see that by splitting our original list into two lists, we can create a
new version of the list with a number of operations in the order of the size of
the list divided by 2.
Theo I agree, but 50,000 is still a big number.
Joe Indeed, but nobody prevents us from applying the same trick again, splitting
list 1 and list 2 in two lists each.
Theo How exactly?
Joe We can make list 1.1 with elements 0 to 24,999, then list 1.2 with elements
25,000 to 49,999, list 2.1 with elements 50,000 to 74,999, and list 2.2 with ele-
ments 75,000 to 99,999.
Theo Can you draw that on the blackboard?
Joe Sure.

## 페이지 209

9.2 The efficiency of persistent data structures 181
Now, it’s Joe that goes to the blackboard. He draws the diagram in figure 9.3.
«Next»
List
List
«Next»
List 1 List 2 List 2
List 1.1 List 1.2 List 2.1 List 2.2 «Next»
0...24,499 25,000...49,999 50,000...74,999 75,000...99,999 List 2.2
75,000...99,999
Figure 9.3 Structural sharing when a list of 100,000 elements is split twice
Theo Let me count the number of operations for updating a single element. It takes
2 operations of sharing and 1 operation of copying 25,000 elements. Overall, it
takes 25,002 operations to create a new version of the list.
Joe Correct!
Theo Let’s split the list again then!
Joe Absolutely. In fact, we can split the list again and again until the size of the
lists is at most 2. Can you guess what is the complexity of creating a new ver-
sion then?
Theo I’d say around log2 N operations.
Joe I see that you remember well your material from school. Do you have a gut
feeling about what is log2 N when N is 100,000?
Theo Let me see...2 to the power of 10 is around 1,000, and 2 to the power of 7 is
128. So, it should be a bit less than 17.
Joe It’s 16.6 to be precise. It means that in order to update an element in a per-
sistent list of 100,000 elements, we need around 17 operations. The same goes
for accessing elements.
Theo Nice, but 17 is still not negligible.
Joe I agree. We can easily improve the performance of accessing elements by using
a higher branching factor in our tree.
Theo What do you mean?
Joe Instead of splitting by 2 at each level, we could split by 32.
Theo But the running time of our algorithm would still grow with log N.
Joe You’re right. From a theoretical perspective, it’s the same. From a practical
perspective, however, it makes a big difference.
Theo Why?
Joe Because log32 N is 5 times lower than log2 N.

## 페이지 210

182 CHAPTER 9 Persistent data structures
Theo That’s true: 2 to the power of 5 is 32.
Joe Back to our list of 100,000 elements, can you tell me how many operations are
required to access an element if the branching factor is 32?
Theo With a branching factor of 2, it was 16.6. If I divide 16.6 by 5, I get 3.3.
Joe Correct!
TIP By using a branching factor of 32, we make elements accessed in persistent lists
more efficient.
Theo Does this trick also improve the performance of updating an element in a list?
Joe Yes, indeed, it does.
Theo How? We’d have to copy 32 elements at each level instead of 2 elements. It’s a
16× performance hit that’s not compensated for by the fact that the tree depth
is reduced by 5×!
Joe I see that you are quite sharp with numbers. There is another thing to take
into consideration in our practical analysis of the performance: modern CPU
architecture.
Theo Interesting. The more you tell me about persistent data structures, the more I
understand why you wanted to have this session at a university: it’s because
we’re dealing with all this academic stuff.
Joe Yep. So, to continue, modern CPUs read and write data from and to the main
memory in units of cache lines, often 32 or 64 bytes long.
Theo What difference does that make?
Joe A nice consequence of this data access pattern is that copying an array of size
32 is much faster than copying 16 arrays of size 2 that belong to different levels
of the tree.
Theo Why is that?
Joe The reason is that copying an array of size 32 can be done in a single pair of
cache accesses: one for read and one for write. Although for arrays that belong
to different tree levels, each array requires its own pair of cache accesses, even
if there are only 2 elements in the array.
Theo In other words, the performance of updating a persistent list is dominated by
the depth of the tree.
TIP In modern CPU architectures, the performance of updating a persistent list is
dominated much more by the depth of the tree than by the number of nodes at each
level of the tree.
Joe That’s correct, up to a certain point. With today’s CPUs, using a branching fac-
tor of 64 would, in fact, decrease the performance of update operations.
Theo I see.
Joe Now, I am going to make another interesting claim that is not accurate from a
theoretical perspective but accurate in practice.
Theo What is it?

## 페이지 211

9.2 The efficiency of persistent data structures 183
Joe The number of operations it takes to get or update an element in a persistent
list with branching factor 32 is constant.
Theo How can that be? You just made the point that the number of operations is
log32 N.
Joe Be patient, my friend. What is the highest number of elements that you can
have in a list, in practice?
Theo I don’t know. I never thought about that.
Joe Let’s assume that it takes 4 bytes to store an element in a list.
Theo OK.
Joe Now, can you tell me how much memory it would take to hold a list with 10 bil-
lion elements?
Theo You mean 1 with 10 zeros?
Joe Yes.
Theo Each element take 4 bytes, so it would be around 40 GB!
Joe Correct. Do you agree that it doesn’t make sense to hold a list that takes 40 GB
of memory?
Theo I agree.
Joe So let’s take 10 billion as an upper bound to the number of elements in a list.
What is log32 of 10 billion?
Once again, Theo uses the blackboard to clarify his thoughts. With that, he quickly finds
the answer.
Theo 1 billion is approximately 2^30. Therefore, 10 billion is around 2^33. That
means that log2 of 10 billion is 33, so log32 of 10 billion should be around
33/5, which is a bit less than 7.
Joe I am impressed again by your sharpness with numbers. To be precise, log32 of
10 billion is 6.64.
Theo (smiling) I didn’t get that far.
Joe Did I convince you that, in practice, accessing or updating an element in a per-
sistent list is essentially constant?
Theo Yes, and I find it quite amazing!
TIP Persistent lists can be manipulated in near constant time.
Joe Me too.
Theo What about persistent maps?
Joe It’s quite similar, but I don’t think we have time to discuss it now.
Startled, Theo looks at his watch. This morning’s session has gone by so quickly. He notices
that it’s time to get back to the office and have lunch.

## 페이지 212

184 CHAPTER 9 Persistent data structures