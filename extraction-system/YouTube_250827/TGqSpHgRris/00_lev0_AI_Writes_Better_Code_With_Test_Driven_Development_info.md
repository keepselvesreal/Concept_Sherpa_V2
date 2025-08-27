# 속성
---
process_status: true
source: https://www.youtube.com/watch?v=TGqSpHgRris
source_type: youtube
source_language: english
structure_type: standalone
content_processing: unified
created_at: 2025-08-27T16:46:32.794450

# 추출
---
## 핵심 내용
이 영상은 AI가 테스트 주도 개발(TDD) 방법론을 통해 프로덕션 레디 코드를 작성하는 방법을 실제 경매 사이트 구현으로 보여주며, Python과 Java 백엔드에서 "Buy-It-Now" 기능을 동시에 개발하는 과정을 통해 AI 코딩의 한계와 올바른 방법론 사용의 중요성을 강조한다.

## 상세 핵심 내용
영상의 핵심은 AI 코드가 프로덕션에서 자주 실패하는 문제를 테스트 주도 개발로 해결하는 것이다. 제작자는 Python과 Java 백엔드를 가진 경매 사이트에서 "Buy-It-Now" 기능을 구현하며, AI가 먼저 테스트를 작성한 후 코드를 구현하는 TDD 방식을 실증한다.

실제 구현 과정에서 흥미로운 차이점들이 드러난다. Java는 엄격한 타입 시스템과 컴파일 과정 덕분에 한 번에 성공적으로 구현되었지만, Python에서는 몇 가지 타입 관련 이슈가 발생했다. 이는 강타입 언어가 AI 코딩에서 가지는 장점을 보여준다.

프론트엔드 구현에서 문제가 발생한 부분이 특히 교육적이다. TDD 없이 구현한 프론트엔드는 buyout 기능이 실행될 때 적절히 처리하지 못하는 버그를 보였고, 이를 통해 올바른 방법론 없이는 AI 코딩도 한계가 있음을 실증했다.

제작자는 AI 코딩이 100% 생산성 향상을 보장한다는 과대광고를 경계하며, 실제로는 적절한 소프트웨어 개발 방법론과 기본적인 코딩 스킬이 필요하다고 강조한다. TDD는 이미 검증된 프레임워크로서 AI 에이전트가 자체 테스트를 통해 코드의 정확성을 확인할 수 있게 해준다.

## 상세 내용
테스트 주도 개발의 AI 적용은 여러 단계로 이루어진다. 먼저 AI는 구현하려는 기능에 대한 포괄적인 테스트 케이스를 작성한다. 이 과정에서 정상적인 케이스뿐만 아니라 엣지 케이스도 고려된다. 예를 들어, buyout 가격이 시작 가격보다 높아야 한다는 비즈니스 로직이나, buyout 가격 없이도 경매가 생성될 수 있어야 한다는 하위 호환성 요구사항 등이 테스트에 반영된다.

흥미롭게도 Java와 Python 구현 사이에 나타난 차이점은 언어 특성이 AI 코딩에 미치는 영향을 보여준다. Java의 엄격한 타입 시스템은 컴파일 타임에 많은 오류를 잡아내며, 이는 AI가 더 안정적인 코드를 작성하는 데 도움이 된다. 반면 Python에서는 런타임에 발견되는 타입 관련 이슈들이 있었고, 이는 동적 타입 언어의 한계를 보여준다.

프론트엔드 구현에서 발생한 문제는 방법론의 중요성을 극명하게 보여준다. TDD 없이 구현된 프론트엔드는 buyout 기능 실행 시 경매가 종료되는 상황을 제대로 처리하지 못했다. 이는 AI 코딩에서 흔히 발생하는 문제로, 모든 시나리오를 미리 고려하지 않으면 예상치 못한 상황에서 실패할 수 있음을 보여준다.

제작자가 강조하는 또 다른 중요한 점은 AI 코딩의 현실적인 한계이다. AI는 분명히 생산성을 향상시키는 도구이지만, 기본적인 프로그래밍 지식과 디버깅 능력 없이는 AI가 생성한 코드의 문제를 해결할 수 없다. 이는 많은 AI 코딩 튜토리얼이 놓치는 부분으로, 실제 개발 환경에서는 항상 완벽한 코드가 생성되지 않기 때문이다.

TDD의 "Red-Green-Refactor" 사이클이 AI 코딩에서 어떻게 작동하는지도 흥미롭다. AI는 먼저 실패하는 테스트를 작성하고(Red), 그 테스트를 통과하는 최소한의 코드를 구현한다(Green). 이 과정에서 AI는 불필요하게 복잡한 코드를 작성하는 경향을 억제하고, 실제로 필요한 기능에만 집중할 수 있다.

병렬 개발 접근법도 주목할 만하다. 두 개의 Claude Code 세션을 동시에 실행하여 Java와 Python 백엔드를 병렬로 개발하는 방식은 실제 팀 개발 환경에서의 활용 가능성을 시사한다. 각 AI 에이전트가 특정 기술 스택에 집중함으로써 더 나은 결과를 얻을 수 있음을 보여준다.

## 주요 화제
- **테스트 주도 개발(TDD)**: AI가 먼저 테스트를 작성한 후 코드를 구현하는 방법론
- **프로덕션 레디 AI 코드**: 실제 운영 환경에서 안정적으로 작동하는 코드 작성 전략
- **언어별 구현 차이**: Java의 강타입 시스템 vs Python의 동적 타입 시스템
- **Buy-It-Now 기능 구현**: 경매 시스템에 즉시 구매 기능 추가하는 실제 사례
- **AI 코딩의 현실적 한계**: 과대광고와 실제 성능 사이의 차이점
- **병렬 개발 전략**: 여러 AI 세션을 동시에 활용한 효율적 개발 방법

## 부차 화제
- **경매 사이트 아키텍처**: Python과 Java 백엔드가 하나의 데이터베이스를 공유하는 구조
- **Claude Code 사용법**: AI 코딩 도구의 실제 활용 방법과 팁
- **엣지 케이스 테스팅**: buyout 가격 검증, 하위 호환성 등의 경계 조건 처리
- **프론트엔드 연동 문제**: 백엔드 변경사항이 프론트엔드에 미치는 영향
- **Git 워크플로우**: AI 개발 과정에서의 버전 관리 방법
- **컴파일 언어의 장점**: Java 컴파일 과정이 제공하는 코드 품질 보장
- **AI Native Engineer 커뮤니티**: 제작자의 교육 프로그램 소개
- **실시간 디버깅**: 개발 중 발생한 문제의 즉시 해결 과정
- **최소 구현 원칙**: TDD에서 테스트를 통과하는 최소한의 코드만 작성하는 접근법
- **타입 안정성**: 정적 타입 언어가 AI 코딩에서 제공하는 이점

# 내용
---
# AI Writes Better Code With Test Driven Development

## Introduction: Production-Ready AI Code

[00:00] Everybody wants production ready AI code, but the brutal truth is AI code breaks in production more often than not. And in this video, I'm going to solve that problem for you because I'm going to teach you how you can make your AI agent test its own code using testdriven development. This means that AI will first write the tests to actually know whether its implementation is correct or not, thereby being a self-testing AI agent. And to prove that this works, I'm going to be implementing this strategy on a codebase that uses both Python as well as Java. So that no matter what programming language you use, you know how to use the strategy properly a senior engineer.

## Demo Application: Auction Site with Python and Java Backends

[00:37] So let's get started. Welcome to our test application of today, an auction site that's implemented in both Python as well as Java. And this front end interacts with both of these backends at once. And these backends actually communicate over the same database. So, for example, I can actually create a sample auction on the Python site here. And then let's go ahead and bid on this Raspberry Pi cluster kit with Python Pete. I'm going to bid $250. And then you can indeed see that now I am the highest bidder. And if I switch to Java side of things, I can actually enter a bid here as well. I can, for example, say that I want to bid 270 bucks with Java Jane. So, I'm going to go ahead and place a bid. And you can actually see now that my bid must be at least $275 because this actually has a current price and then a minimum increment. So, okay, we'll go ahead and actually bid 275 bucks then. And there we go. We can even for example close the current auction and then go ahead and create a new sample auction in the Java side as well just to show you that these backends are interoperable. They both have the same endpoints.

## Implementing Buy-It-Now Feature with Test-Driven Development

[01:41] Now, we are going to be implementing a new feature on this auctioning website, namely the ability to set the price at which an item can be immediately purchased. You see this a lot on platforms eBay, right? Where you're able to just bid a specific amount and then the item is guaranteed to be yours. So, let's go ahead and see how we're going to implement that in both of these backends using testdriven development. First, we have to explore the codebase. So, let's go ahead and jump right into Visual Studio Code. In here, you can actually see that we have a couple of folders. You can see here how we have a Java backend, a Python backend, and this simple web interface, which is just an HTML file. And to build this new feature, I actually have prepared a prompt. And this prompt will actually be included in the description down below. No need to worry about that for now. And this prompt actually describes how Claw Code should implement a new feature using test-driven development.

[02:33] So, let's actually go ahead and check out what we're going to be building. We're going to be building a buy it now feature for the auctioning system. Now the thing is there's a lot of requirements here about adding an optional field, setting a certain buyout price that must be higher than the starting price etc. But the process of building this feature doesn't start with actually creating the code for the feature itself. No, actually test-driven development is a form of development where you first write the tests for your feature which will obviously fail because the code has not been implemented yet. And then from that point forward, your AI agent will implement the actual code. And the beautiful part is after it has implemented the code, it can run all of the tests again. And if they all pass, then you know that your code is actually genuinely functional.

## Test-Driven Development Methodology and Edge Cases

[03:18] And of course, you can have a bit of a human in the loop element here as well, where you can, for example, first check the unit tests before you let the AI agent actually write the code to make sure that the tests already match your expectation. So in this case, what's actually going to happen is we're going to be implementing eight test cases. For example, creating an auction with a valid buyout price, but we also want to test some edge cases, right? That's how you're going to get production ready code. For example, we want to make sure that auctions can still be created without a buyout price to make sure that we have backwards compatibility with how the system worked before. So that's really how this prompt works on the high level. But in order to do test-driven development, you do actually need an existing test suite. In this case, if we open for example the Python backend folder, you will see how we actually have a test auction service Python file and this file contains our current unit tests. Similarly on the Java side of things, if we go into source, you can actually see we have a test folder here as well. And you can see how we actually have various tests, for example, for the auction service. And this is basically the test suite that Claude code is going to be extending with test-driven development before it actually implements the new bidding feature.

## Implementing Tests and Code Across Both Backends

[04:33] In any case, enough talking. Let's get coding. So, what I'm going to do is I'm actually going to go ahead and open two new windows because I want to implement this feature on both the Java back end as well as the Python back end. But I'm not going to make Cloud Code do both backends at once. That's just asking for problems. I want Cloud Code to be able to focus on one programming language at a time. All right. So, I set up two terminal windows, one for the Python backend and then one for the Java backend. And all I'm going to do now is actually just start up two clawed code windows. And I'm going to say proceed for this one. I do trust my own back end, of course. And then what I'm going to do is I'm actually just going to paste this test-driven development feature prompt because it already includes all of the directives that Claude Code needs to get started on writing the actual test first. So, we're going to paste the exact same prompt into both of these Cloud Code sessions. And in a way, we're actually going to be parallelizing this effort, right? Because we're going to have two agents working on both of the actual backends at the same time.

## AI Coding Limitations and Importance of Skills

[05:32] Now, you can actually see here that it's going to be starting to implement this feature by using strict testdriven development methodology. And while it's coming up with the first test, I just wanted to let you know that watching this video until the very end is very important because there's so much content out there nowadays that tries to make you believe that AI coding will 100 extra productivity and that AI code can just oneshot the most complex applications out there. But this is not true. AI coding has been a great productivity booster for me as an actual senior engineer, but it has its limits. But by using real software methodologies test-driven development, you can actually write productionready AI code. You just have to follow tutorials this one and really understand how to write proper AI code first. There are a lot of distracting methodologies out there that people try to teach you the BMAT method. And I'm not saying that these methods are bad. It's just that it doesn't compensate for lack of skills. If you for example don't know how to code, then you are going to get stuck with AI coding no matter what method you're using because it's going to make a mistake now and then and then if you don't know any Python or Java then how are you going to fix this application? That's right, you will not be able to and that's where you get stuck. So actually understanding how to code properly is super important and that's what you're learning today because test-driven development has been a tested framework that has been used in software development for many years now.

## Test Results and Implementation Differences

[06:52] Okay, enough theoretical talk. Let's actually see what cloud code is up to right now. And you can actually see that it's understood the codebase structure and of course it's explored different files for the Java side of things compared to the Python files. The Python files are a lot flatter. There's a lot more included in one single file whereas the Java files are a little bit more split apart. It's an interesting difference between writing Java and Python code. Right. And now you can see that the first failing test has been written. I'm going to give this terminal a little bit more room so you can see what's going on. I'm going to go ahead and allow it to make these edits. And then if we check out our git work tree, you can see that finally we have our first test here. This is a new test that will actually fail because if you look here, you can actually see that set buyout price is not even a valid method because it's not been implemented yet. That's a good thing. That's how we're actually approaching this test-driven development properly. So now what you can see is that claw code is going to run all tests to confirm that these new tests do fail. So here you go. It's written a bunch of new failing tests and now it's actually going to go ahead and run all of the tests. And I think I can actually show you if I do controlr here that a lot of these tests are failing. That's exactly what we want. So we can go ahead and toggle back and you can indeed see that in this case that's a great thing. Cloud code is aware that it's supposed to be failing. And now it's actually going to be implementing the minimum code to make the tests pass.

[08:15] And this is a super important element as well. A lot of the times AI code is super verbose and it will write way more code than it needs to. In this case, cloud code will write the minimum amount of code that it needs to in order to make the tests pass. And now on the left side here, you can see that it's starting to actually finish up those tests on the Python file as well. So that's great. I'm going to go ahead and approve all of that there too. And you can see here how the approach is the exact same. It doesn't matter whether you're using a strict language Java or a more loosely typed language Python. You can use this method regardless of the programming language. And indeed here you can see that the Python tests are failing as well which is actually expected. Now I'm going to go ahead and give cloud code the time that it needs to actually write the implementation code. And then we'll have a look at whether the tests will pass.

[09:02] So on the bottom right you can see after a while cloud code has finished the implementation and now when running all of the tests you can see that all the tests are actually passing which is perfect. And now you can actually see here on the left in our change log that we actually have modifications in the actual root application. So for example, we now have a new big decimal buyout price. And then if we go into the auction service, you can actually see that if the buyout price is included, we do a couple of validations which all have to do with making sure that these tests that it was creating earlier can actually pass. For example, there are tests here fail when buyout price is less than or equal to starting price, which is a great test case, right? Because we want to make sure that the buyer price has to be more than the starting price. It doesn't make sense for the auction system otherwise. So, you can see here how it actually works very well. Now, let's go ahead and see how far ahead it is with the Python implementation. And you can see that it's running all the tests, but there are some issues here. It seems decimal places is not valid for Padantics decimal field. Now, it's interesting that it actually oneshot all the Java unit tests, but it's having some trouble with Python. And that has to do with the fact that Java is a much more strictly typed language, which is also something that is really beneficial for an AI coding mechanism. Because if you look here on the bottom right, you can actually compile the code as well with a language Java, which gives you a lot of guarantees on the I guess baseline quality of the code. Just because code is compiling doesn't mean that the code is perfect but it's definitely a step forward and you know that the code is at least meeting some kind of minimum requirement there right so of course if we try and run clean compile it will actually work because claude code was able to oneshot the Java implementation here whereas here on the Python side of things finally it did actually manage to implement the test suite correctly but it's actually a relatively simple feature and you can see here already how the behavior drifts between these two different programming languages. And that's another great learning point for you from this video. You should pick the language that you're the most comfortable with, but it can be beneficial to learn a more strict typed language Java or C. You can also implement types in a programming language Python, but it's still not really the same as a language that can compile in a real way a Java application.

## Frontend Implementation and Real-World Testing

[11:21] Anyway, I digress. We now have code that runs on the back end of both the Java application and the Python one, which is great. But I'm sure that you want to see some proof of this, some actual proof in the web application instead of it just being in the back ends. So let's go ahead and implement a change in our HTML page so we can actually interact with this new feature. What I'm going to be doing is I'm going to go to my files here and then I'm going to go ahead and drag in index.html HTML and I'm going to do that inside of the Java chat session that I have because the Java implementation is strictly typed. So I trust this a little bit more compared to the Python implementation since I have the luxury to choose anyway. And I'm going to say the following. This is our web page to interact with the back end. In fact, we interact with both a Java and Python back end with the same implementation. Given your latest Java edition, rework the HTML/JavaScript to include the ability to handle the buyout price. The sample auctions that the front end calls should include a buyout price and this price should of course be displayed in the front end. Here we go. This is what I want to do now. I wanted to rework that HTML file. So while cloud code is working on this implementation, I just wanted to let you know that these kinds of real AI coding strategies is what I focus on in my AI native engineer community. And in this community, you can learn how to accelerate yourself with AI regardless of whether you are working on your career or a business. So you can check out the community in the link in the description below. Otherwise, I'll see you in just a second and we'll check out how this has been implemented in our front end.

[13:14] So it seems it's done with the front end implementation. It wants to test the front end itself, but I'm just going to go ahead and exit out of the session because we're going to do that manually, right? So in our application, I can now go ahead and create a new sample auction. And then you will see that we actually have a buyout price set of $150. So I can actually just create an initial bid of 55 bucks which will work just fine. And then now I can actually create a buyout price bid of 155bucks. So I'm going to go ahead and place a bit here. And then actually something seems to go wrong. So what seems to happen here is that I place a bid and the auction is closed off. But the thing is my front end doesn't really know that that is a possibility. my front end continuously tries to fetch the latest auction and it doesn't really have a way of knowing that the auction was actually closed off because our front end doesn't actually have any logic for when a buyout price is reached. And this actually shows you why test-driven development is so important. We did not do test-driven development for our front end. So our front end does sort of work now, but it's already running into issues. And that is the reality of AI coding without a proper framework test-driven development. So what I have to do now is now I have to go back into claude and actually just communicate that this issue exists and then let's see if we can fix it. So I can for example say here the front end does not know how to deal with a bid that's placed that actually buys out the item because the front end continuously refreshes the auction. I actually get an ID error. And you can see here that now I have to go back to Claude and try to fix the error. If I had actually done test-driven development for my front end from the very beginning, I probably could have oneshot that implementation as well. This shows you the reality of AI coding. Other content would probably not show you this and just act everything is working. But this is the truth that you see here on this channel. You have to use the right coding methodology to actually get success out of AI coding. Looks we're done. Let's go back into our front end. Give it a full refresh just to make sure. We're going to go ahead and create a new sample auction. And then I'm just going to go ahead and buy that out straight away with 500 bucks. Going to go ahead and place a bid. And there you go. Now we can actually see that the front end is able to deal with the new buying out logic.

## Conclusion: The Power of Proper AI Coding Methodology

[15:31] And this just shows you how powerful using the right methodologies can be for AI coding. So I hope that from this video you've learned that using the right methodology to do AI coding can give you so many amazing real results. If you want to escape the trap of vibe coding and actually get productive with AI as an engineer, you should definitely check out my AI native engineering community in the link in the description below. And I hope to see you there.

# 구성
---
