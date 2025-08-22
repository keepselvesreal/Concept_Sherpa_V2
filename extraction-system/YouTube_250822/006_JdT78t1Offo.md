# Anthropic Co-founder: Building Claude Code, Lessons From GPT-3 &amp; LLM System Design

**Extracted Time:** 2025-08-22 16:01:08

---

[00:00] When we started out, we didn't seem like
[00:02] we were going to be successful at all.
[00:06] OpenAI had a billion dollars and like
[00:09] all of these all of this star power and
[00:11] we had seven co-founders in co like
[00:13] trying to build something and we didn't
[00:15] know if we were necessarily going to
[00:16] make a product or what the products
[00:17] would look like. One thing that's
[00:19] interesting to look at is just that
[00:21] humanity is on track for like the
[00:23] largest infrastructure buildout of all
[00:24] time. Tell us about the early days of
[00:26] anthropic. So you had a general idea of
[00:28] this sort of like long-term mission that
[00:30] you wanted to do to, you know, not
[00:32] destroy humanity, but like what did you
[00:34] actually work on for the first year? How
[00:36] did that converge on an actual product?
[00:39] [Music]
[00:45] Welcome back to another episode of The
[00:47] Light Cone. Today we've got a real
[00:49] treat, co-founder of Anthropic, Tom
[00:51] Brown.
[00:52] Excited to be here. So Tom, one of the
[00:54] things that a lot of the people watching
[00:56] uh would love to figure out is you got
[00:58] started in tech at the age of 21, fresh
[01:02] from MIT. How does someone go from that
[01:05] in 2009 to literally co-founding
[01:09] something as important as anthropic?
[01:12] Summer 2009, linked language. Two of my
[01:15] friends had started that out. I think
[01:17] they had seen one of our other friends,
[01:19] Kyle Vote, kind of do a YC company. And
[01:21] so it was in the water that that's a
[01:22] thing that we could try to do. They
[01:24] started out I was the first employee
[01:26] back then. Yeah. You guys let me join
[01:28] for all the dinners and stuff like that
[01:30] too. I could have instead gone to like a
[01:32] big tech company or something like that.
[01:33] And I think probably just as a software
[01:36] engineer, I might have learned more
[01:37] software engineering skills. But I think
[01:40] by being there with the other
[01:44] co-founders without anyone telling us
[01:46] what to do basically like we had to
[01:48] figure out how to live, how to like the
[01:50] company would die by default. I think in
[01:52] school there was a lot of like a feeling
[01:53] of more of people would give me tasks
[01:55] and I would do the tasks. It's kind of
[01:56] like a dog waiting for like food to be
[01:58] like fed to them in their bowl or
[02:00] something like that. And I think for
[02:01] that company it was more like wolves and
[02:03] we have to like hunt our real like food
[02:05] otherwise like we're our kids are going
[02:07] to starve or something like that. I
[02:08] think that that mindset I think has been
[02:10] like the most valuable mindset that
[02:13] shift that I've had for trying to do
[02:15] like bigger more exciting things.
[02:17] Yeah. Big tech just teaches you to work
[02:20] at a big tech company whereas uh it's
[02:23] much more fun to be a wolf.
[02:24] Yeah. How did you go from like so
[02:26] working at friend's startup to then you
[02:29] started your own one? So linked was um
[02:32] we ran the company for a bit. I ended up
[02:34] going back to to school afterwards and
[02:37] then when I left school I went to this
[02:40] company Mopub
[02:41] the mobile advertising thing right?
[02:42] Yeah. Yeah. I was like the first
[02:44] engineer there. I was like okay I want
[02:46] to be a wolf but like I was really bad
[02:48] at programming also. I was like very
[02:51] very struggling as like a a like
[02:53] software engineer. I know I want to do
[02:55] more but I don't know how to do it yet.
[02:56] And so I think that was kind of like a
[02:58] experience getting to scale something.
[03:00] Winter 2012, one of my friends who was
[03:02] my smartest friend from college pitched
[03:05] me on let's go and start a YC company.
[03:07] We did at the time solid stage. This was
[03:10] before Docker existed. And so the idea
[03:12] was try to make it easier to do DevOps,
[03:14] but Docker doesn't exist. So it's going
[03:16] to be a more flexible Heroku, which
[03:18] basically meant a more complicated like
[03:20] Heroku. And so we I remember we like we
[03:23] interviewed with you guys. I think folks
[03:25] didn't really understand what we were
[03:27] trying to build. I think we didn't
[03:28] really understand what we were trying to
[03:29] build that much
[03:30] when you're trying to do something new.
[03:31] That's actually sometimes common.
[03:33] Yeah. I think we were an outlier there
[03:35] cuz we like did our interviews and then
[03:36] we got called back driving back to San
[03:38] Francisco and TLB had written on the
[03:40] board like an angry frowny face and what
[03:43] are you actually going to build? And so
[03:46] he like wanted us to explain that. I
[03:49] guess we explained it enough or he was
[03:51] just like these guys still don't know
[03:52] what they're doing but maybe they'll
[03:54] figure it out. Halfway through I kind of
[03:56] felt I still didn't actually understand
[03:58] what we were going to build and how we
[04:01] would attach a mission to it that like I
[04:02] wanted to to work on for my whole life.
[04:05] Yeah.
[04:05] Um and so I left PG actually introed me
[04:08] to Michael Waxman who was the grouper
[04:11] founder.
[04:12] Yeah. So,
[04:12] so Grouper was a dating app only it was
[04:15] novel in that you had what three guys
[04:18] and three girls. Y
[04:19] this was before AI in a lot of ways. So
[04:21] there was like a set of a team of people
[04:23] who would manually link people up,
[04:25] right? And they'd meet up at a bar and
[04:28] shenanigans would ensue.
[04:30] Yes. Reliably shenanigans. People didn't
[04:33] always have a great time. I think you
[04:34] went you went on a couple group.
[04:36] Okay.
[04:37] The pitch for grouper for me for like
[04:39] why I was excited for it was just I was
[04:42] like an incredibly awkward kid. What I
[04:45] wanted to do was to basically have a
[04:48] thing that lets awkward people like me
[04:50] go out and talk to other people for me
[04:53] to talk to girls and feel like I was
[04:56] safe doing it with like my friends
[04:57] around and stuff like that. And so I
[04:58] think who were going to be our employees
[05:00] was important. I did like all of our
[05:02] engineering interviews. who would take
[05:03] someone. The only person who went on
[05:05] more was Greg Brockman.
[05:07] I think he had I think he had a he had a
[05:09] phase where like every single week
[05:11] he would go and like post on uh Slack or
[05:14] Hip Chat at the time.
[05:15] New York and he was hanging out at the
[05:16] Recurse Center during this period. I
[05:18] think
[05:18] Oh, I I think he was at Stripe. Maybe
[05:21] maybe for part of it he was at Recurse.
[05:22] Yeah. But he also had uh I think just
[05:25] like a phase where he would just at
[05:26] Stripe he would just like post in their
[05:28] thing every like I'm going on grouper
[05:29] who's going for like a whole year.
[05:31] So I I ended up being close with Greg
[05:33] which which ended up being a connection
[05:35] to the open AAI.
[05:36] What was the journey like? Because you
[05:37] started as u you just graduated from MIT
[05:40] CS. You were 21. You became first an
[05:44] early employee for all these YC
[05:46] startups. Then you started your company
[05:47] just a couple years later. And what was
[05:51] the path for you to eventually become
[05:53] the co-founder of Anthropic? It was like
[05:55] a long path but it's pretty impressive.
[05:57] How how did you get there? I mean, it
[05:59] sounds like getting in touch with Greg
[06:01] at that moment moment.
[06:04] Uh, and then you were one of the first
[06:05] uh, you know, a couple dozen people to
[06:07] join OpenAI as a result.
[06:10] Yeah. So, I left Grouper 2014,
[06:14] June 2014, and I joined OpenAI
[06:19] I think a year later. I tried to like
[06:21] build up courage to make the switch to
[06:23] be a to try to learn AI research. At the
[06:26] time I was like, "Okay, it seems like
[06:27] sometime in our lifetimes we might end
[06:29] up making transformative AI. If we do,
[06:31] that would be the biggest thing. Maybe
[06:33] there's some way that I could help out,
[06:35] but also I got like a B minus in linear
[06:38] algebra in college." And so it seemed
[06:41] like at the time you needed to be just
[06:42] top superstar in order to try to help
[06:44] out with that at all. And so I think I
[06:46] had like a lot of uncertainty about
[06:47] whether I would be able to help. And
[06:49] also I'd had some success with startups.
[06:51] And so a lot of me was just like rather
[06:53] than trying to retool at this like I
[06:54] could try to do another startup or
[06:56] something like that. I feel like in that
[06:58] period um going to work on AI research
[07:00] which is not seen as like a ser like not
[07:03] like a practically serious thing to do
[07:04] and you're in a world where it's like
[07:06] people try and build companies and do
[07:07] these like really practical things like
[07:08] what did your were your friends like oh
[07:10] that's really cool you're going to go
[07:11] work on AI stuff or was it
[07:12] not really
[07:14] I think my friends were like that sounds
[07:15] that sounds weird and bad kind of like
[07:18] it it doesn't really seem like it
[07:19] doesn't seem like like AI safety is a
[07:21] thing we should be wear like
[07:22] overpopulation on Mars doesn't make any
[07:23] sense and my friends were also just like
[07:25] I don't know if you're going to be good
[07:26] at that tough. I think that for that
[07:29] reason, I think I didn't try very hard
[07:31] for I like kind of flip-flopped on it
[07:33] for like 6 months trying to build up
[07:34] courage to do it.
[07:36] And what were you specifically at this
[07:37] point? Like you're reading research
[07:39] papers like what it what does it look
[07:41] like?
[07:41] Yeah. So, first I was just kind of
[07:44] hanging out. I built like an art car for
[07:45] Titanic 7 and stuff like that.
[07:47] Oh, that was fun. Yeah.
[07:48] Yeah. So I I spent like a whole summer
[07:51] like 3 months after Grouper doing that
[07:52] cuz honestly I was I was like kind of
[07:54] burned out for Grouper where I know
[07:56] startups like the highs are high like
[07:57] the lows are low and we weren't working
[07:59] at the end. Our business wasn't
[08:00] succeeding. Our revenue was going down
[08:03] but I my main job still was like
[08:04] recruiting engineers and so I had to
[08:06] like pitch them on this dream that I had
[08:07] had but I like no longer really
[08:09] sounds like a death march. And so I was
[08:12] super burnt out and I was like, "Okay,
[08:13] Tom, like chill out, do some yoga, like
[08:15] do some CrossFit, like build an art
[08:16] car." And
[08:17] what was the hindsight? Like, you know,
[08:18] hindsight's 2020. What's the
[08:20] retrospective on like Grouper obviously
[08:22] attracted all these really, really smart
[08:24] people. The graphs were up and to the
[08:26] right and then it flatlined and maybe
[08:28] started declining. What happened?
[08:30] I think that when we started the
[08:32] competition was like, "Okay, Cupid.
[08:35] It was all web- based."
[08:36] All web- based. The main problem that I
[08:38] think we were solving was the it's hard
[08:41] to like go and put yourself out there
[08:42] and go like talk to someone new and they
[08:44] might just be like I don't want to talk
[08:46] to you. You seem weird. And so we solved
[08:48] that by just blind matching. Tinder came
[08:51] out while we were doing grouper and
[08:53] Tinder solved that same problem with
[08:55] both people have to show interest before
[08:57] you get matched. So there's also no
[08:58] worries about getting rejected. And I
[09:00] think that they just had better that was
[09:02] a better solution to that same problem.
[09:03] So good work Tinder. Good work all the
[09:05] swipers. I think that that that solved
[09:07] the like mission that we were trying to
[09:09] solve better than we solved it.
[09:10] And then yeah, like when did you get
[09:12] serious about AI and just how did you
[09:14] approach
[09:16] it?
[09:16] Three months of like kind of playing and
[09:18] having fun and then I ran out of money
[09:20] also when I had like my personal runway.
[09:23] I I ran out and so I was like, okay, I
[09:26] think that I'm going to need 6 months of
[09:28] stealth study to have a shot at getting
[09:31] a job. At that point it was Deep Mind or
[09:33] Google Brain were the two places to do
[09:35] work there or MIRI. Merie was the third
[09:37] one that I was like looking at. So I was
[09:39] like if I want to help out with that
[09:41] those are the three places to look at. I
[09:43] don't have any of the skills yet. I need
[09:44] six months of self-study to feel like I
[09:47] would not be a drag on them and like
[09:48] actually be helping instead.
[09:49] Can you um maybe explain a bit what was
[09:53] that self study like? Because I'm sure
[09:54] there's a lot of software engineers
[09:55] right now in their 20s are looking to
[09:57] retool to become AI researchers. What
[10:00] was what was that six months like? Even
[10:02] though as you said you had uh gotten a B
[10:04] minus in linear algebra which is like
[10:06] core
[10:06] might have been a C++. I'm not I should
[10:08] check.
[10:10] I'm going to keep telling
[10:11] that's pretty impressive where where you
[10:12] got to.
[10:12] Yeah. Yeah. It turned out okay. First I
[10:14] did a contract actually with Twitch um
[10:16] and like earned like enough to have that
[10:18] six months of runway. So I did like
[10:20] three-month contract with Twitch and
[10:21] then I made a a plan to self-study. I
[10:24] don't think it's the right plan now for
[10:25] people too at least 2015. What did it
[10:28] looked like? It was like take a Corsera
[10:29] course on machine learning, try to solve
[10:33] some Kaggle projects, read linear
[10:36] algebra done right, and uh I had a
[10:39] statistics textbook. I think I had YC
[10:41] alumni credits and so I bought like a
[10:44] GPU
[10:46] and I would like SSH into the GPU to
[10:48] like work through my courses for it.
[10:50] And this is right after Yeah, it was
[10:52] already after Alex Knack, right?
[10:54] This is after Alex Neck. Yeah. So I was
[10:56] mostly doing image image classification
[10:58] stuff that I was trying to learn was
[11:00] like the thing that all the courses
[11:01] would teach you to do.
[11:02] How did you get the open AI job?
[11:04] Because you were one of the few
[11:06] engineers. It was mostly researchers and
[11:08] they had pretty stacked team of
[11:09] researchers.
[11:10] I messaged Greg um as soon as OpenAI was
[11:13] announced and I was like I'd love to
[11:15] help out in some way. I got a B minus in
[11:17] my linear algebra but I know some
[11:20] engineering. I've done a bit of
[11:21] distributed systems work. if you guys
[11:22] need help, I'm like happy to mop floors
[11:24] if if you guys need I want to help out,
[11:26] however. And I think Greg was like,
[11:28] yeah, I think there's like a posity of
[11:30] people who he said posity, too. I was
[11:32] like, fancy word there. There's a posity
[11:34] of people who know both machine learning
[11:37] and distributed systems. So, like, yes,
[11:38] you should do that. I think he
[11:40] introduced me to Peter Aiel also to help
[11:42] me put together like a little course for
[11:44] myself, too. And then I checked in on
[11:46] with him, I think every month or
[11:48] something. And then after a couple
[11:50] months he was like oh we actually have a
[11:51] project which is uh we need to put
[11:53] together we want to play a game like
[11:55] play games can you help uh make
[11:58] Starcraft environment and so I joined to
[12:01] like help them with the Starcraft uh
[12:02] environment. So that that ended up I
[12:04] think getting my foot in the door. I I
[12:06] didn't do any machine learning work with
[12:08] them for the first nine months that I
[12:10] was there basically.
[12:11] And what did OpenAI feel like at this
[12:13] point? Like had it raised much funding?
[12:15] Did it have like an office? which is
[12:17] what will do it. Did it feel like a
[12:18] startup?
[12:18] So it was in the chocolate on top of the
[12:20] dandelion chocolate factory. Um
[12:22] this is after Greg's apartment. That's
[12:24] the
[12:25] after Greg's apartment. Yeah. So like
[12:26] right after Greg's apartment in the
[12:27] chocolate factory when it kicked off,
[12:29] right? It was like a billion dollars of
[12:31] committed funding from Elon. It felt
[12:33] like it was like very solid.
[12:34] The other interesting milestone for you
[12:37] was when you got to build a lot of the
[12:40] engineering around the training for GBT.
[12:44] Yeah. For GP3
[12:45] for and how how what was that? Because
[12:48] you got from GPT2 was in TPUs, right?
[12:50] Yep.
[12:51] And the big breakthrough in GPT3 was
[12:53] like use more compute and using GPUs.
[12:55] Yep. So I ended up working at OpenAI for
[12:58] a year, left, went to Google Brain for a
[13:00] year, came back, and then GPT3 was 2018
[13:04] through 2019 was like building up to
[13:06] GP3, which exactly as you said was like
[13:09] scaling things up. I think that like
[13:10] Daario had seen the big trend of scaling
[13:12] laws basically. You published a paper
[13:14] for that.
[13:15] Yeah. Yeah.
[13:15] And that's like a pretty important paper
[13:18] that now has withtood the test of time
[13:20] and we're living now the dream of it.
[13:23] Definitely like seeing that line of
[13:24] reliably you get more intelligence if
[13:26] you spend more compute with the right
[13:28] recipe was the main thing that was at
[13:29] least for me was like this is a thing
[13:31] that's like happening happening now cuz
[13:33] you could look even at the time we
[13:34] weren't spending very much money on the
[13:37] on the training jobs at the time and you
[13:40] could see that there was scaling there
[13:42] and then also Danny Hernandez did a
[13:44] paper at the time that showed uh how
[13:46] much cheaper algorithmic efficiency was
[13:48] making stuff over time too and like
[13:50] those two things stack together that was
[13:52] like, oh wow, we're going to get a lot
[13:53] more intelligence over the next few
[13:56] years.
[13:56] So, it was noteworthy and surprising
[13:59] when you saw it.
[14:01] Yeah. And I I think the thing that
[14:02] seemed the weirdest to me is like I'm
[14:03] not a physicist, but like all these
[14:05] physicists were were doing this stuff.
[14:06] The like original scaling laws paper
[14:08] just the like very straight line over
[14:10] like 12 orders of magnitude. I'm just
[14:12] like 12 orders of magnitude is like just
[14:15] like a stupidly large amount of I've
[14:17] like never seen anything go over 12
[14:18] orders of magnitude. that convinced me
[14:20] to definitely pivot all of my work into
[14:22] scaling which I I hadn't been doing
[14:24] before.
[14:25] Can I ask a like kind of lay person
[14:27] question? I mean
[14:28] is it fair to say that the scaling law
[14:31] might show up in all of these other
[14:33] domains then they're like are there like
[14:36] two five 100 10,000 domains where the
[14:39] scaling law could hold that we're just
[14:40] not investing into?
[14:42] Yeah. So I think in physics scaling laws
[14:45] hold all over the place which I didn't
[14:46] know at the time but um within physics
[14:49] like there's a whole field called
[14:50] phenomenology that basically looks at
[14:52] various aspects of the world and then
[14:55] does those types of fits and they they
[14:57] find these like power law distributions
[14:59] all over the all over the place. This
[15:01] was like I think the first one that I
[15:04] had ever seen in a um like computer
[15:06] science adjacent thing which I I think
[15:09] was like interesting and surprising and
[15:12] and at the time it was people were mad
[15:14] about it. They actually were like you're
[15:15] throwing money at GPUs or just like
[15:18] wasting money. This is very wasteful.
[15:20] Yeah. That was sort of
[15:20] People are still mad about that.
[15:22] Yes. Different people now but still
[15:25] people mad about it.
[15:26] Yeah. Yeah. I guess. Yeah. The
[15:27] researchers were mad at that too where
[15:28] it's like it's it's not elegant. you're
[15:30] just like brute forcing it. The like
[15:32] jester cap like stack more layers like
[15:35] which I think I think like anthropics
[15:37] slogan I think is like do the stupid
[15:39] thing that works. That was a thing where
[15:40] like this was very clearly the very
[15:42] stupid thing that that works.
[15:44] Can you uh tell us then how you ended up
[15:46] collecting the last infinity stone
[15:49] with? Yeah, with Enthropic because
[15:51] there's very few people in the world
[15:52] that have basically worked at OpenAI,
[15:54] deep mind and anthropic and you were
[15:57] part of the team that spun off from
[15:59] GPD3.
[16:00] Yeah.
[16:00] And then started Anthropic. So how was
[16:03] how was that jump?
[16:04] There were two teams there. That was the
[16:06] safety or and the scaling or were the
[16:08] two orgs that reported into Daario and
[16:11] Daniela. I think we had just like worked
[16:14] together extremely well. One thing I
[16:16] think that was great both at OpenAI and
[16:18] and at Anthropic was just like we had a
[16:20] culture where like everything is on
[16:22] Slack 100% of things on Slack. And
[16:25] within that all public channels, great
[16:27] communication. I think that that group
[16:29] also was the group that took the scaling
[16:31] laws the most seriously where it was
[16:33] like okay like this actually is going to
[16:35] be transformative. there's going to be a
[16:37] handoff where like humanity will hand
[16:40] off control to transformative AI AI at
[16:43] some point and hopefully like they'll be
[16:44] aligned with us and like that'll be a
[16:46] good transition that goes well but it
[16:48] might not be the stakes are incredibly
[16:50] high and so I think that group was very
[16:52] focused on like how do we make sure that
[16:54] that's taken seriously enough and that
[16:57] like we've built an institution that can
[16:58] handle the weight of that that ended up
[17:00] being the core group that left to join
[17:02] Anthropic and I think I think it wasn't
[17:04] clear at all to me that like that was
[17:06] the right thing for the world at the
[17:08] time. In hindsight now, it seems like
[17:09] that was a good choice. I think what was
[17:11] kind of cool then too is when we started
[17:13] out, we didn't seem like we were going
[17:16] to be successful at all. OpenAI had a
[17:20] billion dollars and like all of these
[17:22] all of this star power and we had seven
[17:24] co-founders in COVID like trying to
[17:27] build something and we didn't know if we
[17:28] were necessarily going to make a product
[17:29] or what the products would look like.
[17:31] And so I think that what was interesting
[17:33] from that too is that all of the initial
[17:36] people who joined were there for the
[17:37] mission too. They all could have worked
[17:39] somewhere else for more prestige, more
[17:42] more more money. People would have known
[17:44] what they were doing etc.
[17:45] Well stayed at that opening eye
[17:47] basically.
[17:47] Exactly. Yeah. That that exactly that's
[17:49] been an interesting thing then that I
[17:51] think has been like the key to like
[17:52] letting our culture or like let our org
[17:54] scale. We're like 2,000 people now but
[17:56] we still have a thing where it doesn't
[17:58] seem like politics have creeped in. And
[18:00] I think a lot of that is like the first
[18:01] hundred people all were just there for
[18:03] the mission. So like if something starts
[18:04] to go wrong, they'll like raise their
[18:06] hand and be like, "It seems like this
[18:07] person might not be acting for the for
[18:09] the mission." YC's next batch is now
[18:12] taking applications. Got a startup in
[18:14] you? Apply at y combinator.com/apply.
[18:17] It's never too early and filling out the
[18:19] app will level up your idea. Okay, back
[18:22] to the video.
[18:23] Hey, tell us about the early days of
[18:25] anthropic. So the the seven you broke
[18:27] off from open AI, you had a general idea
[18:30] of the sort of like
[18:32] long-term mission that you wanted to do
[18:34] to you know not destroy humanity but
[18:36] like how did what did you actually work
[18:39] on for the first year? How did that
[18:40] converge on an actual product? So first
[18:43] year the main thing that I tried to do
[18:46] was just build the training
[18:47] infrastructure that we needed to train a
[18:49] model and then get the compute that we
[18:51] needed to train the model. Those were
[18:52] like my two main projects. all the other
[18:54] things that you need to do when you're
[18:56] like starting up a company too. So like
[18:58] set up a Brex account and like I don't
[19:00] know like all all of that all of that
[19:02] stuff. We started out with seven
[19:03] co-founders. Within like a few months I
[19:06] think like 25 folks from OpenAI um
[19:10] overall had joined. So we had like a
[19:12] pretty substantial team that like
[19:13] already knew how to work together too.
[19:14] And so that helped us get up and running
[19:17] faster.
[19:18] And at what point did you launch the
[19:19] first product and when did things begin
[19:21] to actually start working? So the first
[19:23] product that we launched was after
[19:25] chatgpt. We had like a maybe nine months
[19:28] before chat gpt. We had a slackbot
[19:31] version of like claude one.
[19:33] Oh yeah, we had that in the YC uh slack
[19:36] actually.
[19:36] Yeah. Yeah.
[19:37] Yeah. I remember like Tom Blfield adding
[19:39] all of you guys to it.
[19:42] It was really cool.
[19:43] And then I think that at the time though
[19:45] we didn't know whether or not we wanted
[19:46] to launch it as a product. We didn't
[19:49] know if doing so would be good for the
[19:51] world at the time. I think we hadn't
[19:53] really thought through our theory of
[19:54] impact that much for like how we
[19:56] actually will make stuff work well.
[19:57] Plus, I think actually in hindsight like
[19:59] if we had tried to launch it, we like
[20:01] wouldn't have had the serving
[20:02] infrastructure to have done it. And I
[20:04] think because we weren't sure whether or
[20:06] not we wanted to, we like hesitated for
[20:08] too long on building that
[20:09] infrastructure, which I think is
[20:10] learning for for me.
[20:13] I mean, at this time, ChatGpt had not
[20:15] launched yet. Chat GPD hadn't launched
[20:16] and so I guess we didn't know that it
[20:17] would be a big deal too.
[20:18] This is around the pandemic 2022.
[20:21] This is summer 2022. Yep. And then chat
[20:23] GPD launched fall 2022 and then we
[20:28] relaunched our API after that and then
[20:30] claude AI after that also. I think it
[20:34] didn't seem like it was working
[20:35] basically until Claude 35 and coding. I
[20:39] think like really really like through
[20:40] that whole time then until about a year
[20:43] ago it seemed like it wasn't clear that
[20:46] we were going to end up being like a
[20:47] successful company.
[20:48] We actually saw that in the startups
[20:50] because we kind of get a bit of a vibe
[20:53] check in terms of what is the preferred
[20:54] model for startups. So all of 2023 open
[20:57] AI was the response. Then things started
[21:00] to turn in 2024
[21:03] is when uh we saw claw 3.5 and
[21:06] especially sonnet was starting to get a
[21:08] market share per se in the YC batches
[21:10] going from single digit to at some point
[21:12] like 20 and to 30% and especially for
[21:15] coding
[21:16] y
[21:17] became the default choice which was very
[21:20] interesting. Can you tell us about how
[21:22] that emergent behavior and the spikiness
[21:23] on that particular skill
[21:25] must be 80% now or 90.
[21:27] Yeah. for coding even more especially
[21:28] now clock code. What was that? Was that
[21:31] on purpose or just kind of happened?
[21:33] I think that we invested more in trying
[21:36] to make the model really good at code
[21:38] because we wanted the model to be good
[21:39] at code was one thing
[21:42] and you did it.
[21:42] Yeah.
[21:43] And then I think seeing seeing the
[21:45] reaction of everyone to it was like okay
[21:47] yeah like let's go much harder on that
[21:49] also.
[21:50] And this is before 3.5 sonnet. you'd
[21:53] already invested enough in coding to
[21:54] realize that that was really promising
[21:56] and you decided to double down.
[21:57] I think this really was like individuals
[21:59] within the org being like we want to do
[22:01] coding uh before 35 sonnet and then when
[22:03] we saw 35 sonnet's really good product
[22:05] market fit that was good signal to like
[22:07] go go for that
[22:08] and do you guys know like the day that
[22:10] you guys launched 3.5 sonnet did you
[22:12] know that you had something really
[22:14] special and this was going to be the
[22:15] turning point for the company or were
[22:17] you as surprised as openi when they
[22:18] launched chat GBT and it just like
[22:20] unexpectedly took off? Yeah, I I wish
[22:21] that I wish that we had like more
[22:24] foresight on that, but no, I think I
[22:25] think it was surprising for us too like
[22:27] how how big of a deal it was. And then I
[22:29] think 37 sonnet also like surprised us
[22:31] by how much it unlocked like agentic
[22:33] coding. I think for for each of these
[22:35] things, yeah, we move quite fast in
[22:37] rolling them out and so we really um
[22:39] often don't know what the results are
[22:42] going to be there.
[22:43] I think it's what made a lot of these
[22:45] coding agent startups work. I mean
[22:47] there's a crazy story of Replet winning
[22:50] going to 100 million in uh just 10
[22:52] months right there's cursor of course a
[22:55] story and all built on all these with
[22:58] with sonnet
[22:59] I think that all all of those things
[23:00] have been surprising to me and then also
[23:02] just like in my working with claude too
[23:04] like I think I continue to be surprised
[23:06] by like the type of stuff that it can do
[23:08] and I I do think with each one there's
[23:10] like more stuff that kind of unlocks but
[23:11] one of my friends was telling me that
[23:12] she had some code that she uh some code
[23:15] source tool that she wanted to modify,
[23:17] but she didn't have the source code for
[23:18] it. She had the compiled binary, and
[23:20] she's like, "Claude, can you can you
[23:21] decompile this?" Like, "Yeah, can can
[23:24] you disassemble the assembly?" And
[23:25] Claude Claude chewed on it for 10
[23:27] minutes and like made a C version of it.
[23:29] And so then she had the thing to which
[23:32] is insane. And she's like, "Yeah, like
[23:33] if I spent 3 days on it, I probably
[23:35] could have gotten the hex tables and
[23:37] like wrote a little code to do, but like
[23:39] it did the whole thing, made up variable
[23:40] names for them, etc." So I do think that
[23:42] like we keep getting surprised by stuff
[23:44] that model has memorized all the hex
[23:46] tables it can think through try to work
[23:47] through it. I think we're going to
[23:49] continue to be surprised by that sort of
[23:50] stuff too.
[23:51] If you pull like the YC founders they
[23:53] prefer using anthropic models for coding
[23:55] by like a huge margin that's much larger
[23:58] than what you would predict if you just
[24:00] looked at the benchmark results.
[24:01] Yeah.
[24:02] So there there seems to be some X factor
[24:05] that makes people really like these
[24:07] models for coding. Do you know what it
[24:09] is and is it intentional in some way or
[24:11] it just came out of the black box
[24:13] somehow?
[24:13] I think that the benchmarks benchmarks
[24:16] are like easy to game where I think that
[24:18] all the other big labs I think have
[24:20] teams where they like their whole job
[24:21] with the team is to like make the
[24:22] benchmarks scores good and we don't have
[24:25] such a team. And so I think that I think
[24:27] that that is probably the biggest
[24:29] factor.
[24:29] You don't teach to the test.
[24:31] We don't teach to the test cuz I I do
[24:33] feel like if you start doing that then
[24:34] like it has weird bad incentives. Maybe
[24:36] we could like put that team under
[24:37] marketing or something like that and
[24:39] then ignore all the benchmarks. But I
[24:40] think that that's one reasons why
[24:42] there's some train test mismatch there.
[24:45] So the evaluations are more qualitative
[24:47] but internally or you have your internal
[24:49] We have internal benchmarks. Yeah. But
[24:51] we don't we don't publish them.
[24:52] And is it the internal benchmarks that
[24:53] the teams are really focused on
[24:55] improving?
[24:56] That's right. Yeah. So we have internal
[24:57] benchmarks that the team focuses on and
[24:59] improving and then we also have a bunch
[25:00] of tasks like I think that accelerating
[25:03] our own engineers is like a top top
[25:06] priority for us too and so we we do a
[25:08] ton of like dog fooding there to make
[25:10] sure that it's helping with our folks
[25:11] too. Going back to go Golden Golden Gate
[25:13] Claude, there's a lot of sort of inter
[25:15] the interpretability seems like it's a
[25:17] big part of it. And then most people
[25:19] would say that, you know, Claude's
[25:21] personality just feels better. And then
[25:24] how do you sort of at once be very
[25:26] quantitative, but then also, you know,
[25:28] build evals around personality.
[25:30] The evals for personality are kind of
[25:33] complicated, too, for like how do you
[25:34] tell if like Claude has like a good
[25:36] heart or something like that? It's like
[25:38] hard to hard to know. Um, but I do think
[25:40] that that's like Amanda Ascll's team's
[25:42] mandate is I think she describes it as
[25:44] like being like a a good world traveler
[25:46] where like it can like Claude goes and
[25:48] talks with all sorts of people from
[25:49] different backgrounds and like each of
[25:50] the people should come from come to that
[25:52] being like I I like feel good about like
[25:54] this conversation that I've had interp
[25:56] really I think is like a long-term bet
[25:58] right where it's like right now the
[25:59] models aren't that scary but at some
[26:00] point they're going to be more scary and
[26:02] so I think the hope there is to have
[26:04] some ability to know what's actually
[26:06] going on under the hood when it becomes
[26:08] more intense. Then more recently, Claude
[26:10] Code's been a real success. Can you talk
[26:13] us through like how did that project get
[26:14] started internally? And again, was it
[26:16] like a uh did you like know this time it
[26:18] was going to work or was it a surprise?
[26:20] Claude Code was um an internal tool
[26:23] also. So like try to help out our our
[26:25] engineers within Anthropic that uh yeah,
[26:28] Boris um had like hacked together.
[26:31] There's an internal anthropic engineer
[26:32] wanting to build it for themselves
[26:33] for internal for other internal
[26:35] engineers. Yeah. For him and other
[26:36] internal engineers. And then um I think
[26:38] yeah I think we definitely didn't know
[26:40] that it would be successful out there.
[26:42] And I I think I think to to some degree
[26:43] like we really had fully just bet on the
[26:46] API before that with the intention being
[26:49] like there's like so many so many
[26:52] startups out there with so many good
[26:54] ideas. Who are we to like figure out
[26:56] what the right product is to build on
[26:58] top of this stuff? Everyone out there is
[27:00] going to build better stuff than us. And
[27:01] so put all of our effort into just
[27:03] making the best possible API. And I
[27:05] think that this surprised me as like
[27:07] okay like we actually were able to make
[27:08] something that like as a product was
[27:11] like better than the other products out
[27:12] on the market for this agentic use. I
[27:15] have like some theory that like part of
[27:17] that came from like a mind shift of
[27:19] seeing Claude as like the user uh for
[27:21] this thing too. For like link that we
[27:23] were like trying to build things for
[27:25] teachers were like our users for for
[27:27] grouper it was like single people in New
[27:29] York mostly I guess. Um, for this I
[27:32] think really the the like users are the
[27:34] developers but also I think the users is
[27:36] Claude. It's like give Claude the right
[27:38] tools that Claude can actually do that
[27:40] effectively help Claude get the right
[27:42] context to work effectively. This team
[27:45] was like the most focused on Claude as
[27:48] like a user which I think makes sense
[27:50] that you guys would understand Claude
[27:51] the best. Yeah, I I do think that that's
[27:54] a place where like startup founders
[27:56] though like can can do that too. And I
[27:57] think that that's that's probably a rich
[27:59] vein for people to like make tools that
[28:01] are better for models as users.
[28:04] That's the perfect anthropomorphization
[28:06] of like the LLM itself. Like the agent
[28:09] is one of the stakeholders is one of the
[28:10] users that you would go after and try to
[28:12] like empower.
[28:13] Yeah. Yeah. Totally. which actually
[28:15] makes a lot of sense why you guys
[28:17] actually got MCP to work to do tool
[28:21] calling because a bunch of other labs
[28:23] had tried to do something and the
[28:25] standard that stuck that really took off
[28:28] was yours.
[28:29] Yeah, I think that that seems like a
[28:30] similar one too where it's like
[28:32] model model focused
[28:33] going back to claw code. So like success
[28:35] is really exciting. It's also scary for
[28:37] like cursor and other companies that
[28:39] have built on top of the API like what's
[28:42] your advice to founders building
[28:44] products like how should they think
[28:45] about building on the API but also
[28:47] worrying about like anthropic or one of
[28:49] the labs building something better than
[28:50] they can build.
[28:51] I think I was kind of surprised that
[28:53] claude code like we we did build a thing
[28:55] that was like uh like the best in the
[28:57] market there too. It's not super clear
[28:59] to me what the big advantage was for us
[29:01] for Claude code besides more empathy for
[29:03] Claude or something. That's actually I
[29:05] think that's actually really interesting
[29:06] insight. Like it seems like the thing
[29:07] that Yeah. you were building for a
[29:09] specific user that you knew really well
[29:11] that other people wouldn't have thought
[29:12] to build for versus like you had some
[29:14] like intrinsic technology advantage.
[29:17] Yeah. Like I think a startup could could
[29:18] have done that same thing too, right?
[29:20] Yeah.
[29:20] I think we're the most like developer
[29:22] focused lab. I think we're the most like
[29:24] API focused lab too. So I think we want
[29:26] to make sure that we have the best
[29:28] platform for people to build stuff on
[29:30] cuz this thing is growing so incredibly
[29:32] quickly. like we're not going to be the
[29:34] fastest at figuring out all the ways
[29:36] that we need to empower Claude to do the
[29:39] work that connects Claude to the entire
[29:41] human business that's like human human
[29:43] world is all designed for humans but
[29:45] like we need to get the models to be
[29:47] able to be productive members of uh the
[29:49] economy.
[29:50] Are there like ideas or areas you would
[29:52] love to see developers building in or
[29:54] like areas you don't you you think are
[29:56] like underappreciated right now? Yeah,
[29:59] Claude code is like how do you get
[30:01] Claude to be a useful pair programmer
[30:04] kind of um or like junior engineer.
[30:06] You've got like a level
[30:10] two or three or something like that that
[30:11] you can work with or like very spiky
[30:13] because also it can do the like weird
[30:14] disassembly stuff that like a super high
[30:16] level suite would struggle with. Less
[30:18] good at knowing what type of work to do.
[30:21] Needs kind of a lot of handholding.
[30:22] Needs a lot of context from it. That's
[30:24] like one very particular subset of work
[30:27] that can be done. Uh if you look at like
[30:29] all the stuff that happens in businesses
[30:34] besides that, it's like a very tiny
[30:36] fraction of like all the work that's
[30:38] done in businesses that like a smart
[30:40] person who knows how to code and like
[30:43] use lots of tools but doesn't have that
[30:45] much context yet uh would want to do. So
[30:48] I think I think finding ways to coach
[30:51] Claude or uh co coach whatever model to
[30:54] like do useful tasks for businesses
[30:58] seems like there's just like a huge huge
[31:00] space there.
[31:01] So Tom, a big part of your job is like
[31:04] owning all the compute infrastructure
[31:05] that makes anthropic work. Can you talk
[31:07] about like what what is the compute
[31:09] infrastructure behind this giant thing?
[31:10] Now, one thing that's interesting to
[31:12] look at is just that humanity is on
[31:15] track for like the largest
[31:16] infrastructure buildout of all time.
[31:18] Now,
[31:18] this is going to be larger than the
[31:19] Apollo project, larger than the
[31:21] Manhattan project.
[31:22] It'll be bigger than both of them next
[31:23] year if it keeps on the current
[31:25] trajectory, which is like roughly 3x per
[31:28] year increase in spending on AGI
[31:32] compute, which is just bonkers. Yeah.
[31:34] Like 3x per year is wild. I think it's
[31:36] going to keep up on the 3x per year
[31:38] trajectory. It's already locked in for
[31:40] that for for next year and then it's a
[31:44] little bit open for for 2027.
[31:46] I mean anecdotally internal to YC uh we
[31:49] can't get enough you know credits across
[31:52] all of the top frontier models including
[31:54] Claude. So you got to help us out a
[31:55] little bit.
[31:57] Yeah.
[31:58] We're just I mean everyone's
[31:59] bottlenecked literally every you know
[32:01] it's like give me more intelligence. I
[32:02] can't have enough.
[32:03] Yeah. And I know you guys have been
[32:04] looking at more hardware startups also
[32:06] for like more accelerators. I think that
[32:08] we will see more accelerators coming
[32:09] online to 2027. That's a good a good
[32:12] space. Also like data center tech I
[32:14] think is a big one.
[32:15] Where are the bottlenecks for you guys
[32:16] now? Is it like getting enough
[32:19] electricity, getting enough GPUs,
[32:21] getting construction permits,
[32:23] power, people are using jet engines to
[32:25] get power. That's nuts.
[32:27] Overall for the buildout, I think power
[32:30] is going to be the biggest bottleneck,
[32:32] especially power in the US. Like we want
[32:33] to build in the US. That's one of our
[32:35] biggest policy goals is to like get the
[32:38] US to like build more data centers,
[32:40] permit more data centers, make it easier
[32:42] to build.
[32:42] Is the answer renewables or is it uh
[32:45] nuclear?
[32:46] I I definitely I feel like yes, yes, all
[32:48] all of those things. I wish I wish that
[32:49] nuclear was easier to build.
[32:52] Anthropic is the only major lab that
[32:54] uses not just one kind of GPU, but the
[32:57] GPUs from three different manufacturers.
[33:00] Can you talk about that and how how how
[33:01] that strategy has played out?
[33:03] Yeah. Yeah. So we use um GPUs, TPUs and
[33:06] tranium. Downside of doing that is that
[33:08] we split our performance engineering
[33:10] teams across all of those platforms
[33:12] which is a ton of extra work. The
[33:13] positive thing is it gives us the
[33:15] flexibility to both one like soak up
[33:18] that extra capacity because there there
[33:20] just is more of those altogether than
[33:22] just one and then two is we can use the
[33:24] like right chips for the right jobs
[33:26] where some chips will be better for
[33:28] inference, some chips will be better for
[33:30] training and we can match the the right
[33:32] chips to the right jobs. So yeah, I
[33:34] think that that's kind of the the
[33:36] trade-off there. I guess one cool thing
[33:37] is just connecting the dots through your
[33:39] career and how all of this compounded
[33:42] because you you were the one engineer
[33:45] building that change of the architecture
[33:46] from TPUs to GPUs back at OpenAI that
[33:49] got GPD3 to actually scale and now
[33:52] you're in charge of that at a much much
[33:54] bigger scale year years later. I don't
[33:57] know if that kind of connected dots for
[33:59] you. The big move from TPUs to GPUs at
[34:02] OpenAI I think was partly driven just
[34:04] that PyTorch was a better software stack
[34:06] on top of them than TensorFlow on top of
[34:09] TPUs. And I think that that then
[34:11] unlocked fast iteration where like if
[34:14] you have like a good reliable software
[34:16] stack then you can experiment quickly
[34:18] just like build a whole system that
[34:20] works. I think that that's the thing
[34:21] that we really strive for now at
[34:23] Anthropic too is a challenge of having
[34:25] many more platforms is that it's harder
[34:27] to write all the good software. I think
[34:29] building the muscle of knowing how to
[34:31] build that software well so that all of
[34:33] the people who build on top of that low
[34:35] level can have a great experience with
[34:37] it is the most important thing there.
[34:38] Do you have advice for um kind of like a
[34:40] younger Tom version of yourself who now
[34:44] you've seen and went through this crazy
[34:46] journey? If someone was you back in the
[34:48] 20s living today and they wanted to ride
[34:51] and join the AI revolution, what would
[34:53] you say to them?
[34:54] And very specifically something we see
[34:56] from a lot of hear from a lot of college
[34:57] students at the moment is they uh they
[34:59] don't know what like if they should stay
[35:01] in college like are there going to be
[35:02] jobs for them what like how is the world
[35:05] going to change and what should they do?
[35:07] taking more risks I think is is wise and
[35:10] then also trying to work on stuff where
[35:13] your friends would be really excited and
[35:16] impressed if you did it or a more
[35:18] idealized version of yourself would be
[35:20] really like proud of yourself if you
[35:22] succeeded at it I think is like probably
[35:23] the thing that I would I would try to
[35:25] tell a younger version of myself
[35:27] more intrinsic less exttrinsic like
[35:29] don't chase these other credentials and
[35:31] getting the degree or whatever you know
[35:33] working at Fang like those are just
[35:35] irrelevant
[35:36] as of today.
[35:37] Yeah, exactly.
[35:38] That's all we have time for today. We'll
[35:42] see you guys next time.
[35:45] [Music]