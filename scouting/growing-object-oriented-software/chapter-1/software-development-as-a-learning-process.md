Line1 # Software Development as a Learning Process (pp.3-4)
Line2 
Line3 ---
Line4 **Page 3**
Line5 
Line6 Chapter 1
Line7 What Is the Point of
Line8 Test-Driven Development?
Line9 One must learn by doing the thing; for though you think you know it,
Line10 you have no certainty, until you try.
Line11 —Sophocles
Line12 Software Development as a Learning Process
Line13 Almost all software projects are attempting something that nobody has done
Line14 before (or at least that nobody in the organization has done before). That some-
Line15 thing may refer to the people involved, the application domain, the technology
Line16 being used, or (most likely) a combination of these. In spite of the best efforts of
Line17 our discipline, all but the most routine projects have elements of surprise. Inter-
Line18 esting projects—those likely to provide the most beneﬁt—usually have a lot
Line19 of surprises.
Line20 Developers often don’t completely understand the technologies they’re using.
Line21 They have to learn how the components work whilst completing the project.
Line22 Even if they have a good understanding of the technologies, new applications
Line23 can force them into unfamiliar corners. A system that combines many signiﬁcant
Line24 components (which means most of what a professional programmer works on)
Line25 will be too complex for any individual to understand all of its possibilities.
Line26 For customers and end users, the experience is worse. The process of building
Line27 a system forces them to look at their organization more closely than they have
Line28 before. They’re often left to negotiate and codify processes that, until now,
Line29 have been based on convention and experience.
Line30 Everyone involved in a software project has to learn as it progresses. For the
Line31 project to succeed, the people involved have to work together just to understand
Line32 what they’re supposed to achieve, and to identify and resolve misunderstandings
Line33 along the way. They all know there will be changes, they just don’t know what
Line34 changes. They need a process that will help them cope with uncertainty as their
Line35 experience grows—to anticipate unanticipated changes.
Line36 3
Line37 
Line38 
Line39 ---
Line40 
Line41 ---
Line42 **Page 4**
Line43 
Line44 Feedback Is the Fundamental Tool
Line45 We think that the best approach a team can take is to use empirical feedback to
Line46 learn about the system and its use, and then apply that learning back to the system.
Line47 A team needs repeated cycles of activity. In each cycle it adds new features and
Line48 gets feedback about the quantity and quality of the work already done. The team
Line49 members split the work into time boxes, within which they analyze, design,
Line50 implement, and deploy as many features as they can.
Line51 Deploying completed work to some kind of environment at each cycle is critical.
Line52 Every time a team deploys, its members have an opportunity to check their as-
Line53 sumptions against reality. They can measure how much progress they’re really
Line54 making, detect and correct any errors, and adapt the current plan in response to
Line55 what they’ve learned. Without deployment, the feedback is not complete.
Line56 In our work, we apply feedback cycles at every level of development, organizing
Line57 projects as a system of nested loops ranging from seconds to months, such as:
Line58 pair programming, unit tests, acceptance tests, daily meetings, iterations, releases,
Line59 and so on. Each loop exposes the team’s output to empirical feedback so that
Line60 the team can discover and correct any errors or misconceptions. The nested
Line61 feedback loops reinforce each other; if a discrepancy slips through an inner loop,
Line62 there is a good chance an outer loop will catch it.
Line63 Each feedback loop addresses different aspects of the system and development
Line64 process. The inner loops are more focused on the technical detail: what a unit of
Line65 code does, whether it integrates with the rest of the system. The outer loops are
Line66 more focused on the organization and the team: whether the application serves
Line67 its users’ needs, whether the team is as effective as it could be.
Line68 The sooner we can get feedback about any aspect of the project, the better.
Line69 Many teams in large organizations can release every few weeks. Some teams re-
Line70 lease every few days, or even hours, which gives them an order of magnitude
Line71 increase in opportunities to receive and respond to feedback from real users.
Line72 Incremental and Iterative Development
Line73 In a project organized as a set of nested feedback loops, development is
Line74 incremental and iterative.
Line75 Incremental development builds a system feature by feature, instead of building
Line76 all the layers and components and integrating them at the end. Each feature is
Line77 implemented as an end-to-end “slice” through all the relevant parts of the system.
Line78 The system is always integrated and ready for deployment.
Line79 Iterative development progressively reﬁnes the implementation of features in
Line80 response to feedback until they are good enough.
Line81 Chapter 1
Line82 What Is the Point of Test-Driven Development?
Line83 4
Line84 
Line85 
Line86 ---
