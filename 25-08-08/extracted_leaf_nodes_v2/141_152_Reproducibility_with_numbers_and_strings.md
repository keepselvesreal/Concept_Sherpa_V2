# 15.2 Reproducibility with numbers and strings

**메타데이터:**
- ID: 141
- 레벨: 2
- 페이지: 342-345
- 페이지 수: 4
- 부모 ID: 138
- 텍스트 길이: 7241 문자

---

lity with numbers and strings
Theo In fact, we don’t even need a debugger in order to capture a function context.
Dave But the function context is basically made of its arguments. How can you
inspect the arguments of a function without a debugger?
Theo By modifying the code of the function under investigation and printing the
serialization of the arguments to the console.
Dave I don’t get that.
Theo Let me show you what I mean with a function that deals with numbers.
Dave OK.
Theo Take for instance a function that returns the nth digit of a number.
Dave Oh no, I hate digit arithmetic!
Theo Don’t worry, we’ll find some code for it on the web.
Theo googles “nth digit of a number in JavaScript” and takes a piece of code from Stack-
Overflow that seems to work.

15.2 Reproducibility with numbers and strings 315
Listing15.1 Calculate the nth digit of a number
function nthDigit(a, n) {
return Math.floor((a / (Math.pow(10, n - 1)))) % 10;
}
Dave Do you understand how it works?
Theo Let’s see, dividing a by 10n–1 is like right-shifting it n–1 places. Then we need to
get the rightmost digit.
Dave And the last digit of a number is obtained by the modulo 10 operation?
Theo Right! Now, imagine that this function is called down the stack when some
endpoint is triggered. I’m going to modify it by adding context-capturing code.
Dave What’s that?
Theo Context-capturing code is code that we insert at the beginning of a function
body to print the values of the arguments. Let me edit the nthDigit code to
give you an example.
Listing15.2 Capturing a context made of numbers
function nthDigit(a, n) {
console.log(a);
console.log(n);
return Math.floor((a / (Math.pow(10, n - 1)))) % 10;
}
Dave It looks trivial.
Theo It is trivial for now, but it will get less trivial in a moment. Now, tell me what
happens when I trigger the endpoint.
Dave When the endpoint is triggered, the program will display the two numbers, a
and n, in the console.
Theo Exactly, and what would you have to do in order to replay the function in the
same context as when the endpoint was triggered?
Dave I would need to copy the values of a and n from the console, paste them into
the REPL, and call nthDigit with those two values.
Theo What makes you confident that when we run nthDigit in the REPL, it will
reproduce exactly what happened when the endpoint was triggered? Remem-
ber, the REPL might run in a separate process.
Dave I know that nthDigit depends only on its arguments.
Theo Good. Now, how can you be sure that the arguments you pass are the same as
the arguments that were passed?
Dave A number is a number!
Theo I agree with you. Let’s move on and see what happens with strings.
Dave I expect it to be exactly the same.
Theo It’s going to be almost the same. Let’s write a function that receives a sentence
and a prefix and returns true when the sentence contains a word that starts
with the prefix.

316 CHAPTER 15 Debugging
Dave Why would anyone ever need such a weird function?
Theo It could be useful for the Library Management System when a user wants to
find books whose title contains a prefix.
Dave Interesting. I’ll talk about that with Nancy. Anyway, coding such a function
seems quite obvious. I need to split the sentence string into an array of words
and then check whether a word in the array starts with the prefix.
Theo How are you going to check whether any element of the array satisfies the
condition?
Dave I think I’ll use Lodash filter and check the length of the returned array.
Theo That would work but it might have a performance issue.
Dave Why?
Theo Think about it for a minute.
Dave I got it! filter processes all the elements in the array rather than stopping
after the first match. Is there a function in Lodash that stops after the first
match?
Theo Yes, it’s called find.
Dave Cool. I’ll use that. Hang on.
Dave reaches over for his laptop and write the code to check whether a sentence contains a
word that starts with a prefix. After a brief period, he shows Theo his implementation of
hasWordStartingWith using _.find.
Listing15.3 Checking if a sentence contains a word starting with a prefix
function hasWordStartingWith(sentence, prefix) {
var words = sentence.split(" ");
return _.find(words, function(word) {
return word.startsWith(prefix);
}) != null;
}
Theo OK, now, please add the context-capturing code at the beginning of the function.
Dave Sure, let me edit this code a bit. Voilà!
Listing15.4 Capturing a context made of strings
function hasWordStartingWith(sentence, prefix) {
console.log(sentence);
console.log(prefix);
var words = sentence.split(" ");
return _.find(words, function(word) {
return word.startsWith(prefix);
}) != null;
}
Theo Let me inspect your code for a minute. I want to see what happens when I
check whether the sentence “I like the word reproducibility” contains a word that
starts with li.

15.2 Reproducibility with numbers and strings 317
Theo uses Dave’s laptop to examine Dave’s code. It returns true as expected, but it doesn’t
display to the console the text that Dave expected. He shares his surprise with Theo.
Listing15.5 Testing hasWordStartingWith
hasWordStartingWith("I like the word \"reproducibility\"", "li");
// It returns true
// It displays the following two lines:
// I like the word "reproducibility"
// li
Dave Where are the quotes around the strings? And where are the backslashes
before the quotes surrounding the word reproducibility?
Theo They disappeared!
Dave Why?
Theo When you print a string to the console, the content of the string is displayed
without quotes. It’s more human-readable.
Dave Bummer! That’s not good for reproducibility. So, after I copy and paste a
string I have to manually wrap it with quotes and backslashes.
Theo Fortunately, there is a simpler solution. If you serialize your string to JSON,
then it has the quotes and the backslashes. For instance, this code displays the
string you expected.
Listing15.6 Displaying to the console the serialization of a string
console.log(JSON.stringify(
"I like the word \"reproducibility\""));
// → "I like the word \"reproducibility\""
Dave I didn’t know that strings were considered valid JSON data. I thought only
objects and arrays were valid.
Theo Both compound data types and primitive data types are valid JSON data.
Dave Cool! I’ll fix the code in hasWordStartingWith that captures the string argu-
ments. Here you go.
Listing15.7 Capturing a context made of strings using JSON serialization
function hasWordStartingWith(sentence, prefix) {
console.log(JSON.stringify(sentence));
console.log(JSON.stringify(prefix));
var words = sentence.split(" ");
return _.find(words, function(word) {
return word.startsWith(prefix);
}) != null;
}
Theo Great! Capturing strings takes a bit more work than with numbers, but with
JSON they’re not too bad.
Dave Right. Now, I’m curious to see if using JSON serialization for context capturing
works well with numbers.

318 CHAPTER 15 Debugging
Theo It works. In fact, it works well with any data, whether it’s a primitive data type or
a collection.
Dave Nice!
Theo Next, I’ll show you how to use this approach to reproduce a real scenario that
happens in the context of the Library Management System.
Dave No more digit arithmetic?
Theo No more!