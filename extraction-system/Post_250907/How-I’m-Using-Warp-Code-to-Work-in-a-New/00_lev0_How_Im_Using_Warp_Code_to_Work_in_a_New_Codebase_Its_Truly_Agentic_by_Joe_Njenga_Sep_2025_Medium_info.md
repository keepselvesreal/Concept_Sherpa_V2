# 속성
---
process_status: true
source: https://medium.com/@joe.njenga/how-im-using-warp-code-to-work-in-a-new-codebase-it-s-truly-agentic-76066c10eb36
source_type: post
source_language: english
structure_type: standalone
content_processing: unified
folder_name: How-I’m-Using-Warp-Code-to-Work-in-a-New
created_at: 2025-09-07T00:24:42.533779

# 추출
---
## 핵심 내용
Joe Njenga가 새로운 코드베이스 작업에서 Warp Code(ADE - Agentic Development Environment)를 활용한 실제 경험과 방법론을 공유하며, Warp가 단순 터미널 도구나 IDE 포크와 달리 멀티 에이전트 병렬 실행과 코드베이스 이해를 통해 개발 생산성을 크게 향상시키는 차세대 AI 코딩 도구임을 입증한 실무 가이드이다. (길이: 19775 문자)

## 상세 핵심 내용
Joe Njenga는 GosuCoder의 평가에서 Warp가 모든 AI 코딩 도구 중 1-2위를 차지했다는 점을 강조하며, Warp의 독특한 접근 방식을 소개한다. Warp는 Claude Code처럼 터미널 기반도, Cursor처럼 VS Code 포크도 아닌, IDE와 터미널이 결합된 ADE(Agentic Development Environment)로서 에이전트 중심 개발을 위해 설계되었다는 점이 핵심이다.

실제 테스트를 위해 200줄 규모의 간단한 태스크 관리 웹앱(Express 백엔드 + 바닐라 JS 프런트엔드)을 구축하고, 이를 미지의 코드베이스로 가정하여 Warp의 능력을 검증했다. 기존 방식으로는 1시간 가량 소요되던 코드베이스 분석이 30초 만에 완료되었으며, API 검증 방식, 연결 실패 처리, 에러 핸들링 버그 등 9가지 주요 이슈를 즉시 식별했다.

특히 인상적인 부분은 Warp가 단순히 코드 스니펫을 제공하는 것이 아니라, 프런트엔드와 백엔드를 아우르는 완전한 솔루션을 생성한다는 점이다. JSON 파싱 에러로 인한 서버 크래시 문제를 해결할 때, Warp는 에러 핸들링 미들웨어 추가, API 엔드포인트 업데이트, 표준화된 에러 응답 형식 적용, 입력 검증 추가 등 멀티파일 업데이트를 통한 포괄적인 해결책을 제시했다.

대규모 코드베이스에서의 고급 기능도 주목할 만하다. 실시간 코드베이스 인덱싱, 50K+ 라인 대용량 파일 지원, 프로젝트 범위 규칙 시스템(WARP.md), 멀티 레포지토리 지원, 컨텍스트 관리 등이 포함되며, 특히 병렬 에이전트 코딩 기능을 통해 여러 에이전트가 서로 다른 역할을 수행하며 협업할 수 있다.

## 상세 내용
Warp의 차별화된 가치는 단순한 코드 생성을 넘어서는 체계적인 코드베이스 이해와 상황 인식에 있다. 기존 AI 코딩 도구들이 개별 파일이나 코드 조각에 집중하는 반면, Warp는 전체 프로젝트의 맥락을 파악하고 컴포넌트 간의 관계성을 이해한다. 이는 Terminal-Bench에서 1위, SWE-bench Verified에서 75.8%라는 높은 성능 점수로도 입증된다.

실제 사용 경험에서 드러난 Warp의 강점은 '이해 vs 추측'의 차이다. 미지의 코드베이스에서 작업할 때 개발자가 겪는 가장 큰 어려움은 한 부분을 수정했을 때 다른 부분에 미치는 영향을 예측하기 어렵다는 점이다. Warp는 코드베이스 인덱싱을 통해 이러한 의존성과 상호작용을 파악하고, 변경 사항이 전체 시스템에 미치는 영향을 고려한 솔루션을 제공한다.

코드 리뷰 인터페이스의 설계도 실용적이다. 변경 사항을 시각적 diff 에디터로 보여주며, 실제 파일에 적용하기 전에 개발자가 모든 변경사항을 검토할 수 있도록 한다. 'Accept', 'Refine', 'Edit manually', 'Cancel' 옵션을 제공하여 개발자가 완전한 제어권을 유지하도록 설계되었으며, 코드는 로컬에만 저장되어 보안도 보장한다.

대규모 프로젝트에서의 확장성도 인상적이다. 계층적 구성 시스템(root WARP.md, api/WARP.md, ui/WARP.md)을 통해 프로젝트 전반의 규칙과 각 서브디렉토리별 특화 규칙을 동시에 적용할 수 있다. 마이크로서비스 아키텍처에서 여러 레포지토리 간의 의존성을 이해해야 하는 상황에서 멀티 레포지토리 지원 기능이 특히 유용하다.

병렬 에이전트 시스템은 Warp만의 독특한 접근법이다. 서로 다른 역할을 가진 여러 에이전트가 동시에 작업하며 협업할 수 있어, 복잡한 프로젝트에서 개발 효율성을 크게 향상시킨다. 이는 단순히 빠른 코드 생성을 넘어서, 품질 높은 솔루션을 체계적으로 구축할 수 있는 환경을 제공한다.

결론적으로 Warp는 AI 코딩 도구의 새로운 패러다임을 제시한다. 기존 도구들의 한계였던 컨텍스트 부족과 단편적 접근을 극복하고, 전체적이고 체계적인 코드베이스 이해를 바탕으로 한 intelligent coding assistance를 실현했다.

## 주요 화제
- **Warp의 독특한 포지셔닝**: Claude Code나 Cursor와 달리 IDE+터미널 결합형 ADE(Agentic Development Environment)로 설계
- **성능 벤치마크**: GosuCoder 평가에서 1-2위, Terminal-Bench 1위, SWE-bench Verified 75.8% 달성
- **코드베이스 이해 능력**: 30초 내 전체 프로젝트 구조 파악 및 9가지 핵심 이슈 식별
- **멀티파일 솔루션**: 프런트엔드-백엔드 통합 에러 핸들링 개선으로 5분 내 완전한 버그 수정
- **비주얼 diff 리뷰**: 변경사항 적용 전 완전한 검토 및 제어 시스템 제공
- **대규모 코드베이스 지원**: 50K+ 라인 실시간 인덱싱, 멀티 레포지토리, 계층적 규칙 시스템
- **병렬 에이전트 시스템**: 여러 에이전트의 동시 협업을 통한 개발 효율성 극대화

## 부차 화제
- **실제 테스트 앱 구성**: Express.js + 바닐라 JavaScript로 구성된 200줄 태스크 관리 웹앱
- **식별된 9가지 버그**: 구문 오류, HTTP 상태 미확인, 글로벌 에러 핸들러 부재, 잘못된 ID 처리 등
- **JSON 파싱 취약점**: 잘못된 JSON으로 인한 서버 크래시 문제와 해결 방안
- **테스트 명령어 생성**: 에러 핸들링 수정 후 자동 테스트 커맨드 제공
- **코드베이스 인덱싱 설정**: .warpindexingignore 파일과 Settings > Code > Codebase Index 관리
- **프로젝트 범위 규칙**: WARP.md, CLAUDE.md, .cursorrules 등 다양한 규칙 파일 지원
- **컨텍스트 관리**: @ 심볼을 통한 파일/폴더 검색 및 공개 URL 스크래핑 기능
- **AutoWPMCP 프로젝트**: Claude와 WordPress 연결 MCP 서버를 통한 대규모 코드베이스 테스트
- **보안 고려사항**: 로컬 레포지토리에서만 작업, 서버에 코드 미저장 정책

# 내용
---
# How Im Using Warp Code to Work in a New Codebase Its Truly Agentic by Joe Njenga Sep 2025 Medium

[

![Joe Njenga](https://miro.medium.com/v2/resize:fill:48:48/1*0Hoc7r7_ybnOvk1t8yR3_A.jpeg)



](https://medium.com/@joe.njenga?source=post_page---byline--76066c10eb36---------------------------------------)

Press enter or click to view image in full size

![Warp ADE Tutorial](https://miro.medium.com/v2/resize:fit:1050/1*aMQp4OpX0gGGCGF8Favf6w.png)

Warp Screenshot — Featured Image / By Author

Recently, I discovered Warp and have been surprised at what’s possible with Agentic Coding.

I also found out that,

Other devs are discovering it too, as GosuCoder recently [_evaluated all AI coding tools_](https://x.com/thinkverse/status/1962914145696686560?s=46&t=JoYj8tvsJswaXzpccByWQg), and **_Warp was #1 or #2 across the tests._**

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*9f1zAU1H2tD37YjrHv9h9g.png)

Screenshot of AI Coding Analysis by GosuCoder / Credit — X / [GosuCoder](https://x.com/GosuCoder/status/1962567750913794094)

AI coding tools are growing in number, making it even more confusing to pick the best for your needs, **_but the silver lining is that only a few are worth your time._**

> One such tool is Warp.

In my testing, I found it to be very different in the approach to agentic coding and its unique features, which I will unpack in this article through a practical project.

But first, what makes Warp different?

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*AYZRuLLF_wmEQ0IfSKJAhw.gif)

Warp UI and Features Demo / By Author

> **Warp, unlike other AI coding tools, has a different approach that's neither a terminal tool like Claude Code nor a VS Code IDE fork like Cursor. It's in fact a unique tool that allows you to spin multiple agents running in parallel, offering a combination approach to AI coding — you can use it in terminal mode, and run normal coding operations.**

It’s not an IDE but an ADE (Agentic Development Environment), which is essentially an IDE and terminal in one, but designed for agentic-first development.

> **Unlike Claude Code or Cursor, Warp scored #1 on Terminal-Bench and hit 75.8% on SWE-bench Verified, making it the highest-performing coding agent available.**

You can use Warp for coding in many ways; however, the best testing approach was to start by coding a new Codebase to assess its learning capabilities and then develop a production-ready codebase.

In a practical sense,

One of my common issues is when I have to start working on a new task from an existing project.

> **An example of such an instance is when you inherit a codebase with little or no documentation and need to be productive fast.**

So, I set out to test Warp using a new codebase.

Last week,

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*UF2uc0lYxZPxy7MRkb9MPA.png)

Warp Testing Demo App — Screenshot

**_I quickly built a simple Warp testing demo app — a task management web app that handles basic CRUD operations: an Express backend, a vanilla JavaScript frontend, and about 200 lines of code total._**

I wanted to use this app as my new codebase to test what’s possible with Warp.

To follow along, you’ll need to download and install Warp and get familiar with its UI — you can download it from their website [_here._](https://www.warp.dev/)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*3HPF-Ps80_HpqCWCLuHKug.gif)

Warp Download — Supports MacOS, Windows & Linux

After downloading and setting it up, let's get down to testing it.

Even with this small codebase I built, I had questions when approaching it as if it were unfamiliar.

-   How does the API handle validation?
-   What happens when the frontend loses connection?
-   Are there any hidden bugs in the error handling?

> **My old way of doing this is to spend an hour reading through files, tracing function calls, and building mental maps of how everything connects.**

But now, my approach with Warp is simple: I ask it to explain the new codebase.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*E-ys_JFgU-_PTA48qs9I4g.gif)

Within minutes, Warp had indexed the entire project and could answer specific questions about the code structure, potential issues, and improvement opportunities.

The difference isn’t just speed. It’s about understanding versus guessing.

> **When you’re working with unfamiliar code, you need confidence in your changes. You need to know that fixing one bug won’t create three others.**

Now,

Here’s how I use Warp to become productive in any new codebase, using this task management app as a real example.

I’ll show you each step with actual prompts and results.

## **Asking Warp to Summarize a Codebase**

The first thing I do with any codebase is ask Warp to give me the overview.

I opened my task management app in Warp and navigated to the project directory.

Warp immediately detected the Git repository and started indexing the source code in the background.

While indexing runs, I started with this prompt:

```
<span id="0107" data-selectable-paragraph="">Summarize <span>this</span> task management codebase - what does it <span>do</span>, <br>the architecture, and <span>where</span> are the key files? </span>
```

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*HLbF_gM38ayb2nLJz40vEw.gif)

The response included:

-   **_Main functionality: CRUD operations for tasks with in-memory storage_**
-   **_Tech stack: Express.js backend with vanilla JavaScript frontend_**
-   **_Key files: app.js (server), public/index.html (UI), public/js/app.js (frontend logic)_**
-   **_API structure: RESTful endpoints at /api/todos_**
-   **_Data flow: Frontend fetches → Express routes → in-memory array → JSON responses_**

This took 30 seconds while my manual exploration would have taken 30 minutes.

### Detailed Codebase Analysis

Once I understood the general structure, I got specific:

```
<span id="5bf7" data-selectable-paragraph=""><span>Show</span> me how error handling works <span>in</span> this app. <br><span>Are</span> there <span>any</span> potential issues?</span>
```

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*ZZt_0--8IDtA1JTW75i7kA.gif)

Detailed Codebase Analysis

> **It quickly identified nine issues with my codebase and gave me recommendations.**

### **Critical Issues & Vulnerabilities**

**1\. Syntax Errors**  
The frontend JavaScript has multiple critical syntax errors

```
<span id="de83" data-selectable-paragraph=""><br><span>const</span> response = <span>await</span> <span>fetch</span>(<span>/api/</span>todos/, {  <br><br><span>await</span> <span>fetch</span>(<span>/api/</span>todos/, {  <br><br><br>totalCount.<span>textContent</span> = <span>Total</span>: ;  <br>completedCount.<span>textContent</span> = <span>Completed</span>: ;  <br><br><br>li.<span>className</span> = 	odo-item ;  <br>li.<span>innerHTML</span> = \  </span>
```

**2\. HTTP Response Status Not Checked**  
Frontend doesn’t check if HTTP requests were successful:

```
<span id="3c9a" data-selectable-paragraph=""><span>const</span> response = <span>await</span> fetch(<span>'/api/todos'</span>);<br><span>this</span>.todos = <span>await</span> response.json(); </span>
```

Should be:

```
<span id="04cb" data-selectable-paragraph=""><span>const</span> response = <span>await</span> <span>fetch</span>(<span>'/api/todos'</span>);<br><span>if</span> (!response.<span>ok</span>) {<br>    <span>throw</span> <span>new</span> <span>Error</span>(<span>`HTTP error! status: <span>${response.status}</span>`</span>);<br>}<br><span>this</span>.<span>todos</span> = <span>await</span> response.<span>json</span>();</span>
```

**3\. No Global Error Handler**  
The Express server has no global error handler:

```
<span id="325a" data-selectable-paragraph=""><br>app.<span>use</span>(<span>(<span>err, req, res, next</span>) =&gt;</span> {<br>    <span>console</span>.<span>error</span>(err.<span>stack</span>);<br>    res.<span>status</span>(<span>500</span>).<span>json</span>({ <span>error</span>: <span>'Something went wrong!'</span> });<br>});</span>
```

**4\. Invalid ID Handling**

```
<span id="cb87" data-selectable-paragraph=""><span>const</span> id = parseInt(req.<span>params</span>.id);<br></span>
```

If someone sends _/api/todos/abc, parseInt(“abc”)_ returns NaN, causing unpredictable behavior.

**5\. No User Feedback on Errors**  
Frontend only logs errors to console — users see no error messages:

```
<span id="7d17" data-selectable-paragraph="">console.<span>error</span>(<span>'Failed to load todos:'</span>, <span>error</span>);<br></span>
```

**6\. Race Conditions**

Frontend doesn’t handle concurrent operations or loading states:

```
<span id="ab53" data-selectable-paragraph=""><span>this</span>.addTodo(title);<br>input.value = <span>''</span>; </span>
```

**7\. No Request Timeout**

Fetch requests have no timeout — they can hang indefinitely.

**8\. Missing Input Sanitization**  
Backend accepts any string as a title without sanitization:

```
<span id="5b3b" data-selectable-paragraph=""><span>const</span> { title } = req.body;<br></span>
```

**9\. JSON Parsing Vulnerability**

No limit on request body size — vulnerable to JSON bombing attacks.

Unlike basic code search, Warp understood the context and relationships between frontend and backend error scenarios.

“What happens if the server restarts? Will users lose their tasks?” and so on…

Warp explained the recommended approach to fixing the existing issues.

> **This is where Warp’s codebase indexing becomes powerful as the first step to working with a new codebase.**

Warp doesn’t just read individual files — it understands how the pieces work together.

Next, it was to test its ability to fix a bug.

## **Asking Warp to Make a Small Bug Fix**

I needed to fix actual issues in the task management app.

From my analysis, I identified a critical problem:

> **The app crashes when users send invalid JSON to the API endpoints. Time to see how Warp’s coding agent handles real bug fixes.**

### **Finding and Fixing the Bug**

I gave Warp this prompt:

```
<span id="b0bc" data-selectable-paragraph="">The server crashes <span>when</span> invalid JSON <span>is</span> sent <span>to</span> /api/todos. <br>Add proper <span>error</span> handling <span>to</span> prevent crashes <span>and</span> <span>return</span> meaningful <span>error</span><br> messages.</span>
```

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*ReL40YLX8oELcKKIOlYY9g.gif)

Warp immediately identified the problem in different files, and it created a task list that would address each of these errors one after another, and this included :

-   Add JSON parsing error middleware
-   Add a global error handler
-   Add input validation middleware
-   Add request size and rate limiting

It started working on the error, fixed one after another, and provided the code with the diff and the options to accept or reject the changes.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*hJqyOjkhWuro6ztuLIOueA.png)

Instead of just showing me code snippets, Warp generated a complete solution:

1.  Added error-handling middleware for JSON parsing
2.  Updated API endpoints with try-catch blocks
3.  Standardized error response format
4.  Added input validation for required fields

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*Sl0CAeg5GSP2apU2Uy0PzA.gif)

Here’s what impressed me: **_Warp didn’t just fix the immediate issue. It improved error handling across the entire application following consistent patterns._**

### Multi-File Updates

The fix involved changes to multiple parts of the codebase:

**Backend changes:**

-   Added JSON error handling middleware
-   Updated all API endpoints with proper error responses
-   Added input validation for task creation

**Frontend changes:**

-   Updated error handling in public/js/app.js
-   Added user-friendly error messages
-   Improved network failure handling

> **This is where Warp wins — It understands the full application context and makes coordinated changes across the frontend and backend.**

### **Testing the Fix**

I asked Warp to help test the fix:

```
<span id="dc69" data-selectable-paragraph="">Generate commands <span>to</span> test the <span>error</span> handling we just added</span>
```

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*S4tb5pb0rRWeqTmVzP_hnw.gif)

It generated all the commands necessary to test this app and fixed all the errors.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*RWQc74ifLCkYjxELMn0Fqw.gif)

The server now returns proper error responses instead of crashing. The frontend displays meaningful messages to users.

> **This complete debugging and fixing process took 5 minutes with Warp, compared to what would have been an hour of manual work.**

## **Reviewing Changes Before Applying Them**

When Warp’s agent generates code changes, it opens them in a built-in visual diff editor before applying anything to your files.

This is where Warp’s approach differs from tools that immediately apply changes or show you text suggestions.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*99CFr8yvJzRDbh30lXx8mw.gif)

Based on the documentation, here’s how the review process works:

### Visual Diff Interface

Changes are grouped into clear hunks for easy inspection. Use the UP and DOWN arrow keys (or mouse clicks) to move between hunks.

**_For multi-file changes, use the LEFT and RIGHT arrow keys to switch between files._**

The interface shows you exactly what will change before any modifications are made to your actual files.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*f1HC_8vKCwbvv3bg-cqH5w.gif)

### Control Over Changes

You have several options when reviewing:

-   **Accept**: Once satisfied with the changes, you can apply the diffs using ENTER or by clicking “Accept Changes” to apply the modifications. These modifications will not be applied to the files unless you explicitly accept them.
-   **Refine**: Press R or select the “Refine” button to provide follow-up instructions in natural language. The agent will regenerate the diff based on your input.
-   **Edit manually**: To manually adjust the code, press E or click “Edit” to switch into an editable view.
-   **Cancel**: To cancel a pending operation, use CTRL-C (on Mac, Windows, or Linux systems). Similarly, you can exit the editor at any time with ESC.

### No Automatic Application

Code diffs generated by Warp are never stored on their servers.

> **Warp coding agent only works on local repositories.**

Nothing gets changed in your codebase until you explicitly approve it. This gives you complete control over what modifications happen to your code.

> **I also liked the simple Code review UI that gives you easy navigation and a simple way to track changes :**

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*zNMPy9pmKPrV2hTZBphasg.png)

## Advanced Features for Larger Codebases

My task management app was just a starting point.

Warp’s advanced features become essential when working with larger, more complex projects.

## Codebase Indexing for Scale

Warp indexes your Git-tracked codebase to help Agents understand your code and generate accurate, context-aware responses.

**_No code is stored on Warp servers._**

Warp is designed for professional environments and supports real-time codebase indexing and large files with over 50K+ lines.

To test it,

I pulled one of my recent large codebases of an MCP server I built to connect Claude to WordPress — [**AutoWPMCP**](https://medium.com/@joe.njenga/i-built-a-claude-to-wordpress-mcp-server-to-fully-automate-your-site-try-it-here-da89a1b5d431)**.**

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*hLvdi-BjRilS6M9q_en2Ow.gif)

It handles a large codebase indexing with ease and does not hang or crash like other tools I have tested before.

Here's how indexing works:

-   You can view and manage your indexed codebases under Settings > Code > Codebase Index. You can also choose whether to automatically index new folders as you navigate them.
-   For large projects, Warp supports several ignore files to give you control over what gets indexed. This allows each developer to focus context on the parts of the codebase most relevant to their work.
-   You can use .warpindexingignore files to exclude specific content, similar to how .gitignore works.

### **1) Project-Scoped Rules**

Project-Scoped Rules live in your codebase and apply automatically when working within that project.

They’re stored in a WARP.md file

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*kbq-C845BuJ877yXccJ6jA.gif)

The rules system supports hierarchical configuration:

Warp automatically applies the WARP.md file in both the root directory and the current directory. If you edit files in another subdirectory, Warp makes a best-effort attempt to include that subdirectory’s WARP.md as well.

This means you can have:

-   Project-wide rules in the root WARP.md
-   API-specific rules in api/WARP.md
-   Frontend-specific rules in ui/WARP.md

Warp currently supports the following Rules files: CLAUDE.md, .cursorrules, AGENT.MD, AGENTS.md, GEMINI.md, .clinerules, .windsurfrules, .github/copilot-instructions.md

### 2) Multi-Repository Support

Warp supports referencing context across multiple indexed repositories.

This is particularly useful for microservice architectures where you need to understand dependencies between different codebases.

### 3) Context Management

Using the @ symbol to search for and attach a file or folder from the project root. Additionally, no codebase indexing (via Codebase Context) is required — file search is available immediately in any Git-initialized directory.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*mCFravfgVJLCuGxi7I2f6g.gif)

You can also attach a public URL to a prompt to provide website content as context.

When a URL is included, the agent will scrape the page and extract relevant information to inform its response.

These features transform how you work with complex codebases by providing intelligent context awareness without manual setup.

## Parallel Agentic Coding

One of the features that impressed me with Warp is the ability to spin multiple agents working together. You can create various agents and assign them different roles.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*2-6g-svkqU36iGYEhSTcGA.gif)

_This is a feature I would like to explore further in my upcoming tutorial. If you haven't joined us yet,_ [**_consider following me on Medium_**](https://medium.com/@joe.njenga) _to stay updated on other Warp tutorials._

## **Final Thoughts**

Working with unfamiliar codebases doesn't have to be intimidating anymore.

> **What used to take hours of manual exploration now takes minutes. Warp's approach feels very natural and easy..**

My task management app was simple, but the workflow scales. Whether you're debugging a microservice architecture or contributing to an open-source project with thousands of files, the same principles apply.

> Ask questions instead of guessing. Let AI handle reconnaissance while you focus on solving real problems. Review changes before applying them.

The combination of codebase indexing, intelligent diff management, and project-scoped rules creates a development experience that feels both powerful and safe.

After testing Warp's capabilities on several projects, I understand why it scored #1 on [**_Terminal-Bench_**](https://www.tbench.ai/leaderboard)**.**

> **Have you tested Warp, and what was your experience? Let us know in the comments below.**

# 구성
---
