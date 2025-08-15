### 1.9.5 Test-Driven Development

**Question**: For test driven development, do you have any tips because I often see that Claude just spits out the entire implementation and then writes test cases. Sometimes they don't, they fail and then I'm trying to prompt it to write the test cases first but I also don't want to verify them by myself because I haven't seen implementation yet so do you have an iterative approach that you've ever tried for test driven development?

**Eric**: Yeah yeah I definitely, test driven development is very useful in vibe coding as long as you can understand what the test cases are even without that it helps Claude be a little bit more self consistent even if you yourself don't look at the tests.

But a lot of times, I'd say it's easy for Claude to go down a rabbit hole of writing tests that are too implementation specific. When I'm trying to do this, a lot of times I will encourage, I will give Claude examples of like, hey, just write three end-to-end tests and, you know, do the happy path, an error case, and this other error case. And I'm very prescriptive about that. I want the test to be general and end to end. And I think that helps make sure it's something that I can understand and it's something that Claude can do without getting too in the weeds.

I'll also say a lot of times when I'm vibe coding the only part of the code or at least the first part of the code that I'll read is the tests to make sure that if I agree with the tests and the tests pass then I feel pretty good about the code. That works best if you can encourage Claude to write very minimalist end-to-end tests.
