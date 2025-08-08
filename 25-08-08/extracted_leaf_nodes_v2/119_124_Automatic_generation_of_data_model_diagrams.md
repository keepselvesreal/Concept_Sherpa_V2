# 12.4 Automatic generation of data model diagrams

**메타데이터:**
- ID: 119
- 레벨: 2
- 페이지: 288-289
- 페이지 수: 2
- 부모 ID: 114
- 텍스트 길이: 3835 문자

---

eneration of data model diagrams
Before going home, Theo phones Joe to tell him about how he and Dave used data valida-
tion inside the system. Joe tells Theo that that’s exactly how he recommends doing it and
suggests he come and visit Theo and Dave at the office tomorrow. He wants to show them
some cool advanced stuff related to data validation. The next day, with coffee in hand, Joe
starts the discussion.
Joe Are you guys starting to feel the power of data validation à la DOP?
Dave Yes, it’s a bit less convenient to validate a JSON Schema than it is to write the
class of function arguments, but this drawback is compensated by the fact that
JSON Schema supports conditions that go beyond static types.
Theo We also realized that we don’t have to validate data for each and every function.
Joe Correct. Now, let me show you another cool thing that we can do with JSON
Schema.
Dave What’s that?
Joe Generate a data model diagram.
Dave Wow! How does that work?
Joe There are tools that receive a JSON Schema as input and produce a diagram in
a data model format.
Dave What is a data model format?
Joe It’s a format that allows you to define a data model in plain text. After that, you
can generate an image from the text. My favorite data format is PlantUML.
 NOTE For more on PlantUML, see https://plantuml.com/.
Dave Do you know of other tools that generate data model diagrams?
Joe I have used JSON Schema Viewer and Malli.

12.4 Automatic generation of data model diagrams 261
 NOTE You can find information on the JSON Schema Viewer at https://navneethg
.github.io/jsonschemaviewer/ and on Malli at https://github.com/metosin/malli.
Joe shows Dave and Theo the PlantUML diagram that Malli generated (listing 12.18) from
the catalog schema in listings 12.16 and 12.17.
Listing12.18 A PlantUML diagram generated from the catalog data schema
@startuml
Entity1 *-- Entity2
Entity1 *-- Entity4
Entity2 *-- Entity3
class Entity1 {
+ booksByIsbn: {Entity2}
+ authorsById: {Entity4}
}
class Entity2 {
+ title : String
+ publicationYear: Number
+ isbn: String
+ authorIds: [String]
+ bookItems: [Entity3]
}
class Entity3 {
+ id: String
+ libId: String
+ purchaseDate: String
+ isLent: Boolean
}
class Entity4 {
+ id: String
+ name: String
+ bookIsbns: [String]
}
@enduml
Dave Is it possible to visualize this diagram?
Joe Absolutely. Let me copy and paste the diagram text into the PlantText online
tool.
 NOTE See https://www.planttext.com/ for more on the PlantText online tool.
Dave opens his web browser and types the URL for PlantText. After copying and pasting
the text, he steps aside so that Theo and Dave can view the diagram that looks like the
image in figure 12.2.

262 CHAPTER 12 Advanced data validation
C Entity1
booksByIsbn: {Entity2}
authorsById: {Entity3}
C Entity2 C Entity4
title : String id: String
publicationYear: Number name: String
isbn: String booklsbns: [String]
authorlds: [String]
bookltems: [Entity3]
C Entity3
id: String
libld: String
Figure 12.2 A visualization of
purchaseDate: String
the PlantUML diagram generated
isLent: Boolean
from the catalog data schema
Dave That’s cool! But why are the diagram entities named Entity1, Entity2, and
so on?
Joe Because in JSON Schema, there’s no way to give a name to a schema. Malli has
to autogenerate random names for you.
Theo Also, I see that the extra information we have in the schema, like the number
range for publicationYear and string regular expression for isbn, is missing
from the diagram.
Joe Right, that extra information is not part of the data model. That’s why it’s not
included in the generated data model diagram.
Dave Anyway, it’s very cool!
Joe If you guys like the data model generation feature, I’m sure you’re going to
like the next feature.
Dave What’s it about?
Joe Automatic generation of unit tests.
Theo Wow, sounds exciting!