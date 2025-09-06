# Grading System

<!-- 추출 정보
노드 ID: 13
제목: Grading System
추출 길이: 660자
추출 시간: 2025-08-13 17:34:03
-->

## Grading System

But you can see here we have a simple grading system. S through F where S is the best and F is the worst. We have a classic prompt format. We can collapse everything to quickly understand it. Use the nano agent MCP server, execute and then report the results in the response format. And so you can see the response format is a simple grading scheme.

We are using Claude code Opus 4.1 as an LLM as a judge to manage all this for us. And then inside the evaluation details, we're just passing in the lops, the lower order prompts - the prompts that contain the detail that we want to swap in and out as we evaluate different agentic behavior.
