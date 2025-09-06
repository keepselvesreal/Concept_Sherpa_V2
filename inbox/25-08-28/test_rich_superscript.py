#!/usr/bin/env python3
"""
생성 시간: 2025-08-28 09:41:35
핵심 내용: Rich 라이브러리를 사용한 터미널 윗첨자 스타일링 테스트
상세 내용: 
    - test_rich_styles() (line 15): 다양한 Rich 스타일 테스트
    - demo_dop_response() (line 35): DOP 응답 예시로 실제 사용 시연
상태: active
주소: test_rich_superscript
참조: 없음
"""

from rich.console import Console
from rich.text import Text

def test_rich_styles():
    """다양한 Rich 스타일로 윗첨자 표현 테스트"""
    console = Console()
    
    console.print("\n🔧 Rich 라이브러리 윗첨자 스타일 테스트", style="bold blue")
    console.print("=" * 50)
    
    # 방법 1: 작은 글씨로 위첨자 흉내
    console.print("\n1. 작은 글씨 + 색상:")
    text = Text("데이터 지향 프로그래밍")
    text.append("⁵", style="dim red small")
    console.print(text)
    
    # 방법 2: 괄호 스타일
    console.print("\n2. 괄호 스타일:")
    console.print("데이터 지향 프로그래밍[red][5][/red]")
    
    # 방법 3: ^ 기호 사용
    console.print("\n3. ^ 기호 스타일:")
    console.print("데이터 지향 프로그래밍[bright_red]^5^[/bright_red]")
    
    # 방법 4: 유니코드 윗첨자
    console.print("\n4. 유니코드 윗첨자:")
    console.print("데이터 지향 프로그래밍[cyan]⁵[/cyan]")
    
    # 방법 5: 박스 스타일
    console.print("\n5. 박스 스타일:")
    console.print("데이터 지향 프로그래밍[on bright_blue] 5 [/on bright_blue]")

def demo_dop_response():
    """DOP 응답 예시로 실제 사용 시연"""
    console = Console()
    
    console.print("\n🎯 실제 AI 응답 스타일 시연", style="bold green")
    console.print("=" * 50)
    
    # 실제 응답처럼 보이는 예시
    console.print("\n데이터 지향 프로그래밍은 [bold]데이터와 그 변환에 초점을 맞춘[/bold] 프로그래밍 패러다임입니다[bright_red]^5^[/bright_red].")
    
    console.print("\n주요 특징:")
    console.print("• 데이터 구조를 먼저 설계[cyan]^10^[/cyan]")
    console.print("• 불변성(Immutability)[yellow]^14^[/yellow]")
    console.print("• 데이터와 로직 분리[green]^21^[/green]")
    
    console.print("\n장점:")
    console.print("• 메모리 지역성 향상[blue]^66^[/blue]")
    console.print("• 디버깅 용이[magenta]^71^[/magenta]")
    
    console.print("\n[dim]출처: DOP_with_lines.md의 해당 라인 번호[/dim]")

if __name__ == "__main__":
    test_rich_styles()
    demo_dop_response()