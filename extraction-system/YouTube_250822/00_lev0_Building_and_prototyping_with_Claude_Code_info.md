# 속성
---
process_status: true
source: https://youtu.be/JdT78t1Offo?si=Xw070goEEbsWz1EW
source_type: youtube
source_language: korean
structure_type: standalone
content_processing: unified
created_at: 2025-08-22T16:01:06.588536

# 추출
---
## 핵심 내용
태수야, 이 내용을 보면 Claude Code는 개발자들이 자신의 필요에 의해 직접 프로토타핑하고 빠르게 기능을 추가하는 문화로 발전하고 있어. 특히 '멀티-클로딩'이라고 해서 개발자들이 여러 개의 Claude 세션을 동시에 돌리면서 각각 다른 작업을 시키는 패턴이 예상보다 훨씬 일반적이 되었고, CLAUDE.md 파일을 통한 커스터마이징과 SDK를 활용한 전문 에이전트 구축이 핵심적인 활용 방식으로 자리잡고 있다는 게 인상적이야. 결국 명확한 소통이 가장 중요한 성공 요소라는 점도 놓치면 안 될 부분이고.

## 상세 핵심 내용
태수야, 이 내용을 보면 Claude Code의 개발 문화가 정말 흥미로워. 팀이 "dogfooding"을 극도로 활용하는데, 문서를 쓰는 대신 바로 프로토타입을 만들어서 자신들이 직접 사용해보고 반응이 좋으면 바로 출시하는 방식이야. 이게 가능한 이유는 Claude Code로 기능을 프로토타이핑하는 게 너무 빠르고 쉽기 때문이지.

"멀티-클로딩"이라는 예상치 못한 사용 패턴이 정말 인상적이야. 개발자들이 6개의 Claude 세션을 동시에 돌리면서, 하나는 질문만 하고 코드는 건드리지 않게 하고, 다른 하나는 실제 코드 편집을 담당하게 하는 식으로 역할을 분담하는 거지. 이게 단순히 파워유저만의 패턴이 아니라 일반적인 사용법이 된 거야.

CLAUDE.md 파일의 중요성도 눈에 띄어. 코드 아키텍처, 주의사항, 모범 사례를 여기에 투자하면 출력 품질이 극적으로 향상된다는 거야. 커스텀 슬래시 명령어나 훅 기능도 마찬가지고.

Claude Code SDK는 정말 게임 체인저 같아. 1년 동안 완벽하게 다듬은 하네스를 제공해서 개발자들이 복잡한 기반 작업 없이 바로 시스템 프롬프트와 핵심 기능에만 집중할 수 있게 해주는 거지. 보안 에이전트, 사고 대응 에이전트, 심지어 법무나 컴플라이언스 에이전트까지 만들어지고 있어.

결국 핵심은 명확한 소통이야. 마법 같은 도구가 아니라 명확하게 목적, 평가 기준, 제약사항을 전달해야 제대로 작동한다는 거지. 이상한 결과가 나오면 Claude에게 직접 물어보라는 조언도 실용적이고.

## 상세 내용
태수, 이 인터뷰에서 Claude Code의 핵심적인 세부사항들을 정리해보면 다음과 같은 중요한 내용들이 나와 있어.

개발팀의 문화와 프로세스 측면에서 보면, Claude Code 팀은 제품 중심적 사고를 가진 엔지니어들로 구성되어 있고, 대부분의 기능들이 개발자들이 "이런 기능이 있었으면 좋겠다"고 생각해서 직접 만드는 방식으로 탄생한다는 점이 흥미로워. 전통적인 문서 작성 프로세스 대신, Claude Code를 사용해서 기능을 프로토타이핑하는 것이 워낙 빠르기 때문에 대부분의 개발자들이 바로 구현부터 시작해서 내부적으로 테스트해보고, 반응이 좋으면 출시하는 방식을 채택하고 있어. 여기서 "Ants"라고 부르는 것은 Anthropic 직원들을 말하는 것 같고, 이런 강력한 도그푸딩 문화는 의도적으로 만든 것이라고 해.

제품 아키텍처 관점에서는 슬래시 커맨드 같은 기본 요소들이 잘 구축되어 있어서 새로운 기능을 추가하기가 상당히 쉽다는 점을 강조하고 있어. 특히 hooks 기능의 경우, 개발자들이 터미널에 익숙하기 때문에 새로운 기능을 도입하기가 수월하고, 결국 hook은 스크립트일 뿐이라서 특별한 지식 없이도 Claude Code를 커스터마이징할 수 있다는 장점이 있어.

사용자 성장과 채택 패턴에서 정말 흥미로운 부분이 나오는데, NPM 설치 후 별다른 설정 없이 바로 작동한다는 것이 핵심적인 장점이야. 작은 회사와 큰 회사 사이에 사용 패턴의 차이가 뚜렷하게 나타나는데, 작은 회사의 엔지니어들은 "auto-accept mode"를 사용해서 Claude가 각각의 편집에 대한 승인 없이 자율적으로 작업하도록 하는 경향이 있어. 그리고 여기서 정말 놀라운 것은 "multi-Clauding"이라는 현상인데, 개발자들이 동시에 6개의 Claude 세션을 열어두고 작업한다는 거야. 각각이 다른 브랜치나 다른 Git 저장소 복사본에서 작업하면서, 하나가 멈추면 다른 것으로 넘어가서 계속 작업을 진행시키는 방식이지.

반대로 대기업에서는 "plan mode"를 선호하는데, 이것은 Claude Code가 코드베이스를 탐색하고 아키텍처를 이해해서 실제 작업에 뛰어들기 전에 엔지니어링 계획을 세우는 기능이야. 더 어렵고 복잡한 변경사항에 대해서는 이런 접근법이 매우 유용하다고 해.

예상치 못한 사용 패턴들도 상당히 흥미로운데, multi-Clauding이 파워 유저들만의 기능이 아니라 실제로 많은 사람들이 사용하는 일반적인 패턴이 되었다는 점이야. 예를 들어, 하나는 질문만 하고 코드 편집은 하지 않는 Claude 인스턴스를 두고, 다른 하나는 실제로 코드를 편집하는 용도로 사용해서 서로 충돌하지 않게 하는 방식을 쓴다고 해. 또한 보안 에이전트, 인시던트 대응 에이전트 같은 특수 목적의 에이전트들을 만드는 것도 흔한 패턴이 되었어.

커스터마이징 방법으로는 CLAUDE.md 파일에 많은 투자를 하는 것이 가장 일반적인 방법이라고 해. 이 파일은 Claude Code에게 코드 아키텍처, 코드베이스의 함정들, 베스트 프랙티스에 대해 알려주는 최적의 장소이고, 여기에 투자하면 출력 품질이 극적으로 향상된다고 해. 다른 방법으로는 커스텀 슬래시 커맨드를 추가하는 것과 커스텀 hooks를 추가하는 것이 있어. 예를 들어 Claude Code가 커밋하기 전에 린터를 실행하도록 하거나, 작업이 끝날 때마다 특정 작업을 수행하도록 하는 것들이지.

Claude Code SDK에 대해서는 일반적인 에이전트를 구축하는 훌륭한 방법이라고 소개하고 있어. 핵심 구성 요소들에 모두 접근할 수 있고, 커스텀 도구를 가져올 수 있으며, 사용자 턴 처리와 실행을 담당해주고, API 에러가 있을 때 백오프 처리도 해주고, 적극적인 프롬프트 캐싱으로 성능도 보장해준다고 해. 코딩 외에도 법률 에이전트, 컴플라이언스 에이전트까지 프로토타이핑하는 사례들이 나오고 있다는 것이 인상적이야.

SDK의 미래에 대해서는 극도로 커스터마이징 가능하게 만들겠다는 계획을 밝히고 있어. 시스템 프롬프트나 도구들을 자신만의 구현으로 교체할 수 있고, 필요한 기능만 골라서 사용할 수 있도록 하겠다는 거지. 예를 들어 할일 목록 기능이 필요하면 그것을 사용하고, 필요 없으면 쉽게 삭제할 수 있고, 에이전트가 메모리를 업데이트해야 한다면 해당 도구를 추가할 수 있다는 식이야.

베스트 프랙티스와 소통 팁에서는 명확한 의사소통이 가장 중요하다고 강조하고 있어. 작업의 목적이 무엇인지, 작업 결과를 어떻게 평가할 것인지, 디자인 시스템의 제약사항이 무엇인지를 명확히 표현해야 한다는 거야. 마법 같은 도구가 아니라, 결국 명확히 의사소통했을 때 Claude Code가 작업을 수행하거나 왜 못하는지 이유를 알려줄 수 있다는 관점이야.

그리고 만약 Claude Code가 이상한 일을 했다면, 왜 그랬는지 직접 물어볼 수 있다는 점도 유용한 팁이야. Claude가 어떤 파일에서 무언가를 읽고 특정 인상을 받았다고 설명할 수도 있고, 이런 식으로 Claude와의 대화를 디버깅 도구로 활용할 수 있다는 거지.

전체적으로 보면 Claude Code는 단순한 코딩 도구를 넘어서 개발자들의 워크플로우를 근본적으로 바꾸고 있는 플랫폼으로 발전하고 있다는 느낌이야. 특히 multi-Clauding 같은 예상치 못한 사용 패턴들이 나타나고, 이것이 다시 제품 개발에 피드백되는 선순환 구조가 인상적이고, 개발팀의 도그푸딩 문화가 이런 혁신을 가능하게 하는 핵심 요소인 것 같아.

## 주요 화제
- 개발팀 문화와 빠른 프로토타이핑: Claude Code 팀이 문서 작성 대신 직접 기능을 프로토타입하여 내부 테스트를 거쳐 출시하는 애자일한 개발 문화
- 멀티 클로딩과 사용자 맞춤화: 개발자들이 동시에 여러 Claude 세션을 실행하며 각각을 다른 목적으로 특화시키는 예상치 못한 사용 패턴
- CLAUDE.md 파일과 커스터마이징: 코드베이스 아키텍처, 모범 사례, 주의사항을 기록하는 CLAUDE.md 파일 투자가 출력 품질을 극적으로 향상시키는 방법
- Claude Code SDK를 통한 에이전트 개발: 범용 에이전트 구축을 위한 SDK로 SRE, 보안, 법률, 컴플라이언스 에이전트까지 다양한 분야에서 활용 가능
- 명확한 소통의 중요성: Claude Code와 효과적으로 작업하기 위해서는 작업 목적, 평가 기준, 제약사항을 명확히 전달하는 것이 핵심

## 부차 화제
- 멀티클로딩 전략: 개발자들이 6개의 Claude 세션을 동시에 실행하며 각각 다른 작업이나 저장소 복사본에서 작업하는 사용 패턴
- 회사 규모별 사용 차이: 소규모 회사는 auto-accept 모드로 자율적 실행을 선호하고, 대기업은 plan 모드를 통한 사전 계획 수립을 중시
- 특화 에이전트 개발: 보안 에이전트, 인시던트 대응 에이전트, 법무 에이전트, 컴플라이언스 에이전트 등 도메인별 전문화
- CLAUDE.md 파일의 중요성: 코드베이스 아키텍처, 주의사항, 모범 사례를 문서화하여 출력 품질을 극적으로 향상시키는 핵심 요소
- 커뮤니케이션 기반 디버깅: Claude에게 직접 "왜 그렇게 생각했는지" 질문하여 추론 과정을 파악하고 문제를 해결하는 대화형 접근법

# 내용
---
# Building and prototyping with Claude Code

## Development Team Culture and Process

[00:00] These developers tend to run multiple Claude sessions at once, and they've started calling So you might see sessions where people have six Claudes open on their computer at the same time.

[00:16] Hey, I'm Alex. I lead Claude Relations here at Anthropic. Today we're gonna be and I'm joined by my colleague Cat.

[00:22] Hey, I'm Cat. I'm the product manager for Claude Code.

[00:26] Cat, I wanna kick this the insane rate of It feels every time I open it up in my terminal, there's a new product or a new feature, something for me to use. Can you walk me through of the team going from an idea to actually shipping

[00:44] Yeah, so the Claude Code team is full of very product-minded engineers and a lot of these features It's you're a developer and you really wish you had this thing, and then you build it for yourself. And the way that our process works is instead of writing a doc, it's so fast to use Claude Code to prototype a feature that most of the time people and then they ship it And if the reception is really positive, then that's a very strong signal that the external world will it too. And that's actually our bar And then of course there's always features that aren't exactly right that need some tweaking. And if we feel okay, that much, then we just go and we say okay, what else could we change about this?

[01:31] And when we say "Ants," do

[01:33] Yes, yes. That's really fascinating. I've never seen a product have as strong of "dogfooding" Do you think that's or that just naturally arise from the product itself?

[01:48] It is quite intentional, and it's also a really important reason why Claude Code works so well. Because it's so easy to prototype we do push people to but it's hard to reason about exactly how a because developers are so heterogeneous in their workflows. So oftentimes, even if you wanna do something, even if you theoretically know that you wanna build an IDE integration, there's still a range you could go about it. And often prototyping is the only way that you can really feel how the product will actually be in your workflow. So yeah, it's through the that we decide what version of

## Product Architecture and Feature Development

[02:35] I see. And there's something about the, almost the flexibility but also the constraints that allows for easy addition which I've because we have the primitives built out of slash commands and things, it's easy to add another

[02:53] Yeah, it's totally And because so many developers are familiar with the terminal, it makes new feature because for example, for which lets you add a bit of determinism around Claude Code events, because every developer and really at the end of the day, all a hook is, is a script. And so you don't need to to customize Claude Code. You write this script that and then you add it to one and now you have some determinism.

[03:35] We're really trying to meet customers or developers where they are with this tool.

## User Growth and Adoption Patterns

[03:41] Switching gears slightly, so alongside this insane rate of shipping is also the insane growth with developers everywhere. Can you walk me through to be on this rocket ship and how are we seeing various developers, whether it's at startups or individuals or at even large enterprises, use Claude?

[04:01] So one of the magical is that the onboarding is so smooth. After you do the NPM install, Claude Code just without any configuration. And this is true whether through to if you're an I think this is the Because it has access to and files that you have, you have this very clear mental model for what Claude Code is capable of.

[04:33] We do see different use between smaller companies and larger ones. We find that engineers tend to run Claude more autonomously using things "auto-accept mode," which lets Claude make edits by itself without approval of each one. We also find that these developers tend to run multiple and they've started calling So you might see sessions where people have six Claudes open on their computer at the same time. Maybe each of them are in or in a different copy of the Git repo, and they're just Whenever anyone stops they'll jump in there and then send it off and let it continue running.

[05:20] And on the other end of the spectrum for larger companies, we find that engineers really So "plan mode" is a way for developers to tell Claude Code to take a second, explore the code base, understand the architecture, and create an engineering plan before actually jumping And so we find that this is really useful for harder tasks and more complex changes.

## Unexpected Usage Patterns and Customization

[05:47] So going back to multi-Clauding just 'cause I think that's I'm sure we imagined folks wanting to do things that, but it was somewhat surprising. Is there other things oh wow, this is a usage pattern that we really did not expect that have popped up organically and we've shifted our

[06:10] Yeah, I think multi-Clauding because this is something that we thought was just a power user feature that a few people would wanna do. But in fact this is in which people use Claude. And so for example, they might have one Claude instance where they only ask questions and this one doesn't edit code. That way they can have in the same repo that does edit code and these two don't Other things that we've seen are people really to handle specialized tasks.

[06:44] So we've seen people build security agents, incident response agents. And what that made us realize is that integrations are so important for making sure Claude Code works well. And so we've been encouraging people to spend more time to hey, these are the CLI or to set up remote MCP servers to get access to logs and

[07:12] When these engineers are does that mean they're creating sub-agents or are they creating markdown files CLAUDE.md files? How exactly are they creating these different types of agents?

[07:25] Yeah, I think the most common ways that we've seen people customize is by investing a lot So the CLAUDE.md file is And so it's the best place for you to tell Claude Code about how the code is architected, any gotchas in the code base, any best practices. And investing in CLAUDE.md we've heard dramatically improves the quality of the output.

[07:55] The other way that people is by adding custom slash commands. So if there's a prompt you can add that into and you could also check these in so that you share them And then you can also add custom hooks. So if for example, you want Claude Code to run lints before it makes a commit, this is something that's great for a hook. If you want Claude Code to every time it's done working, this is actually the original inspiration for making hooks. And so these are all customizations that people are building today.

## Claude Code SDK and Agent Development

[08:32] Tell me more about, what is the Claude Code SDK?

[08:35] The Claude Code SDK is a great way to build general agents. The Claude Code SDK gives you access to all of the core building including you can bring you can bring your own custom tools, and what you get from the where we handle the user turns and we handle executing You get to use our so that you don't need to And we also handle interacting So we make sure that we have backoff if there's any API errors. We very aggressively prompt cache to make sure that your If you are prototyping if you use the Claude Code SDK, you can get up and running with something pretty powerful within

[09:29] We've been seeing people build We open-sourced our Claude which is completely built on the SDK, and we've seen people build SRE agents, incident response agents. And these are just Outside of coding, we've seen people prototype legal agents, compliance agents. This is very much intended for all your agent needs.

[09:57] The SDK is pretty amazing to me. I feel we've lived in for so long. And now we're moving to almost where we're gonna handle all the nitty-gritty of Where is the SDK headed? What's next there?

[10:17] We're really excited about the SDK as the next way to unlock We're investing very heavily in making sure the SDK is best-in-class for building agents. So all of the nice features that you have in Claude Code will be available out and you can pick and choose So for example, if you want your agent to be able to have a to-do list, great. You have the to-do list If you don't want that, it's really easy to just delete that tool. If your agent needs to to update its memory, you And if you decide, okay, or it'll edit files in a different way, you can just bring your

[11:05] Okay, so it's extremely customizable, basically general purpose in the sense that you could swap out the system prompt or the tools for your own implementations. And they just nicely slot in to whatever thing you're building for, whether it's in an entirely Right?

[11:20] I'm really excited to see what I think especially for people who are just trying to prototype an agent, this is I think to get started. We really spent almost a year perfecting this harness, and this is the same harness And so if you want to just jump right into the specific and you wanna jump right into just working on the system prompt to share context about the and you don't wanna deal this is the best way to circumvent all the general purpose harness and just add your

## Best Practices and Communication Tips

[12:05] Hmm, all right. Well, you heard it here. You gotta go build on the SDK. Before we wrap up here, I'm really curious to hear your own tips for how you use Claude Code, and what are some best practices we can share with developers?

[12:17] When you work with Claude I think the most important thing is to clearly communicate what I think a lot of people is this magical It's very much about, okay, did I clearly articulate what my purpose with this task is, how I'm evaluating the output of the task, any constraints in the design system. And I think usually when you can clearly Claude Code will either be able to do them or just tell you that I'm not able to do because A, B, C and do you wanna try

[13:06] So it's all about the communication just as if you're working

[13:10] Yeah, totally. And another thing is if you notice that Claude Code did something weird, you could actually just ask And it might tell you something oh, okay, there was something or I read something in this file that gave me this impression. And then that way you can actually use talking to Claude as a way to debug. It doesn't always work, but I think it's definitely worth trying. And it's a common

[13:39] You use Claude Code I love it. The same way that if they say something you might feel, "Oh, interesting. what gave you that impression? Or why did you think this?" And I think you can do

[13:54] That's fascinating. Well, Cat, this has been great. Really, we appreciate the time. Thank you.

# Building and prototyping with Claude Code

## Development Team Culture and Process

[00:00] These developers tend to run multiple Claude sessions at once, and they've started calling So you might see sessions where people have six Claudes open on their computer at the same time.

[00:16] Hey, I'm Alex. I lead Claude Relations here at Anthropic. Today we're gonna be and I'm joined by my colleague Cat.

[00:22] Hey, I'm Cat. I'm the product manager for Claude Code.

[00:26] Cat, I wanna kick this the insane rate of It feels every time I open it up in my terminal, there's a new product or a new feature, something for me to use. Can you walk me through of the team going from an idea to actually shipping

[00:44] Yeah, so the Claude Code team is full of very product-minded engineers and a lot of these features It's you're a developer and you really wish you had this thing, and then you build it for yourself. And the way that our process works is instead of writing a doc, it's so fast to use Claude Code to prototype a feature that most of the time people and then they ship it And if the reception is really positive, then that's a very strong signal that the external world will it too. And that's actually our bar And then of course there's always features that aren't exactly right that need some tweaking. And if we feel okay, that much, then we just go and we say okay, what else could we change about this?

[01:31] And when we say "Ants," do

[01:33] Yes, yes. That's really fascinating. I've never seen a product have as strong of "dogfooding" Do you think that's or that just naturally arise from the product itself?

[01:48] It is quite intentional, and it's also a really important reason why Claude Code works so well. Because it's so easy to prototype we do push people to but it's hard to reason about exactly how a because developers are so heterogeneous in their workflows. So oftentimes, even if you wanna do something, even if you theoretically know that you wanna build an IDE integration, there's still a range you could go about it. And often prototyping is the only way that you can really feel how the product will actually be in your workflow. So yeah, it's through the that we decide what version of

## Product Architecture and Feature Development

[02:35] I see. And there's something about the, almost the flexibility but also the constraints that allows for easy addition which I've because we have the primitives built out of slash commands and things, it's easy to add another

[02:53] Yeah, it's totally And because so many developers are familiar with the terminal, it makes new feature because for example, for which lets you add a bit of determinism around Claude Code events, because every developer and really at the end of the day, all a hook is, is a script. And so you don't need to to customize Claude Code. You write this script that and then you add it to one and now you have some determinism.

[03:35] We're really trying to meet customers or developers where they are with this tool.

## User Growth and Adoption Patterns

[03:41] Switching gears slightly, so alongside this insane rate of shipping is also the insane growth with developers everywhere. Can you walk me through to be on this rocket ship and how are we seeing various developers, whether it's at startups or individuals or at even large enterprises, use Claude?

[04:01] So one of the magical is that the onboarding is so smooth. After you do the NPM install, Claude Code just without any configuration. And this is true whether through to if you're an I think this is the Because it has access to and files that you have, you have this very clear mental model for what Claude Code is capable of.

[04:33] We do see different use between smaller companies and larger ones. We find that engineers tend to run Claude more autonomously using things "auto-accept mode," which lets Claude make edits by itself without approval of each one. We also find that these developers tend to run multiple and they've started calling So you might see sessions where people have six Claudes open on their computer at the same time. Maybe each of them are in or in a different copy of the Git repo, and they're just Whenever anyone stops they'll jump in there and then send it off and let it continue running.

[05:20] And on the other end of the spectrum for larger companies, we find that engineers really So "plan mode" is a way for developers to tell Claude Code to take a second, explore the code base, understand the architecture, and create an engineering plan before actually jumping And so we find that this is really useful for harder tasks and more complex changes.

## Unexpected Usage Patterns and Customization

[05:47] So going back to multi-Clauding just 'cause I think that's I'm sure we imagined folks wanting to do things that, but it was somewhat surprising. Is there other things oh wow, this is a usage pattern that we really did not expect that have popped up organically and we've shifted our

[06:10] Yeah, I think multi-Clauding because this is something that we thought was just a power user feature that a few people would wanna do. But in fact this is in which people use Claude. And so for example, they might have one Claude instance where they only ask questions and this one doesn't edit code. That way they can have in the same repo that does edit code and these two don't Other things that we've seen are people really to handle specialized tasks.

[06:44] So we've seen people build security agents, incident response agents. And what that made us realize is that integrations are so important for making sure Claude Code works well. And so we've been encouraging people to spend more time to hey, these are the CLI or to set up remote MCP servers to get access to logs and

[07:12] When these engineers are does that mean they're creating sub-agents or are they creating markdown files CLAUDE.md files? How exactly are they creating these different types of agents?

[07:25] Yeah, I think the most common ways that we've seen people customize is by investing a lot So the CLAUDE.md file is And so it's the best place for you to tell Claude Code about how the code is architected, any gotchas in the code base, any best practices. And investing in CLAUDE.md we've heard dramatically improves the quality of the output.

[07:55] The other way that people is by adding custom slash commands. So if there's a prompt you can add that into and you could also check these in so that you share them And then you can also add custom hooks. So if for example, you want Claude Code to run lints before it makes a commit, this is something that's great for a hook. If you want Claude Code to every time it's done working, this is actually the original inspiration for making hooks. And so these are all customizations that people are building today.

## Claude Code SDK and Agent Development

[08:32] Tell me more about, what is the Claude Code SDK?

[08:35] The Claude Code SDK is a great way to build general agents. The Claude Code SDK gives you access to all of the core building including you can bring you can bring your own custom tools, and what you get from the where we handle the user turns and we handle executing You get to use our so that you don't need to And we also handle interacting So we make sure that we have backoff if there's any API errors. We very aggressively prompt cache to make sure that your If you are prototyping if you use the Claude Code SDK, you can get up and running with something pretty powerful within

[09:29] We've been seeing people build We open-sourced our Claude which is completely built on the SDK, and we've seen people build SRE agents, incident response agents. And these are just Outside of coding, we've seen people prototype legal agents, compliance agents. This is very much intended for all your agent needs.

[09:57] The SDK is pretty amazing to me. I feel we've lived in for so long. And now we're moving to almost where we're gonna handle all the nitty-gritty of Where is the SDK headed? What's next there?

[10:17] We're really excited about the SDK as the next way to unlock We're investing very heavily in making sure the SDK is best-in-class for building agents. So all of the nice features that you have in Claude Code will be available out and you can pick and choose So for example, if you want your agent to be able to have a to-do list, great. You have the to-do list If you don't want that, it's really easy to just delete that tool. If your agent needs to to update its memory, you And if you decide, okay, or it'll edit files in a different way, you can just bring your

[11:05] Okay, so it's extremely customizable, basically general purpose in the sense that you could swap out the system prompt or the tools for your own implementations. And they just nicely slot in to whatever thing you're building for, whether it's in an entirely Right?

[11:20] I'm really excited to see what I think especially for people who are just trying to prototype an agent, this is I think to get started. We really spent almost a year perfecting this harness, and this is the same harness And so if you want to just jump right into the specific and you wanna jump right into just working on the system prompt to share context about the and you don't wanna deal this is the best way to circumvent all the general purpose harness and just add your

## Best Practices and Communication Tips

[12:05] Hmm, all right. Well, you heard it here. You gotta go build on the SDK. Before we wrap up here, I'm really curious to hear your own tips for how you use Claude Code, and what are some best practices we can share with developers?

[12:17] When you work with Claude I think the most important thing is to clearly communicate what I think a lot of people is this magical It's very much about, okay, did I clearly articulate what my purpose with this task is, how I'm evaluating the output of the task, any constraints in the design system. And I think usually when you can clearly Claude Code will either be able to do them or just tell you that I'm not able to do because A, B, C and do you wanna try

[13:06] So it's all about the communication just as if you're working

[13:10] Yeah, totally. And another thing is if you notice that Claude Code did something weird, you could actually just ask And it might tell you something oh, okay, there was something or I read something in this file that gave me this impression. And then that way you can actually use talking to Claude as a way to debug. It doesn't always work, but I think it's definitely worth trying. And it's a common

[13:39] You use Claude Code I love it. The same way that if they say something you might feel, "Oh, interesting. what gave you that impression? Or why did you think this?" And I think you can do

[13:54] That's fascinating. Well, Cat, this has been great. Really, we appreciate the time. Thank you.

# Building and prototyping with Claude Code

## Development Team Culture and Process

[00:00] These developers tend to run multiple Claude sessions at once, and they've started calling So you might see sessions where people have six Claudes open on their computer at the same time.

[00:16] Hey, I'm Alex. I lead Claude Relations here at Anthropic. Today we're gonna be and I'm joined by my colleague Cat.

[00:22] Hey, I'm Cat. I'm the product manager for Claude Code.

[00:26] Cat, I wanna kick this the insane rate of It feels every time I open it up in my terminal, there's a new product or a new feature, something for me to use. Can you walk me through of the team going from an idea to actually shipping

[00:44] Yeah, so the Claude Code team is full of very product-minded engineers and a lot of these features It's you're a developer and you really wish you had this thing, and then you build it for yourself. And the way that our process works is instead of writing a doc, it's so fast to use Claude Code to prototype a feature that most of the time people and then they ship it And if the reception is really positive, then that's a very strong signal that the external world will it too. And that's actually our bar And then of course there's always features that aren't exactly right that need some tweaking. And if we feel okay, that much, then we just go and we say okay, what else could we change about this?

[01:31] And when we say "Ants," do

[01:33] Yes, yes. That's really fascinating. I've never seen a product have as strong of "dogfooding" Do you think that's or that just naturally arise from the product itself?

[01:48] It is quite intentional, and it's also a really important reason why Claude Code works so well. Because it's so easy to prototype we do push people to but it's hard to reason about exactly how a because developers are so heterogeneous in their workflows. So oftentimes, even if you wanna do something, even if you theoretically know that you wanna build an IDE integration, there's still a range you could go about it. And often prototyping is the only way that you can really feel how the product will actually be in your workflow. So yeah, it's through the that we decide what version of

## Product Architecture and Feature Development

[02:35] I see. And there's something about the, almost the flexibility but also the constraints that allows for easy addition which I've because we have the primitives built out of slash commands and things, it's easy to add another

[02:53] Yeah, it's totally And because so many developers are familiar with the terminal, it makes new feature because for example, for which lets you add a bit of determinism around Claude Code events, because every developer and really at the end of the day, all a hook is, is a script. And so you don't need to to customize Claude Code. You write this script that and then you add it to one and now you have some determinism.

[03:35] We're really trying to meet customers or developers where they are with this tool.

## User Growth and Adoption Patterns

[03:41] Switching gears slightly, so alongside this insane rate of shipping is also the insane growth with developers everywhere. Can you walk me through to be on this rocket ship and how are we seeing various developers, whether it's at startups or individuals or at even large enterprises, use Claude?

[04:01] So one of the magical is that the onboarding is so smooth. After you do the NPM install, Claude Code just without any configuration. And this is true whether through to if you're an I think this is the Because it has access to and files that you have, you have this very clear mental model for what Claude Code is capable of.

[04:33] We do see different use between smaller companies and larger ones. We find that engineers tend to run Claude more autonomously using things "auto-accept mode," which lets Claude make edits by itself without approval of each one. We also find that these developers tend to run multiple and they've started calling So you might see sessions where people have six Claudes open on their computer at the same time. Maybe each of them are in or in a different copy of the Git repo, and they're just Whenever anyone stops they'll jump in there and then send it off and let it continue running.

[05:20] And on the other end of the spectrum for larger companies, we find that engineers really So "plan mode" is a way for developers to tell Claude Code to take a second, explore the code base, understand the architecture, and create an engineering plan before actually jumping And so we find that this is really useful for harder tasks and more complex changes.

## Unexpected Usage Patterns and Customization

[05:47] So going back to multi-Clauding just 'cause I think that's I'm sure we imagined folks wanting to do things that, but it was somewhat surprising. Is there other things oh wow, this is a usage pattern that we really did not expect that have popped up organically and we've shifted our

[06:10] Yeah, I think multi-Clauding because this is something that we thought was just a power user feature that a few people would wanna do. But in fact this is in which people use Claude. And so for example, they might have one Claude instance where they only ask questions and this one doesn't edit code. That way they can have in the same repo that does edit code and these two don't Other things that we've seen are people really to handle specialized tasks.

[06:44] So we've seen people build security agents, incident response agents. And what that made us realize is that integrations are so important for making sure Claude Code works well. And so we've been encouraging people to spend more time to hey, these are the CLI or to set up remote MCP servers to get access to logs and

[07:12] When these engineers are does that mean they're creating sub-agents or are they creating markdown files CLAUDE.md files? How exactly are they creating these different types of agents?

[07:25] Yeah, I think the most common ways that we've seen people customize is by investing a lot So the CLAUDE.md file is And so it's the best place for you to tell Claude Code about how the code is architected, any gotchas in the code base, any best practices. And investing in CLAUDE.md we've heard dramatically improves the quality of the output.

[07:55] The other way that people is by adding custom slash commands. So if there's a prompt you can add that into and you could also check these in so that you share them And then you can also add custom hooks. So if for example, you want Claude Code to run lints before it makes a commit, this is something that's great for a hook. If you want Claude Code to every time it's done working, this is actually the original inspiration for making hooks. And so these are all customizations that people are building today.

## Claude Code SDK and Agent Development

[08:32] Tell me more about, what is the Claude Code SDK?

[08:35] The Claude Code SDK is a great way to build general agents. The Claude Code SDK gives you access to all of the core building including you can bring you can bring your own custom tools, and what you get from the where we handle the user turns and we handle executing You get to use our so that you don't need to And we also handle interacting So we make sure that we have backoff if there's any API errors. We very aggressively prompt cache to make sure that your If you are prototyping if you use the Claude Code SDK, you can get up and running with something pretty powerful within

[09:29] We've been seeing people build We open-sourced our Claude which is completely built on the SDK, and we've seen people build SRE agents, incident response agents. And these are just Outside of coding, we've seen people prototype legal agents, compliance agents. This is very much intended for all your agent needs.

[09:57] The SDK is pretty amazing to me. I feel we've lived in for so long. And now we're moving to almost where we're gonna handle all the nitty-gritty of Where is the SDK headed? What's next there?

[10:17] We're really excited about the SDK as the next way to unlock We're investing very heavily in making sure the SDK is best-in-class for building agents. So all of the nice features that you have in Claude Code will be available out and you can pick and choose So for example, if you want your agent to be able to have a to-do list, great. You have the to-do list If you don't want that, it's really easy to just delete that tool. If your agent needs to to update its memory, you And if you decide, okay, or it'll edit files in a different way, you can just bring your

[11:05] Okay, so it's extremely customizable, basically general purpose in the sense that you could swap out the system prompt or the tools for your own implementations. And they just nicely slot in to whatever thing you're building for, whether it's in an entirely Right?

[11:20] I'm really excited to see what I think especially for people who are just trying to prototype an agent, this is I think to get started. We really spent almost a year perfecting this harness, and this is the same harness And so if you want to just jump right into the specific and you wanna jump right into just working on the system prompt to share context about the and you don't wanna deal this is the best way to circumvent all the general purpose harness and just add your

## Best Practices and Communication Tips

[12:05] Hmm, all right. Well, you heard it here. You gotta go build on the SDK. Before we wrap up here, I'm really curious to hear your own tips for how you use Claude Code, and what are some best practices we can share with developers?

[12:17] When you work with Claude I think the most important thing is to clearly communicate what I think a lot of people is this magical It's very much about, okay, did I clearly articulate what my purpose with this task is, how I'm evaluating the output of the task, any constraints in the design system. And I think usually when you can clearly Claude Code will either be able to do them or just tell you that I'm not able to do because A, B, C and do you wanna try

[13:06] So it's all about the communication just as if you're working

[13:10] Yeah, totally. And another thing is if you notice that Claude Code did something weird, you could actually just ask And it might tell you something oh, okay, there was something or I read something in this file that gave me this impression. And then that way you can actually use talking to Claude as a way to debug. It doesn't always work, but I think it's definitely worth trying. And it's a common

[13:39] You use Claude Code I love it. The same way that if they say something you might feel, "Oh, interesting. what gave you that impression? Or why did you think this?" And I think you can do

[13:54] That's fascinating. Well, Cat, this has been great. Really, we appreciate the time. Thank you.

# Building and prototyping with Claude Code

## Development Team Culture and Process

[00:00] These developers tend to run multiple Claude sessions at once, and they've started calling So you might see sessions where people have six Claudes open on their computer at the same time.

[00:16] Hey, I'm Alex. I lead Claude Relations here at Anthropic. Today we're gonna be and I'm joined by my colleague Cat.

[00:22] Hey, I'm Cat. I'm the product manager for Claude Code.

[00:26] Cat, I wanna kick this the insane rate of It feels every time I open it up in my terminal, there's a new product or a new feature, something for me to use. Can you walk me through of the team going from an idea to actually shipping

[00:44] Yeah, so the Claude Code team is full of very product-minded engineers and a lot of these features It's you're a developer and you really wish you had this thing, and then you build it for yourself. And the way that our process works is instead of writing a doc, it's so fast to use Claude Code to prototype a feature that most of the time people and then they ship it And if the reception is really positive, then that's a very strong signal that the external world will it too. And that's actually our bar And then of course there's always features that aren't exactly right that need some tweaking. And if we feel okay, that much, then we just go and we say okay, what else could we change about this?

[01:31] And when we say "Ants," do

[01:33] Yes, yes. That's really fascinating. I've never seen a product have as strong of "dogfooding" Do you think that's or that just naturally arise from the product itself?

[01:48] It is quite intentional, and it's also a really important reason why Claude Code works so well. Because it's so easy to prototype we do push people to but it's hard to reason about exactly how a because developers are so heterogeneous in their workflows. So oftentimes, even if you wanna do something, even if you theoretically know that you wanna build an IDE integration, there's still a range you could go about it. And often prototyping is the only way that you can really feel how the product will actually be in your workflow. So yeah, it's through the that we decide what version of

## Product Architecture and Feature Development

[02:35] I see. And there's something about the, almost the flexibility but also the constraints that allows for easy addition which I've because we have the primitives built out of slash commands and things, it's easy to add another

[02:53] Yeah, it's totally And because so many developers are familiar with the terminal, it makes new feature because for example, for which lets you add a bit of determinism around Claude Code events, because every developer and really at the end of the day, all a hook is, is a script. And so you don't need to to customize Claude Code. You write this script that and then you add it to one and now you have some determinism.

[03:35] We're really trying to meet customers or developers where they are with this tool.

## User Growth and Adoption Patterns

[03:41] Switching gears slightly, so alongside this insane rate of shipping is also the insane growth with developers everywhere. Can you walk me through to be on this rocket ship and how are we seeing various developers, whether it's at startups or individuals or at even large enterprises, use Claude?

[04:01] So one of the magical is that the onboarding is so smooth. After you do the NPM install, Claude Code just without any configuration. And this is true whether through to if you're an I think this is the Because it has access to and files that you have, you have this very clear mental model for what Claude Code is capable of.

[04:33] We do see different use between smaller companies and larger ones. We find that engineers tend to run Claude more autonomously using things "auto-accept mode," which lets Claude make edits by itself without approval of each one. We also find that these developers tend to run multiple and they've started calling So you might see sessions where people have six Claudes open on their computer at the same time. Maybe each of them are in or in a different copy of the Git repo, and they're just Whenever anyone stops they'll jump in there and then send it off and let it continue running.

[05:20] And on the other end of the spectrum for larger companies, we find that engineers really So "plan mode" is a way for developers to tell Claude Code to take a second, explore the code base, understand the architecture, and create an engineering plan before actually jumping And so we find that this is really useful for harder tasks and more complex changes.

## Unexpected Usage Patterns and Customization

[05:47] So going back to multi-Clauding just 'cause I think that's I'm sure we imagined folks wanting to do things that, but it was somewhat surprising. Is there other things oh wow, this is a usage pattern that we really did not expect that have popped up organically and we've shifted our

[06:10] Yeah, I think multi-Clauding because this is something that we thought was just a power user feature that a few people would wanna do. But in fact this is in which people use Claude. And so for example, they might have one Claude instance where they only ask questions and this one doesn't edit code. That way they can have in the same repo that does edit code and these two don't Other things that we've seen are people really to handle specialized tasks.

[06:44] So we've seen people build security agents, incident response agents. And what that made us realize is that integrations are so important for making sure Claude Code works well. And so we've been encouraging people to spend more time to hey, these are the CLI or to set up remote MCP servers to get access to logs and

[07:12] When these engineers are does that mean they're creating sub-agents or are they creating markdown files CLAUDE.md files? How exactly are they creating these different types of agents?

[07:25] Yeah, I think the most common ways that we've seen people customize is by investing a lot So the CLAUDE.md file is And so it's the best place for you to tell Claude Code about how the code is architected, any gotchas in the code base, any best practices. And investing in CLAUDE.md we've heard dramatically improves the quality of the output.

[07:55] The other way that people is by adding custom slash commands. So if there's a prompt you can add that into and you could also check these in so that you share them And then you can also add custom hooks. So if for example, you want Claude Code to run lints before it makes a commit, this is something that's great for a hook. If you want Claude Code to every time it's done working, this is actually the original inspiration for making hooks. And so these are all customizations that people are building today.

## Claude Code SDK and Agent Development

[08:32] Tell me more about, what is the Claude Code SDK?

[08:35] The Claude Code SDK is a great way to build general agents. The Claude Code SDK gives you access to all of the core building including you can bring you can bring your own custom tools, and what you get from the where we handle the user turns and we handle executing You get to use our so that you don't need to And we also handle interacting So we make sure that we have backoff if there's any API errors. We very aggressively prompt cache to make sure that your If you are prototyping if you use the Claude Code SDK, you can get up and running with something pretty powerful within

[09:29] We've been seeing people build We open-sourced our Claude which is completely built on the SDK, and we've seen people build SRE agents, incident response agents. And these are just Outside of coding, we've seen people prototype legal agents, compliance agents. This is very much intended for all your agent needs.

[09:57] The SDK is pretty amazing to me. I feel we've lived in for so long. And now we're moving to almost where we're gonna handle all the nitty-gritty of Where is the SDK headed? What's next there?

[10:17] We're really excited about the SDK as the next way to unlock We're investing very heavily in making sure the SDK is best-in-class for building agents. So all of the nice features that you have in Claude Code will be available out and you can pick and choose So for example, if you want your agent to be able to have a to-do list, great. You have the to-do list If you don't want that, it's really easy to just delete that tool. If your agent needs to to update its memory, you And if you decide, okay, or it'll edit files in a different way, you can just bring your

[11:05] Okay, so it's extremely customizable, basically general purpose in the sense that you could swap out the system prompt or the tools for your own implementations. And they just nicely slot in to whatever thing you're building for, whether it's in an entirely Right?

[11:20] I'm really excited to see what I think especially for people who are just trying to prototype an agent, this is I think to get started. We really spent almost a year perfecting this harness, and this is the same harness And so if you want to just jump right into the specific and you wanna jump right into just working on the system prompt to share context about the and you don't wanna deal this is the best way to circumvent all the general purpose harness and just add your

## Best Practices and Communication Tips

[12:05] Hmm, all right. Well, you heard it here. You gotta go build on the SDK. Before we wrap up here, I'm really curious to hear your own tips for how you use Claude Code, and what are some best practices we can share with developers?

[12:17] When you work with Claude I think the most important thing is to clearly communicate what I think a lot of people is this magical It's very much about, okay, did I clearly articulate what my purpose with this task is, how I'm evaluating the output of the task, any constraints in the design system. And I think usually when you can clearly Claude Code will either be able to do them or just tell you that I'm not able to do because A, B, C and do you wanna try

[13:06] So it's all about the communication just as if you're working

[13:10] Yeah, totally. And another thing is if you notice that Claude Code did something weird, you could actually just ask And it might tell you something oh, okay, there was something or I read something in this file that gave me this impression. And then that way you can actually use talking to Claude as a way to debug. It doesn't always work, but I think it's definitely worth trying. And it's a common

[13:39] You use Claude Code I love it. The same way that if they say something you might feel, "Oh, interesting. what gave you that impression? Or why did you think this?" And I think you can do

[13:54] That's fascinating. Well, Cat, this has been great. Really, we appreciate the time. Thank you.

# 구성
---

