# 속성
---
process_status: true
source_type: youtube
structure_type: standalone
document_language: english

# 추출
---
## 핵심 내용
Archon은 AI 코딩의 가장 큰 문제인 동적 컨텍스트 관리를 해결하는 혁신적인 시스템입니다. 기존의 단순한 프롬프트 방식과 달리, Archon은 완전한 RAG 시스템, 웹 크롤링, 작업 관리를 통합하여 AI 에이전트가 필요할 때마다 자동으로 정확한 문서를 검색할 수 있게 합니다. 이를 통해 코딩 과정에서 컨텍스트가 부족하거나 업데이트가 필요한 상황에서도 AI가 스스로 필요한 정보를 찾아 작업을 지속할 수 있습니다.

## 상세 핵심 내용
Archon은 AI 코딩의 핵심 문제인 동적 컨텍스트 관리를 해결하는 혁신적인 솔루션입니다. 기존 AI 코딩 도구들의 한계는 단순히 큰 프롬프트를 제공하는 것만으로는 충분하지 않다는 점이었습니다. 코딩 과정에서 오류가 발생하거나 새로운 구현이 필요할 때, 개발자는 지속적으로 컨텍스트를 업데이트해야 하는 번거로움이 있었습니다.

Archon의 핵심은 AI 에이전트가 필요한 정확한 데이터를 최대한 빠르게 검색할 수 있는 지식 기반 시스템입니다. 프로젝트 탭에는 문서(docs)와 작업(tasks) 두 가지 필수 탭이 있어 완전한 컨텍스트 관리 시스템을 제공합니다. 템플릿 기능을 통해 아키텍처 문서나 기능 PRD 같은 체계적인 문서화가 가능하며, 작업 탭은 프로젝트 범위에 따라 백로그를 자동으로 채워 AI 에이전트가 독립적으로 작업을 관리할 수 있게 합니다.

가장 혁신적인 기능은 완전한 RAG(Retrieval-Augmented Generation) 시스템 구현입니다. 단순한 텍스트 검색이 아닌 적절한 데이터베이스를 설정하여 의미론적 검색을 수행합니다. 예를 들어, Apple 개발자 사이트의 Swift UI 문서 전체(505페이지, 126,000단어 이상)를 가져와 프로그래밍 방식으로 모든 링크를 따라가며 정보를 체계적으로 추출할 수 있습니다.

핵심은 AI 에이전트가 Archon과 통합되어 약간의 불확실성이라도 느끼면 자동으로 필요한 문서를 검색한다는 점입니다. 이를 통해 코딩 에이전트는 작업 실행 도구로, Archon은 모든 지식과 지침이 저장된 컨텍스트 박스로 역할을 분담하여 효율적인 개발 환경을 구축합니다.

## 주요 화제
- AI 코딩의 현재 한계와 문제점: 기존 AI 코딩 도구들이 단순한 대형 프롬프트나 컨텍스트 엔지니어링만으로는 동적인 코딩 과정에서 발생하는 오류나 추가 컨텍스트 요구에 대응하지 못한다는 근본적 문제를 다룹니다.

- Archon 시스템의 혁신적 지식 베이스 솔루션: AI 에이전트가 필요한 정확한 데이터를 빠르게 검색할 수 있는 전용 지식 베이스 시스템으로서 프로젝트 관리, 문서화, 작업 관리를 통합한 완전한 컨텍스트 관리 시스템을 제공합니다.

- 작업 관리와 지식 베이스 통합: 프로젝트 범위에 기반하여 백로그가 자동으로 채워지고 AI 에이전트가 독립적으로 작업을 관리하며 컨텍스트를 잃지 않고 작업 메모리를 유지하는 시스템을 설명합니다.

- 강력한 RAG 시스템과 웹 크롤링 기능: 단순한 텍스트 검색이 아닌 완전한 RAG 데이터베이스를 구축하여 의미론적 검색을 통해 빠르고 정확한 개인화된 검색 결과를 제공하며, 웹사이트 전체를 체계적으로 크롤링하여 문서를 수집하는 기능을 다룹니다.

- 실제 설치 및 구성 가이드: GitHub 저장소 클론부터 Supabase 데이터베이스 설정, 환경 파일 구성, MCP 서버 연결까지의 구체적인 설치 과정을 단계별로 설명합니다.

- 실제 개발 프로세스와 결과: 프로젝트 생성부터 요구사항 정의, Swift UI 앱 개발 예시를 통해 AI 코딩 에이전트가 Archon과 통합되어 불확실성이 있을 때 자동으로 필요한 문서를 가져오는 실제 작업 흐름을 보여줍니다.

## 부차 화제
"00 Lev0 Retrieval Agents Actually Solved Ai Codings Biggest Problem"에서 다루는 부차 화제들을 체계적으로 정리하면 다음과 같습니다:

- 컨텍스트 엔지니어링의 한계: AI 코딩에서 모델의 컨텍스트 윈도우에 필요한 정보만 채우는 기법이 코딩 중 발생하는 예상치 못한 상황에서 지속적인 업데이트가 필요하다는 문제점을 설명합니다.

- Archon의 프로젝트 구조: 각 프로젝트가 docs와 tasks 두 개의 필수 탭으로 구성되어 AI 에이전트에게 완전한 프로젝트 지식을 제공하는 컨텍스트 관리 시스템을 설명합니다.

- 문서화 템플릿 시스템: AI 에이전트가 연결될 때 아키텍처 문서나 기능 PRD 같은 템플릿을 따라 체계적으로 문서를 생성하여 무작위 문서화를 방지하는 기능을 설명합니다.

- 자동 작업 생성 및 관리: 프로젝트 범위와 문서를 기반으로 백로그가 자동으로 관련 작업들로 채워지고 AI 에이전트가 독립적으로 작업을 관리하는 시스템을 설명합니다.

- MCP 서버 연동: Archon을 Claude Code나 Cursor 같은 AI 에이전트에 연결하는 설정 과정이 간단하다는 점을 설명합니다.

- 웹 크롤링 기능: Apple의 SwiftUI 문서처럼 대용량 온라인 문서를 프로그래밍 방식으로 수집하여 지식 베이스에 추가하는 기능을 설명합니다.

- Supabase 데이터베이스 설정: RAG 시스템 구현을 위해 Supabase를 메인 데이터베이스로 사용하며 무료 버전으로도 충분하다는 점을 설명합니다.

- 임베딩을 위한 추가 API 키: RAG 구현을 위해 문서의 단어를 의미 기반 수치로 변환하는 과정에서 Google Gemini나 OpenAI의 추가 API 키가 필요하다는 점을 설명합니다.

- 실시간 문서 검색 통합: 코딩 에이전트가 불확실성을 느낄 때마다 자동으로 필요한 문서를 가져오는 통합 기능을 설명합니다.

- PDF 업로드 지원: 커스텀 지식이나 내부 문서를 위해 PDF 파일을 업로드할 수 있는 기능을 설명합니다.

# 내용
---
# Retrieval Agents ACTUALLY Solved AI Coding's Biggest Problem

## Current Limitations and Problems in AI Coding

AI coding is constantly evolving. Whether you use Claude Code or Cursor, it doesn't matter. People are realizing that simply giving a large prompt to your AI coder is not enough anymore. This realization led to the introduction of context engineering a while back.

Context engineering is basically the art of filling the context window of the model with only the stuff that it needs to know for a specific task. Sounds good in theory, right? But here's the issue. You never follow a set path when coding. You encounter errors. You might need to implement something new or you discover you need additional context midway through. When that happens, you're stuck. You need to constantly update your context.

## Archon: The Revolutionary Knowledge Base Solution

What you really need is your own knowledge base. And not just any knowledge base, but one through which the AI agent can get the accurate data it wants as fast as possible. This is where this new agent system, Archon, comes in.

Let's start with the projects tab. I have two projects here, a test project and a task glass project. Each project contains two essential tabs, docs and tasks. This is your complete context management system. Your documentation lives here giving your AI agent full knowledge of your project.

When I open this, you'll notice they've added templates. This means when your AI agent connects, whether it's Claude or Cursor, it doesn't create random documentation. It follows these templates like architecture documentation or feature PRDs, keeping everything properly organized.

## Task Management and Knowledge Base Integration

The tasks tab works beautifully with your documentation based on your project scope, meaning what you want to build. The backlog automatically populates with relevant tasks. The AI agent manages tasks independently and maintains task memory. It never loses context and always knows which tasks need completion.

You can create unlimited projects and manage them efficiently. In my task class project, for instance, one task sits in the backlog while 13 are actively in progress.

Next is the MCP server which connects Archon to your AI agents. Setup is remarkably simple. They have setup commands for all agents like Claude Code whose command is really hard to search up. This is especially valuable for users uncomfortable with code editors or terminals.

## Powerful RAG System and Web Crawling

Here's the feature that makes Archon exceptional, the knowledge base. The knowledge base accepts any documentation you need. You can add links to any tools documentation. For example, I imported the entire Swift UI documentation from Apple's developer site. That's 505 pages containing over 126,000 words.

In the add knowledge base section, you'll find categories of knowledge. You can add URLs or hosted documentation sites. The applications extend beyond AI coding. You can personalize documentation and create knowledge bases for anything. You can also upload PDFs for custom knowledge or internal documentation.

What makes this different from other tools? Archon implements a complete RAG system. When you install it, you're setting up a proper database for RAG instead of simple text search. The system stores data and applies semantic search. The result is fast, accurate, and personalized retrieval.

## Practical Example and Setup Process

Here's a practical example. In my test projects doc section, I can add project specific sources. Say I'm building a Swift app and Liquid Glass UI just released. LLMs don't know about it yet. The solution is feeding Archon the Swift UI documentation.

I added the docs to the knowledge base, set the crawl depth to two, which is optimal, and let the crawler process everything. The crawler works programmatically. It follows every link on the site, navigates through menus, enters each page, and extracts all information systematically.

This is a comprehensive system combining context engineering, RAG, web scraping, and task management in one platform. When our community creates something this powerful, others build on it to create even more innovative tools. That's the beauty of this community.

## Installation and Configuration Guide

So, this is the GitHub repository of Archon. And the first thing you're going to do is come here and copy the link. Then you'll go back into your terminal. You're going to clone the GitHub repository and add it inside your chosen directory.

After the GitHub repository is installed, you're going to run this specific command that's shown right here in the GitHub repository. This command will create your env file where you need to put some important variables.

Now, since Archon is a proper knowledge hub, it needs a proper database to perform RAG and all the AI searching capabilities that it provides. For this, the author has chosen to use Supabase as the main database. And setting it up is really simple. The great thing is you don't need to pay for this. The free version of Supabase is absolutely enough for what we need.

Next, you need to create your database tables inside Supabase. But don't worry about having to do that manually. They've provided an automatically configured setup that makes this incredibly easy. All you have to do is open the current repository inside Cursor so you can easily access all the files.

## Real Development Process and Results

After you've set everything up and your services are running, when you open the front-end link in your browser, you're going to be greeted with this onboarding flow. The first thing you'll need is an additional API key. You can go ahead and choose between Google Gemini or OpenAI for this.

The reason you need to provide another API key is for the RAG implementation. To make RAG work, the system needs to convert the words in your documents into numbers based on their meaning. This conversion process is what makes the search so fast and accurate and it requires a model to create these meaningful numerical representations.

First, you create a new project like I did. After creating the project, I went into Claude Code and asked it to search for all the projects. It fetched my project and returned the ID along with the description. In that description, I had defined that it should only use local storage, follow a specific architecture, and be built with Swift UI.

Next, I told it that I wanted to build the app and provided some requirements. For example, I specified that it must use Liquid Glass and that I just wanted two pages in the app for now. Think of this step as writing a PRD and you can discuss this with Claude Code and finalize this.

Think of your coding agent as the tool that's only there to execute tasks while Archon is the context box where all your knowledge and instructions live. Going back to the process, once the documentation was ready and it had the Swift UI knowledge base in it, it needed to create tasks.

Now you might wonder how it knows when to use the documentation. Before as you know the big issue was that giving some context for a single task and many times that context wouldn't turn out to be enough. With Archon, this problem is completely solved. The coding agent is integrated with Archon so that whenever it feels even the slightest uncertainty, it automatically fetches the required documentation.

# Retrieval Agents ACTUALLY Solved AI Coding's Biggest Problem

## Current Limitations and Problems in AI Coding

AI coding is constantly evolving. Whether you use Claude Code or Cursor, it doesn't matter. People are realizing that simply giving a large prompt to your AI coder is not enough anymore. This realization led to the introduction of context engineering a while back.

Context engineering is basically the art of filling the context window of the model with only the stuff that it needs to know for a specific task. Sounds good in theory, right? But here's the issue. You never follow a set path when coding. You encounter errors. You might need to implement something new or you discover you need additional context midway through. When that happens, you're stuck. You need to constantly update your context.

## Archon: The Revolutionary Knowledge Base Solution

What you really need is your own knowledge base. And not just any knowledge base, but one through which the AI agent can get the accurate data it wants as fast as possible. This is where this new agent system, Archon, comes in.

Let's start with the projects tab. I have two projects here, a test project and a task glass project. Each project contains two essential tabs, docs and tasks. This is your complete context management system. Your documentation lives here giving your AI agent full knowledge of your project.

When I open this, you'll notice they've added templates. This means when your AI agent connects, whether it's Claude or Cursor, it doesn't create random documentation. It follows these templates like architecture documentation or feature PRDs, keeping everything properly organized.

## Task Management and Knowledge Base Integration

The tasks tab works beautifully with your documentation based on your project scope, meaning what you want to build. The backlog automatically populates with relevant tasks. The AI agent manages tasks independently and maintains task memory. It never loses context and always knows which tasks need completion.

You can create unlimited projects and manage them efficiently. In my task class project, for instance, one task sits in the backlog while 13 are actively in progress.

Next is the MCP server which connects Archon to your AI agents. Setup is remarkably simple. They have setup commands for all agents like Claude Code whose command is really hard to search up. This is especially valuable for users uncomfortable with code editors or terminals.

## Powerful RAG System and Web Crawling

Here's the feature that makes Archon exceptional, the knowledge base. The knowledge base accepts any documentation you need. You can add links to any tools documentation. For example, I imported the entire Swift UI documentation from Apple's developer site. That's 505 pages containing over 126,000 words.

In the add knowledge base section, you'll find categories of knowledge. You can add URLs or hosted documentation sites. The applications extend beyond AI coding. You can personalize documentation and create knowledge bases for anything. You can also upload PDFs for custom knowledge or internal documentation.

What makes this different from other tools? Archon implements a complete RAG system. When you install it, you're setting up a proper database for RAG instead of simple text search. The system stores data and applies semantic search. The result is fast, accurate, and personalized retrieval.

## Practical Example and Setup Process

Here's a practical example. In my test projects doc section, I can add project specific sources. Say I'm building a Swift app and Liquid Glass UI just released. LLMs don't know about it yet. The solution is feeding Archon the Swift UI documentation.

I added the docs to the knowledge base, set the crawl depth to two, which is optimal, and let the crawler process everything. The crawler works programmatically. It follows every link on the site, navigates through menus, enters each page, and extracts all information systematically.

This is a comprehensive system combining context engineering, RAG, web scraping, and task management in one platform. When our community creates something this powerful, others build on it to create even more innovative tools. That's the beauty of this community.

## Installation and Configuration Guide

So, this is the GitHub repository of Archon. And the first thing you're going to do is come here and copy the link. Then you'll go back into your terminal. You're going to clone the GitHub repository and add it inside your chosen directory.

After the GitHub repository is installed, you're going to run this specific command that's shown right here in the GitHub repository. This command will create your env file where you need to put some important variables.

Now, since Archon is a proper knowledge hub, it needs a proper database to perform RAG and all the AI searching capabilities that it provides. For this, the author has chosen to use Supabase as the main database. And setting it up is really simple. The great thing is you don't need to pay for this. The free version of Supabase is absolutely enough for what we need.

Next, you need to create your database tables inside Supabase. But don't worry about having to do that manually. They've provided an automatically configured setup that makes this incredibly easy. All you have to do is open the current repository inside Cursor so you can easily access all the files.

## Real Development Process and Results

After you've set everything up and your services are running, when you open the front-end link in your browser, you're going to be greeted with this onboarding flow. The first thing you'll need is an additional API key. You can go ahead and choose between Google Gemini or OpenAI for this.

The reason you need to provide another API key is for the RAG implementation. To make RAG work, the system needs to convert the words in your documents into numbers based on their meaning. This conversion process is what makes the search so fast and accurate and it requires a model to create these meaningful numerical representations.

First, you create a new project like I did. After creating the project, I went into Claude Code and asked it to search for all the projects. It fetched my project and returned the ID along with the description. In that description, I had defined that it should only use local storage, follow a specific architecture, and be built with Swift UI.

Next, I told it that I wanted to build the app and provided some requirements. For example, I specified that it must use Liquid Glass and that I just wanted two pages in the app for now. Think of this step as writing a PRD and you can discuss this with Claude Code and finalize this.

Think of your coding agent as the tool that's only there to execute tasks while Archon is the context box where all your knowledge and instructions live. Going back to the process, once the documentation was ready and it had the Swift UI knowledge base in it, it needed to create tasks.

Now you might wonder how it knows when to use the documentation. Before as you know the big issue was that giving some context for a single task and many times that context wouldn't turn out to be enough. With Archon, this problem is completely solved. The coding agent is integrated with Archon so that whenever it feels even the slightest uncertainty, it automatically fetches the required documentation.

# 구성
---
