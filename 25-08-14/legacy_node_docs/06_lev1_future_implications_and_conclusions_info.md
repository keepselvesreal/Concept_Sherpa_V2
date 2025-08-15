# 속성
process_status: true

# 추출

## 핵심 내용
AI 모델의 진정한 가치는 개별적인 성능이 아니라 복잡한 도구 체인을 통한 실제 업무 수행 능력에서 드러나며, 앞으로는 작업별로 성능, 비용, 속도를 적절히 균형잡는 엔지니어링 능력이 핵심이 될 것입니다. 더 많은 컴퓨팅 자원이 확보된 현재, 단일 모델보다는 전문화된 소형 에이전트부터 온디바이스 모델까지 다양한 옵션을 활용할 수 있는 인프라와 도구를 구축하는 것이 중요합니다.

## 상세 핵심 내용
### 현재 진행 중인 평가 프레임워크

현재 우리가 수행하고 있는 작업은 agentic prompt를 기반으로 한 모델 평가입니다. 평가 기준은 **성능(Performance)**, **속도(Speed)**, **비용(Cost)**의 세 가지 핵심 요소로 구성됩니다. 모델이 작업을 완수하지 못한다면, 속도나 비용은 의미가 없다는 것이 기본 전제입니다.

평가 결과에 따르면, 현실적인 성능 평가에서는 모든 모델이 완벽하지 않습니다. 특히 Opus는 뛰어난 성능에도 불구하고 극도로 높은 비용 문제를 보여주며, GPT-5는 예상보다 많은 토큰을 소모하며 비효율적인 모습을 보였습니다.

### 산업 혁신의 핵심 이해

이번 주는 breakthrough week으로, 그 어느 때보다 많은 컴퓨팅 파워에 접근할 수 있게 되었습니다. 이러한 혁신을 이해하고 활용할 수 있는 이유는 산업의 근본적 수준에서의 이해에 기반합니다.

모든 AI 작업은 **세 가지 핵심 개념**에 기반합니다:
- **Context(맥락)**
- **Model(모델)**  
- **Prompt(프롬프트)**

이 세 요소를 이해한다면 평가 시스템, 벤치마크, 에이전트를 구축할 수 있습니다. 모든 것이 이 기본 구조 위에 구축되기 때문입니다.

### 패러다임의 전환

현재 AI 개발에서 중요한 패러다임 전환이 일어나고 있습니다:

**이전**: 개별 프롬프트나 단일 모델 중심
**현재**: 긴 도구 호출 체인에서 모델이 수행할 수 있는 작업 중심

진정한 모델의 가치 제안은 **실제 end-to-end 작업**에서 드러나고 있습니다. 개별적인 응답보다는 연속적인 작업 수행 능력이 핵심 평가 지표가 되었습니다.

### 전략적 트레이드오프 관리

미래의 성공은 **적절한 시점에 성능, 비용, 속도 간의 트레이드오프를 어떻게 관리하느냐**에 달려 있습니다. 모든 작업에 최고급 모델(Opus 4)이 필요한 것은 아닙니다:

**모델 선택 전략**:
- **GPT-5**: Opus 4보다 훨씬 저렴한 대안
- **Mini 모델**: 더 경제적인 옵션
- **Sonnet 4**: 특정 작업에 적합한 스케일링
- **전문화된 소형 에이전트**: 맞춤형 솔루션
- **온디바이스 모델**: 미래 지향적 인프라

### 미래 준비 전략

#### 인프라 및 도구 구축
현재 시점에서 중요한 것은 **미래를 위한 인프라와 도구를 구축**하는 것입니다. 소형 온디바이스 모델들이 지속적으로 개선되고 있으므로, 이들이 준비되었을 때 즉시 활용할 수 있는 체계를 마련해야 합니다.

#### 역량 기반 투자
앞으로는 **모든 모델에 대한 투자를 늘려** 어떤 모델이 어떤 작업을 수행할 수 있는지 파악하고, 올바른 트레이드오프를 만들 수 있는 능력을 구축할 계획입니다.

### 엔지니어링의 본질

엔지니어링의 핵심은 **트레이드오프**입니다: 성능, 속도, 비용. 하루 중 다른 시간에, 작업하는 태스크에 따라 다른 요소들이 중요해집니다. 이러한 동적 우선순위 조정 능력이 미래 AI 시스템 활용의 핵심 역량이 될 것입니다.

### 지속적 학습과 적응

결론적으로, 현재의 AI 혁신 속도와 다양성을 고려할 때, 가장 중요한 것은 **지속적인 학습과 적응 능력**입니다. 기술적 기반을 탄탄히 하고, 다양한 옵션을 이해하며, 상황에 맞는 최적의 선택을 할 수 있는 능력을 기르는 것이 미래 성공의 열쇠입니다.

## 주요 화제
- 에이전트 성능 평가 기준: 성능, 속도, 비용의 3가지 핵심 지표를 통한 모델 평가 체계와 실제 작업 수행 능력에 대한 중요성

- 모델별 비용 효율성 분석: Opus의 높은 비용, GPT-5의 토큰 소모 문제, 각 모델의 가격 대비 성능 비교와 경제성 평가

- AI 산업 컴퓨팅 자원의 혁신: 이전보다 더 많은 컴퓨팅 파워 활용 가능성과 이를 통한 산업 발전 동력

- 기본 원리 기반 기술 이해: Context, Model, Prompt라는 3대 핵심 요소를 통한 AI 시스템의 근본적 구조 파악

- 개별 모델에서 도구 체인으로의 패러다임 전환: 단일 모델 성능보다는 연속적인 도구 호출을 통한 실제 업무 처리 능력의 중요성 증대

- 상황별 모델 선택 전략: 업무 특성에 따른 적절한 모델 선택(Opus 4, GPT-5, Sonnet 4, Mini 등)과 성능-비용-속도 간의 최적 균형점 찾기

- 전문화된 소형 에이전트 개발: Nano Agent 코드베이스를 활용한 맞춤형 에이전트 구축과 에이전트 코딩의 기초 이해

- 온디바이스 모델의 미래 가능성: 소형 로컬 모델의 발전 전망과 이에 대비한 인프라 구축의 필요성

- 엔지니어링 트레이드오프 원칙: 작업과 시점에 따라 달라지는 성능-속도-비용 간의 우선순위 결정과 최적화 전략

- 지속적인 모델 투자와 역량 매핑: 다양한 모델들의 특성과 적합한 업무 영역을 파악하기 위한 지속적인 연구와 투자의 중요성

## 부차 화제
- 모델 성능 평가의 다차원적 접근법: 성능, 속도, 비용의 삼각 측정을 통한 종합적 모델 평가 방법론

- 특정 모델들의 비용 효율성 분석: Opus의 높은 비용 문제와 GPT5의 예상치 못한 토큰 소비량 증가 현상

- API를 통한 모델 성능의 일관성 문제: GPT5가 API 환경에서 보이는 불안정한 성능과 예측 가능성 부족

- 컴퓨팅 자원 접근성의 급격한 향상: 현재 시점에서 이전보다 훨씬 많은 컴퓨팅 파워를 활용할 수 있는 환경 변화

- AI 개발의 핵심 삼각구조 이론: 컨텍스트, 모델, 프롬프트라는 세 가지 기본 요소를 통한 모든 AI 시스템 구축 방법론

- 도구 체인 기반 모델 활용의 패러다임 전환: 개별 프롬프트나 모델보다는 연속적인 도구 호출을 통한 실제 업무 수행 능력의 중요성

- 상황별 모델 선택 최적화 전략: 작업의 성격과 우선순위에 따른 적절한 모델 선택과 성능-비용-속도 간의 균형점 찾기

- 소형 특화 에이전트 개발 가능성: 나노 에이전트 코드베이스를 기반으로 한 맞춤형 소형 에이전트 구축 방안

- 온디바이스 모델의 미래 발전 전망: 소형 로컬 모델들의 성능 향상과 이를 위한 인프라 준비 필요성

- 모델별 작업 능력 매핑의 중요성: 각 모델이 수행 가능한 작업 유형을 파악하여 최적의 선택을 위한 데이터 축적

- 엔지니어링에서의 상황별 우선순위 변화: 하루 중 시간대와 작업 특성에 따라 달라지는 성능, 속도, 비용의 상대적 중요도

# 내용
## Future Implications and Conclusions

So, that's what we're doing here. But the key here is: here's the agentic prompt that's running. Read the readme. Give me the first 10 lines and the last 10 lines. So this is what we're evaluating our models against. So now we can say for this fundamental agent decoding task, how did our models perform?

And we are evaluating on performance. So did it do the job? Speed and cost. Obviously if the model can't do the job, it doesn't matter if it's fast or how much it costs or how cheap it is.

So, you can see kind of some rough grades here. If you look at the overall breakdown of this task, we have some rough grades. It's not all roses when you really flatten the playing field.

Take a look at Opus for instance. We all know that Opus costs, but we don't really realize how much this model costs. It's extraordinarily expensive. And you can see here, for some reason, GPT5 had to churn and turn and churn its output tokens to figure out how to get this response properly. Terrible cost there. I'm actually surprised this chewed up that many tokens. I've seen this run much better, but I have seen some weirdness with GPT5 through the API.

This has been a breakthrough week. It's very clear to me that there is more compute than ever to tap into. I'm able to understand and move and work through these innovations because I understand the industry at a fundamental level.

Everything we do is based off just one concept. The big three: context, model, and prompt. Everything is based off these. If you understand these, you can build evals, you can build benchmarks, you can build agents because they're all just scaffolded on top of these.

So, we have more compute than ever. It's not about the prompt anymore. It's not about the individual model anymore. It's about what the model can do in long chains of tool calls. The true value proposition of models is being exposed. It's real work end to end.

And the thing to keep an eye on is: do you know how to trade off performance, cost, and speed when the time is right? Because I can guarantee you, you don't always need Opus 4. You might be able to settle with GPT5, which is much cheaper, by the way, than Opus 4. Or you might be able to go further. You can just use five mini. Maybe you need to scale to Sonnet four for that task. Fine.

But maybe you can build your own specialized small agent. You can build off from the nano agent codebase that is going to be available to you. Link in the description. I'm going to clean this up and make sure it's available for you so that you can understand agentic coding at a fundamental level.

But maybe you can go even further beyond and use a small on-device model. These are only going to get better. So you want to have the infrastructure in place and the tooling in place to understand the capabilities so when it's ready you can hop on it.

I can tell you right now I'm going to be investing more into these models across the board so I know what tasks can be accomplished by what model so I can make the right tradeoff. Engineering is all about tradeoffs: performance, speed, cost. At different times of the day, based on the task you're working on, different things matter.

So super long one. Thanks for sticking with me here. Stay focused and keep building.

# 구성
