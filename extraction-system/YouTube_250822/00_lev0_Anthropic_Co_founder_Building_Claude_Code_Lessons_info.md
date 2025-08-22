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
Line 14: 태수야, 이 영상은 Anthropic의 Claude Code 제품 개발 과정과 사용 패턴을 다룬 내용이야. 개발팀이 자체적으로 도구를 사용하면서 필요한 기능을 바로 프로토타입하고 배포하는 "dogfooding" 방식으로 빠른 제품 개발을 하고 있고, 사용자들이 예상과 다르게 여러 Claude 세션을 동시에 돌리는 "multi-Clauding" 패턴을 보여주고 있다는 게 흥미롭네. Claude Code를 효과적으로 사용하려면 다른 개발자와 소통하듯 명확하게 목적과 제약사항을 전달하는 것이 가장 중요하다고 강조하고 있어.

## 상세 핵심 내용
Line 17: 태수야, 이 영상에서 나온 핵심 내용들을 좀 더 자세히 설명해줄게.

Line 19: 먼저 "dogfooding" 개발 방식이 정말 인상적이야. Anthropic의 Claude Code 팀은 문서 작성부터 시작하는 전통적인 방식 대신, 개발자가 필요한 기능을 직접 프로토타입으로 만들어서 팀 내부에서 써보고, 반응이 좋으면 바로 출시하는 방식을 쓰고 있어. 이게 가능한 이유는 Claude Code 자체가 워낙 빠르게 프로토타입을 만들 수 있는 도구이기 때문이지. 이런 방식으로 기능 개발 속도가 엄청나게 빨라지고, 실제 사용자 니즈를 정확히 파악할 수 있다는 장점이 있어.

Line 21: "Multi-Clauding"은 예상 밖의 사용 패턴인데, 개발자들이 하나의 컴퓨터에서 6개의 Claude 세션을 동시에 돌리는 거야. 각각 다른 용도로 사용하는데, 예를 들어 하나는 질문 전용(코드 수정 안 함), 다른 하나는 실제 코드 편집용으로 나누어서 충돌을 방지하거나, 각각 다른 브랜치나 레포지토리에서 작업하면서 하나가 멈추면 다른 걸로 바로 넘어가는 식으로 활용하고 있어.

Line 23: 사용자 규모별로도 패턴이 다른데, 작은 회사들은 "auto-accept mode"를 써서 Claude가 승인 없이 자동으로 편집하게 하는 반면, 큰 기업들은 "plan mode"를 선호해서 Claude가 먼저 코드베이스를 분석하고 엔지니어링 계획을 세운 다음 실행하도록 한다는 점도 흥미로워.

Line 25: 가장 중요한 건 Cat이 강조한 소통 방식이야. Claude Code를 마법처럼 모든 걸 알아서 해주는 도구로 생각하지 말고, 다른 개발자와 협업하듯이 목적, 평가 기준, 제약사항을 명확하게 전달해야 한다는 거지. 그리고 Claude가 이상하게 행동하면 "왜 그렇게 생각했어?"라고 물어보면서 디버깅하는 것도 유용한 팁이야.

## 상세 내용
Line 28: 태수야, 이 영상에서 정말 중요한 인사이트들이 많이 나왔는데, 냉철하게 분석해보자.

Line 30: **팀 문화와 개발 프로세스의 핵심**

Line 32: Anthropic의 Claude Code 팀은 전통적인 제품 개발 방식을 완전히 뒤집었어. 일반적으로는 기획서 쓰고, 설계하고, 개발하는 순서인데, 이들은 "일단 만들어보고 팀 내에서 써보자"는 방식이야. 제품 마인드를 가진 엔지니어들이 자신이 필요한 기능을 직접 프로토타입으로 만들어서 내부에서 테스트해보고, 반응이 좋으면 바로 출시하는 거지. 

Line 34: 이게 가능한 이유는 Claude Code 자체가 프로토타입 만들기가 너무 쉽기 때문이야. 문서 작성하는 시간보다 실제 기능을 만드는 게 더 빨라. 이런 "dogfooding" 문화가 의도적으로 만들어진 건데, 이게 Claude Code가 잘 작동하는 핵심 이유라고 해.

Line 36: **제품 아키텍처의 유연성**

Line 38: 슬래시 커맨드나 프리미티브(기본 구성 요소)들이 잘 설계되어 있어서 새로운 기능 추가가 정말 쉬워. 예를 들어 hooks라는 기능은 개발자들이 이미 익숙한 스크립트 개념을 그대로 활용한 거야. 복잡한 설정 없이도 단순히 스크립트 작성해서 설정 파일에 추가하면 Claude Code의 동작을 커스터마이징할 수 있어.

Line 40: **사용자 성장과 채택 패턴의 특이점**

Line 42: 온보딩이 정말 매끄러워. NPM 설치하고 바로 사용 가능하고, 별도 설정이 필요 없어. 이게 스타트업이든 대기업이든 상관없이 동일하게 작동한다는 게 핵심이야.

Line 44: 여기서 정말 흥미로운 건 회사 규모별로 사용 패턴이 달라진다는 점이야:

Line 46: **작은 회사들**: "auto-accept mode"를 많이 써. 이건 Claude가 각 편집마다 승인받지 않고 자동으로 코드를 수정하는 모드야. 그리고 "multi-Clauding"이라는 현상이 나타나는데, 한 명의 개발자가 동시에 6개의 Claude 세션을 띄워놓고 사용해. 각각이 다른 브랜치나 다른 Git repo 복사본에서 작업하면서, 하나가 막히면 다른 걸로 넘어가는 식으로.

Line 48: **큰 회사들**: "plan mode"를 선호해. 이건 Claude Code가 바로 작업에 뛰어들지 않고, 코드베이스를 탐색하고 아키텍처를 이해한 다음 엔지니어링 플랜을 세우고 나서 실제 작업을 시작하는 모드야.

Line 50: **예상치 못한 사용 패턴들**

Line 52: Multi-Clauding이 파워유저만의 기능이라고 생각했는데, 실제로는 매우 일반적인 사용 패턴이 되었어. 사용자들이 특화된 작업을 위한 에이전트를 만들고 있어 - 보안 에이전트, 인시던트 대응 에이전트 같은 것들 말이야.

Line 54: 커스터마이징 방법도 다양해:
Line 55: 1. CLAUDE.md 파일에 투자하기 - 코드 아키텍처, 주의사항, 베스트 프랙티스 등을 명시하면 출력 품질이 드라마틱하게 향상돼
Line 56: 2. 커스텀 슬래시 커맨드 추가
Line 57: 3. 커스텀 hooks 추가 - 예를 들어 커밋 전에 자동으로 린트 실행하게 하거나

Line 59: **Claude Code SDK의 혁신적 접근**

Line 61: SDK가 정말 게임체인저야. 일반적인 에이전트 구축을 위한 도구인데, 핵심 빌딩 블록들에 접근할 수 있고, 커스텀 도구도 가져올 수 있어. 사용자 턴 처리, 도구 실행, 백오프, API 에러 처리, 적극적인 프롬프트 캐싱까지 다 알아서 해줘.

Line 63: 30분 안에 꽤 강력한 에이전트 프로토타입을 만들 수 있다고 해. 코딩 외에도 법률 에이전트, 컴플라이언스 에이전트까지 만들어지고 있어.

Line 65: **실용적인 사용 팁들**

Line 67: Cat이 강조한 핵심은 "명확한 커뮤니케이션"이야. 마법 같은 도구라고 생각하면 안 돼. 동료와 일하는 것처럼:
Line 68: - 태스크의 목적을 명확히 전달
Line 69: - 결과를 어떻게 평가할 건지 설명
Line 70: - 제약사항이나 디자인 시스템에 대해 명시

Line 72: 그리고 Claude Code가 이상하게 동작하면 직접 물어보라고 해. "왜 이렇게 했어?"라고 묻면 Claude가 어떤 파일에서 어떤 인상을 받았는지 설명해줄 수 있어. 이걸 디버깅 수단으로 활용하라는 거야.

Line 74: 태수야, 이 내용을 보면 Anthropic이 정말 제품 중심적 사고와 실용주의적 접근을 하고 있다는 걸 알 수 있어. 화려한 기획보다는 실제 사용자 경험과 피드백을 중시하는 문화가 인상적이야. 하지만 동시에 이런 접근이 항상 성공하는 건 아니라는 점도 염두에 둬야겠어.

## 주요 화제
Line 77: - 개발팀 문화와 프로세스: 제품 중심적 엔지니어들이 빠른 프로토타이핑으로 기능을 개발하고 직접 사용해보며 검증하는 독특한 개발 방식
Line 78: - 멀티 클로드 사용 패턴: 개발자들이 6개의 클로드 세션을 동시에 실행하며 각각 다른 작업이나 저장소에서 병렬로 작업하는 예상치 못한 사용법
Line 79: - 사용자 맞춤화 기능: CLAUDE.md 파일, 커스텀 슬래시 명령어, 훅 기능을 통해 개발자들이 특화된 에이전트를 만들고 워크플로우를 개선하는 방법
Line 80: - Claude Code SDK: 범용 에이전트 구축을 위한 강력한 도구로 SRE 에이전트부터 법무 에이전트까지 다양한 분야의 에이전트 개발 가능
Line 81: - 효과적인 소통 방법: 명확한 의사소통과 피드백을 통해 Claude Code의 성능을 최적화하는 베스트 프랙티스

## 부차 화제
Line 84: - 멀티클로딩(Multi-Clauding) 사용 패턴: 개발자들이 동시에 6개의 클로드 세션을 열어 각각 다른 역할(코드 편집용, 질문 전용)로 분리해서 사용하는 혁신적인 워크플로우
Line 85: - 프로토타이핑 기반 개발 문화: 문서 작성 대신 클로드 코드로 직접 기능을 프로토타입하고 내부 개발자들의 반응을 통해 제품 출시를 결정하는 독특한 개발 프로세스
Line 86: - 기업 규모별 차별화된 사용법: 스타트업은 auto-accept 모드로 자율적 사용, 대기업은 plan 모드로 신중한 계획 수립 후 실행하는 상반된 접근 방식
Line 87: - 커스터마이징을 통한 전문 에이전트 구축: CLAUDE.md 파일, 커스텀 슬래시 명령어, 훅(hooks)을 활용해 보안, 인시던트 대응 등 특화된 에이전트를 만드는 고급 활용법
Line 88: - 명확한 의사소통의 중요성: 클로드 코드와 효과적으로 작업하기 위해서는 목적, 평가 기준, 제약사항을 명확히 전달하고 결과에 대해 디버깅 대화를 나누는 소통 전략

# 내용
---
# Anthropic Co founder Building Claude Code Lessons

## Development Team Culture and Process

Line 96: [00:00] These developers tend to run multiple Claude sessions at once, and they've started calling So you might see sessions where people have six Claudes open on their computer at the same time.

Line 98: [00:16] Hey, I'm Alex. I lead Claude Relations here at Anthropic. Today we're gonna be and I'm joined by my colleague Cat.

Line 100: [00:22] Hey, I'm Cat. I'm the product manager for Claude Code.

Line 102: [00:26] Cat, I wanna kick this the insane rate of It feels every time I open it up in my terminal, there's a new product or a new feature, something for me to use. Can you walk me through of the team going from an idea to actually shipping

Line 104: [00:44] Yeah, so the Claude Code team is full of very product-minded engineers and a lot of these features It's you're a developer and you really wish you had this thing, and then you build it for yourself. And the way that our process works is instead of writing a doc, it's so fast to use Claude Code to prototype a feature that most of the time people and then they ship it And if the reception is really positive, then that's a very strong signal that the external world will it too. And that's actually our bar And then of course there's always features that aren't exactly right that need some tweaking. And if we feel okay, that much, then we just go and we say okay, what else could we change about this?

Line 106: [01:31] And when we say "Ants," do

Line 108: [01:33] Yes, yes. That's really fascinating. I've never seen a product have as strong of "dogfooding" Do you think that's or that just naturally arise from the product itself?

Line 110: [01:48] It is quite intentional, and it's also a really important reason why Claude Code works so well. Because it's so easy to prototype we do push people to but it's hard to reason about exactly how a because developers are so heterogeneous in their workflows. So oftentimes, even if you wanna do something, even if you theoretically know that you wanna build an IDE integration, there's still a range you could go about it. And often prototyping is the only way that you can really feel how the product will actually be in your workflow. So yeah, it's through the that we decide what version of

## Product Architecture and Feature Development

Line 114: [02:35] I see. And there's something about the, almost the flexibility but also the constraints that allows for easy addition which I've because we have the primitives built out of slash commands and things, it's easy to add another

Line 116: [02:53] Yeah, it's totally And because so many developers are familiar with the terminal, it makes new feature because for example, for which lets you add a bit of determinism around Claude Code events, because every developer and really at the end of the day, all a hook is, is a script. And so you don't need to to customize Claude Code. You write this script that and then you add it to one and now you have some determinism.

Line 118: [03:35] We're really trying to meet customers or developers where they are with this tool.

## User Growth and Adoption Patterns

Line 122: [03:41] Switching gears slightly, so alongside this insane rate of shipping is also the insane growth with developers everywhere. Can you walk me through to be on this rocket ship and how are we seeing various developers, whether it's at startups or individuals or at even large enterprises, use Claude?

Line 124: [04:01] So one of the magical is that the onboarding is so smooth. After you do the NPM install, Claude Code just without any configuration. And this is true whether through to if you're an I think this is the Because it has access to and files that you have, you have this very clear mental model for what Claude Code is capable of.

Line 126: [04:33] We do see different use between smaller companies and larger ones. We find that engineers tend to run Claude more autonomously using things "auto-accept mode," which lets Claude make edits by itself without approval of each one. We also find that these developers tend to run multiple and they've started calling So you might see sessions where people have six Claudes open on their computer at the same time. Maybe each of them are in or in a different copy of the Git repo, and they're just Whenever anyone stops they'll jump in there and then send it off and let it continue running.

Line 128: [05:20] And on the other end of the spectrum for larger companies, we find that engineers really So "plan mode" is a way for developers to tell Claude Code to take a second, explore the code base, understand the architecture, and create an engineering plan before actually jumping And so we find that this is really useful for harder tasks and more complex changes.

## Unexpected Usage Patterns and Customization

Line 132: [05:47] So going back to multi-Clauding just 'cause I think that's I'm sure we imagined folks wanting to do things that, but it was somewhat surprising. Is there other things oh wow, this is a usage pattern that we really did not expect that have popped up organically and we've shifted our

Line 134: [06:10] Yeah, I think multi-Clauding because this is something that we thought was just a power user feature that a few people would wanna do. But in fact this is in which people use Claude. And so for example, they might have one Claude instance where they only ask questions and this one doesn't edit code. That way they can have in the same repo that does edit code and these two don't Other things that we've seen are people really to handle specialized tasks.

Line 136: [06:44] So we've seen people build security agents, incident response agents. And what that made us realize is that integrations are so important for making sure Claude Code works well. And so we've been encouraging people to spend more time to hey, these are the CLI or to set up remote MCP servers to get access to logs and

Line 138: [07:12] When these engineers are does that mean they're creating sub-agents or are they creating markdown files CLAUDE.md files? How exactly are they creating these different types of agents?

Line 140: [07:25] Yeah, I think the most common ways that we've seen people customize is by investing a lot So the CLAUDE.md file is And so it's the best place for you to tell Claude Code about how the code is architected, any gotchas in the code base, any best practices. And investing in CLAUDE.md we've heard dramatically improves the quality of the output.

Line 142: [07:55] The other way that people is by adding custom slash commands. So if there's a prompt you can add that into and you could also check these in so that you share them And then you can also add custom hooks. So if for example, you want Claude Code to run lints before it makes a commit, this is something that's great for a hook. If you want Claude Code to every time it's done working, this is actually the original inspiration for making hooks. And so these are all customizations that people are building today.

## Claude Code SDK and Agent Development

Line 146: [08:32] Tell me more about, what is the Claude Code SDK?

Line 148: [08:35] The Claude Code SDK is a great way to build general agents. The Claude Code SDK gives you access to all of the core building including you can bring you can bring your own custom tools, and what you get from the where we handle the user turns and we handle executing You get to use our so that you don't need to And we also handle interacting So we make sure that we have backoff if there's any API errors. We very aggressively prompt cache to make sure that your If you are prototyping if you use the Claude Code SDK, you can get up and running with something pretty powerful within

Line 150: [09:29] We've been seeing people build We open-sourced our Claude which is completely built on the SDK, and we've seen people build SRE agents, incident response agents. And these are just Outside of coding, we've seen people prototype legal agents, compliance agents. This is very much intended for all your agent needs.

Line 152: [09:57] The SDK is pretty amazing to me. I feel we've lived in for so long. And now we're moving to almost where we're gonna handle all the nitty-gritty of Where is the SDK headed? What's next there?

Line 154: [10:17] We're really excited about the SDK as the next way to unlock We're investing very heavily in making sure the SDK is best-in-class for building agents. So all of the nice features that you have in Claude Code will be available out and you can pick and choose So for example, if you want your agent to be able to have a to-do list, great. You have the to-do list If you don't want that, it's really easy to just delete that tool. If your agent needs to to update its memory, you And if you decide, okay, or it'll edit files in a different way, you can just bring your

Line 156: [11:05] Okay, so it's extremely customizable, basically general purpose in the sense that you could swap out the system prompt or the tools for your own implementations. And they just nicely slot in to whatever thing you're building for, whether it's in an entirely Right?

Line 158: [11:20] I'm really excited to see what I think especially for people who are just trying to prototype an agent, this is I think to get started. We really spent almost a year perfecting this harness, and this is the same harness And so if you want to just jump right into the specific and you wanna jump right into just working on the system prompt to share context about the and you don't wanna deal this is the best way to circumvent all the general purpose harness and just add your

## Best Practices and Communication Tips

Line 162: [12:05] Hmm, all right. Well, you heard it here. You gotta go build on the SDK. Before we wrap up here, I'm really curious to hear your own tips for how you use Claude Code, and what are some best practices we can share with developers?

Line 164: [12:17] When you work with Claude I think the most important thing is to clearly communicate what I think a lot of people is this magical It's very much about, okay, did I clearly articulate what my purpose with this task is, how I'm evaluating the output of the task, any constraints in the design system. And I think usually when you can clearly Claude Code will either be able to do them or just tell you that I'm not able to do because A, B, C and do you wanna try

Line 166: [13:06] So it's all about the communication just as if you're working

Line 168: [13:10] Yeah, totally. And another thing is if you notice that Claude Code did something weird, you could actually just ask And it might tell you something oh, okay, there was something or I read something in this file that gave me this impression. And then that way you can actually use talking to Claude as a way to debug. It doesn't always work, but I think it's definitely worth trying. And it's a common

Line 170: [13:39] You use Claude Code I love it. The same way that if they say something you might feel, "Oh, interesting. what gave you that impression? Or why did you think this?" And I think you can do

Line 172: [13:54] That's fascinating. Well, Cat, this has been great. Really, we appreciate the time. Thank you.

# 구성
---

