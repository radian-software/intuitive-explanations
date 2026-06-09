---
title: |
  How Replit used legal threats to kill my open-source project
date: 2021-07-13
---

<link href="/css/replit.css" rel="stylesheet">

<blockquote class="replit" cite="CEO of Replit, in an email to me"> I
think you should take it down and stop working on it. I'll be engaging
our lawyers on Monday if it's still up by then. <span
class="ellipsis">[...]</span> We were a tiny company when you interned
with us <span class="ellipsis">[...]</span> Luckily we're bigger now,
and crucially have a lot of money to pay for top lawyers now if we're
forced to go that route.</blockquote>

**I received an official response from Replit and my open-source
project will be back up soon; please see [the bottom of the blog
post](#how-did-replit-respond-to-this-blog-post) for an update. The
rest of the content here will remain as a historical artifact.**

Hi, my name is Radon. I graduated college last year and now work as a
software engineer in DevOps/Infrastructure. In my free time, I also
maintain [a number of open-source
projects](https://github.com/raxod502).

While I was in college, I interned at the startup Replit. This blog
post is the story of how Replit is using legal threats and their
venture-capital funding to bully me into shutting down an open-source
project they don't like.

**Table of contents**

<!-- toc -->

- [What's Replit?](#whats-replit)
- [What was my open-source project?](#what-was-my-open-source-project)
- [What happened when I shared my open-source project with Replit?](#what-happened-when-i-shared-my-open-source-project-with-replit)
- [What happened after Replit threatened to sue me?](#what-happened-after-replit-threatened-to-sue-me)
- [Is Replit right?](#is-replit-right)
- [Why would Replit do this?](#why-would-replit-do-this)
- [How did Replit respond to this blog post?](#how-did-replit-respond-to-this-blog-post)
- [So is Riju back up now?](#so-is-riju-back-up-now)

<!-- tocstop -->

## What's Replit?

Replit makes a webapp you can use to run code online in different
programming languages. This is nothing new ([just Google "run python
online"](https://www.google.com/search?q=run+python+online) for
proof), so Replit's value proposition is extra features like sharing
your work, installing third-party packages, and hosting webapps.

I worked for Replit in Summer 2019, where I was asked to rebuild
Replit's package management stack and make it open-source. If you like
reading about tech stuff, [here's the post I wrote for Replit's
blog](https://web.archive.org/web/20210504051428/https://blog.replit.com/upm),
and [here's the code on GitHub](https://web.archive.org/web/20211221134407/https://github.com/replit/upm).

I took a job elsewhere in Summer 2020, but still chatted with them
occasionally by email when they reached out to tell me about something
cool Replit had developed.

## What was my open-source project?

<center><img src="/assets/riju-languages.png" alt="Screenshot of
language select page in Riju" width="100%" /></center>

The aspect of Replit that I really enjoyed was how it supported lots
of different programming languages. (I wrote [another blog post for
Replit](https://web.archive.org/web/20210504023410/https://blog.replit.com/elisp)
about how they do that.) That got me thinking: how many programming
languages could you possibly cram into a single website?

To explore that question, I put together my own little webapp that
could run code online. After about a day, I had something that worked.
(If you're wondering why it was so fast---it turns out you only need
[30 lines of code](https://github.com/raxod502/python-in-a-box) to let
people run Python code in a webapp! This may be why there are so many
websites for running Python online...)

After it was working, I started adding as many different programming
languages as I could. As you can see from this excerpt of my project's
version history, I got a little overexcited:

```
                                                                   languages
                                                                   ---------
2020-06-05 df9ba38 Initial commit                                          0
2020-06-05 5e3a4a4 Install some packages into a Docker image               0
2020-06-05 e937c8f Simple Express server with "Hello world"                0
2020-06-06 0961498 Embed terminal on frontend app                          0
2020-06-06 c66cf63 Embed Monaco editor on frontend                         0
2020-06-06 27ab1f7 Add "run" button                                        0
2020-06-06 f417858 You can run Python code now                             1
2020-06-07 d543081 You can run many languages now                          8
2020-06-07 e2a3e71 All languages 17 working now                           17
2020-06-07 473c50c ALL THE LANGUAGES                                      25
2020-06-08 3718315 even more languages                                    33
2020-06-08 548c1c1 repl.it superiority!!                                  38
2020-06-08 1ae424f More languages, we need all the languages              48
2020-06-09 c34ccf2 A lot more languages                                   77
2020-06-09 846caf2 At this point the number of languages is absurd        79
```

I eventually ended up with 216 languages, including [all 38 languages
from
Replit](https://web.archive.org/web/20210512193221/https://replit.com/languages),
[all 100 languages from Yusuke Endoh's "Quine
Relay"](https://github.com/mame/quine-relay), and a good deal more
besides. You might ask: Why did I spend so much time adding obscure
programming languages to a webapp nobody was going to use? Well, let
me put it this way: Is it the weirdest 2020 hobby you've seen?

## What happened when I shared my open-source project with Replit?

One day, I got an email from Replit letting me know about a new
feature they released. I figured this was a good time to share my
open-source project with them, in case they wanted to take inspiration
from any of my work:

<p><center><img src="/assets/replit-email-1.png" alt="Screenshot of an
email from Replit sharing a post from their blog, and my response
sharing my open-source project with them" width="100%" /></center></p>

At first, I got a positive response. But then, 30 minutes later, out
of nowhere, Replit accused me of unethical behavior and stealing their
design:

<a id="replit-email-2"></a>
<p><center><img src="/assets/replit-email-2.png" alt="Screenshot of
one email from Replit praising my open-source project, and an
immediately subsequent one accusing me of unethical behavior and
stealing 'internal design decisions'" width="100%" /></center></p>

Now, none of the ideas I used in my open-source project were "internal
design decisions": they've all been published publicly on Replit's
blog (I knew this because I'd been asked to *write* some of those blog
posts during my internship). And my project also wasn't any more of a
Replit clone than any of the other websites on the first few pages of
Google results for "run python online", most of which look exactly the
same:

<p><center><img src="/assets/replit-ui-montage.png" alt="Screenshot of
nine different webapps that let you run Python online, all of which
look more or less identical" width="100%" /></center></p>

But I figured I might have missed something, so I asked for details:

<p><center><img src="/assets/replit-email-3.png" alt="Screenshot
excerpt of my email asking Replit for details about what ideas they
were claiming I stole" width="100%" /></center></p>

(The rest of this email is basically me repeating the previous
paragraph of this article, but with a lot more technical details. You
can read the whole email [on Imgur](https://imgur.com/a/OaEOwu2),
mirrored [on the Internet
Archive](https://web.archive.org/web/20210530184721/https://imgur.com/a/OaEOwu2).)

Unfortunately, Replit refused to provide any specifics on what they
were saying I had done wrong, reiterated their previous statements,
and threatened me with a lawsuit:

<p><center><img src="/assets/replit-email-4.png" alt="Screenshot of an
email from Replit threatening me with a lawsuit" width="100%"
/></center></p>

And then just to put a cherry on top, Replit sent me another email
reminding me that they [just raised $20 million from their investors
last
month](https://web.archive.org/web/20250417011844/https://venturebeat.com/business/replit-raises-20-million-for-collaborative-browser-based-coding/),
and they weren't afraid to use it against me. The "me" in question
being one of their previous interns who just graduated from college a
year ago, and who isn't running any kind of commercial operation
whatsoever.

<a id="replit-email-5"></a>
<p><center><img src="/assets/replit-email-5.png" alt="Screenshot of an
email from Replit threatening me with their money" width="100%"
/></center></p>

I'd like to point out two things about this email:

* The remark about "commits like this"---this is actually misleading.
  There's only one commit in my project that mentions Replit, and it's
  the one I already showed you earlier, from my third day of coding,
  when I'd just added all 38 languages that Replit supported, before
  moving onto the 178 other languages I wanted to add.
* The remark about me being a "demanding" intern---I'm not actually
  sure what this is meant to imply, especially since Replit had just
  tried to recruit me earlier that day (see the screenshot of their
  first email). But I'll leave it alone because it's not really
  relevant to the issue at hand.

## What happened after Replit threatened to sue me?

Naturally, I took down my project right away, gave it some time for
feelings to cool, and sent Replit an apology. I figured something
might have been lost over email, so I asked to get on a call:

<p><center><img src="/assets/replit-email-6.png" alt="Screenshot of an
email in which I apologize to Replit and ask to have a call"
width="100%" /></center></p>

Unfortunately, Replit ignored this email, so I sent them another one
following up. This one got a response, but not the one I was hoping
for:

<p><center><img src="/assets/replit-email-7.png" alt="Screenshot of an
email from Replit making it clear that they have no intention of
talking to me further" width="100%" /></center></p>

Just in case Replit didn't understand that I wasn't OK with this
situation, I sent three follow-up emails explaining as such over the
next few weeks, all of which were ignored.

In other words, Replit stands by its threat: if I re-publish my
open-source project, then they will sue me with "top lawyers".

## Is Replit right?

Replit claimed that my open-source project was:

1. a clone of Replit
2. based on their trade secrets ("internal design decisions")
3. unethical to build

Let's examine this claim, part by part:

1. In developing my project, was I making a clone of Replit?
2. In developing my project, did I make use of any trade secrets of
   Replit?
3. Was it unethical for me to develop an open-source project that's
   similar to Replit, after working for them?

Questions 1 and 2 have a fair number of technical details, so I've put
them [in a separate post](evidence). The TL;DR is:

1. My project isn't any more similar to Replit than the 15 other
   (commercial!) ones you can find on Google by searching "run python
   online" or "online programming environment".
2. Every similarity between my project and Replit can be explained by
   looking only at GitHub repositories and blog posts that were
   *published online by Replit itself*, making them obviously not any
   kind of secret.

Let's address question 3 here:

> Q: Was it unethical for me to develop an open-source project that's
> similar to Replit, after working for them?

In my opinion, the answer to this question is no, for a number of
reasons:

* Riju is entirely non-commercial. Unlike Replit, I didn't seek
  funding from any source---advertising, donations, fundraising,
  subscriptions, whatever. I have no interest in running a business,
  and never really *wanted* Riju to become too popular, since I was
  the one paying the server bill.
* Riju wasn't stealing customers from Replit. Based on my analytics
  data, there were 38 visits to Riju during the month of February.
  (Half of those were probably me.) Meanwhile, Replit had [over 7
  million
  users](https://web.archive.org/web/20210505162911/https://twitter.com/Replit/status/1389976994423525378).
  There's obviously no sense in which Riju was competing with Replit.
* Riju wasn't *built* as a competitor to Replit, either. Since the
  architecture was limited to running on a single server, anyone could
  bring the entire system down just by typing in a [fork
  bomb](https://en.wikipedia.org/wiki/Fork_bomb)---and one of my
  friends did, just to see what would happen. (The system crashed.) If
  I were designing a product to compete with Replit, I certainly
  wouldn't have picked an architecture that could only scale to
  toy-project size.
* Replit's core value proposition isn't letting you run code online
  (you can do this in dozens of places for free), it's the features
  they offer on top of running code. Riju categorically lacked all of
  these features, including: having a user account, saving your work,
  sharing your work, publishing webapps, persistent workspaces,
  discussion forums, integration with GitHub, etc. etc.
* I had no bad intentions towards Replit when developing Riju, and
  wasn't trying to hide anything. As proof of these claims, I offer
  the fact that I had the project public on my GitHub from the
  beginning, and the fact that Replit found out about the project
  because I openly shared it with them of my own volition, extending
  an offer for them to take inspiration from my work.
* Riju was never intended to be a product, it was intended to be a
  personal playground / art piece. As proof of this claim, I offer the
  fact that I spent dozens of hours adding languages like
  [Hexagony](https://esolangs.org/wiki/Hexagony) and
  [SNOBOL](https://www.regressive.org/snobol4/) rather making it so
  you could save your work(!).

I'm not a business person. I'm just an open-source dev who likes to
build weird things for fun. (If you doubt my track record of building
things that don't make money, just check out [the list on my
website](/about/projects), and note the conspicuous absence of
anything that's ever made a cent of revenue.)

I would never try to steal someone's business after I worked with
them. Hurting Replit was not my intent in working on Riju, and to
accuse me otherwise---especially without asking a single clarifying
question, and refusing all offers to have a discussion---shows a great
deal of bad faith on the part of Replit, in my opinion.

If you'd like to decide for yourself who is in the right, I'm happy to
put all of the evidence out in the open (except the code, because
Replit's standing by its promise to sue me if I do). Again, I have [a
separate post](evidence) with all the technical details. And you can
also read all communications between me and Replit, in full and
unabridged form, [on Imgur](https://imgur.com/a/OaEOwu2), mirrored [on
the Internet
Archive](https://web.archive.org/web/20210530184721/https://imgur.com/a/OaEOwu2)).
(Technical details about Replit internals redacted, as well as any
statement that could reveal such details indirectly.)

## Why would Replit do this?

Replit's stated ideals include:

* encouraging open-source development (e.g. [open-sourcing parts of
  their technology](https://github.com/replit), [adding GitHub support
  to
  Replit](https://web.archive.org/web/20210522215545/https://blog.replit.com/github);
  Replit's CEO: ["I owe my entire career to
  open-source"](https://web.archive.org/web/20210108083314/https://amasad.me/github))
* giving back to the community (from [the blog post Replit asked me to
  write](https://web.archive.org/web/20210504051428/https://blog.replit.com/upm):
  "we are migrating [...] to do our part in improving the ecosystem
  for developers everywhere"; "Giving back to the community. The core
  of our language-agnostic package management is now open-source on
  GitHub")
* making it easy to share and remix your creations (e.g. Replit's CEO
  on learning to program: ["I'd download projects related to what I
  wanted to build \[...\] change & tinker with them, and get
  inspired"](https://web.archive.org/web/20210522215545/https://blog.replit.com/github);
  he advises others to
  [fork](https://web.archive.org/web/20210522212135/https://twitter.com/amasad/status/1395074521804148738)
  and
  [remix](https://web.archive.org/web/20210211025614/https://twitter.com/amasad/status/1359697571011125253)
  too, and sells this philosophy as [a differentiating feature of
  Replit](https://web.archive.org/web/20210522212034/https://twitter.com/amasad/status/1392517080017108992))

However, Replit's actions in this case reveal hypocrisy:

* they say they encourage open-source development, but when my
  open-source project offended them, they shut it down with extreme
  prejudice
* they claim to be giving back to the community through their
  open-source and blog posts, but when I tried to use those ideas in a
  community project, they threatened to sue me
* they say they make it easy to share and remix your creations---but
  when I tried to remix Replit itself, I became a *persona non grata*

In Replit's emails to me, their threats were based on the fact that I
had worked for them in the past. However, I believe this reasoning is
a smokescreen. To see why, let's take a look at some tweets that
Replit's CEO, Amjad, posted just after threatening me by email:

<p><center><img src="/assets/replit-tweet-1.png" alt="Screenshot of
Amjad's deleted tweet calling for 'copycats' to be banned from venture
capital" width="75%" /></center></p>

<p><center><img src="/assets/replit-tweet-2.png" alt="Screenshot of
Amjad's deleted tweet denigrating 'copycats'" width="60%"
/></center></p>

Amjad later deleted these tweets because [they proved
controversial](https://web.archive.org/web/20210505050939/https://twitter.com/amasad/status/1377604981549752320):

<p><center><img src="/assets/replit-tweet-3.png" alt="Screenshot of
Amjad's tweet explaining that they deleted their previous,
controversial tweets" width="60%" /></center></p>

In these tweets, Amjad points out that Athens Research was clearly
inspired by another company, and argues that they should therefore be
"ridiculed" and banned from receiving funding. Furthermore, he says:
"I stand by what I said about copycats in general", i.e. he disdains
all people that he thinks are "copying" existing ones, not just the
specific company in his tweet.

There is a clear resemblance between Amjad's comments on Athens
Research and his legal threats towards my own project. He even used
exactly the same word, "copycat", in both. In the case of Athens
Research, there was nothing Amjad could do to express his disdain
besides denigrate them on Twitter. But in my case, since I had worked
for Replit before, Amjad had an excuse to throw accusations my
way---accusations that, if you aren't familiar with the facts, sound
like they could be legitimate.

I'd also like to reiterate that the person Replit is threatening with
"top lawyers" and "a lot of money" is a *new grad* with *no company*,
*no funding*, and *no commercial ambitions*. If someone with an actual
commercial enterprise were to offend Replit, I shudder to think what
treatment *they* might receive.

<p align="right">
  Radon Rosborough, June 2021
</p>

## How did Replit respond to this blog post?

After I posted the article in the morning, it was [discussed
extensively on Hacker
News](https://web.archive.org/web/20260520003438/https://news.ycombinator.com/item?id=27424195).
Around 5pm, Amjad posted an apology on Hacker News, [which has also
been
discussed](https://web.archive.org/web/20241015072304/https://news.ycombinator.com/item?id=27429234).

<p><center><img src="/assets/amjad-hn-1.png" alt="Screenshot of an
email from Amjad apologizing for making legal threats, and my reply
indicating I would like to have a call" width="70%" /></center></p>

He also reached out to schedule a call, which I naturally agreed to:

<p><center><img src="/assets/replit-email-8.png" alt="Screenshot of an
email from Amjad promising that he will not sue me, and my response
thanking him and clarifying a point about how he quoted me"
width="100%" /></center></p>

During the call, Amjad apologized for making legal threats, but
reiterated that he felt I had made a clone of Replit and that I had
acted unethically. Eventually we agreed to disagree, and he promised
in writing that he was fine with my putting my project back up:

<p><center><img src="/assets/replit-email-9.png" alt="Screenshot of
Amjad's comment on HackerNews saying that he apologizes for making
legal threats, but still feels I acted unethically" width="100%"
/></center></p>

In retrospect, I'm a little disappointed that Amjad:

* didn't apologize for (or mention) [publicly doubling
  down](https://web.archive.org/web/20210608153700/https://twitter.com/amasad/status/1401957368510906369)
  on his decision to threaten me, and didn't post an update to that
  thread after the phone call
* didn't apologize for (or mention) [publicly
  retweeting](https://web.archive.org/web/20210607231029/https://twitter.com/amasad)
  an accusation that I "literally stole and published IP", although he
  did at least delete the retweet
* didn't apologize for (or mention) making a [nebulous personal
  attack](#replit-email-5) in writing that I was a "demanding intern"
  right after [trying to hire me](#replit-email-2)
* said in the phone call, right after "apologizing", that he felt as
  if he had invited me into his house and I had betrayed his trust
* still refused to list any specific part of Replit he thought I had
  copied, even when I asked him for such details multiple times during
  the phone call, despite his continuing to claim both privately and
  publicly that I copied Replit unethically
* misquoted me in writing to make me look like I agreed with his
  accusations, right after reaching out to apologize for his behavior

All in all, I think this could have gone better.

Nonetheless, I'm happy that we were able to get the situation worked
out amicably, and I look forward to moving on with my life---including
putting Riju back up, after I can get things compiling again :)

Peace.

## So is Riju back up now?

Yes! Check it out at <https://riju.codes/>, and join the community on
GitHub at <https://github.com/raxod502/riju>. I'd love to work on the
project with you <3

(Please note that Riju is only available on IPv6-enabled networks due
to the higher financial cost of supporting legacy protocols. If your
network [does not support IPv6](https://test-ipv6.com/) then please
consider asking your network administrator or service provider to do
their part in supporting modern internet standards. You can consider
accessing Riju through a VPN as a workaround.)
