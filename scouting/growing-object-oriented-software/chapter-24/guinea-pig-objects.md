Line1 # "Guinea Pig" Objects (pp.284-288)
Line2 
Line3 ---
Line4 **Page 284**
Line5 
Line6 “Guinea Pig” Objects
Line7 In the “ports and adapters” architecture we described in “Designing for
Line8 Maintainability” (page 47), the adapters map application domain objects onto
Line9 the system’s technical infrastructure. Most of the adapter implementations we
Line10 see are generic; for example, they often use reﬂection to move values between
Line11 domains. We can apply such mappings to any type of object, which means we
Line12 can change our domain model without touching the mapping code.
Line13 The easiest approach when writing tests for the adapter code is to use types
Line14 from the application domain model, but this makes the test brittle because it
Line15 binds together the application and adapter domains. It introduces a risk of mis-
Line16 leadingly breaking tests when we change the application model, because we
Line17 haven’t separated the concerns.
Line18 Here’s an example. A system uses an XmlMarshaller to marshal objects to and
Line19 from XML so they can be sent across a network. This test exercises XmlMarshaller
Line20 by round-tripping an AuctionClosedEvent object: a type that the production
Line21 system really does send across the network.
Line22 public class XmlMarshallerTest {
Line23   @Test public void 
Line24 marshallsAndUnmarshallsSerialisableFields() {
Line25     XMLMarshaller marshaller = new XmlMarshaller();
Line26     AuctionClosedEvent original = new AuctionClosedEventBuilder().build();
Line27     String xml = marshaller.marshall(original);
Line28     AuctionClosedEvent unmarshalled = marshaller.unmarshall(xml);
Line29     assertThat(unmarshalled, hasSameSerialisableFieldsAs(original));
Line30   }
Line31 }
Line32 Later we decide that our system won’t send an AuctionClosedEvent after all,
Line33 so we should be able to delete the class. Our refactoring attempt will fail because
Line34 AuctionClosedEvent is still being used by the XmlMarshallerTest. The irrelevant
Line35 coupling will force us to rework the test unnecessarily.
Line36 There’s a more signiﬁcant (and subtle) problem when we couple tests to domain
Line37 types: it’s harder to see when test assumptions have been broken. For example,
Line38 our XmlMarshallerTest also checks how the marshaller handles transient and
Line39 non-transient ﬁelds. When we wrote the tests, AuctionClosedEvent included both
Line40 kind of ﬁelds, so we were exercising all the paths through the marshaller. Later,
Line41 we removed the transient ﬁelds from AuctionClosedEvent, which means that we
Line42 have tests that are no longer meaningful but do not fail. Nothing is alerting us
Line43 that we have tests that have stopped working and that important features are
Line44 not being covered.
Line45 Chapter 24
Line46 Test Flexibility
Line47 284
Line48 
Line49 
Line50 ---
Line51 
Line52 ---
Line53 **Page 285**
Line54 
Line55 We should test the XmlMarshaller with speciﬁc types that are clear about the
Line56 features that they represent, unrelated to the real system. For example, we can
Line57 introduce helper classes in the test:
Line58 public class XmlMarshallerTest {
Line59   public static class MarshalledObject {
Line60     private String privateField = "private";
Line61     public final String publicFinalField = "public final";
Line62     public int primitiveField;
Line63 // constructors, accessors for private field, etc.
Line64   }
Line65   public static class WithTransient extends MarshalledObject {
Line66     public transient String transientField = "transient";
Line67   }  
Line68   @Test public void 
Line69 marshallsAndUnmarshallsSerialisableFields() {
Line70     XMLMarshaller marshaller = new XmlMarshaller();
Line71 WithTransient original = new WithTransient();
Line72     String xml = marshaller.marshall(original);
Line73     AuctionClosedEvent unmarshalled = marshaller.unmarshall(xml);
Line74     assertThat(unmarshalled, hasSameSerialisableFieldsAs(original));
Line75   }
Line76 } 
Line77 The WithTransient class acts as a “guinea pig,” allowing us to exhaustively
Line78 exercise the behavior of our XmlMarshaller before we let it loose on our produc-
Line79 tion domain model. WithTransient also makes our test more readable because
Line80 the class and its ﬁelds are examples of “Self-Describing Value” (page 269), with
Line81 names that reﬂect their roles in the test.
Line82 285
Line83 Guinea Pig Objects
Line84 
Line85 
Line86 ---
Line87 
Line88 ---
Line89 **Page 286**
Line90 
Line91 This page intentionally left blank
