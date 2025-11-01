Line1 # Two Implementations (pp.318-322)
Line2 
Line3 ---
Line4 **Page 318**
Line5 
Line6 Put the Timeout Values in One Place
Line7 Both observation strategies use a timeout to detect that the system has failed.
Line8 Again, there’s a balance to be struck between a timeout that’s too short, which will
Line9 make the tests unreliable, and one that’s too long, which will make failing tests too
Line10 slow. This balance can be different in different environments, and will change as
Line11 the system grows over time.
Line12 When the timeout duration is deﬁned in one place, it’s easy to ﬁnd and change.
Line13 The team can adjust its value to ﬁnd the right balance between speed and reliability
Line14 as the system develops.
Line15 Two Implementations
Line16 Scattering ad hoc sleeps and timeouts throughout the tests makes them difﬁcult
Line17 to understand, because it leaves too much implementation detail in the tests
Line18 themselves. Synchronization and assertion is just the sort of behavior that’s
Line19 suitable for factoring out into subordinate objects because it usually turns into
Line20 a bad case of duplication if we don’t. It’s also just the sort of tricky code that we
Line21 want to get right once and not have to change again.
Line22 In this section, we’ll show an example implementation of each observation
Line23 strategy.
Line24 Capturing Notiﬁcations
Line25 An event-based assertion waits for an event by blocking on a monitor until it
Line26 gets notiﬁed or times out. When the monitor is notiﬁed, the test thread wakes
Line27 up and continues if it ﬁnds that the expected event has arrived, or blocks again.
Line28 If the test times out, then it raises a failure.
Line29 NotificationTrace is an example of how to record and test notiﬁcations sent
Line30 by the system. The setup of the test will arrange for the tested code to call
Line31 append() when the event happens, for example by plugging in an event listener
Line32 that will call the method when triggered. In the body of the test, the test thread
Line33 calls containsNotification() to wait for the expected notiﬁcation or fail if it
Line34 times out. For example:
Line35 trace.containsNotification(startsWith("WANTED"));
Line36 will wait for a notiﬁcation string that starts with WANTED.
Line37 Within NotificationTrace, incoming notiﬁcations are stored in a list trace,
Line38 which is protected by a lock traceLock. The class is generic, so we don’t specify
Line39 the type of these notiﬁcations, except to say that the matchers we pass into
Line40 containsNotification() must be compatible with that type. The implementation
Line41 uses Timeout and NotificationStream classes that we’ll describe later.
Line42 Chapter 27
Line43 Testing Asynchronous Code
Line44 318
Line45 
Line46 
Line47 ---
Line48 
Line49 ---
Line50 **Page 319**
Line51 
Line52 public class NotificationTrace<T> {
Line53   private final Object traceLock = new Object();
Line54   private final List<T> trace = new ArrayList<T>(); 1
Line55   private long timeoutMs;
Line56 // constructors and accessors to configure the timeout […]
Line57   public void append(T message) { 2
Line58     synchronized (traceLock) {
Line59       trace.add(message);
Line60 traceLock.notifyAll();
Line61     }
Line62   }
Line63   public void containsNotification(Matcher<? super T> criteria) 3
Line64     throws InterruptedException 
Line65   { 
Line66     Timeout timeout = new Timeout(timeoutMs); 
Line67     synchronized (traceLock) {
Line68       NotificationStream<T> stream = new NotificationStream<T>(trace, criteria);
Line69       while (! stream.hasMatched()) {
Line70         if (timeout.hasTimedOut()) {
Line71           throw new AssertionError(failureDescriptionFrom(criteria));
Line72         }
Line73         timeout.waitOn(traceLock);
Line74       }
Line75     }
Line76   }
Line77   private String failureDescriptionFrom(Matcher<? super T> matcher) {  […] 
Line78     // Construct a description of why there was no match, 
Line79     // including the matcher and all the received messages. 
Line80 }
Line81 1
Line82 We store notiﬁcations in a list so that they’re available to us for other queries
Line83 and so that we can include them in a description if the test fails (we don’t
Line84 show how the description is constructed).
Line85 2
Line86 The append() method, called from a worker thread, appends a new notiﬁca-
Line87 tion to the trace, and then tells any threads waiting on traceLock to wake
Line88 up because there’s been a change. This is called by the test infrastructure
Line89 when triggered by an event in the system.
Line90 3
Line91 The containsNotification() method, called from the test thread, searches
Line92 through all the notiﬁcations it has received so far. If it ﬁnds a notiﬁcation
Line93 that matches the given criteria, it returns. Otherwise, it waits until more
Line94 notiﬁcations arrive and checks again. If it times out while waiting, then it
Line95 fails the test.
Line96 The nested NotificationStream class searches the unexamined elements in its
Line97 list for one that matches the given criteria. It allows the list to grow between calls
Line98 to hasMatched() and picks up after the last element it looked at.
Line99 319
Line100 Two Implementations
Line101 
Line102 
Line103 ---
Line104 
Line105 ---
Line106 **Page 320**
Line107 
Line108 private static class NotificationStream<N> {
Line109   private final List<N> notifications;
Line110   private final Matcher<? super N> criteria;
Line111   private int next = 0;
Line112   public NotificationStream(List<N> notifications, Matcher<? super N> criteria) {
Line113     this.notifications = notifications;
Line114     this.criteria = criteria;
Line115   }
Line116   public boolean hasMatched() {
Line117     while (next < notifications.size()) {
Line118       if (criteria.matches(notifications.get(next)))
Line119         return true;
Line120       next++;
Line121     }
Line122     return false;
Line123   }
Line124 }
Line125 NotificationTrace is one example of a simple coordination class between test
Line126 and worker threads. It uses a simple approach, although it does avoid a possible
Line127 race condition where a background thread delivers a notiﬁcation before the test
Line128 thread has started waiting. Another implementation, for example, might have
Line129 containsNotification() only search messages received after the previous call.
Line130 What is appropriate depends on the context of the test.
Line131 Polling for Changes
Line132 A sample-based assertion repeatedly samples some visible effect of the system
Line133 through a “probe,” waiting for the probe to detect that the system has entered
Line134 an expected state. There are two aspects to the process of sampling: polling the
Line135 system and failure reporting, and probing the system for a given state. Separating
Line136 the two helps us think clearly about the behavior, and different tests can reuse the
Line137 polling with different probes.
Line138 Poller is an example of how to poll a system. It repeatedly calls its probe, with
Line139 a short delay between samples, until the system is ready or the poller times out.
Line140 The poller drives a probe that actually checks the target system, which we’ve
Line141 abstracted behind a Probe interface.
Line142 public interface Probe {
Line143   boolean isSatisfied();
Line144   void sample();
Line145   void describeFailureTo(Description d);
Line146 }
Line147 The probe’s sample() method takes a snapshot of the system state that the test
Line148 is interested in. The isSatisfied() method returns true if that state meets the
Line149 test’s acceptance criteria. To simplify the poller logic, we allow isSatisfied()
Line150 to be called before sample().
Line151 Chapter 27
Line152 Testing Asynchronous Code
Line153 320
Line154 
Line155 
Line156 ---
Line157 
Line158 ---
Line159 **Page 321**
Line160 
Line161 public class Poller {
Line162   private long timeoutMillis;
Line163   private long pollDelayMillis;
Line164 // constructors and accessors to configure the timeout […]
Line165   public void check(Probe probe) throws InterruptedException {
Line166     Timeout timeout = new Timeout(timeoutMillis);
Line167     while (! probe.isSatisfied()) {
Line168       if (timeout.hasTimedOut()) {
Line169         throw new AssertionError(describeFailureOf(probe));
Line170       }
Line171       Thread.sleep(pollDelayMillis);
Line172       probe.sample();
Line173     }
Line174   }
Line175   private String describeFailureOf(Probe probe) { […] 
Line176 }
Line177 This simple implementation delegates synchronization with the system to
Line178 the probe. A more sophisticated version might implement synchronization in the
Line179 poller, so it could be shared between probes. The similarity to NotificationTrace
Line180 is obvious, and we could have pulled out a common abstract structure, but we
Line181 wanted to keep the designs clear for now.
Line182 To poll, for example, for the length of a ﬁle, we would write this line in a test:
Line183 assertEventually(fileLength("data.txt", is(greaterThan(2000))));
Line184 This wraps up the construction of our sampling code in a more expressive
Line185 assertion. The helper methods to implement this are:
Line186 public static void assertEventually(Probe probe) throws InterruptedException {
Line187   new Poller(1000L, 100L).check(probe);
Line188 }
Line189 public static Probe fileLength(String path, final Matcher<Integer> matcher) {
Line190   final File file = new File(path);
Line191   return new Probe() {
Line192     private long lastFileLength = NOT_SET;
Line193     public void sample() { lastFileLength = file.length(); }
Line194     public boolean isSatisfied() { 
Line195       return lastFileLength != NOT_SET && matcher.matches(lastFileLength);
Line196     }
Line197     public void describeFailureTo(Description d) {
Line198       d.appendText("length was ").appendValue(lastFileLength);
Line199     }
Line200   };
Line201 }
Line202 Separating the act of sampling from checking whether the sample is satisfactory
Line203 makes the structure of the probe clearer. We can hold on to the sample result to
Line204 report the unsatisfactory result we found if there’s a failure.
Line205 321
Line206 Two Implementations
Line207 
Line208 
Line209 ---
Line210 
Line211 ---
Line212 **Page 322**
Line213 
Line214 Timing Out
Line215 Finally we show the Timeout class that the two example assertion classes use. It
Line216 packages up time checking and synchronization:
Line217 public class Timeout {
Line218  private final long endTime;
Line219   public Timeout(long duration) {
Line220     this.endTime = System.currentTimeMillis() + duration;
Line221   }
Line222   public boolean hasTimedOut() { return timeRemaining() <= 0; }
Line223   public void waitOn(Object lock) throws InterruptedException {
Line224     long waitTime = timeRemaining();
Line225     if (waitTime > 0) lock.wait(waitTime);
Line226   }
Line227   private long timeRemaining() { return endTime - System.currentTimeMillis(); }
Line228 }
Line229 Retroﬁtting a Probe
Line230 We can now rewrite the test from the introduction. Instead of making an assertion
Line231 about the current holding of a stock, the test must wait for the holding of the
Line232 stock to reach the expected level within an acceptable time limit.
Line233 @Test public void buyAndSellOfSameStockOnSameDayCancelsOutOurHolding() {
Line234   Date tradeDate = new Date();
Line235   send(aTradeEvent().ofType(BUY).onDate(tradeDate).forStock("A").withQuantity(10));
Line236   send(aTradeEvent().ofType(SELL).onDate(tradeDate).forStock("A").withQuantity(10));
Line237 assertEventually(holdingOfStock("A", tradeDate, equalTo(0)));
Line238 }
Line239 Previously, the holdingOfStock() method returned a value to be compared.
Line240 Now it returns a Probe that samples the system’s holding and returns if it meets
Line241 the acceptance criteria deﬁned by a Hamcrest matcher—in this case equalTo(0).
Line242 Runaway Tests
Line243 Unfortunately, the new version of the test is still unreliable, even though we’re
Line244 now sampling for a result. The assertion is waiting for the holding to become
Line245 zero, which is what we started out with, so it’s possible for the test to pass before
Line246 the system has even begun processing. This test can run ahead of the system
Line247 without actually testing anything.
Line248 Chapter 27
Line249 Testing Asynchronous Code
Line250 322
Line251 
Line252 
Line253 ---
