"""
생성 시간: 2025-08-10 22:28:30 KST
핵심 내용: DOP에서의 데이터 검증 (7.1절) - 시스템 경계에서의 데이터 검증 중요성
상세 내용:
    - Theo와 Joe의 대화 시작 (32-37행): OOP에서 DOP로 전환 시 데이터 검증에 대한 우려
    - 데이터 검증의 필요성 설명 (38-95행): DOP에서도 데이터 검증이 가능하고 권장됨
    - 시스템 경계 다이어그램 (56-64행): 웹서버의 클라이언트, 데이터베이스, 웹서비스 경계
    - 두 가지 데이터 검증 유형 테이블 (92-95행): 경계에서의 검증 vs 내부 검증
상태: 활성  
주소: chapter7_01_data_validation_in_dop
참조: 원본 파일 /home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md
"""

# 7.1 Data validation in DOP

=== 페이지 170 ===
142 CHAPTER 7 Basic data validation
7.1 Data validation in DOP
Theo has rescheduled his meetings. With such an imposing deadline, he's still not sure if
he's made a big mistake giving DOP a second chance.
 NOTE The reason why Theo rescheduled his meetings is explained in the opener
for part 2. Take a moment to read the opener if you missed it.
Joe What aspect of OOP do you think you will miss the most in your big project?
Theo Data validation.
Joe Can you elaborate a bit?
Theo In OOP, I have this strong guarantee that when a class is instantiated, its mem-
ber fields have the proper names and proper types. But with DOP, it's so easy
to have small mistakes in field names and field types.
Joe Well, I have good news for you! There is a way to validate data in DOP.
Theo How does it work? I thought DOP and data validation were two contradictory
concepts!
Joe Not at all. It's true that DOP doesn't force you to validate data, but it doesn't
prevent you from doing so. In DOP, the data schema is separate from the data
representation.
Theo I don't get how that would eliminate data consistency issues.
Joe According to DOP, the most important data to validate is data that crosses the
boundaries of the system.
Theo Which boundaries are you referring to?
Joe In the case of a web server, it would be the areas where the web server commu-
nicates with its clients and with its data sources.
Theo A diagram might help me see it better.
Joe goes to the whiteboard and picks up the pen. He then draws a diagram like the one in
figure 7.1.
Client (e.g., web browser)
Data
Web server
Data Data
Web service Database Figure 7.1 High-level architecture of
a modern web server

=== 페이지 171 ===
7.2 JSON Schema in a nutshell 143
Joe This architectural diagram defines what we call the boundaries of the system in
terms of data exchange. Can you tell me what the three boundaries of the sys-
tem are?
 NOTE The boundaries of a system are defined as the areas where the system exchanges
data.
Theo Let me see. The first one is the client boundary, then we have the database
boundary, and finally, the web service boundary.
Joe Exactly! It's important to identify the boundaries of a system because, in
DOP, we differentiate between two kinds of data validation: validation that
occurs at the boundaries of the system and validation that occurs inside the
system. Today, we're going to focus on validation that occurs at the boundar-
ies of the system.
Theo Does that mean data validation at the boundaries of the system is more
important?
Joe Absolutely! Once you've ensured that data going into and out of the system is
valid, the odds for an unexpected piece of data inside the system are pretty low.
TIP When data at system boundaries is validated, it's not critical to validate data
again inside the system.
Theo Why do we need data validation inside the system then?
Joe It has to do with making it easier to code your system as your code base grows.
Theo And, what's the main purpose of data validation at the boundaries?
Joe To prevent invalid data from going in and out of the system, and to display
informative errors when we encounter invalid data. Let me draw a table on the
whiteboard so you can see the distinction (table 7.1).
Table 7.1 Two kinds of data validation
Kind of data validation Purpose Environment
Boundaries Guardian Production
Inside Ease of development Dev
Theo When will you teach me about data validation inside the system?
Joe Later, when the code base is bigger.