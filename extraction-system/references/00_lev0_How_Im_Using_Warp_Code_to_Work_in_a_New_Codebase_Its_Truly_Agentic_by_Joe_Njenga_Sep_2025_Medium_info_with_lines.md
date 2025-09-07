Line 1: # 속성
Line 2: ---
Line 3: process_status: true
Line 4: source: https://medium.com/@joe.njenga/how-im-using-warp-code-to-work-in-a-new-codebase-it-s-truly-agentic-76066c10eb36
Line 5: source_type: post
Line 6: source_language: english
Line 7: structure_type: standalone
Line 8: content_processing: unified
Line 9: folder_name: How-I’m-Using-Warp-Code-to-Work-in-a-New
Line 10: created_at: 2025-09-06T23:55:37.977196
Line 11: 
Line 12: # 추출
Line 13: ---
Line 14: ## 핵심 내용
Line 15: Joe Njenga가 Warp라는 AI 코딩 도구를 사용해 새로운 코드베이스에서 빠르게 생산성을 높이는 방법을 소개하며, Warp가 다른 AI 코딩 도구들과 차별화되는 점과 실제 사용 경험을 태스크 관리 웹앱 프로젝트를 통해 설명한 글 (길이: 19775 문자)
Line 16: 
Line 17: ## 상세 핵심 내용
Line 18: Warp는 기존의 Claude Code나 Cursor와는 다른 접근 방식을 채택한 ADE(Agentic Development Environment)로, IDE와 터미널을 하나로 통합한 도구다. GosuCoder의 평가에서 모든 AI 코딩 도구 중 1-2위를 차지했으며, Terminal-Bench에서 1위, SWE-bench Verified에서 75.8%의 성과를 거뒀다.
Line 19: 
Line 20: 저자는 200줄 규모의 Express 백엔드와 바닐라 자바스크립트 프론트엔드로 구성된 태스크 관리 앱을 새로운 코드베이스로 간주하고 Warp를 테스트했다. 기존 방식으로는 한 시간이 걸렸을 코드 이해가 30초 만에 가능했고, 버그 수정과 에러 핸들링 개선이 5분 만에 완료됐다.
Line 21: 
Line 22: Warp의 가장 큰 강점은 코드베이스 전체를 인덱싱해서 파일 간의 관계와 맥락을 이해한다는 점이다. 단순히 개별 파일을 읽는 것이 아니라, 프론트엔드와 백엔드 간의 에러 시나리오까지 파악해서 협조적인 변경사항을 만들어낸다.
Line 23: 
Line 24: ## 상세 내용
Line 25: **Warp의 차별화 포인트와 아키텍처**
Line 26: Warp는 기존 AI 코딩 도구들의 한계를 극복한 독특한 접근법을 제시한다. Claude Code처럼 터미널 도구도 아니고, Cursor처럼 VS Code IDE 포크도 아닌, 완전히 새로운 형태의 ADE(Agentic Development Environment)다. 여러 에이전트를 병렬로 실행할 수 있는 조합 접근법을 통해 터미널 모드와 일반 코딩 작업을 모두 지원한다.
Line 27: 
Line 28: **실전 테스트를 통한 성능 검증**
Line 29: 저자가 구축한 태스크 관리 웹앱을 통한 실전 테스트에서 Warp의 진가가 드러났다. 코드베이스 요약 요청 시 30초 만에 주요 기능(CRUD 작업), 기술 스택(Express.js + 바닐라 JS), 핵심 파일들, API 구조, 데이터 플로우까지 완벽하게 파악했다. 수동 탐색으로는 30분이 걸렸을 작업이었다.
Line 30: 
Line 31: **포괄적인 에러 분석과 수정 능력**
Line 32: 단순한 에러 핸들링 질의에 대해 Warp는 9가지 심각한 문제점을 식별했다: 문법 오류, HTTP 응답 상태 미확인, 글로벌 에러 핸들러 부재, 잘못된 ID 처리, 사용자 피드백 부재, 경합 조건, 요청 타임아웃 부재, 입력 검증 부재, JSON 파싱 취약점 등. 더 인상적인 것은 문제 식별에서 그치지 않고 전체 애플리케이션에 일관된 패턴으로 개선사항을 적용했다는 점이다.
Line 33: 
Line 34: **시각적 Diff 인터페이스와 변경사항 제어**
Line 35: Warp는 변경사항을 바로 적용하지 않고 내장된 시각적 diff 에디터에서 먼저 검토할 수 있게 한다. 변경사항이 명확한 덩어리로 그룹화되어 UP/DOWN 키로 이동하고, 다중 파일 변경 시 LEFT/RIGHT 키로 파일을 전환할 수 있다. 수락, 개선, 수동 편집, 취소 등의 옵션을 제공해 개발자가 완전한 제어권을 가진다.
Line 36: 
Line 37: **대규모 코드베이스 지원과 고급 기능**
Line 38: Git 추적 코드베이스를 인덱싱해서 50K+ 라인의 대용량 파일도 지원한다. 프로젝트별 규칙(WARP.md), 다중 저장소 지원, @ 심볼을 통한 컨텍스트 관리, 공개 URL 스크래핑 등의 고급 기능을 제공한다. 마이크로서비스 아키텍처에서 여러 코드베이스 간의 종속성을 이해하는 데 특히 유용하다.
Line 39: 
Line 40: **병렬 에이전트 시스템의 잠재력**
Line 41: 여러 에이전트를 동시에 실행해서 서로 다른 역할을 부여할 수 있는 기능은Warp만의 독특한 강점이다. 이를 통해 복잡한 프로젝트에서 각기 다른 전문 영역을 담당하는 에이전트들이 협력해서 작업할 수 있다.
Line 42: 
Line 43: ## 주요 화제
Line 44: - **Warp의 독특한 위치**: ADE(Agentic Development Environment)로서 기존 도구들과 차별화
Line 45: - **성능 벤치마크**: Terminal-Bench 1위, SWE-bench Verified 75.8% 달성으로 최고 성능 입증
Line 46: - **코드베이스 이해 속도**: 수동으로 30분 걸리던 작업을 30초에 완료하는 혁신적 효율성
Line 47: - **포괄적 에러 분석**: 9가지 심각한 문제점을 자동으로 식별하고 해결책 제시
Line 48: - **시각적 변경사항 관리**: diff 에디터를 통한 안전한 코드 변경 검토 및 적용
Line 49: - **대규모 프로젝트 지원**: 50K+ 라인 코드와 다중 저장소 인덱싱 능력
Line 50: 
Line 51: ## 부차 화제
Line 52: - **GosuCoder 평가**: 모든 AI 코딩 도구를 비교 평가한 결과에서 Warp가 상위권 차지
Line 53: - **태스크 관리 앱 테스트**: 200줄 규모의 Express + 바닐라 JS 프로젝트로 실전 테스트
Line 54: - **JSON 파싱 버그 수정**: 서버 크래시 문제를 5분 만에 해결한 실제 사례
Line 55: - **다중 파일 업데이트**: 프론트엔드와 백엔드를 동시에 수정하는 협조적 변경
Line 56: - **프로젝트별 규칙 시스템**: WARP.md 파일을 통한 계층적 구성 지원
Line 57: - **병렬 에이전트 기능**: 여러 에이전트를 동시 실행해서 역할 분담하는 고급 기능
Line 58: - **AutoWPMCP 프로젝트**: 대규모 코드베이스 테스트용으로 사용한 WordPress MCP 서버
Line 59: - **컨텍스트 관리 기능**: @ 심볼과 URL 스크래핑을 통한 지능적 컨텍스트 제공
Line 60: 
Line 61: # 내용
Line 62: ---
Line 63: # How Im Using Warp Code to Work in a New Codebase Its Truly Agentic by Joe Njenga Sep 2025 Medium
Line 64: 
Line 65: [
Line 66: 
Line 67: ![Joe Njenga](https://miro.medium.com/v2/resize:fill:48:48/1*0Hoc7r7_ybnOvk1t8yR3_A.jpeg)
Line 68: 
Line 69: 
Line 70: 
Line 71: ](https://medium.com/@joe.njenga?source=post_page---byline--76066c10eb36---------------------------------------)
Line 72: 
Line 73: Press enter or click to view image in full size
Line 74: 
Line 75: ![Warp ADE Tutorial](https://miro.medium.com/v2/resize:fit:1050/1*aMQp4OpX0gGGCGF8Favf6w.png)
Line 76: 
Line 77: Warp Screenshot — Featured Image / By Author
Line 78: 
Line 79: Recently, I discovered Warp and have been surprised at what’s possible with Agentic Coding.
Line 80: 
Line 81: I also found out that,
Line 82: 
Line 83: Other devs are discovering it too, as GosuCoder recently [_evaluated all AI coding tools_](https://x.com/thinkverse/status/1962914145696686560?s=46&t=JoYj8tvsJswaXzpccByWQg), and **_Warp was #1 or #2 across the tests._**
Line 84: 
Line 85: Press enter or click to view image in full size
Line 86: 
Line 87: ![](https://miro.medium.com/v2/resize:fit:1050/1*9f1zAU1H2tD37YjrHv9h9g.png)
Line 88: 
Line 89: Screenshot of AI Coding Analysis by GosuCoder / Credit — X / [GosuCoder](https://x.com/GosuCoder/status/1962567750913794094)
Line 90: 
Line 91: AI coding tools are growing in number, making it even more confusing to pick the best for your needs, **_but the silver lining is that only a few are worth your time._**
Line 92: 
Line 93: > One such tool is Warp.
Line 94: 
Line 95: In my testing, I found it to be very different in the approach to agentic coding and its unique features, which I will unpack in this article through a practical project.
Line 96: 
Line 97: But first, what makes Warp different?
Line 98: 
Line 99: Press enter or click to view image in full size
Line 100: 
Line 101: ![](https://miro.medium.com/v2/resize:fit:1050/1*AYZRuLLF_wmEQ0IfSKJAhw.gif)
Line 102: 
Line 103: Warp UI and Features Demo / By Author
Line 104: 
Line 105: > **Warp, unlike other AI coding tools, has a different approach that's neither a terminal tool like Claude Code nor a VS Code IDE fork like Cursor. It's in fact a unique tool that allows you to spin multiple agents running in parallel, offering a combination approach to AI coding — you can use it in terminal mode, and run normal coding operations.**
Line 106: 
Line 107: It’s not an IDE but an ADE (Agentic Development Environment), which is essentially an IDE and terminal in one, but designed for agentic-first development.
Line 108: 
Line 109: > **Unlike Claude Code or Cursor, Warp scored #1 on Terminal-Bench and hit 75.8% on SWE-bench Verified, making it the highest-performing coding agent available.**
Line 110: 
Line 111: You can use Warp for coding in many ways; however, the best testing approach was to start by coding a new Codebase to assess its learning capabilities and then develop a production-ready codebase.
Line 112: 
Line 113: In a practical sense,
Line 114: 
Line 115: One of my common issues is when I have to start working on a new task from an existing project.
Line 116: 
Line 117: > **An example of such an instance is when you inherit a codebase with little or no documentation and need to be productive fast.**
Line 118: 
Line 119: So, I set out to test Warp using a new codebase.
Line 120: 
Line 121: Last week,
Line 122: 
Line 123: Press enter or click to view image in full size
Line 124: 
Line 125: ![](https://miro.medium.com/v2/resize:fit:1050/1*UF2uc0lYxZPxy7MRkb9MPA.png)
Line 126: 
Line 127: Warp Testing Demo App — Screenshot
Line 128: 
Line 129: **_I quickly built a simple Warp testing demo app — a task management web app that handles basic CRUD operations: an Express backend, a vanilla JavaScript frontend, and about 200 lines of code total._**
Line 130: 
Line 131: I wanted to use this app as my new codebase to test what’s possible with Warp.
Line 132: 
Line 133: To follow along, you’ll need to download and install Warp and get familiar with its UI — you can download it from their website [_here._](https://www.warp.dev/)
Line 134: 
Line 135: Press enter or click to view image in full size
Line 136: 
Line 137: ![](https://miro.medium.com/v2/resize:fit:1050/1*3HPF-Ps80_HpqCWCLuHKug.gif)
Line 138: 
Line 139: Warp Download — Supports MacOS, Windows & Linux
Line 140: 
Line 141: After downloading and setting it up, let's get down to testing it.
Line 142: 
Line 143: Even with this small codebase I built, I had questions when approaching it as if it were unfamiliar.
Line 144: 
Line 145: -   How does the API handle validation?
Line 146: -   What happens when the frontend loses connection?
Line 147: -   Are there any hidden bugs in the error handling?
Line 148: 
Line 149: > **My old way of doing this is to spend an hour reading through files, tracing function calls, and building mental maps of how everything connects.**
Line 150: 
Line 151: But now, my approach with Warp is simple: I ask it to explain the new codebase.
Line 152: 
Line 153: Press enter or click to view image in full size
Line 154: 
Line 155: ![](https://miro.medium.com/v2/resize:fit:1050/1*E-ys_JFgU-_PTA48qs9I4g.gif)
Line 156: 
Line 157: Within minutes, Warp had indexed the entire project and could answer specific questions about the code structure, potential issues, and improvement opportunities.
Line 158: 
Line 159: The difference isn’t just speed. It’s about understanding versus guessing.
Line 160: 
Line 161: > **When you’re working with unfamiliar code, you need confidence in your changes. You need to know that fixing one bug won’t create three others.**
Line 162: 
Line 163: Now,
Line 164: 
Line 165: Here’s how I use Warp to become productive in any new codebase, using this task management app as a real example.
Line 166: 
Line 167: I’ll show you each step with actual prompts and results.
Line 168: 
Line 169: ## **Asking Warp to Summarize a Codebase**
Line 170: 
Line 171: The first thing I do with any codebase is ask Warp to give me the overview.
Line 172: 
Line 173: I opened my task management app in Warp and navigated to the project directory.
Line 174: 
Line 175: Warp immediately detected the Git repository and started indexing the source code in the background.
Line 176: 
Line 177: While indexing runs, I started with this prompt:
Line 178: 
Line 179: ```
Line 180: <span id="0107" data-selectable-paragraph="">Summarize <span>this</span> task management codebase - what does it <span>do</span>, <br>the architecture, and <span>where</span> are the key files? </span>
Line 181: ```
Line 182: 
Line 183: Press enter or click to view image in full size
Line 184: 
Line 185: ![](https://miro.medium.com/v2/resize:fit:1050/1*HLbF_gM38ayb2nLJz40vEw.gif)
Line 186: 
Line 187: The response included:
Line 188: 
Line 189: -   **_Main functionality: CRUD operations for tasks with in-memory storage_**
Line 190: -   **_Tech stack: Express.js backend with vanilla JavaScript frontend_**
Line 191: -   **_Key files: app.js (server), public/index.html (UI), public/js/app.js (frontend logic)_**
Line 192: -   **_API structure: RESTful endpoints at /api/todos_**
Line 193: -   **_Data flow: Frontend fetches → Express routes → in-memory array → JSON responses_**
Line 194: 
Line 195: This took 30 seconds while my manual exploration would have taken 30 minutes.
Line 196: 
Line 197: ### Detailed Codebase Analysis
Line 198: 
Line 199: Once I understood the general structure, I got specific:
Line 200: 
Line 201: ```
Line 202: <span id="5bf7" data-selectable-paragraph=""><span>Show</span> me how error handling works <span>in</span> this app. <br><span>Are</span> there <span>any</span> potential issues?</span>
Line 203: ```
Line 204: 
Line 205: Press enter or click to view image in full size
Line 206: 
Line 207: ![](https://miro.medium.com/v2/resize:fit:1050/1*ZZt_0--8IDtA1JTW75i7kA.gif)
Line 208: 
Line 209: Detailed Codebase Analysis
Line 210: 
Line 211: > **It quickly identified nine issues with my codebase and gave me recommendations.**
Line 212: 
Line 213: ### **Critical Issues & Vulnerabilities**
Line 214: 
Line 215: **1\. Syntax Errors**  
Line 216: The frontend JavaScript has multiple critical syntax errors
Line 217: 
Line 218: ```
Line 219: <span id="de83" data-selectable-paragraph=""><br><span>const</span> response = <span>await</span> <span>fetch</span>(<span>/api/</span>todos/, {  <br><br><span>await</span> <span>fetch</span>(<span>/api/</span>todos/, {  <br><br><br>totalCount.<span>textContent</span> = <span>Total</span>: ;  <br>completedCount.<span>textContent</span> = <span>Completed</span>: ;  <br><br><br>li.<span>className</span> = 	odo-item ;  <br>li.<span>innerHTML</span> = \  </span>
Line 220: ```
Line 221: 
Line 222: **2\. HTTP Response Status Not Checked**  
Line 223: Frontend doesn’t check if HTTP requests were successful:
Line 224: 
Line 225: ```
Line 226: <span id="3c9a" data-selectable-paragraph=""><span>const</span> response = <span>await</span> fetch(<span>'/api/todos'</span>);<br><span>this</span>.todos = <span>await</span> response.json(); </span>
Line 227: ```
Line 228: 
Line 229: Should be:
Line 230: 
Line 231: ```
Line 232: <span id="04cb" data-selectable-paragraph=""><span>const</span> response = <span>await</span> <span>fetch</span>(<span>'/api/todos'</span>);<br><span>if</span> (!response.<span>ok</span>) {<br>    <span>throw</span> <span>new</span> <span>Error</span>(<span>`HTTP error! status: <span>${response.status}</span>`</span>);<br>}<br><span>this</span>.<span>todos</span> = <span>await</span> response.<span>json</span>();</span>
Line 233: ```
Line 234: 
Line 235: **3\. No Global Error Handler**  
Line 236: The Express server has no global error handler:
Line 237: 
Line 238: ```
Line 239: <span id="325a" data-selectable-paragraph=""><br>app.<span>use</span>(<span>(<span>err, req, res, next</span>) =&gt;</span> {<br>    <span>console</span>.<span>error</span>(err.<span>stack</span>);<br>    res.<span>status</span>(<span>500</span>).<span>json</span>({ <span>error</span>: <span>'Something went wrong!'</span> });<br>});</span>
Line 240: ```
Line 241: 
Line 242: **4\. Invalid ID Handling**
Line 243: 
Line 244: ```
Line 245: <span id="cb87" data-selectable-paragraph=""><span>const</span> id = parseInt(req.<span>params</span>.id);<br></span>
Line 246: ```
Line 247: 
Line 248: If someone sends _/api/todos/abc, parseInt(“abc”)_ returns NaN, causing unpredictable behavior.
Line 249: 
Line 250: **5\. No User Feedback on Errors**  
Line 251: Frontend only logs errors to console — users see no error messages:
Line 252: 
Line 253: ```
Line 254: <span id="7d17" data-selectable-paragraph="">console.<span>error</span>(<span>'Failed to load todos:'</span>, <span>error</span>);<br></span>
Line 255: ```
Line 256: 
Line 257: **6\. Race Conditions**
Line 258: 
Line 259: Frontend doesn’t handle concurrent operations or loading states:
Line 260: 
Line 261: ```
Line 262: <span id="ab53" data-selectable-paragraph=""><span>this</span>.addTodo(title);<br>input.value = <span>''</span>; </span>
Line 263: ```
Line 264: 
Line 265: **7\. No Request Timeout**
Line 266: 
Line 267: Fetch requests have no timeout — they can hang indefinitely.
Line 268: 
Line 269: **8\. Missing Input Sanitization**  
Line 270: Backend accepts any string as a title without sanitization:
Line 271: 
Line 272: ```
Line 273: <span id="5b3b" data-selectable-paragraph=""><span>const</span> { title } = req.body;<br></span>
Line 274: ```
Line 275: 
Line 276: **9\. JSON Parsing Vulnerability**
Line 277: 
Line 278: No limit on request body size — vulnerable to JSON bombing attacks.
Line 279: 
Line 280: Unlike basic code search, Warp understood the context and relationships between frontend and backend error scenarios.
Line 281: 
Line 282: “What happens if the server restarts? Will users lose their tasks?” and so on…
Line 283: 
Line 284: Warp explained the recommended approach to fixing the existing issues.
Line 285: 
Line 286: > **This is where Warp’s codebase indexing becomes powerful as the first step to working with a new codebase.**
Line 287: 
Line 288: Warp doesn’t just read individual files — it understands how the pieces work together.
Line 289: 
Line 290: Next, it was to test its ability to fix a bug.
Line 291: 
Line 292: ## **Asking Warp to Make a Small Bug Fix**
Line 293: 
Line 294: I needed to fix actual issues in the task management app.
Line 295: 
Line 296: From my analysis, I identified a critical problem:
Line 297: 
Line 298: > **The app crashes when users send invalid JSON to the API endpoints. Time to see how Warp’s coding agent handles real bug fixes.**
Line 299: 
Line 300: ### **Finding and Fixing the Bug**
Line 301: 
Line 302: I gave Warp this prompt:
Line 303: 
Line 304: ```
Line 305: <span id="b0bc" data-selectable-paragraph="">The server crashes <span>when</span> invalid JSON <span>is</span> sent <span>to</span> /api/todos. <br>Add proper <span>error</span> handling <span>to</span> prevent crashes <span>and</span> <span>return</span> meaningful <span>error</span><br> messages.</span>
Line 306: ```
Line 307: 
Line 308: Press enter or click to view image in full size
Line 309: 
Line 310: ![](https://miro.medium.com/v2/resize:fit:1050/1*ReL40YLX8oELcKKIOlYY9g.gif)
Line 311: 
Line 312: Warp immediately identified the problem in different files, and it created a task list that would address each of these errors one after another, and this included :
Line 313: 
Line 314: -   Add JSON parsing error middleware
Line 315: -   Add a global error handler
Line 316: -   Add input validation middleware
Line 317: -   Add request size and rate limiting
Line 318: 
Line 319: It started working on the error, fixed one after another, and provided the code with the diff and the options to accept or reject the changes.
Line 320: 
Line 321: Press enter or click to view image in full size
Line 322: 
Line 323: ![](https://miro.medium.com/v2/resize:fit:1050/1*hJqyOjkhWuro6ztuLIOueA.png)
Line 324: 
Line 325: Instead of just showing me code snippets, Warp generated a complete solution:
Line 326: 
Line 327: 1.  Added error-handling middleware for JSON parsing
Line 328: 2.  Updated API endpoints with try-catch blocks
Line 329: 3.  Standardized error response format
Line 330: 4.  Added input validation for required fields
Line 331: 
Line 332: Press enter or click to view image in full size
Line 333: 
Line 334: ![](https://miro.medium.com/v2/resize:fit:1050/1*Sl0CAeg5GSP2apU2Uy0PzA.gif)
Line 335: 
Line 336: Here’s what impressed me: **_Warp didn’t just fix the immediate issue. It improved error handling across the entire application following consistent patterns._**
Line 337: 
Line 338: ### Multi-File Updates
Line 339: 
Line 340: The fix involved changes to multiple parts of the codebase:
Line 341: 
Line 342: **Backend changes:**
Line 343: 
Line 344: -   Added JSON error handling middleware
Line 345: -   Updated all API endpoints with proper error responses
Line 346: -   Added input validation for task creation
Line 347: 
Line 348: **Frontend changes:**
Line 349: 
Line 350: -   Updated error handling in public/js/app.js
Line 351: -   Added user-friendly error messages
Line 352: -   Improved network failure handling
Line 353: 
Line 354: > **This is where Warp wins — It understands the full application context and makes coordinated changes across the frontend and backend.**
Line 355: 
Line 356: ### **Testing the Fix**
Line 357: 
Line 358: I asked Warp to help test the fix:
Line 359: 
Line 360: ```
Line 361: <span id="dc69" data-selectable-paragraph="">Generate commands <span>to</span> test the <span>error</span> handling we just added</span>
Line 362: ```
Line 363: 
Line 364: Press enter or click to view image in full size
Line 365: 
Line 366: ![](https://miro.medium.com/v2/resize:fit:1050/1*S4tb5pb0rRWeqTmVzP_hnw.gif)
Line 367: 
Line 368: It generated all the commands necessary to test this app and fixed all the errors.
Line 369: 
Line 370: Press enter or click to view image in full size
Line 371: 
Line 372: ![](https://miro.medium.com/v2/resize:fit:1050/1*RWQc74ifLCkYjxELMn0Fqw.gif)
Line 373: 
Line 374: The server now returns proper error responses instead of crashing. The frontend displays meaningful messages to users.
Line 375: 
Line 376: > **This complete debugging and fixing process took 5 minutes with Warp, compared to what would have been an hour of manual work.**
Line 377: 
Line 378: ## **Reviewing Changes Before Applying Them**
Line 379: 
Line 380: When Warp’s agent generates code changes, it opens them in a built-in visual diff editor before applying anything to your files.
Line 381: 
Line 382: This is where Warp’s approach differs from tools that immediately apply changes or show you text suggestions.
Line 383: 
Line 384: Press enter or click to view image in full size
Line 385: 
Line 386: ![](https://miro.medium.com/v2/resize:fit:1050/1*99CFr8yvJzRDbh30lXx8mw.gif)
Line 387: 
Line 388: Based on the documentation, here’s how the review process works:
Line 389: 
Line 390: ### Visual Diff Interface
Line 391: 
Line 392: Changes are grouped into clear hunks for easy inspection. Use the UP and DOWN arrow keys (or mouse clicks) to move between hunks.
Line 393: 
Line 394: **_For multi-file changes, use the LEFT and RIGHT arrow keys to switch between files._**
Line 395: 
Line 396: The interface shows you exactly what will change before any modifications are made to your actual files.
Line 397: 
Line 398: Press enter or click to view image in full size
Line 399: 
Line 400: ![](https://miro.medium.com/v2/resize:fit:1050/1*f1HC_8vKCwbvv3bg-cqH5w.gif)
Line 401: 
Line 402: ### Control Over Changes
Line 403: 
Line 404: You have several options when reviewing:
Line 405: 
Line 406: -   **Accept**: Once satisfied with the changes, you can apply the diffs using ENTER or by clicking “Accept Changes” to apply the modifications. These modifications will not be applied to the files unless you explicitly accept them.
Line 407: -   **Refine**: Press R or select the “Refine” button to provide follow-up instructions in natural language. The agent will regenerate the diff based on your input.
Line 408: -   **Edit manually**: To manually adjust the code, press E or click “Edit” to switch into an editable view.
Line 409: -   **Cancel**: To cancel a pending operation, use CTRL-C (on Mac, Windows, or Linux systems). Similarly, you can exit the editor at any time with ESC.
Line 410: 
Line 411: ### No Automatic Application
Line 412: 
Line 413: Code diffs generated by Warp are never stored on their servers.
Line 414: 
Line 415: > **Warp coding agent only works on local repositories.**
Line 416: 
Line 417: Nothing gets changed in your codebase until you explicitly approve it. This gives you complete control over what modifications happen to your code.
Line 418: 
Line 419: > **I also liked the simple Code review UI that gives you easy navigation and a simple way to track changes :**
Line 420: 
Line 421: Press enter or click to view image in full size
Line 422: 
Line 423: ![](https://miro.medium.com/v2/resize:fit:1050/1*zNMPy9pmKPrV2hTZBphasg.png)
Line 424: 
Line 425: ## Advanced Features for Larger Codebases
Line 426: 
Line 427: My task management app was just a starting point.
Line 428: 
Line 429: Warp’s advanced features become essential when working with larger, more complex projects.
Line 430: 
Line 431: ## Codebase Indexing for Scale
Line 432: 
Line 433: Warp indexes your Git-tracked codebase to help Agents understand your code and generate accurate, context-aware responses.
Line 434: 
Line 435: **_No code is stored on Warp servers._**
Line 436: 
Line 437: Warp is designed for professional environments and supports real-time codebase indexing and large files with over 50K+ lines.
Line 438: 
Line 439: To test it,
Line 440: 
Line 441: I pulled one of my recent large codebases of an MCP server I built to connect Claude to WordPress — [**AutoWPMCP**](https://medium.com/@joe.njenga/i-built-a-claude-to-wordpress-mcp-server-to-fully-automate-your-site-try-it-here-da89a1b5d431)**.**
Line 442: 
Line 443: Press enter or click to view image in full size
Line 444: 
Line 445: ![](https://miro.medium.com/v2/resize:fit:1050/1*hLvdi-BjRilS6M9q_en2Ow.gif)
Line 446: 
Line 447: It handles a large codebase indexing with ease and does not hang or crash like other tools I have tested before.
Line 448: 
Line 449: Here's how indexing works:
Line 450: 
Line 451: -   You can view and manage your indexed codebases under Settings > Code > Codebase Index. You can also choose whether to automatically index new folders as you navigate them.
Line 452: -   For large projects, Warp supports several ignore files to give you control over what gets indexed. This allows each developer to focus context on the parts of the codebase most relevant to their work.
Line 453: -   You can use .warpindexingignore files to exclude specific content, similar to how .gitignore works.
Line 454: 
Line 455: ### **1) Project-Scoped Rules**
Line 456: 
Line 457: Project-Scoped Rules live in your codebase and apply automatically when working within that project.
Line 458: 
Line 459: They’re stored in a WARP.md file
Line 460: 
Line 461: Press enter or click to view image in full size
Line 462: 
Line 463: ![](https://miro.medium.com/v2/resize:fit:1050/1*kbq-C845BuJ877yXccJ6jA.gif)
Line 464: 
Line 465: The rules system supports hierarchical configuration:
Line 466: 
Line 467: Warp automatically applies the WARP.md file in both the root directory and the current directory. If you edit files in another subdirectory, Warp makes a best-effort attempt to include that subdirectory’s WARP.md as well.
Line 468: 
Line 469: This means you can have:
Line 470: 
Line 471: -   Project-wide rules in the root WARP.md
Line 472: -   API-specific rules in api/WARP.md
Line 473: -   Frontend-specific rules in ui/WARP.md
Line 474: 
Line 475: Warp currently supports the following Rules files: CLAUDE.md, .cursorrules, AGENT.MD, AGENTS.md, GEMINI.md, .clinerules, .windsurfrules, .github/copilot-instructions.md
Line 476: 
Line 477: ### 2) Multi-Repository Support
Line 478: 
Line 479: Warp supports referencing context across multiple indexed repositories.
Line 480: 
Line 481: This is particularly useful for microservice architectures where you need to understand dependencies between different codebases.
Line 482: 
Line 483: ### 3) Context Management
Line 484: 
Line 485: Using the @ symbol to search for and attach a file or folder from the project root. Additionally, no codebase indexing (via Codebase Context) is required — file search is available immediately in any Git-initialized directory.
Line 486: 
Line 487: Press enter or click to view image in full size
Line 488: 
Line 489: ![](https://miro.medium.com/v2/resize:fit:1050/1*mCFravfgVJLCuGxi7I2f6g.gif)
Line 490: 
Line 491: You can also attach a public URL to a prompt to provide website content as context.
Line 492: 
Line 493: When a URL is included, the agent will scrape the page and extract relevant information to inform its response.
Line 494: 
Line 495: These features transform how you work with complex codebases by providing intelligent context awareness without manual setup.
Line 496: 
Line 497: ## Parallel Agentic Coding
Line 498: 
Line 499: One of the features that impressed me with Warp is the ability to spin multiple agents working together. You can create various agents and assign them different roles.
Line 500: 
Line 501: Press enter or click to view image in full size
Line 502: 
Line 503: ![](https://miro.medium.com/v2/resize:fit:1050/1*2-6g-svkqU36iGYEhSTcGA.gif)
Line 504: 
Line 505: _This is a feature I would like to explore further in my upcoming tutorial. If you haven't joined us yet,_ [**_consider following me on Medium_**](https://medium.com/@joe.njenga) _to stay updated on other Warp tutorials._
Line 506: 
Line 507: ## **Final Thoughts**
Line 508: 
Line 509: Working with unfamiliar codebases doesn't have to be intimidating anymore.
Line 510: 
Line 511: > **What used to take hours of manual exploration now takes minutes. Warp's approach feels very natural and easy..**
Line 512: 
Line 513: My task management app was simple, but the workflow scales. Whether you're debugging a microservice architecture or contributing to an open-source project with thousands of files, the same principles apply.
Line 514: 
Line 515: > Ask questions instead of guessing. Let AI handle reconnaissance while you focus on solving real problems. Review changes before applying them.
Line 516: 
Line 517: The combination of codebase indexing, intelligent diff management, and project-scoped rules creates a development experience that feels both powerful and safe.
Line 518: 
Line 519: After testing Warp's capabilities on several projects, I understand why it scored #1 on [**_Terminal-Bench_**](https://www.tbench.ai/leaderboard)**.**
Line 520: 
Line 521: > **Have you tested Warp, and what was your experience? Let us know in the comments below.**
Line 522: 
Line 523: # 구성
Line 524: ---
