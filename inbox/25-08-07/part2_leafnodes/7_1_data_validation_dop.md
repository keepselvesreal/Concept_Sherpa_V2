# 7.1 Data validation in DOP

Theo has rescheduled his meetings. With such an imposing deadline, he’s still not sure if
he’s made a big mistake giving DOP a second chance.
 NOTE The reason why Theo rescheduled his meetings is explained in the opener
for part 2. Take a moment to read the opener if you missed it.
Joe What aspect of OOP do you think you will miss the most in your big project?
Theo Data validation.
Joe Can you elaborate a bit?
Theo In OOP, I have this strong guarantee that when a class is instantiated, its mem-
ber fields have the proper names and proper types. But with DOP, it’s so easy
to have small mistakes in field names and field types.
Joe Well, I have good news for you! There is a way to validate data in DOP.
Theo How does it work? I thought DOP and data validation were two contradictory
concepts!
Joe Not at all. It’s true that DOP doesn’t force you to validate data, but it doesn’t
prevent you from doing so. In DOP, the data schema is separate from the data
representation.
Theo I don’t get how that would eliminate data consistency issues.
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

## 페이지 171