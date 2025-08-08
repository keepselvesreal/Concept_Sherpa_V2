# 8.1 The complexity of locks

8.1 The complexity of locks
This Sunday afternoon, while riding his bike across the Golden Gate Bridge, Theo thinks
about the Klafim project with concern, not yet sure that betting on DOP was a good
choice. Suddenly, Theo realizes that he hasn’t yet scheduled the next session with Joe. He
gets off his bike to call Joe. Bad luck, the line is busy.
When Theo gets home, he tries to call Joe again, but once again the phone is busy. After
dinner, Theo tries to call Joe one more time, with the same result—a busy signal. “Obvi-
ously, Joe is very busy today,” Theo tells himself. Exhausted by his 50-mile bike ride at an
average of 17 miles per hour, he falls asleep on the sofa. When Theo wakes up, he’s elated
to see a text message from Joe, “See you Monday morning at 11 AM?” Theo answers with a
thumbs up and prepares for another week of work.
When Joe arrives at the office, Theo asks him why his phone was constantly busy the day
before. Joe answers that he was about to ask Theo the same question. They look at each
other, puzzled, and then simultaneously break into laughter as they realize what hap-
pened: in an amazing coincidence, they’d tried to phone each other at exactly the same
times. They both say at once:
“A deadlock!”
They both head for Theo’s office. When they get to Theo’s desk, Joe tells him that today’s
session is going to be about concurrency management in multi-threaded environments.
Joe How do you usually manage concurrency in a multi-threaded environment?
Theo I protect access to critical sections with a lock mechanism, a mutex, for instance.
Joe When you say access, do you mean write access or also read access?
Theo Both!
Joe Why do you need to protect read access with a lock?
Theo Because, without a lock protection, in the middle of a read, a write could hap-
pen in another thread. It would make my read logically inconsistent.
Joe Another option would be to clone the data before processing it in a read.
Theo Sometimes I would clone the data; but in many cases, when it’s large, it’s too
expensive to clone.
TIP Cloning data to avoid read locks doesn’t scale.
Joe In DOP, we don’t need to clone or to protect read access.
Theo Because data is immutable?
Joe Right. When data is immutable, even if a write happens in another thread
during a read, it won’t make the read inconsistent because the write never
mutates the data that is read.
Theo In a sense, a read always works on a data snapshot.
Joe Exactly!
TIP When data is immutable, a read is always safe.
Theo But what about write access? Don’t you need to protect that with locks?
Joe Nope.

## 페이지 193