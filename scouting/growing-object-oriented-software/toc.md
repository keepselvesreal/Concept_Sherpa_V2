# Cover  (p.Cover)

# Contents (p.ix)

# Foreword (p.xv)

# Preface (p.xvii)

# Acknowledgments (p.xxi)

# About the Authors (p.xxiii)

# Part I: Introduction (p.Cover)

## 1. Chapter 1: What Is the Point of Test-Driven Development? (p.ii)

### 1.1 Software Development as a Learning Process (p.ii)

### 1.2 Feedback Is the Fundamental Tool (p.iii)

### 1.3 Practices That Support Change (p.iv)

### 1.4 Test-Driven Development in a Nutshell (p.v)

### 1.5 The Bigger Picture (p.vi)

### 1.6 Testing End-to-End (p.vii)

### 1.7 Levels of Testing (p.viii)

### 1.8 External and Internal Quality (p.ix)

## 2. Chapter 2: Test-Driven Development with Objects (p.xii)

### 2.1 A Web of Objects (p.xii)

### 2.2 Values and Objects (p.xii)

### 2.3 Follow the Messages (p.xiii)

### 2.4 Tell, Don't Ask (p.xvi)

### 2.5 But Sometimes Ask (p.xvi)

### 2.6 Unit-Testing the Collaborating Objects (p.xvii)

### 2.7 Support for TDD with Mock Objects (p.xviii)

## 3. Chapter 3: An Introduction to the Tools (p.xx)

### 3.1 Stop Me If You've Heard This One Before (p.xx)

### 3.2 A Minimal Introduction to JUnit 4 (p.xx)

### 3.3 Hamcrest Matchers and assertThat() (p.xxiii)

### 3.4 jMock2: Mock Objects (p.xxiv)

# Part II: The Process of Test-Driven Development (p.4)

## 4. Chapter 4: Kick-Starting the Test-Driven Cycle (p.6)

### 4.1 Introduction (p.6)

### 4.2 First, Test a Walking Skeleton (p.7)

### 4.3 Deciding the Shape of the Walking Skeleton (p.8)

### 4.4 Build Sources of Feedback (p.10)

### 4.5 Expose Uncertainty Early (p.11)

## 5. Chapter 5: Maintaining the Test-Driven Cycle (p.14)

### 5.1 Introduction (p.14)

### 5.2 Start Each Feature with an Acceptance Test (p.14)

### 5.3 Separate Tests That Measure Progress from Those That Catch Regressions (p.15)

### 5.4 Start Testing with the Simplest Success Case (p.16)

### 5.5 Write the Test That You'd Want to Read (p.17)

### 5.6 Watch the Test Fail (p.17)

### 5.7 Develop from the Inputs to the Outputs (p.18)

### 5.8 Unit-Test Behavior, Not Methods (p.18)

### 5.9 Listen to the Tests (p.19)

### 5.10 Tuning the Cycle (p.20)

## 6. Chapter 6: Object-Oriented Style (p.22)

### 6.1 Introduction (p.22)

### 6.2 Designing for Maintainability (p.22)

### 6.3 Internals vs. Peers (p.25)

### 6.4 No And's, Or's, or But's (p.26)

### 6.5 Object Peer Stereotypes (p.27)

### 6.6 Composite Simpler Than the Sum of Its Parts (p.28)

### 6.7 Context Independence (p.29)

### 6.8 Hiding the Right Information (p.30)

### 6.9 An Opinionated View (p.31)

## 7. Chapter 7: Achieving Object-Oriented Design (p.32)

### 7.1 How Writing a Test First Helps the Design (p.32)

### 7.2 Communication over Classification (p.33)

### 7.3 Value Types (p.34)

### 7.4 Where Do Objects Come From? (p.35)

### 7.5 Identify Relationships with Interfaces (p.38)

### 7.6 Refactor Interfaces Too (p.38)

### 7.7 Compose Objects to Describe System Behavior (p.39)

### 7.8 Building Up to Higher-Level Programming (p.40)

### 7.9 And What about Classes? (p.42)

## 8. Chapter 8: Building on Third-Party Code (p.44)

### 8.1 Introduction (p.44)

### 8.2 Only Mock Types That You Own (p.44)

### 8.3 Mock Application Objects in Integration Tests (p.46)

# Part III: A Worked Example (p.48)

## 9. Chapter 9: Commissioning an Auction Sniper (p.50)

### 9.1 To Begin at the Beginning (p.50)

### 9.2 Communicating with an Auction (p.53)

### 9.3 Getting There Safely (p.54)

### 9.4 This Isn't Real (p.56)

## 10. Chapter 10: The Walking Skeleton (p.58)

### 10.1 Get the Skeleton out of the Closet (p.58)

### 10.2 Our Very First Test (p.59)

### 10.3 Some Initial Choices (p.61)

## 11. Chapter 11: Passing the First Test (p.64)

### 11.1 Building the Test Rig (p.64)

### 11.2 Failing and Passing the Test (p.70)

### 11.3 The Necessary Minimum (p.77)

## 12. Chapter 12: Getting Ready to Bid (p.80)

### 12.1 An Introduction to the Market (p.80)

### 12.2 A Test for Bidding (p.81)

### 12.3 The AuctionMessageTranslator (p.87)

### 12.4 Unpacking a Price Message (p.93)

### 12.5 Finish the Job (p.96)

## 13. Chapter 13: The Sniper Makes a Bid (p.98)

### 13.1 Introducing AuctionSniper (p.98)

### 13.2 Sending a Bid (p.101)

### 13.3 Tidying Up the Implementation (p.106)

### 13.4 Defer Decisions (p.111)

### 13.5 Emergent Design (p.112)

## 14. Chapter 14: The Sniper Wins the Auction (p.114)

### 14.1 First, a Failing Test (p.114)

### 14.2 Who Knows about Bidders? (p.115)

### 14.3 The Sniper Has More to Say (p.118)

### 14.4 The Sniper Acquires Some State (p.119)

### 14.5 The Sniper Wins (p.121)

### 14.6 Making Steady Progress (p.123)

## 15. Chapter 15: Towards a Real User Interface (p.124)

### 15.1 A More Realistic Implementation (p.124)

### 15.2 Displaying Price Details (p.127)

### 15.3 Simplifying Sniper Events (p.134)

### 15.4 Follow Through (p.139)

### 15.5 Final Polish (p.143)

### 15.6 Observations (p.146)

## 16. Chapter 16: Sniping for Multiple Items (p.150)

### 16.1 Testing for Multiple Items (p.150)

### 16.2 Adding Items through the User Interface (p.158)

### 16.3 Observations (p.164)

## 17. Chapter 17: Teasing Apart Main (p.166)

### 17.1 Finding a Role (p.166)

### 17.2 Extracting the Chat (p.167)

### 17.3 Extracting the Connection (p.170)

### 17.4 Extracting the SnipersTableModel (p.172)

### 17.5 Observations (p.176)

## 18. Chapter 18: Filling In the Details (p.180)

### 18.1 A More Useful Application (p.180)

### 18.2 Stop When We've Had Enough (p.180)

### 18.3 Observations (p.187)

## 19. Chapter 19: Handling Failure (p.190)

### 19.1 What If It Doesn't Work? (p.190)

### 19.2 Detecting the Failure (p.192)

### 19.3 Displaying the Failure (p.193)

### 19.4 Disconnecting the Sniper (p.194)

### 19.5 Recording the Failure (p.196)

### 19.6 Observations (p.200)

# Part IV: Sustainable Test-Driven Development (p.202)

## 20. Chapter 20: Listening to the Tests (p.204)

### 20.1 Introduction (p.204)

### 20.2 I Need to Mock an Object I Can't Replace (without Magic) (p.205)

### 20.3 Logging Is a Feature (p.208)

### 20.4 Mocking Concrete Classes (p.210)

### 20.5 Don't Mock Values (p.212)

### 20.6 Bloated Constructor (p.213)

### 20.7 Confused Object (p.215)

### 20.8 Too Many Dependencies (p.216)

### 20.9 Too Many Expectations (p.217)

### 20.10 What the Tests Will Tell Us (If We're Listening) (p.219)

## 21. Chapter 21: Test Readability (p.222)

### 21.1 Introduction (p.222)

### 21.2 Test Names Describe Features (p.223)

### 21.3 Canonical Test Structure (p.226)

### 21.4 Streamline the Test Code (p.227)

### 21.5 Assertions and Expectations (p.229)

### 21.6 Literals and Variables (p.230)

## 22. Chapter 22: Constructing Complex Test Data (p.232)

### 22.1 Introduction (p.232)

### 22.2 Test Data Builders (p.233)

### 22.3 Creating Similar Objects (p.234)

### 22.4 Combining Builders (p.236)

### 22.5 Emphasizing the Domain Model with Factory Methods (p.236)

### 22.6 Removing Duplication at the Point of Use (p.237)

### 22.7 Communication First (p.239)

## 23. Chapter 23: Test Diagnostics (p.242)

### 23.1 Design to Fail (p.242)

### 23.2 Small, Focused, Well-Named Tests (p.243)

### 23.3 Explanatory Assertion Messages (p.243)

### 23.4 Highlight Detail with Matchers (p.243)

### 23.5 Self-Describing Value (p.244)

### 23.6 Obviously Canned Value (p.245)

### 23.7 Tracer Object (p.245)

### 23.8 Explicitly Assert That Expectations Were Satisfied (p.246)

### 23.9 Diagnostics Are a First-Class Feature (p.246)

## 24. Chapter 24: Test Flexibility (p.248)

### 24.1 Introduction (p.248)

### 24.2 Test for Information, Not Representation (p.249)

### 24.3 Precise Assertions (p.250)

### 24.4 Precise Expectations (p.252)

### 24.5 "Guinea Pig" Objects (p.259)

# Part V: Advanced Topics (p.262)

## 25. Chapter 25: Testing Persistence (p.264)

### 25.1 Introduction (p.264)

### 25.2 Isolate Tests That Affect Persistent State (p.265)

### 25.3 Make Tests Transaction Boundaries Explicit (p.267)

### 25.4 Testing an Object That Performs Persistence Operations (p.269)

### 25.5 Testing That Objects Can Be Persisted (p.272)

### 25.6 But Database Tests Are S-l-o-w! (p.275)

## 26. Chapter 26: Unit Testing and Threads (p.276)

### 26.1 Introduction (p.276)

### 26.2 Separating Functionality and Concurrency Policy (p.277)

### 26.3 Unit-Testing Synchronization (p.281)

### 26.4 Stress-Testing Passive Objects (p.286)

### 26.5 Synchronizing the Test Thread with Background Threads (p.287)

### 26.6 The Limitations of Unit Stress Tests (p.288)

## 27. Chapter 27: Testing Asynchronous Code (p.290)

### 27.1 Introduction (p.290)

### 27.2 Sampling or Listening (p.291)

### 27.3 Two Implementations (p.293)

### 27.4 Runaway Tests (p.297)

### 27.5 Lost Updates (p.298)

### 27.6 Testing That an Action Has No Effect (p.300)

### 27.7 Distinguish Synchronizations and Assertions (p.301)

### 27.8 Externalize Event Sources (p.301)

# Afterword: A Brief History of Mock Objects (p.304)

# Appendix A: jMock2 Cheat Sheet (p.310)

# Appendix B: Writing a Hamcrest Matcher (p.318)

# Bibliography (p.322)

# Index (p.324)

## A (p.324)

## B (p.325)

## C (p.325)

## D (p.326)

## E (p.326)

## F (p.327)

## G (p.327)

## H (p.327)

## I (p.327)

## J (p.328)

## L (p.328)

## M (p.329)

## N (p.329)

## O (p.330)

## P (p.330)

## Q (p.330)

## R (p.330)

## S (p.331)

## T (p.332)

## U (p.333)

## V (p.333)

## W (p.333)

## X (p.333)