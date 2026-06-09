---
title: Appendix A
---

**This page has supplementary material for another post, [How Replit
used legal threats to kill my open-source project](./). Go read it
first, if you haven't already.**

---
<p></p>

In this appendix we examine the following two questions about my
open-source project, called Riju:

1. In developing Riju, was I making a clone of Replit?
2. In developing Riju, did I make use of any trade secrets of Replit?

## 1. Is Riju a clone of Replit?

> Q: In developing Riju, was I making a clone of Replit?

Here's a screenshot of Riju's user interface:

<center><img src="/assets/riju-python.png" alt="Screenshot of running
Python in Riju" width="100%" /></center>

And for comparison, here's what Replit looks like:

<p><center><img src="/assets/replit-ui.png" alt="Screenshot of
Replit's user interface" width="100%" /></center></p>

As you can see, there are exactly two similarities:

* There's a text pane on the left and a terminal on the right.
* There's a button that says Run, and it's colored green.

Personally, I think it's a bit of a stretch to say that Replit has a
monopoly on putting a text pane next to a terminal and a Run button,
but if that's the case, they should also consider suing the following
six companies from the first page of Google results for "run python
online", all of whom do basically the same thing:

* <https://www.programiz.com/python-programming/online-compiler/>
* <https://www.tutorialspoint.com/execute_python_online.php>
* <https://www.onlinegdb.com/online_python_compiler>
* <https://pynative.com/online-python-code-editor-to-execute-python-code/>
* <https://www.w3schools.com/python/python_compiler.asp>
* <https://www.online-python.com/>

Here's a collection of a few screenshots showing the similarity
between all these webapps:

<p><center><img src="/assets/replit-ui-montage.png" alt="Screenshot of
nine different webapps that let you run Python online, all of which
look more or less identical" width="100%" /></center></p>

Replit might also say I was copying the fact that you can run multiple
programming languages online in a single place. If that's the case,
they should also consider suing the following six companies from the
first page of Google results for "run multiple programming languages
online", all of whom---again---do basically the same thing:

* <https://tio.run/>
* [https://code.labstack.com/](https://web.archive.org/web/20220427124816/https://code.labstack.com/)
* <https://onecompiler.com/>
* <https://ideone.com/>
* <https://www.tutorialspoint.com/codingground.htm>
* <https://www.codechef.com/ide>

There's no universe in which Riju is more a clone of Replit than any
of these other services. Enough said.

## 2. Does Riju use any of Replit's trade secrets?

> Q: In developing Riju, did I make use of any trade secrets of
> Replit?

Let's start with the obvious: I wrote all of Riju's code myself, and
this would be trivial to prove publicly if Replit hadn't forced me to
take down the code.

But Replit didn't say I stole the code, they said I was "copying
internal design decisions". In other words, they're referring to this
part of standard employment terms:

> I agree that during and after my employment with the Company, I will
> hold in the strictest confidence and take all reasonable precautions
> to prevent any unauthorized use or disclosure of Company
> Confidential Information.

Replit is claiming that my design decisions in Riju are "Confidential
Information", i.e., trade secrets. But we shouldn't forget another
part of employment law:

> Company Confidential Information shall not include any such
> information which I can establish (i) was publicly known or made
> generally available prior to the time of disclosure by the Company
> to me; (ii) becomes publicly known or made generally available after
> disclosure by the Company to me through no wrongful action or
> omission by me; or (iii) is in my rightful possession, without
> confidentiality obligations, at the time of disclosure by the
> Company as shown by my then-contemporaneous written records.

In other words, **if your trade secrets are public knowledge, or I
already knew about them before you told me, they aren't trade
secrets**. As such, it's easy to prove that Riju doesn't incorporate
any trade secrets of Replit. To do so, **I will explain every aspect
of Riju's design using only information from the public Internet and
my prior published work.**

(Of course, [I am not a lawyer](https://en.wikipedia.org/wiki/IANAL);
I'm an open-source developer who has other things they'd rather be
doing.)

### Riju's API design

In Riju, the frontend and backend communicate primarily using a
persistent websocket in JSON format. There are data events like
`terminalInput` and `terminalOutput` to control the tty, and control
events like `runCode` and `formatCode` that are sent when the user
clicks buttons on the frontend.

Is it a trade secret to use a websocket API with these kind of
messages for code evaluation? No, the fact that Replit uses websockets
is publicly documented [on their
blog](https://web.archive.org/web/20210504022213/https://blog.replit.com/api-docs),
and there is a complete public reference for the exact format of all
their code evaluation websocket messages [in their official
documentation](https://web.archive.org/web/20210502164337/https://protodoc.turbio.repl.co/services).
You might think this is supposed to be a secret internal page, but no,
it's linked [directly from Replit's public
GitHub](https://web.archive.org/web/20210828122650/https://github.com/replit/crosis/).

### Riju's use of per-language config

Riju supports multiple languages by having a JSON configuration per
language, which specifies information like

* how to run the language
* how to start a REPL for it
* how to run a code formatter / LSP server
* what the main file should be called

Is it a trade secret to support multiple languages by abstracting out
a common interface and writing per-language JSON files? Nope, you can
read [right on Replit's
blog](https://web.archive.org/web/20210504023410/https://blog.replit.com/elisp)
that Replit's approach is to "take every programming language that has
a repl and expose them all behind the same command-line interface",
and the blog post even has an example JSON configuration file for one
of Replit's languages.

### Riju's use of Docker to install and run multiple languages

Riju uses per-language configuration to generate shell scripts to
install all its programming languages into a single Docker images
(originally) or into multiple Docker images (later on).

Is it a trade secret to run programming languages online by installing
them into a Docker image, or to set up this installation by generating
shell scripts from per-language configuration? Nope, this process is
documented [on Replit's
blog](https://web.archive.org/web/20210504023410/https://blog.replit.com/elisp),
and there's even open-source code to generate shell scripts and build
such a Docker image [on their public
GitHub](https://web.archive.org/web/20211130092153/https://github.com/replit/polygott).
In case you thought the one-image-versus-many-images decision might be
a trade secret, nope, there's a discussion of that issue [right in the
GitHub
README](https://web.archive.org/web/20211130092153/https://github.com/replit/polygott#overview)
along with a note about what Replit ended up going with.

### Riju's build system

Recent versions of Riju have a rather advanced build system in which:

* for each language, a shell script is generated, which is used to
  install it in an isolated environment and generate a Debian package,
  which is installed into a per-language Docker image
* all build artifacts (generated shell scripts, Debian packages,
  per-language Docker images, and environment base images) are hashed
  based on their source code, and the results are used to generate a
  dependency graph and compute the minimal set of operations necessary
  to propagate any given configuration change

Is any aspect of this build system a trade secret? No, because it
simply has no equivalent whatsoever at Replit; the design was purely
my own innovation. If you'd like to verify this fact for yourself, you
can check out Replit's implementation [on
GitHub](https://web.archive.org/web/20211130092153/https://github.com/replit/polygott).

### Riju's deployment configuration

Riju was hosted on a single DigitalOcean server (at first) or EC2
instance (later on), and runs the server as a single Docker container.
All user sessions are run within a single container, using standard
UNIX permissions to provide isolation.

Is it a trade secret of Replit's to run user code this way? No,
because Replit *doesn't* run user code this way at all: they use [a
container per
session](https://web.archive.org/web/20210504031011/https://blog.replit.com/killing-containers-at-scale),
[multiplexed across a fleet of GCP
nodes](https://web.archive.org/web/20210504031011/https://blog.replit.com/killing-containers-at-scale).

### Riju's tech stack

Here is an exhaustive list of all the languages, libraries,
technologies, and platforms that Riju and Replit share (or that you
might think they share) as part of their tech stacks:

* Languages: C (setuid binary), JavaScript (frontend), Node.js
  (backend)
* Configuration: JSON, JSON Schema, YAML
* Build tools: Make, Webpack
* Infrastructure: Docker
* Libraries: Express, Monaco, Xterm.js

Is the use of any part of this tech stack a trade secret of Replit's?
No, and here's why for each one:

* Languages: The use of C for setuid binaries to run privileged
  operations [is public
  knowledge](https://unix.stackexchange.com/a/369), and as far as I
  know Replit doesn't use this approach anyway. JavaScript is
  literally the only language that can be used for frontend
  development. Node.js is [the #1 most popular web
  technology](https://insights.stackoverflow.com/survey/2020#technology-other-frameworks-libraries-and-tools-all-respondents3)
  and I'd been [using it years before working at
  Replit](https://github.com/MuddCreates/hyperschedule/blob/e1b0b661b4712ec8744b1a033ce63be4789db33e/server.js).
* Configuration: JSON and YAML are [the top two most popular
  configuration
  formats](https://archive.is/EuYji#7ae4),
  and it's easy to [find both in my pre-Replit
  projects](https://github.com/raxod502/pset/tree/d0be46e12e2b134f23994495a63ec5c43850a6d9).
  I've used JSON Schema in projects [predating my work at
  Replit](https://github.com/raxod502/etunes/blob/14aa75dca37a95b3ced0ab76e60422cec0f84ee3/etunes/__init__.py#L334-L470).
* Build tools: I used Make [before I worked at
  Replit](https://github.com/raxod502/straight.el/tree/e51747861be2c5e2f1c990762167eb4b800fdb46).
  Webpack is [the #1 most popular JavaScript module
  bundler](https://ashleynolan.co.uk/blog/frontend-tooling-survey-2016-results#js-bundlers).
* Infrastructure: The fact that Replit uses Docker [is public
  knowledge](https://web.archive.org/web/20210504031011/https://blog.replit.com/killing-containers-at-scale),
  and besides, my technical work with Docker at Replit [is
  open-source](https://web.archive.org/web/20211221134407/https://github.com/replit/upm).
* Libraries: Express is [the #1 most popular Node.js web
  framework](https://x-team.com/blog/most-popular-node-frameworks/),
  and (as with Node.js) I'd been [using it years before working at
  Replit](https://github.com/MuddCreates/hyperschedule/blob/e1b0b661b4712ec8744b1a033ce63be4789db33e/server.js).
  The fact that Replit uses Monaco [is public
  knowledge](https://web.archive.org/web/20210504041816/https://blog.replit.com/intel).
  The fact that they use Xterm.js [is also public
  knowledge](https://web.archive.org/web/20210504042426/https://blog.replit.com/shell).

## 3. Was it unethical to develop Riju?

See [the main post](./#is-replit-right).
