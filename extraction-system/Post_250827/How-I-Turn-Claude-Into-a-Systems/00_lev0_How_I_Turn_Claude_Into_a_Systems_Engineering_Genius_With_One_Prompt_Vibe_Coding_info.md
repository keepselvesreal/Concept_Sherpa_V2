# 속성
---
process_status: true
source: https://medium.com/vibe-coding/how-i-turn-claude-into-a-systems-engineering-genius-with-one-prompt-d342af0f517c
source_type: post
source_language: english
structure_type: standalone
content_processing: unified
folder_name: How-I-Turn-Claude-Into-a-Systems
created_at: 2025-08-27T19:59:55.265646

# 추출
---
## 핵심 내용
전설적인 C 언어 시스템 엔지니어 Eskil Steenberg의 대규모 소프트웨어 아키텍처 강의를 AI 프롬프트로 변환하여, 복잡한 React 코드를 모듈화된 '블랙박스' 컴포넌트로 재구성하는 새로운 개발 방법론을 제시한다. (길이: 6652 문자)

## 상세 핵심 내용
저자는 오픈소스 프로젝트 Mentis에서 React DOM 조작으로 인한 복잡한 버그들을 해결하는 과정에서 큰 좌절을 겪었다. 한 문제를 수정하면 다른 문제가 발생하는 악순환에 빠져있었고, 테스트로도 모든 경우를 잡아낼 수 없었다.

이때 발견한 Eskil Steenberg의 "Architecting LARGE Software Projects" 강의가 전환점이 되었다. 그는 3D 엔진부터 네트워크 게임까지 모든 것을 C 언어로 구축하는 전문가로, 그의 핵심 원칙들은 매우 실용적이었다: 프로젝트 크기에 관계없는 일정한 개발 속도 유지, 한 사람이 하나의 모듈을 완전히 담당, 모든 것이 교체 가능해야 한다는 원칙, 블랙박스 인터페이스를 통한 모듈 간 소통.

저자는 이 강의 내용을 완전히 분석해서 세 개의 AI 프롬프트로 변환했다: Claude Code용(실제 개발), Claude용(계획 및 설계), Cursor용(디버깅 및 테스트 전략). 이 프롬프트들은 언어나 프레임워크에 관계없이 AI가 대규모 시스템을 사고할 수 있도록 훈련시킨다.

결과는 놀라웠다. Mentis의 전체 컨텍스트를 새로운 아키텍처 프롬프트와 함께 Claude에 전달했을 때, React의 예측 불가능한 동작에 의존하지 않고 DOM과 직접 인터페이스하는 방식을 제안받았다. 이는 최소한의 오버헤드로 다른 프레임워크에서도 코드를 재사용할 수 있는 솔루션이었다.

## 상세 내용
이 접근법의 핵심은 Eskil의 철학인 "모든 것은 교체 가능해야 한다"를 AI 개발에 적용한 것이다. AI가 이해하기 어려운 복잡한 코드를 생성하더라도, 모듈화된 시스템에서는 해당 모듈만 쉽게 교체할 수 있다. 이는 AI의 최대 약점 중 하나를 오히려 강점으로 전환시키는 전략이다.

저자가 강조하는 워크플로우는 다음과 같다: 단일 폴더에 집중하고, 해당 컨텍스트와 프롬프트를 Claude에 전달해 전략적 계획을 수립한 후, Claude Code나 Cursor를 사용해 그 계획을 실행한다. 이 방식은 대규모 리팩토링을 관리 가능한 작은 단위로 나누어 처리할 수 있게 한다.

특히 흥미로운 점은 "오늘 5줄의 코드를 쓰는 것이 나중에 1줄을 편집하는 것보다 빠르다"는 Eskil의 원칙이다. 이는 컨텍스트 스위칭이 개발 속도에 미치는 영향을 고려한 것으로, AI 개발에서도 매우 유효한 접근법이다. 새로운 코드를 작성하는 것이 기존 코드를 수정하는 것보다 종종 더 효율적일 수 있다.

이 방법론은 단순히 기술적인 해결책을 넘어서 개발 철학의 변화를 요구한다. 개발자는 더 이상 모든 코드를 완벽하게 이해하려고 노력할 필요가 없고, 대신 시스템을 모듈화하고 인터페이스를 명확히 정의하는 데 집중해야 한다. AI가 생성한 코드가 복잡하거나 버그가 있어도, 해당 모듈만 교체하면 되므로 전체 시스템에 미치는 영향을 최소화할 수 있다.

## 주요 화제
- **모듈러 아키텍처**: 복잡한 시스템을 교체 가능한 독립적인 모듈들로 분해하는 접근법
- **블랙박스 인터페이스**: 모듈 간 소통을 위한 명확하고 단순한 API 설계 원칙
- **AI 프롬프트 엔지니어링**: 시스템 아키텍처 강의를 AI 개발 도구로 변환하는 방법론
- **개발 속도 최적화**: 컨텍스트 스위칭을 최소화하여 일정한 개발 속도 유지하는 전략
- **React DOM 문제 해결**: 예측 불가능한 React 동작 대신 직접적인 DOM 인터페이스 활용

## 부차 화제
- **Eskil Steenberg 강의**: "Architecting LARGE Software Projects" 강의의 핵심 원칙들
- **Mentis 오픈소스 프로젝트**: 복잡한 DOM 조작 버그로 인한 개발 난항 사례
- **세 가지 프롬프트 전략**: Claude Code, Claude, Cursor 각각에 최적화된 프롬프트 설계
- **컨텍스트 기반 리팩토링**: 단일 폴더 집중을 통한 점진적 시스템 개선 방법
- **프레임워크 독립적 설계**: 최소한의 오버헤드로 다양한 프레임워크에서 재사용 가능한 코드 구조
- **인지적 부하 감소**: 개발자가 시스템 전체를 이해하지 않고도 효과적으로 작업할 수 있는 환경 조성
- **GitHub 리소스 공유**: 실제 프롬프트와 강의 트랜스크립트를 포함한 오픈소스 저장소 제공

# 내용
---
# How I Turn Claude Into a Systems Engineering Genius With One Prompt Vibe Coding

# How I Turn Claude Into a Systems Engineering Genius With One Prompt | Vibe Coding

> ## Excerpt
> Learn modular architecture principles that scale. Turn tangled React code into replaceable components using AI prompts from a legendary C programmer.

---
Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*UlwN36mKsWn1Hj1G-ihWSw.png)

Image I created using Midjourney then edited with Figma

## **How a legendary systems engineer’s lecture became my most powerful AI prompt**

[

![Alex Dunlop](https://miro.medium.com/v2/resize:fill:48:48/1*mWvQckMd9GIigTpeHXsv5A.png)



](https://medium.com/@alexjamesdunlop?source=post_page---byline--d342af0f517c---------------------------------------)

Last month I found something that changed how I architect software projects. A lecture from a C engineer named Eskil Steenberg, changed the way I think about systems.

I took this lecture and turned it into three AI prompts that now guide me through every refactor or new project I do.

[Not a Medium member? Keep reading for free by clicking here.](https://medium.com/@alexjamesdunlop/how-i-turn-claude-into-a-systems-engineering-genius-with-one-prompt-d342af0f517c?sk=94dbed9acf55dba92fc296042f5d86fe)

Instead of focusing on preventing AI from creating complex code, I can now break everything up into perfect “black boxes” that any developer _(or AI developer)_ can understand and replace.

## The Problem That Led Me Here

Recently, [Mentis](https://medium.com/vibe-coding/why-im-open-sourcing-the-component-every-chat-app-needs-09ea6fe44f9b) _(my open-source project)_ has had complex bugs which led me to hit a massive wall. Massive shout out to [Abdelrahman](https://github.com/abdelrahmanrafaat) for helping to test and report these issues.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*xI-IRckpmO2sQvnVUgvqNg.png)

Complex issues were caused by weird DOM interactions with React

A lot of the problems stem from DOM manipulation with React, these kinds of bugs make me question my life and sometimes why I started the project in the first place.

The codebase started to grow into a mess where fixing one issue broke another. My tests couldn’t catch everything because the DOM would render differently than how React intended.

## The Discovery That Changed My Software Approach

While taking a break from fixing issues, I came across Eskil Steenberg’s lecture “Architecting LARGE Software Projects”. This guy builds everything from 3D engines to networked games, all in C.

These are my favourite of his core principles:

-   **Constant developer velocity** — _regardless of project size._
-   **One module, one person** — _one person should be able to do everything (given enough time)_.
-   **Everything should be replaceable** — _if you can’t understand it, you can rewrite it easily._
-   **Black box interfaces** — _modules communicate through clean APIs._
-   **Writing 5 lines today** — _rather than editing 1 line later (context switching affects velocity)._

He also suggested making modules that can be reused in different projects which I really like.

In the lecture, he gives an example of how to build a system built for a fighter jet. This helped me realise how much simpler my task is, but my approach needed to change.

> “It’s faster to write five lines of code today than to write one line today and then have to edit it in the future.” — Eskil Steenberg

I would highly recommend watching the video:

## Converting The Theory Of The Lecture

After taking in Eskil’s amazing lecture, it took me a while to really understand _(I even rewatched it a couple of times)_.

The main thing I struggled with was Eskil’s lecture was built for C, a low level language and I’m building for React.

That’s when I had an amazing idea, I took the complete transcript of the lecture and built prompts from it.

I built three prompts that I use:

1.  **Claude Code Prompt** — _For hands on development._
2.  **Claude Prompt** — _For planning and designing._
3.  **Cursor Prompt** — _Debugging and mainly testing strategies._

These prompts are built for any language and any framework. Teaching AI to think on a much larger scale.

## The Lightbulb Context Moment

The prompts were working great, but they had a big issue. They worked better for new projects only. That’s when I remembered another technique I have been using.

The big problem with AI refactoring is you need certainty. With certainty, you need control over what’s changing.

The architecture prompts provide excellent plans for breaking refactors into bite sized chunks. My workflow has become:

-   Focus on a single folder.
-   Pass the context and prompt to Claude.
-   Come up with a strategic plan.
-   Execute that plan using either Claude Code or Cursor.

## My Real Results

I passed my entire Mentis context into Claude with the new architecture prompt and asked for some help.

_The response blew me away._

I needed to interface directly with the DOM instead of relying on React’s unpredictable behaviour.

This new black box DOM interface implementation would allow me to completely reuse the code for different frameworks with minimal overhead.

Something I never thought would be possible and something directly the prompt came up with directly.

## Why This Matters With AI Development

Following Eskil’s principle: “**Everything should be replaceable”** — _if you can’t understand it, you can rewrite it easily._

We can transform some of AI’s biggest weaknesses into a new superpower by structuring our systems as modular, replaceable components.

Now when AI generates code we don’t understand, we can easily replace that module. This allows AI to build something fast while giving us the freedom to refactor or completely rewrite modules when needed.

Everything becomes manageable bite sized chunks.

_Use the power of AI with the power of large systems._

## These Prompts Change Everything

I’ve packaged everything into a GitHub repo with all three prompts and the original video transcript.

View the [prompts here](https://github.com/Alexanderdunlop/ai-architecture-prompts).

## At The End Of The Day

Eskil’s insights are great, focusing on reducing cognitive load (context switching included) and not depending on a single person.

In the new AI era, this is more important than ever, if AI creates something complex or buggy you are able to replace just that module without breaking anything else.

I have spent weeks testing this approach before sharing it. The results for me personally make it a no brainer. Something appeared that I would have never thought of by myself.

_I’m not affiliated with Anthropic, Eskil Steenberg, or any of the tools mentioned. All opinions and experiences shared are based on my own developer experiences and thoughts._

### Resources:

-   [Eskil’s great youtube video](https://www.youtube.com/watch?v=sSpULGNHyoI).
-   [Mentis](https://github.com/alexanderdunlop/mentis).
-   [Prompts & Transcript repo](https://github.com/Alexanderdunlop/ai-architecture-prompts).

### Related Posts:

# 구성
---
