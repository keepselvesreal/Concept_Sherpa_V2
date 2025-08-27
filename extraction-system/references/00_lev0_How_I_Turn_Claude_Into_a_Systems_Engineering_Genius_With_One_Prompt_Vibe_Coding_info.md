# 속성
---
process_status: true
source: https://medium.com/vibe-coding/how-i-turn-claude-into-a-systems-engineering-genius-with-one-prompt-d342af0f517c
source_type: post
source_language: english
structure_type: standalone
content_processing: unified
folder_name: How-I-Turn-Claude-Into-a-Systems
created_at: 2025-08-27T20:12:45.927832

# 추출
---
## 핵심 내용
시스템 엔지니어 Eskil Steenberg의 대규모 소프트웨어 아키텍처 강의에서 영감을 받아 AI 개발에 적용 가능한 모듈형 시스템 설계 원칙을 3개의 AI 프롬프트로 구현하여 복잡한 코드베이스의 리팩토링과 유지보수 문제를 해결한 실제 사례를 공유한 글입니다. (길이: 6485 문자)

## 상세 핵심 내용
개발자 Alex Dunlop은 자신의 오픈소스 프로젝트 Mentis에서 복잡한 DOM 조작과 React 상호작용으로 인한 버그들을 해결하는 과정에서 큰 어려움을 겪었습니다. 이 문제들은 하나의 버그를 수정하면 다른 버그가 발생하는 연쇄적인 문제로 이어졌으며, 테스트로도 모든 케이스를 잡아낼 수 없는 상황이었습니다.

그러던 중 C 언어 개발자이자 3D 엔진과 네트워크 게임을 구축하는 Eskil Steenberg의 "대규모 소프트웨어 프로젝트 아키텍처" 강의를 발견하게 됩니다. 이 강의에서 제시된 핵심 원칙들 - 지속적인 개발자 속도, 한 모듈당 한 사람, 모든 것의 교체 가능성, 블랙박스 인터페이스, 그리고 미래의 수정보다는 현재의 새로운 코드 작성 - 이 Alex의 개발 접근 방식을 근본적으로 바꾸게 됩니다.

Alex은 이 C 기반의 이론을 React와 같은 고수준 언어와 프레임워크에 적용하기 위해 강의 전체 대본을 활용하여 3개의 AI 프롬프트(Claude Code용, Claude용, Cursor용)를 개발했습니다. 이 프롬프트들을 통해 복잡한 시스템을 관리 가능한 작은 단위로 분해할 수 있게 되었으며, AI가 이해하기 어려운 코드를 생성하더라도 해당 모듈만 쉽게 교체할 수 있는 시스템을 구축했습니다.

실제 적용 결과, Mentis 프로젝트에서 React의 예측 불가능한 동작 대신 DOM과 직접 인터페이스하는 블랙박스 구현을 통해 다른 프레임워크에도 최소한의 오버헤드로 재사용 가능한 코드를 만들 수 있게 되었습니다. 이는 AI 개발의 약점을 오히려 장점으로 전환시키는 혁신적인 접근법을 제시합니다.

## 상세 내용
이 글은 현대 AI 기반 개발 환경에서 시스템 설계의 근본적인 패러다임 전환을 제안합니다. 전통적으로 AI 코드 생성의 문제점은 복잡하고 이해하기 어려운 코드를 생성한다는 것이었지만, Eskil Steenberg의 모듈형 아키텍처 원칙을 적용하면 이러한 문제를 오히려 기회로 전환할 수 있습니다.

핵심은 "모든 것이 교체 가능해야 한다"는 원칙입니다. AI가 복잡한 코드를 생성하더라도, 그것이 명확한 인터페이스를 가진 독립적인 모듈로 구성되어 있다면 언제든지 해당 모듈만 이해하기 쉬운 코드로 교체할 수 있습니다. 이는 AI의 빠른 생성 능력과 인간의 이해 가능성 사이의 균형을 제공합니다.

Alex의 경험에서 특히 주목할 점은 기존 프로젝트의 리팩토링에서 이 접근법의 효과가 두드러진다는 것입니다. 단일 폴더에 집중하여 컨텍스트와 프롬프트를 전달하고, 전략적 계획을 수립한 후 실행하는 워크플로우는 대규모 시스템 변경을 관리 가능한 단위로 분해합니다.

이러한 접근법의 철학적 기반은 인지적 부하를 줄이고 컨텍스트 스위칭을 최소화하는 것입니다. "오늘 5줄을 쓰는 것이 나중에 1줄을 수정하는 것보다 빠르다"는 Eskil의 말은 AI 시대에 더욱 중요해집니다. 새로운 모듈을 생성하는 것이 기존 복잡한 코드를 수정하는 것보다 안전하고 예측 가능하기 때문입니다.

또한 이 방법론은 개발팀의 협업 방식도 혁신적으로 바꿉니다. 각 모듈이 독립적이고 교체 가능하다면, 팀원들은 전체 시스템을 이해하지 않고도 특정 모듈에만 집중할 수 있습니다. 이는 Eskil이 제시한 "한 모듈, 한 사람" 원칙과 완벽하게 부합합니다.

## 주요 화제
- **시스템 아키텍처 원칙**: Eskil Steenberg의 5가지 핵심 원칙 (지속적 개발 속도, 모듈당 담당자, 교체 가능성, 블랙박스 인터페이스, 새 코드 우선 작성)
- **AI 프롬프트 엔지니어링**: C 기반 강의를 다양한 언어와 프레임워크에 적용 가능한 3개 AI 프롬프트로 변환
- **모듈형 시스템 설계**: 복잡한 시스템을 독립적이고 교체 가능한 모듈로 분해하는 접근법
- **리팩토링 전략**: 기존 복잡한 코드베이스를 관리 가능한 단위로 나누어 점진적으로 개선하는 방법론
- **AI 코드 생성 문제 해결**: AI가 생성하는 복잡한 코드를 이해 가능한 형태로 관리하는 전략

## 부차 화제
- **Mentis 프로젝트 사례**: 오픈소스 채팅 컴포넌트에서 발생한 DOM-React 상호작용 버그 해결 과정
- **개발 도구 활용**: Claude Code, Claude, Cursor 등 다양한 AI 도구의 특화된 활용법
- **테스트 전략의 한계**: DOM 렌더링 불일치로 인한 테스트 커버리지 문제
- **프레임워크 독립적 설계**: React 의존성을 줄이고 다른 프레임워크로 이식 가능한 코드 구조
- **컨텍스트 스위칭 비용**: 개발자 생산성에 미치는 컨텍스트 전환의 영향과 해결책
- **오픈소스 기여**: GitHub를 통한 프롬프트와 강의 자료 공유
- **개발자 협업**: 단일 담당자 모델과 팀 기반 개발의 균형점

# 내용
---
# How I Turn Claude Into a Systems Engineering Genius With One Prompt Vibe Coding

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
