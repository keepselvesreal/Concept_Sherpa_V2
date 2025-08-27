# How I Turn Claude Into a Systems Engineering Genius With One Prompt Vibe Coding

**생성 시간:** 2025-08-27 21:23:09 KST

**핵심 내용:** 시스템 엔지니어링 원리를 AI 프롬프트에 적용하여 소프트웨어 개발 및 리팩토링 과정을 개선하는 방법에 대한 가이드

**상세 내용:**
- 제목 및 서론 (1-15줄): 전설적인 시스템 엔지니어의 강의를 활용한 AI 프롬프트 접근법 소개
- 문제 정의 섹션 (17-32줄): Mentis 프로젝트에서 발생한 복잡한 버그와 DOM 조작 문제점 설명
- 발견과 변화 섹션 (34-60줄): Eskil Steenberg의 강의에서 얻은 핵심 원리들과 시스템 설계 접근법
- 이론 변환 섹션 (62-75줄): C 언어 기반 강의 내용을 React 개발에 적용하는 과정
- 실제 결과 섹션 (77-90줄): 새로운 접근법을 통해 얻은 구체적인 개선 사항들
- AI 개발의 의의 섹션 (92-100줄): AI 약점을 강점으로 전환하는 모듈화 전략
- 결론 및 자료 섹션 (102-115줄): GitHub 리포지토리와 관련 자료 링크 제공

**상태:** active

---

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*UlwN36mKsWn1Hj1G-ihWSw.png)

Image I created using Midjourney then edited with Figma

## **How a legendary systems engineer's lecture became my most powerful AI prompt**
## **전설적인 시스템 엔지니어의 강의가 어떻게 내 가장 강력한 AI 프롬프트가 되었는지**

[

![Alex Dunlop](https://miro.medium.com/v2/resize:fill:48:48/1*mWvQckMd9GIigTpeHXsv5A.png)



](https://medium.com/@alexjamesdunlop?source=post_page---byline--d342af0f517c---------------------------------------)

Last month I found something that changed how I architect software projects. A lecture from a C engineer named Eskil Steenberg, changed the way I think about systems.

지난달 나는 소프트웨어 프로젝트를 설계하는 방식을 바꾼 무언가를 발견했다. Eskil Steenberg이라는 C 엔지니어의 강의가 시스템에 대한 내 사고방식을 바꾸어 놓았다.

I took this lecture and turned it into three AI prompts that now guide me through every refactor or new project I do.

나는 이 강의를 세 개의 AI 프롬프트로 만들어서 지금은 모든 리팩토링이나 새로운 프로젝트 작업을 이끌어주고 있다.

[Not a Medium member? Keep reading for free by clicking here.](https://medium.com/@alexjamesdunlop/how-i-turn-claude-into-a-systems-engineering-genius-with-one-prompt-d342af0f517c?sk=94dbed9acf55dba92fc296042f5d86fe)

Instead of focusing on preventing AI from creating complex code, I can now break everything up into perfect "black boxes" that any developer _(or AI developer)_ can understand and replace.

AI가 복잡한 코드를 생성하는 것을 막는 데 집중하는 대신, 이제 나는 모든 것을 어떤 개발자든_(또는 AI 개발자든)_ 이해하고 교체할 수 있는 완벽한 "블랙 박스"로 나눌 수 있게 되었다.

## The Problem That Led Me Here
## 나를 여기로 이끈 문제

Recently, [Mentis](https://medium.com/vibe-coding/why-im-open-sourcing-the-component-every-chat-app-needs-09ea6fe44f9b) _(my open-source project)_ has had complex bugs which led me to hit a massive wall. Massive shout out to [Abdelrahman](https://github.com/abdelrahmanrafaat) for helping to test and report these issues.

최근에 [Mentis](https://medium.com/vibe-coding/why-im-open-sourcing-the-component-every-chat-app-needs-09ea6fe44f9b) _(내 오픈소스 프로젝트)_에서 복잡한 버그들이 발생해서 큰 벽에 부딪혔다. 이러한 문제들을 테스트하고 리포트하는 데 도움을 준 [Abdelrahman](https://github.com/abdelrahmanrafaat)에게 큰 감사를 표한다.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*xI-IRckpmO2sQvnVUgvqNg.png)

Complex issues were caused by weird DOM interactions with React

A lot of the problems stem from DOM manipulation with React, these kinds of bugs make me question my life and sometimes why I started the project in the first place.

문제의 대부분은 React와 DOM 조작에서 비롯되는데, 이런 종류의 버그들은 내 인생과 때로는 왜 이 프로젝트를 시작했는지 의문을 갖게 만든다.

The codebase started to grow into a mess where fixing one issue broke another. My tests couldn't catch everything because the DOM would render differently than how React intended.

코드베이스는 하나의 문제를 고치면 다른 문제가 생기는 난장판으로 커지기 시작했다. DOM이 React가 의도한 것과 다르게 렌더링되기 때문에 내 테스트로는 모든 것을 잡아낼 수 없었다.

## The Discovery That Changed My Software Approach
## 내 소프트웨어 접근 방식을 바꾼 발견

While taking a break from fixing issues, I came across Eskil Steenberg's lecture "Architecting LARGE Software Projects". This guy builds everything from 3D engines to networked games, all in C.

문제 해결에서 잠시 휴식을 취하던 중, Eskil Steenberg의 "대규모 소프트웨어 프로젝트 설계" 강의를 발견했다. 이 사람은 3D 엔진부터 네트워크 게임까지 모든 것을 C로 만든다.

These are my favourite of his core principles:

다음은 그의 핵심 원칙 중 내가 가장 좋아하는 것들이다:

-   **Constant developer velocity** — _regardless of project size._
-   **지속적인 개발 속도** — _프로젝트 크기에 관계없이._
-   **One module, one person** — _one person should be able to do everything (given enough time)._
-   **하나의 모듈, 한 사람** — _한 사람이 모든 것을 할 수 있어야 한다 (충분한 시간이 주어진다면)._
-   **Everything should be replaceable** — _if you can't understand it, you can rewrite it easily._
-   **모든 것은 교체 가능해야 한다** — _이해할 수 없다면, 쉽게 다시 쓸 수 있어야 한다._
-   **Black box interfaces** — _modules communicate through clean APIs._
-   **블랙 박스 인터페이스** — _모듈들은 깔끔한 API를 통해 소통한다._
-   **Writing 5 lines today** — _rather than editing 1 line later (context switching affects velocity)._
-   **오늘 5줄 쓰기** — _나중에 1줄을 편집하기보다는 (컨텍스트 스위칭이 속도에 영향을 준다)._

He also suggested making modules that can be reused in different projects which I really like.

그는 또한 다른 프로젝트에서 재사용할 수 있는 모듈을 만들 것을 제안했는데, 이는 내가 정말 좋아하는 아이디어이다.

In the lecture, he gives an example of how to build a system built for a fighter jet. This helped me realise how much simpler my task is, but my approach needed to change.

강의에서 그는 전투기용 시스템을 구축하는 방법에 대한 예를 들었다. 이것은 내 작업이 얼마나 더 간단한지 깨닫게 해주었지만, 내 접근 방식은 바뀔 필요가 있었다.

> "It's faster to write five lines of code today than to write one line today and then have to edit it in the future." — Eskil Steenberg
> "오늘 5줄의 코드를 쓰는 것이 오늘 1줄을 쓰고 나중에 편집해야 하는 것보다 빠르다." — Eskil Steenberg

I would highly recommend watching the video:

나는 이 비디오를 시청할 것을 강력히 추천한다:

## Converting The Theory Of The Lecture
## 강의 이론의 변환

After taking in Eskil's amazing lecture, it took me a while to really understand _(I even rewatched it a couple of times)_.

Eskil의 놀라운 강의를 들은 후, 정말로 이해하는 데 시간이 좀 걸렸다 _(심지어 몇 번 다시 보기도 했다)_.

The main thing I struggled with was Eskil's lecture was built for C, a low level language and I'm building for React.

내가 어려워한 주요 점은 Eskil의 강의가 저수준 언어인 C를 위해 만들어졌는데, 나는 React로 구축하고 있다는 것이었다.

That's when I had an amazing idea, I took the complete transcript of the lecture and built prompts from it.

그때 놀라운 아이디어가 떠올랐다. 강의의 완전한 대본을 가져와서 거기서 프롬프트를 만들었다.

I built three prompts that I use:

나는 사용하는 세 개의 프롬프트를 만들었다:

1.  **Claude Code Prompt** — _For hands on development._
2.  **Claude Code 프롬프트** — _실습 개발용._
3.  **Claude Prompt** — _For planning and designing._
4.  **Claude 프롬프트** — _계획 및 설계용._
5.  **Cursor Prompt** — _Debugging and mainly testing strategies._
6.  **Cursor 프롬프트** — _디버깅 및 주로 테스팅 전략용._

These prompts are built for any language and any framework. Teaching AI to think on a much larger scale.

이 프롬프트들은 어떤 언어와 어떤 프레임워크를 위해서도 만들어졌다. AI가 훨씬 더 큰 규모로 생각하도록 가르치는 것이다.

## The Lightbulb Context Moment
## 번뜩이는 컨텍스트 순간

The prompts were working great, but they had a big issue. They worked better for new projects only. That's when I remembered another technique I have been using.

프롬프트들은 훌륭하게 작동했지만, 큰 문제가 있었다. 새로운 프로젝트에만 더 잘 작동했다. 그때 내가 사용해온 다른 기술이 떠올랐다.

The big problem with AI refactoring is you need certainty. With certainty, you need control over what's changing.

AI 리팩토링의 큰 문제는 확실성이 필요하다는 것이다. 확실성을 위해서는 무엇이 변경되고 있는지에 대한 제어가 필요하다.

The architecture prompts provide excellent plans for breaking refactors into bite sized chunks. My workflow has become:

아키텍처 프롬프트는 리팩토링을 일입 크기의 덩어리로 나누는 훌륭한 계획을 제공한다. 내 워크플로우는 다음과 같아졌다:

-   Focus on a single folder.
-   단일 폴더에 집중한다.
-   Pass the context and prompt to Claude.
-   컨텍스트와 프롬프트를 Claude에게 전달한다.
-   Come up with a strategic plan.
-   전략적 계획을 세운다.
-   Execute that plan using either Claude Code or Cursor.
-   Claude Code나 Cursor를 사용해서 그 계획을 실행한다.

## My Real Results
## 내 실제 결과

I passed my entire Mentis context into Claude with the new architecture prompt and asked for some help.

새로운 아키텍처 프롬프트와 함께 전체 Mentis 컨텍스트를 Claude에게 전달하고 도움을 요청했다.

_The response blew me away._

_그 응답은 나를 완전히 놀라게 했다._

I needed to interface directly with the DOM instead of relying on React's unpredictable behaviour.

React의 예측 불가능한 동작에 의존하는 대신 DOM과 직접 인터페이스해야 했다.

This new black box DOM interface implementation would allow me to completely reuse the code for different frameworks with minimal overhead.

이 새로운 블랙 박스 DOM 인터페이스 구현은 최소한의 오버헤드로 다양한 프레임워크에서 코드를 완전히 재사용할 수 있게 해줄 것이다.

Something I never thought would be possible and something directly the prompt came up with directly.

내가 가능하다고 생각해본 적 없는 것이고, 프롬프트가 직접 제시한 것이다.

## Why This Matters With AI Development
## 이것이 AI 개발에서 중요한 이유

Following Eskil's principle: "**Everything should be replaceable"** — _if you can't understand it, you can rewrite it easily._

Eskil의 원칙을 따라서: "**모든 것은 교체 가능해야 한다"** — _이해할 수 없다면, 쉽게 다시 쓸 수 있어야 한다._

We can transform some of AI's biggest weaknesses into a new superpower by structuring our systems as modular, replaceable components.

우리는 시스템을 모듈화되고 교체 가능한 컴포넌트로 구조화함으로써 AI의 가장 큰 약점 중 일부를 새로운 슈퍼파워로 변환할 수 있다.

Now when AI generates code we don't understand, we can easily replace that module. This allows AI to build something fast while giving us the freedom to refactor or completely rewrite modules when needed.

이제 AI가 우리가 이해할 수 없는 코드를 생성할 때, 우리는 그 모듈을 쉽게 교체할 수 있다. 이것은 AI가 빠르게 무언가를 구축할 수 있게 하면서 동시에 필요할 때 모듈을 리팩토링하거나 완전히 다시 쓸 수 있는 자유를 우리에게 준다.

Everything becomes manageable bite sized chunks.

모든 것이 관리 가능한 일입 크기의 덩어리가 된다.

_Use the power of AI with the power of large systems._

_대규모 시스템의 힘과 함께 AI의 힘을 사용하라._

## These Prompts Change Everything
## 이 프롬프트들은 모든 것을 바꾼다

I've packaged everything into a GitHub repo with all three prompts and the original video transcript.

나는 세 개의 프롬프트와 원본 비디오 대본을 모두 포함해서 GitHub 리포지토리에 패키징했다.

View the [prompts here](https://github.com/Alexanderdunlop/ai-architecture-prompts).

[여기서 프롬프트를 확인하라](https://github.com/Alexanderdunlop/ai-architecture-prompts).

## At The End Of The Day
## 결국

Eskil's insights are great, focusing on reducing cognitive load (context switching included) and not depending on a single person.

Eskil의 통찰은 훌륭하다. 인지 부하를 줄이는 데 집중하고(컨텍스트 스위칭 포함) 한 사람에게 의존하지 않는다.

In the new AI era, this is more important than ever, if AI creates something complex or buggy you are able to replace just that module without breaking anything else.

새로운 AI 시대에서 이것은 그 어느 때보다 중요하다. AI가 복잡하거나 버그가 있는 무언가를 만들면 다른 것을 망가뜨리지 않고 그 모듈만 교체할 수 있다.

I have spent weeks testing this approach before sharing it. The results for me personally make it a no brainer. Something appeared that I would have never thought of by myself.

나는 이 접근법을 공유하기 전에 몇 주간 테스트했다. 개인적으로 얻은 결과는 이것을 당연한 선택으로 만들어준다. 내 혼자서는 절대 생각해내지 못했을 무언가가 나타났다.

_I'm not affiliated with Anthropic, Eskil Steenberg, or any of the tools mentioned. All opinions and experiences shared are based on my own developer experiences and thoughts._

_나는 Anthropic, Eskil Steenberg, 또는 언급된 어떤 도구와도 제휴 관계에 있지 않다. 공유된 모든 의견과 경험은 내 자신의 개발자 경험과 생각에 기반한다._

### Resources:
### 자료:

-   [Eskil's great youtube video](https://www.youtube.com/watch?v=sSpULGNHyoI).
-   [Eskil의 훌륭한 유튜브 비디오](https://www.youtube.com/watch?v=sSpULGNHyoI).
-   [Mentis](https://github.com/alexanderdunlop/mentis).
-   [Mentis](https://github.com/alexanderdunlop/mentis).
-   [Prompts & Transcript repo](https://github.com/Alexanderdunlop/ai-architecture-prompts).
-   [프롬프트 & 대본 리포지토리](https://github.com/Alexanderdunlop/ai-architecture-prompts).

### Related Posts:
### 관련 포스트: