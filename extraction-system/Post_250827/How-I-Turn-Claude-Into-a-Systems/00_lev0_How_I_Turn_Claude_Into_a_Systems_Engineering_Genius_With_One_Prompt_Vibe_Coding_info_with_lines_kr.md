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
Claude를 한 번의 프롬프트로 시스템 엔지니어링 천재로 만드는 방법 Vibe Coding

Press enter or click to view image in full size
전체 크기로 이미지를 보려면 엔터를 누르거나 클릭하세요

![](https://miro.medium.com/v2/resize:fit:1050/1*UlwN36mKsWn1Hj1G-ihWSw.png)

Image I created using Midjourney then edited with Figma
Midjourney로 생성한 후 Figma로 편집한 이미지

## **How a legendary systems engineer's lecture became my most powerful AI prompt**
전설적인 시스템 엔지니어의 강의가 어떻게 내 가장 강력한 AI 프롬프트가 되었는지

[

![Alex Dunlop](https://miro.medium.com/v2/resize:fill:48:48/1*mWvQckMd9GIigTpeHXsv5A.png)



](https://medium.com/@alexjamesdunlop?source=post_page---byline--d342af0f517c---------------------------------------)

Last month I found something that changed how I architect software projects. A lecture from a C engineer named Eskil Steenberg, changed the way I think about systems.
지난 달 소프트웨어 프로젝트를 설계하는 방법을 바꾸는 무언가를 찾았습니다. Eskil Steenberg이라는 C 엔지니어의 강의가 시스템에 대한 제 생각을 바꿔놓았습니다.

I took this lecture and turned it into three AI prompts that now guide me through every refactor or new project I do.
이 강의를 가져와서 세 개의 AI 프롬프트로 만들었고, 이제 이것이 제가 하는 모든 리팩토링이나 새 프로젝트를 안내해줍니다.

[Not a Medium member? Keep reading for free by clicking here.](https://medium.com/@alexjamesdunlop/how-i-turn-claude-into-a-systems-engineering-genius-with-one-prompt-d342af0f517c?sk=94dbed9acf55dba92fc296042f5d86fe)

Instead of focusing on preventing AI from creating complex code, I can now break everything up into perfect "black boxes" that any developer _(or AI developer)_ can understand and replace.
AI가 복잡한 코드를 만드는 것을 방지하는데 집중하는 대신, 이제 모든 것을 어떤 개발자 _(또는 AI 개발자)_ 든지 이해하고 교체할 수 있는 완벽한 "블랙박스"로 나눌 수 있습니다.

## The Problem That Led Me Here
여기까지 오게 된 문제

Recently, [Mentis](https://medium.com/vibe-coding/why-im-open-sourcing-the-component-every-chat-app-needs-09ea6fe44f9b) _(my open-source project)_ has had complex bugs which led me to hit a massive wall. Massive shout out to [Abdelrahman](https://github.com/abdelrahmanrafaat) for helping to test and report these issues.
최근에 [Mentis](https://medium.com/vibe-coding/why-im-open-sourcing-the-component-every-chat-app-needs-09ea6fe44f9b) _(제 오픈소스 프로젝트)_ 에서 복잡한 버그들이 발생해 엄청난 장벽에 부딪혔습니다. 이러한 문제들을 테스트하고 신고해준 [Abdelrahman](https://github.com/abdelrahmanrafaat)에게 큰 감사를 드립니다.

Press enter or click to view image in full size
전체 크기로 이미지를 보려면 엔터를 누르거나 클릭하세요

![](https://miro.medium.com/v2/resize:fit:1050/1*xI-IRckpmO2sQvnVUgvqNg.png)

Complex issues were caused by weird DOM interactions with React
복잡한 문제들은 React와의 이상한 DOM 상호작용으로 인해 발생했습니다

Line 91: A lot of the problems stem from DOM manipulation with React, these kinds of bugs make me question my life and sometimes why I started the project in the first place.
많은 문제들이 React와의 DOM 조작에서 비롯되었는데, 이런 종류의 버그들은 제 인생과 때로는 왜 처음에 이 프로젝트를 시작했는지까지 의문을 갖게 만듭니다.

Line 93: The codebase started to grow into a mess where fixing one issue broke another. My tests couldn't catch everything because the DOM would render differently than how React intended.
코드베이스가 한 문제를 고치면 다른 문제가 생기는 엉망으로 자라기 시작했습니다. DOM이 React가 의도한 것과 다르게 렌더링되어 제 테스트로는 모든 것을 잡아낼 수 없었습니다.

## The Discovery That Changed My Software Approach
제 소프트웨어 접근 방식을 바꾼 발견

Line 97: While taking a break from fixing issues, I came across Eskil Steenberg's lecture "Architecting LARGE Software Projects". This guy builds everything from 3D engines to networked games, all in C.
문제 해결에서 잠시 휴식을 취하던 중 Eskil Steenberg의 "대규모 소프트웨어 프로젝트 설계" 강의를 발견했습니다. 이분은 3D 엔진부터 네트워크 게임까지 모든 것을 C로 구축합니다.

Line 99: These are my favourite of his core principles:
다음은 그의 핵심 원칙 중 제가 가장 좋아하는 것들입니다:

Line 101: **Constant developer velocity** — _regardless of project size._
**지속적인 개발자 속도** — _프로젝트 크기와 관계없이._

Line 102: **One module, one person** — _one person should be able to do everything (given enough time)._
**한 모듈, 한 사람** — _한 사람이 모든 것을 할 수 있어야 합니다 (충분한 시간이 주어진다면)._

Line 103: **Everything should be replaceable** — _if you can't understand it, you can rewrite it easily._
**모든 것이 교체 가능해야 한다** — _이해할 수 없다면, 쉽게 다시 작성할 수 있어야 합니다._

Line 104: **Black box interfaces** — _modules communicate through clean APIs._
**블랙박스 인터페이스** — _모듈들은 깔끔한 API를 통해 소통합니다._

Line 105: **Writing 5 lines today** — _rather than editing 1 line later (context switching affects velocity)._
**오늘 5줄 작성하기** — _나중에 1줄 편집하는 것보다 (컨텍스트 스위칭이 속도에 영향을 미칩니다)._

Line 107: He also suggested making modules that can be reused in different projects which I really like.
그는 또한 다른 프로젝트에서 재사용할 수 있는 모듈을 만들 것을 제안했는데, 이것이 정말 마음에 듭니다.

Line 109: In the lecture, he gives an example of how to build a system built for a fighter jet. This helped me realise how much simpler my task is, but my approach needed to change.
강의에서 그는 전투기용 시스템을 구축하는 방법의 예시를 제공했습니다. 이것은 제 작업이 얼마나 단순한지를 깨닫게 해주었지만, 제 접근 방식을 바꿔야 한다는 것도 알게 되었습니다.

Line 111: > "It's faster to write five lines of code today than to write one line today and then have to edit it in the future." — Eskil Steenberg
> "오늘 코드 5줄을 작성하는 것이 오늘 1줄을 작성하고 나중에 편집해야 하는 것보다 빠르다." — Eskil Steenberg

Line 113: I would highly recommend watching the video:
비디오를 강력히 추천합니다:

## Converting The Theory Of The Lecture
강의의 이론을 변환하기

Line 117: After taking in Eskil's amazing lecture, it took me a while to really understand _(I even rewatched it a couple of times)_.
Eskil의 놀라운 강의를 들은 후, 정말로 이해하는데 시간이 걸렸습니다 _(심지어 몇 번 다시 봤습니다)_.

Line 119: The main thing I struggled with was Eskil's lecture was built for C, a low level language and I'm building for React.
제가 어려워한 주된 것은 Eskil의 강의가 저수준 언어인 C를 위해 만들어졌는데 저는 React로 구축하고 있다는 것이었습니다.

Line 121: That's when I had an amazing idea, I took the complete transcript of the lecture and built prompts from it.
그때 놀라운 아이디어가 떠올랐습니다. 강의의 완전한 대본을 가져와서 그것으로부터 프롬프트를 구축했습니다.

Line 123: I built three prompts that I use:
제가 사용하는 세 개의 프롬프트를 만들었습니다:

Line 125: **Claude Code Prompt** — _For hands on development._
**Claude Code 프롬프트** — _실습 개발용._

Line 126: **Claude Prompt** — _For planning and designing._
**Claude 프롬프트** — _계획 및 설계용._

Line 127: **Cursor Prompt** — _Debugging and mainly testing strategies._
**Cursor 프롬프트** — _디버깅 및 주로 테스트 전략용._

Line 129: These prompts are built for any language and any framework. Teaching AI to think on a much larger scale.
이 프롬프트들은 어떤 언어와 프레임워크든 사용할 수 있도록 구축되었습니다. AI가 훨씬 더 큰 규모로 생각하도록 가르칩니다.

## The Lightbulb Context Moment
번뜩이는 컨텍스트 순간

Line 133: The prompts were working great, but they had a big issue. They worked better for new projects only. That's when I remembered another technique I have been using.
프롬프트들은 훌륭하게 작동했지만 큰 문제가 있었습니다. 새 프로젝트에서만 더 잘 작동했습니다. 그때 제가 사용해왔던 다른 기법이 기억났습니다.

Line 135: The big problem with AI refactoring is you need certainty. With certainty, you need control over what's changing.
AI 리팩토링의 큰 문제는 확실성이 필요하다는 것입니다. 확실성을 위해서는 무엇이 변화하고 있는지에 대한 통제가 필요합니다.

Line 137: The architecture prompts provide excellent plans for breaking refactors into bite sized chunks. My workflow has become:
아키텍처 프롬프트들은 리팩토링을 한 입 크기의 덩어리로 나누는 뛰어난 계획을 제공합니다. 제 워크플로우는 다음과 같아졌습니다:

Line 139: Focus on a single folder.
단일 폴더에 집중합니다.

Line 140: Pass the context and prompt to Claude.
컨텍스트와 프롬프트를 Claude에 전달합니다.

Line 141: Come up with a strategic plan.
전략적 계획을 세웁니다.

Line 142: Execute that plan using either Claude Code or Cursor.
Claude Code 또는 Cursor를 사용해 그 계획을 실행합니다.

## My Real Results
제 실제 결과

Line 146: I passed my entire Mentis context into Claude with the new architecture prompt and asked for some help.
새로운 아키텍처 프롬프트와 함께 제 전체 Mentis 컨텍스트를 Claude에 전달하고 도움을 요청했습니다.

Line 148: _The response blew me away._
_그 답변이 저를 깜짝 놀라게 했습니다._

Line 150: I needed to interface directly with the DOM instead of relying on React's unpredictable behaviour.
React의 예측 불가능한 동작에 의존하는 대신 DOM과 직접 인터페이스해야 했습니다.

Line 152: This new black box DOM interface implementation would allow me to completely reuse the code for different frameworks with minimal overhead.
이 새로운 블랙박스 DOM 인터페이스 구현은 최소한의 오버헤드로 다른 프레임워크에서 코드를 완전히 재사용할 수 있게 해줄 것입니다.

Line 154: Something I never thought would be possible and something directly the prompt came up with directly.
제가 가능하다고 생각해본 적이 없었던 것이고, 프롬프트가 직접 떠올린 것입니다.

## Why This Matters With AI Development
이것이 AI 개발에서 중요한 이유

Line 158: Following Eskil's principle: "**Everything should be replaceable"** — _if you can't understand it, you can rewrite it easily._
Eskil의 원칙을 따르면: "**모든 것이 교체 가능해야 한다"** — _이해할 수 없다면, 쉽게 다시 작성할 수 있어야 합니다._

Line 160: We can transform some of AI's biggest weaknesses into a new superpower by structuring our systems as modular, replaceable components.
시스템을 모듈형의 교체 가능한 컴포넌트로 구조화함으로써 AI의 가장 큰 약점들을 새로운 슈퍼파워로 변환할 수 있습니다.

Line 162: Now when AI generates code we don't understand, we can easily replace that module. This allows AI to build something fast while giving us the freedom to refactor or completely rewrite modules when needed.
이제 AI가 우리가 이해하지 못하는 코드를 생성할 때, 그 모듈을 쉽게 교체할 수 있습니다. 이는 AI가 빠르게 무언가를 구축할 수 있게 하면서 필요할 때 모듈을 리팩토링하거나 완전히 다시 작성할 자유를 제공합니다.

Line 164: Everything becomes manageable bite sized chunks.
모든 것이 관리 가능한 한 입 크기의 덩어리가 됩니다.

Line 166: _Use the power of AI with the power of large systems._
_대규모 시스템의 힘과 함께 AI의 힘을 사용하세요._

## These Prompts Change Everything
이 프롬프트들은 모든 것을 바꿉니다

Line 170: I've packaged everything into a GitHub repo with all three prompts and the original video transcript.
모든 세 개의 프롬프트와 원본 비디오 대본을 포함해 모든 것을 GitHub 저장소에 패키지화했습니다.

Line 172: View the [prompts here](https://github.com/Alexanderdunlop/ai-architecture-prompts).
[여기서 프롬프트들을 확인하세요](https://github.com/Alexanderdunlop/ai-architecture-prompts).

## At The End Of The Day
하루를 마무리하며

Line 176: Eskil's insights are great, focusing on reducing cognitive load (context switching included) and not depending on a single person.
Eskil의 통찰은 훌륭하며, 인지적 부하를 줄이는 것 (컨텍스트 스위칭 포함)과 한 사람에게 의존하지 않는 것에 집중합니다.

Line 178: In the new AI era, this is more important than ever, if AI creates something complex or buggy you are able to replace just that module without breaking anything else.
새로운 AI 시대에는 이것이 그 어느 때보다 중요합니다. AI가 복잡하거나 버그가 있는 무언가를 생성한다면 다른 것을 깨뜨리지 않고 그 모듈만 교체할 수 있습니다.

Line 180: I have spent weeks testing this approach before sharing it. The results for me personally make it a no brainer. Something appeared that I would have never thought of by myself.
이것을 공유하기 전에 이 접근법을 테스트하는데 몇 주를 보냈습니다. 개인적으로 제게는 결과가 당연한 선택이 되었습니다. 제 스스로는 절대 생각해내지 못했을 무언가가 나타났습니다.

Line 182: _I'm not affiliated with Anthropic, Eskil Steenberg, or any of the tools mentioned. All opinions and experiences shared are based on my own developer experiences and thoughts._
_저는 Anthropic, Eskil Steenberg, 또는 언급된 어떤 도구와도 제휴 관계가 없습니다. 공유된 모든 의견과 경험은 제 개인적인 개발자 경험과 생각에 기반합니다._

### Resources:
리소스:

Line 186: [Eskil's great youtube video](https://www.youtube.com/watch?v=sSpULGNHyoI).
[Eskil의 훌륭한 유튜브 비디오](https://www.youtube.com/watch?v=sSpULGNHyoI).

Line 187: [Mentis](https://github.com/alexanderdunlop/mentis).

Line 188: [Prompts & Transcript repo](https://github.com/Alexanderdunlop/ai-architecture-prompts).
[프롬프트 & 대본 저장소](https://github.com/Alexanderdunlop/ai-architecture-prompts).

### Related Posts:
관련 게시글:

# 구성
---