# 속성
---
process_status: true
source: https://medium.com/@joe.njenga/how-im-using-warp-code-to-work-in-a-new-codebase-it-s-truly-agentic-76066c10eb36
source_type: post
source_language: english
structure_type: standalone
content_processing: unified
folder_name: How-I’m-Using-Warp-Code-to-Work-in-a-New
created_at: 2025-09-06T23:55:37.977196

# 추출
---
## 핵심 내용
Joe Njenga가 Warp라는 AI 코딩 도구를 사용해 새로운 코드베이스에서 빠르게 생산성을 높이는 방법을 소개하며, Warp가 다른 AI 코딩 도구들과 차별화되는 점과 실제 사용 경험을 태스크 관리 웹앱 프로젝트를 통해 설명한 글 (길이: 19775 문자)

## 상세 핵심 내용
Warp는 기존의 Claude Code나 Cursor와는 다른 접근 방식을 채택한 ADE(Agentic Development Environment)로, IDE와 터미널을 하나로 통합한 도구다. GosuCoder의 평가에서 모든 AI 코딩 도구 중 1-2위를 차지했으며, Terminal-Bench에서 1위, SWE-bench Verified에서 75.8%의 성과를 거뒀다.

저자는 200줄 규모의 Express 백엔드와 바닐라 자바스크립트 프론트엔드로 구성된 태스크 관리 앱을 새로운 코드베이스로 간주하고 Warp를 테스트했다. 기존 방식으로는 한 시간이 걸렸을 코드 이해가 30초 만에 가능했고, 버그 수정과 에러 핸들링 개선이 5분 만에 완료됐다.

Warp의 가장 큰 강점은 코드베이스 전체를 인덱싱해서 파일 간의 관계와 맥락을 이해한다는 점이다. 단순히 개별 파일을 읽는 것이 아니라, 프론트엔드와 백엔드 간의 에러 시나리오까지 파악해서 협조적인 변경사항을 만들어낸다.

## 상세 내용
**Warp의 차별화 포인트와 아키텍처**
Warp는 기존 AI 코딩 도구들의 한계를 극복한 독특한 접근법을 제시한다. Claude Code처럼 터미널 도구도 아니고, Cursor처럼 VS Code IDE 포크도 아닌, 완전히 새로운 형태의 ADE(Agentic Development Environment)다. 여러 에이전트를 병렬로 실행할 수 있는 조합 접근법을 통해 터미널 모드와 일반 코딩 작업을 모두 지원한다.

**실전 테스트를 통한 성능 검증**
저자가 구축한 태스크 관리 웹앱을 통한 실전 테스트에서 Warp의 진가가 드러났다. 코드베이스 요약 요청 시 30초 만에 주요 기능(CRUD 작업), 기술 스택(Express.js + 바닐라 JS), 핵심 파일들, API 구조, 데이터 플로우까지 완벽하게 파악했다. 수동 탐색으로는 30분이 걸렸을 작업이었다.

**포괄적인 에러 분석과 수정 능력**
단순한 에러 핸들링 질의에 대해 Warp는 9가지 심각한 문제점을 식별했다: 문법 오류, HTTP 응답 상태 미확인, 글로벌 에러 핸들러 부재, 잘못된 ID 처리, 사용자 피드백 부재, 경합 조건, 요청 타임아웃 부재, 입력 검증 부재, JSON 파싱 취약점 등. 더 인상적인 것은 문제 식별에서 그치지 않고 전체 애플리케이션에 일관된 패턴으로 개선사항을 적용했다는 점이다.

**시각적 Diff 인터페이스와 변경사항 제어**
Warp는 변경사항을 바로 적용하지 않고 내장된 시각적 diff 에디터에서 먼저 검토할 수 있게 한다. 변경사항이 명확한 덩어리로 그룹화되어 UP/DOWN 키로 이동하고, 다중 파일 변경 시 LEFT/RIGHT 키로 파일을 전환할 수 있다. 수락, 개선, 수동 편집, 취소 등의 옵션을 제공해 개발자가 완전한 제어권을 가진다.

**대규모 코드베이스 지원과 고급 기능**
Git 추적 코드베이스를 인덱싱해서 50K+ 라인의 대용량 파일도 지원한다. 프로젝트별 규칙(WARP.md), 다중 저장소 지원, @ 심볼을 통한 컨텍스트 관리, 공개 URL 스크래핑 등의 고급 기능을 제공한다. 마이크로서비스 아키텍처에서 여러 코드베이스 간의 종속성을 이해하는 데 특히 유용하다.

**병렬 에이전트 시스템의 잠재력**
여러 에이전트를 동시에 실행해서 서로 다른 역할을 부여할 수 있는 기능은Warp만의 독특한 강점이다. 이를 통해 복잡한 프로젝트에서 각기 다른 전문 영역을 담당하는 에이전트들이 협력해서 작업할 수 있다.

## 주요 화제
- **Warp의 독특한 위치**: ADE(Agentic Development Environment)로서 기존 도구들과 차별화
- **성능 벤치마크**: Terminal-Bench 1위, SWE-bench Verified 75.8% 달성으로 최고 성능 입증
- **코드베이스 이해 속도**: 수동으로 30분 걸리던 작업을 30초에 완료하는 혁신적 효율성
- **포괄적 에러 분석**: 9가지 심각한 문제점을 자동으로 식별하고 해결책 제시
- **시각적 변경사항 관리**: diff 에디터를 통한 안전한 코드 변경 검토 및 적용
- **대규모 프로젝트 지원**: 50K+ 라인 코드와 다중 저장소 인덱싱 능력

## 부차 화제
- **GosuCoder 평가**: 모든 AI 코딩 도구를 비교 평가한 결과에서 Warp가 상위권 차지
- **태스크 관리 앱 테스트**: 200줄 규모의 Express + 바닐라 JS 프로젝트로 실전 테스트
- **JSON 파싱 버그 수정**: 서버 크래시 문제를 5분 만에 해결한 실제 사례
- **다중 파일 업데이트**: 프론트엔드와 백엔드를 동시에 수정하는 협조적 변경
- **프로젝트별 규칙 시스템**: WARP.md 파일을 통한 계층적 구성 지원
- **병렬 에이전트 기능**: 여러 에이전트를 동시 실행해서 역할 분담하는 고급 기능
- **AutoWPMCP 프로젝트**: 대규모 코드베이스 테스트용으로 사용한 WordPress MCP 서버
- **컨텍스트 관리 기능**: @ 심볼과 URL 스크래핑을 통한 지능적 컨텍스트 제공

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
