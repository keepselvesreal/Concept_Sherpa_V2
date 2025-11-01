Line1 # Stop Me If You've Heard This One Before (pp.21-21)
Line2 
Line3 ---
Line4 **Page 21**
Line5 
Line6 Chapter 3
Line7 An Introduction to the Tools
Line8 Man is a tool-using animal. Without tools he is nothing, with tools he
Line9 is all.
Line10 —Thomas Carlyle
Line11 Stop Me If You’ve Heard This One Before
Line12 This book is about the techniques of using tests to guide the development of
Line13 object-oriented software, not about speciﬁc technologies. To demonstrate the
Line14 techniques in action, however, we’ve had to pick some technologies for our ex-
Line15 ample code. For the rest of the book we’re going to use Java, with the JUnit 4,
Line16 Hamcrest, and jMock2 frameworks. If you’re using something else, we hope
Line17 we’ve been clear enough so that you can apply these ideas in your environment.
Line18 In this chapter we brieﬂy describe the programming interfaces for these three
Line19 frameworks, just enough to help you make sense of the code examples in the rest
Line20 of the book. If you already know how to use them, you can skip this chapter.
Line21 A Minimal Introduction to JUnit 4
Line22 We use JUnit 4 (version 4.6 at the time of writing) as our Java test framework.1
Line23 In essence, JUnit uses reﬂection to walk the structure of a class and run whatever
Line24 it can ﬁnd in that class that represents a test. For example, here’s a test that
Line25 exercises a Catalog class which manages a collection of Entry objects:
Line26 public class CatalogTest {
Line27   private final Catalog catalog = new Catalog();
Line28   @Test public void containsAnAddedEntry() { 
Line29     Entry entry = new Entry("fish", "chips");
Line30     catalog.add(entry);
Line31     assertTrue(catalog.contains(entry));
Line32   }
Line33   @Test public void indexesEntriesByName() {
Line34     Entry entry = new Entry("fish", "chips");
Line35     catalog.add(entry);
Line36     assertEquals(entry, catalog.entryFor("fish"));  
Line37     assertNull(catalog.entryFor("missing name"));  
Line38   }
Line39 }
Line40 1. JUnit is bundled with many Java IDEs and is available at www.junit.org.
Line41 21
Line42 
Line43 
Line44 ---
