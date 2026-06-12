---
title: Projects
---

This page lists some of my personal, work, and school projects. You
can find the source code for (almost) all of these projects and more
on my [personal GitHub account][github] and the [Radian LLC GitHub
organization][radian-github].

Projects are organized into sections alphabetically by topic and then
chronologically by when the most work was done on them, and may be
tagged:

* `archived`, in case the project was relatively complete, but is no
  longer planned to be updated or actively maintained to keep it
  functioning.
* `abandoned`, in case I gave up on the project before finishing it,
  and never plan to return (e.g. because it was a bad idea).
* `unfinished`, in case the project isn't in a finished state where it
  is a viable product yet, but I plan to get back to it at some point.
* `as employee at XYZ`, in case the project was completed for an
  employer.
* `as student at XYZ`, in case the project was completed in connection
  with a high school or college class.
* `proprietary`, in case the project is not open-source due to
  ownership by a third party such as a former employer.
* `private`, in case the project is not open-source due to security or
  privacy concerns (e.g.: personal information cannot be easily
  separated from source code).

Unless otherwise specified, projects can be assumed to be generally
feature-complete, open-source, and receiving ongoing maintenance when
needed. But, there are a *lot* of unfinished ideas here, because I
believe in sharing my unimpressive work as well: an unfinished project
may still have an interesting idea, or the code already written might
be helpful to a person who wants to build something similar.

Note that most of these projects are owned and operated by [Radian
LLC], who will be the liable party in the case of legal disputes.
[Reach out][contact] if you have a concern. A subset are my personal
work instead. When in doubt, check the license notice in the relevant
GitHub repository. Obviously, work projects are the property and
liability of the relevant employer(s), and the same applies to some
school projects.

I also do a lot of smaller work outside of the below (e.g.
contributions to others' open-source projects, operational work to
replace personal use of proprietary services); what's listed are the
things that fit reasonably enough into the shape of a "project" that
they can be summarized into a list item.

Just in case it is not clear, **nothing** I publish is AI-generated.

## Table of contents

<!-- toc -->

- [Art and design](#art-and-design)
- [Desktop applications](#desktop-applications)
- [Developer tools, infrastructure](#developer-tools-infrastructure)
- [Emacs projects](#emacs-projects)
- [Games](#games)
- [Mobile apps](#mobile-apps)
- [Multimedia software](#multimedia-software)
- [Research and learning](#research-and-learning)
- [Reverse engineering and web automation](#reverse-engineering-and-web-automation)
- [System administration](#system-administration)
- [Web apps and services, browser extensions](#web-apps-and-services-browser-extensions)
- [Writing](#writing)

<!-- tocstop -->

In case the list is too intimidating, here are some projects that you
may want to start with:

* [Calculus: Intuitive Explanations][cie] - the namesake of this
  website, and my oldest major project
* [Hyperschedule][hyperschedule-source] - my most widely used end-user
  application
* [Kalyn] - the project I feel is the most technically impressive, and
  that I feel has the best [write-up][kalyn-post]
* [MazeGen] - a project that actually looks cool as an object in the
  real world
* [`straight.el`][straight.el] - my most widely used developer tool
* [TerrariaClone] - my first project to become internet-famous

## Art and design

* [MathViewers] (Summer -- Winter 2014, as student of [Boulder High
  School][bhs]; archived): Various programming projects for math
  classes: [generative art], [complex arithmetic][complex numbers]
  visualization, numerical solution of [differential equations].
* [MazeGen] (Fall 2014, as student of [Boulder High School][bhs],
  Design Technology; archived): [Java] application to generate and
  visualize laser-cutter schematics for three-dimensional marble
  mazes.
* [layerize] (Fall 2015, as student of [Boulder High School][bhs],
  Design Technology; archived): [Clojure] application to generate and
  visualize laser-cutter schematics for a cross-sectional model of a
  "[Möbius solid][layerize-inspiration]".
* [MazeGen Neue] (Summer 2016; abandoned): An attempt to rewrite
  [MazeGen] to be slightly less of a mess. Unfortunately, I went much
  too far in the opposite direction and created some [Enterprise
  FizzBuzz], and the project was abandoned.
* Friend Finder (Summer 2021, private; archived): Physical box with
  colored LEDs showing free/busy status of apartment housemates and
  buttons that could be used to summon free housemates for activities.
* [HWTTP] (Summer 2022; unfinished): Joke project that implements an
  [HTTP server] by printing out the requests it receives, on an actual
  printer, and then scans your handwritten responses using [OCR]
  before sending them back to the client.

## Desktop applications

* [CAS] (Summer 2014; abandoned): Failed attempt to create a [computer
  algebra system], like [Mathematica].
* [jflap-tester] (Fall 2016, as student of [Harvey Mudd College][hmc],
  CS 42: Principles & Practice; archived): Script to automatically run
  test cases against student-submitted [DFAs], [NFAs], or [Turing
  machines] in [JFLAP] format.
* [mood-tracker] (Spring 2017; archived): Small [AppleScript] utility
  to record data about personal mood at regular intervals. This
  project was abandoned when I realized that trying to systematize
  everything in my life was actually not making me happier.
* [acc] (Summer 2017 -- Summer 2018; abandoned): Command-line
  accounting tool with first-class support for reconciling multiple
  ledgers interactively. This project was abandoned when it was
  pointed out to me by a friend that I didn't actually have to track
  every single one of my financial transactions. I used a manual
  spreadsheet (reviewed quarterly) for budgeting and cash flow
  analysis for some time, but have now migrated to [regex-accountant].
* [JFLAP Autograder] (Winter 2017, as student assistant at [Harvey
  Mudd College][hmc], CS 81: Computability and Logic; archived):
  Improved automations for grading student submissions of [Turing
  machines] in [JFLAP] format.
* [Radian LLC Financials] (Summer 2022 -- Present): Financial
  transparency reports from [Radian LLC], and code to generate the
  reports.
* [regex-accountant] (Summer 2023 -- Summer 2025; unfinished):
  Aggregating personal finance record-keeper based on total control of
  transaction reconciliation and categorization via interactive rules
  engine and standard interface for ingesting data from reverse
  engineered APIs.
* [Worm Timeline Reference] (Fall 2024; abandoned): Very brief attempt
  at an interactive guide to the hilarious number of characters and
  events in the web serial [Worm].

## Developer tools, infrastructure

* think.quality (Summer -- Winter 2016, as employee of ThinkTopic,
  proprietary): Tool for running company-wide [Clojure] code quality
  audits and dashboard to visualize results.
* [minimal-webapp] (Summer 2016; abandoned): Noble effort to create a
  [ClojureScript] webapp that did not require a huge number of
  incomprehensible build system configuration files that nobody quite
  understood. It almost worked.
* [empty] (Summer 2016): Absolute bare minimum [Leiningen] template.
* CMS Changeset Dashboard (Summer 2017, as employee of [Quantcast],
  proprietary): Full-stack administrator dashboard for an internal
  team to manage an internal database used by an internal webapp used
  by another internal team to manage another internal database. You
  can imagine the customer-facing impact.
* [lazy-map] (Winter 2016, as employee of ThinkTopic): Lazy [map]
  implementation for [Clojure].
* [THE HASHINATOR] (Spring 2017; abandoned): Brief attempt to make
  associative arrays in [Zsh] that don't fall apart immediately if you
  let them come into contact with user input.
* [heroku-buildpack-git-lfs] (Spring 2019, as student of [Harvey Mudd
  College][hmc], CS 121: Software Development): [Heroku] buildpack to
  install [Git LFS] and download assets transparently during build.
* [Webapps Done Right][wdr] (Spring 2019, as student of [Harvey Mudd
  College][hmc], CS 121: Software Development; archived): Guest
  lecture I gave to my class on webapp development using [Python],
  [Pipenv], [Flask], [Heroku]. [Slides here][wdr-slides] and [source
  here][wdr-source].
* [Big-O Reminders] (Summer 2019): Simple way to send reliable push
  notifications to multiple devices from my phone.
* [UPM] (Summer 2019, as employee of [Replit]): Universal
  [package-management][pm] interface for [Python], [Node.js], [Ruby],
  and [Emacs Lisp][elisp].
* [Lossless Path MTU Discovery][clinic-frag] (Fall 2019 -- Spring
  2020, as student of [Harvey Mudd College][hmc], [CS Clinic][clinic];
  archived): Implementation in the [Linux kernel][kernel] of a
  replacement for [Path MTU Discovery][pmtud] with improved
  performance and robustness. [Slides here][clinic-slides] and
  [Internet-Draft here][clinic-frag-id]. *Teammates: [Bradley
  Newton][bradley], [Hakan Alpan][hakan], [Miles President][miles].*
* [IPv6 Routing Extension Header Benchmarking][clinic-bench] (Spring
  2020, as student of [Harvey Mudd College][hmc], [CS Clinic][clinic];
  archived): Systematic procedure for comparing the performance of
  IPv6 routing [extension headers][exthdr] including [Routing Header
  Type 0][rh0], [Segment Routing Header][srh], and [Compressed Routing
  Header][crh]. [Slides here][clinic-slides] and [Internet-Draft
  here][clinic-bench-id]. *Teammates: [Bradley Newton][bradley],
  [Hakan Alpan][hakan], [Miles President][miles].*
* [Life After Mudd][lam] (Winter 2019 -- Spring 2020, as student of
  [Harvey Mudd College][hmc], CS 189: Programming Practicum;
  archived): Geographic visualization webapp for results of a survey
  on post-graduation plans for the Class of 2020. No longer online due
  to lack of interest from newer students.
* CLOC (Spring 2020, private; abandoned): Generate text-based reports
  on my largest projects.
* [OSSCount] (Fall 2021; abandoned): An idea to generate some cute
  graphs of my code contributions to various projects over time. This
  was replaced by [Project Finder] later on.
* Alert Routing Refactor (Fall 2021 -- Summer 2024, as employee of
  [Plaid], proprietary): New architecture for [PromQL]-based alerting
  that allowed [AlertManager] routing configuration to be controlled
  and deployed alongside individual microservices with greatly reduced
  blast radius for bad changes.
* [Nanoma] (Winter 2021; abandoned): Yet another static site
  generator. I didn't finish it, and ended up migrating to [Eleventy]
  instead.
* [Flashcraft Legacy] (Fall 2022; abandoned): Generalized
  user-friendly control panel for running low-duty-cycle [Minecraft]
  servers on a variety of cloud providers. I started the project over
  a year later fully without remembering about the work I already did,
  so this version is now legacy.
* [Sleeping Beauty] (Fall -- Winter 2022): Network utility that puts a
  stateless TCP web server to sleep when not receiving traffic, to
  minimize resource utilization.
* Healthchecks (Fall 2022 -- Present, private): Cron scheduling
  framework for deep uptime monitoring of various personal services.
* [Railway Backdoor] (Fall 2022): Quick utility to find out
  empirically what requests [Railway] uses to healthcheck running
  pods, so I could tune [Sleeping Beauty] to handle them properly.
* [Corona Updown] (Spring 2023): Simple admin interface for turning an
  [EC2 instance] on and off without needing to log in to [AWS].
* [MeLaan] (Summer 2023 -- Summer 2025): [MicroPython] code for
  [Raspberry Pi Pico W][picow] that establishes a persistent
  [TLS-over-TCP][tls] connection to a [Go] server allowing for opening
  my apartment building gate for deliveries when not physically
  present.
* Hyper Light Drift Detector (Summer 2023 -- Summer 2024, as employee
  of [Plaid], proprietary): Automated drift detection and robust
  ownership tracking scaling to thousands of individual [Terraform]
  projects.
* Teamless Clusters (Fall 2023 -- Fall 2024, as employee of [Plaid],
  proprietary): Zero downtime, fully self-service migration of several
  hundred microservices from team-based to service-based [Kubernetes]
  namespace topology.
* [Flashcraft] (Winter 2023; unfinished): Generalized user-friendly
  control panel for running low-duty-cycle [Minecraft] servers on a
  variety of cloud providers. Very little code written thus far.
* Standardized Certificate Management (Winter 2023 -- Winter 2024, as
  employee of [Plaid], proprietary): Centralized database, management
  interface, and automation platform for manually-provisioned or
  otherwise unusual [(m)TLS][mtls] certificates to allow responsible
  teams to manage their own partner authentication requirements.
* Artifactory deprecation (Summer -- Fall 2024, as employee of
  [Plaid], proprietary): Minimal-downtime replacement of [JFrog
  Artifactory][artifactory] with purpose-built tools covering all
  existing use cases at 0.3% of the cost.
* [Wind's Pleasure] (Summer 2024): Cron job to run on a [Postfix] mail
  server that strips embedded advertisements from HTML email, for use
  as a filtering relay.
* [Calendar Redacter] (Winter 2024): Utility to make it easier to
  share free/busy calendar on [Fastmail] without inflating [ICS]
  filesize tremendously.
* [Birthday Filter] (Spring 2025): Utility to maintain [CalDAV]
  birthday calendar from [CardDAV] contacts collection, primarily
  targeted at [Fastmail].
* [GNOME KeyLoop] (Spring 2025): Documentation of the internal [GNOME
  Keyring] file format and a tool to make arbitrary modifications to
  it, since this was not possible using any other tool that existed at
  the time, officially supported or otherwise.
* [Project Finder] (Summer 2025; unfinished): Tool to make sense of
  the by-this-point excessive number of projects I have, generate a
  searchable registry, and create fun statistics and graphs about what
  kind of work I've done over time.
* [Calmerge] (Fall 2025): Utility to merge multiple [CalDAV] calendars
  together and keep them in sync, for example to share a single
  calendar with an external party.
* [FMD Healthcheck] (Spring 2026): Cron job that implements enough of
  [FMD] client-side cryptography to be able to health-check whether
  FMD-Server has been receiving recent pings from a tracked device.

## Emacs projects

* [Radian] (Summer 2016 -- Present): Elegant but practical
  configurations for [Emacs], [Zsh], [Tmux], and [Git].
* [`el-patch`][el-patch] (Winter 2016 -- Fall 2018): [Emacs] package
  for future-proofing Emacs Lisp customizations.
* [`straight.el`][straight.el] (Winter 2016 -- Present):
  Next-generation, purely functional package manager for the [Emacs]
  hacker. *Co-maintainer: [Nicholas Vollmer][progfolio].*
* [diary-manager] (Spring 2017 -- Summer 2018): Command-line tool and
  [Emacs] package for managing daily (encrypted, version-controlled)
  diary entries.
* [elint] (Summer -- Fall 2017; archived): An attempt at deduplicating
  various [CI] utilities for my [Emacs] packages. It didn't provide
  enough value to justify the overhead, although there are other
  projects which provide the same functionality in a more powerful
  manner.
* [`prescient.el`][prescient.el] (Fall 2017 -- Winter 2019): Simple
  but effective sorting and filtering for [Emacs].
* [with-feature] (Fall 2017; abandoned): Replacement for
  [use-package]. Superseded by upstream improvements.
* [org-emacs] (Summer 2018; archived): Pre-set [Emacs] configuration
  for friends who wished to try out [Org] but were otherwise
  unfamiliar with Emacs and the command line.
* [heroku-buildpack-emacs] (Summer 2018): [Heroku] buildpack to
  install [Emacs].
* [Ishikk] (Summer 2018; unfinished): Read-write [Google Calendar]
  interface for Emacs, with graphical week view. If finished, this
  would be repurposed to work with [Fastmail]. However, the 2023
  package [calfw-blocks] might supersede the project.
* [GNU ELPA Mirror][gnu-elpa-mirror] (Summer 2018 -- Summer 2019):
  GitHub mirror of the [GNU ELPA][gnu-elpa] and [Emacsmirror] package
  repositories for use with [`straight.el`][straight.el].
* [Blackout] (Fall 2018): Unified replacement for
  [`diminish.el`][diminish.el], [`delight.el`][delight.el], and
  [`dim.el`][dim.el]; allows hiding or customizing major and minor
  mode lighters in [Emacs].
* [Tabcrush] (Summer 2019; abandoned): High-performance power tool for
  editing large-scale tabular data in [Emacs], intended for use with
  [µTunes][utunes]. Deprecated alongside µTunes.
* [Mercury] (Summer -- Fall 2019; abandoned): [Emacs] interface to
  [Facebook Messenger], [Signal], and SMS (via [Google
  Hangouts][hangouts]). This has been superseded by [Matrix] for me.
* [Apheleia] (Summer 2019): Run code formatters on [Emacs] buffer
  contents without moving the cursor position, using [RCS patches] and
  [dynamic programming].
* [Selectrum] (Fall 2019 -- Spring 2020; archived): Completion and
  incremental narrowing framework for [Emacs], replacing [Ivy] and
  [Helm]. It has been replaced by [Vertico]. *Co-maintainer: [Clemens
  Radermacher][clemera].*
* [CTRLF] (Winter 2019 -- Spring 2020): Better single-buffer text
  search interface for [Emacs], replacing [Isearch] and [Swiper].
* [EMTAS] (Winter 2019; abandoned): Very brief attempt to develop
  formal tooling on [Emacs] startup time optimization.
* [Dumbparens] (Spring 2020; unfinished): Sane delimiter-matching
  package for [Emacs] with primitives based on [syntax tables],
  replacing [Smartparens], [Paredit], and [Electric Pair
  mode][electric-pair-mode]. This is still relevant but bandwidth has
  not been available to drive the project to completion.

## Games

* [TerrariaClone] (Spring 2011 -- Spring 2013; archived): My first
  major project, a clone of [Terraria], preserved as an example of how
  terrible code can be if you don't pay attention to its quality.
  Discussed on [HackerNews][tc-hn].
* [space-grid] (Spring 2012; abandoned): An attempt at a clone of the
  Flash game [Star Relic] in [Python]. It didn't get very far, because
  I didn't actually know any game programming.
* [Mother's Day][mothers-day-2013] (Summer 2013; archived): Small
  [Java] applet that I made for Mother's Day.
* [Watching Paint Dry: The Game][watching paint dry] (Summer 2013;
  archived): Small [Java] applet where you can paint things with the
  mouse, and then watch the paint dry. Yes, really. For Father's Day.
* [tetris-processing] (Winter 2013; archived): Simple clone of
  [Tetris] from high school, this one in [Processing] and featuring
  music.
* [funwithframes] (Winter 2013; archived): Simple game in [Processing]
  where you try to dodge certain squares while being distracted by
  other squares.
* [2048] (Spring -- Summer 2014; archived): Simple clone of the game
  [2048][2048-game], implemented in [Java] with graphical and
  command-line interfaces as well as a few auto-solving algorithms.
* [tetris-python] (Summer 2014; archived): Slightly more advanced
  clone of [Tetris] from high school, this one in [Python] and
  featuring pentominoes and other nonstandard pieces.
* [Christmas Rogue] (Winter 2014; archived): Christmas present for my
  father. [Roguelike] game inspired by [Brogue] and implemented in
  [Java]. Likely the most over-the-top Christmas present I will ever
  give.
* [Drift] (Summer 2017; abandoned): An attempt to learn C++ game
  development based on [SDL].
* [Planetation v1] (Fall -- Winter 2017; abandoned): A second attempt
  to learn [C++] game development based on [SDL].
* [Planetation v2] (Fall 2018; abandoned): A third attempt to learn
  [C++] game development, this time based on [SFML]. This one got
  especially little distance.
* [My puzzle hunt][puzzle-hunt-1] (Summer 2020): A short online
  [puzzle hunt] of my own design, with eight puzzles and a metapuzzle.
* [Transmission] (Winter 2020 -- Spring 2021; abandoned): Attempt at
  an online social deduction game around transmission of information
  through unreliable intermediaries. *Co-author: Owen Gillespie.*
* [Silhouette] (Fall 2021; abandoned): Idea for a game where you would
  be presented with outlines of the visual shape of open-source code
  that you had written, and tried to guess where they were from.
* [TerrariaCloneClone] (Spring 2022; abandoned): Attempt to re-write
  [TerrariaClone] in a less terrible way.
* [Copymantle] (Fall 2025; unfinished): Simple clone of [Semantle]
  that doesn't crash as much.

## Mobile apps

* [TI-84 programs][ti-84-programs] (Spring 2010 -- Spring 2016;
  archived): My first programming ever, on the [TI-84 Plus Silver
  Edition][ti-84] in middle and high school.
* [Hangman 2 2 3 2][hangman2232] (Spring 2013, as student of [Boulder
  High School][bhs], Advanced C++; archived): Class project. [iOS] app
  that plays [hangman] or, depending on usage, the stock market.
* [Chrono Count] (Summer 2013 -- Spring 2014; archived): [iOS] app to
  manage countdowns and countups under arbitrarily complex schedules,
  previously available from the iOS App Store.
* [Gravity] (Winter 2013; archived): Christmas present for my father.
  [iOS] app that simulates [many-body Newtonian gravity][n-body].

## Multimedia software

* [legacy-music-scripts] (Spring 2015 -- Winter 2019; archived):
  Various really old [Python] scripts for downloading music from free
  websites and extracting data from my music library (in iTunes, at
  the time).
* [smarter-playlist] (Fall 2016; archived): [Clojure] application to
  generate iTunes playlists combining variety, cohesiveness, and
  novelty.
* [etunes] (Fall 2017 -- Summer 2018; abandoned): [Declarative],
  [version-controlled][version control] music library manager for
  [Emacs]. Attempt #1 at a personal music library manager. Replaced by
  [fstunes].
* [fstunes] (Winter 2018; abandoned): Extremely minimal music library
  manager leveraging [UNIX filesystem] abstractions. Attempt #2 at a
  personal music library manager. Replaced by [µTunes][utunes].
* [µTunes][utunes] (Spring -- Winter 2019; unfinished): Aggressively
  minimal command-line music player and library manager following the
  [UNIX philosophy], with [Emacs] interface. Attempt #3 at a personal
  music library manager. Was supposed to be replaced by [Pyrelight]
  but is still in current use despite being considered deprecated.
* [µtunes-scripts][utunes-scripts] (Summer -- Winter 2019): Various
  scripts for personal use with [µTunes][utunes], many of which have
  become obsolete and have been removed.
* [Pyrelight] (Spring -- Summer 2020; abandoned): More sophisticated
  command-line music player and library manager. Attempt #4 at a
  personal music library manager. Will be replaced by Shallan.
* [Shallan] (Spring -- Summer 2021; unfinished): Personal music
  library player combining the user-friendly interface and
  cross-device synchronization of [YouTube Music][ytm] with the
  flexibility and ownership of a self-hosted open-source solution.
  Attempt #5 at a personal music library manager.
* [shallan-scripts] (Spring 2021): Simple script for migrating a
  library from [µTunes][utunes] to [Shallan].

## Research and learning

* [Science fair project][science-fair] (Fall 2011 -- Spring 2012, as
  student of [Summit Middle School][summit]; archived): [Boolean
  satisfiability solver][sat] applied to [Sudoku] solving.
* [Projectile Simulator] (Fall 2013, as student of [Boulder High
  School][bhs], AP Physics C; archived): Class project. Hacky [Python]
  GUI in [Tkinter] to solve arbitrary [2D
  kinematics][projectile-motion] problems interactively.
* think.recommend (Winter 2015 -- Summer 2016, as employee of
  ThinkTopic, proprietary): Library for testing and benchmarking
  [collaborative filtering][cf] algorithms.
* [cortex.optimise] (Spring -- Summer 2016, as employee of
  ThinkTopic): General-purpose library for analyzing, visualizing, and
  comparing [gradient descent] algorithms.
* [dfa] (Spring 2016; abandoned): An attempt to use [Clojure] to
  generate [DFAs] using a [genetic algorithm].
* [puzzles] (Summer 2016; archived): Solvers for [KenKen] and [Sudoku]
  puzzles in [Clojure].
* [conway] (Fall 2016; archived): A simple solver for generalized
  [Slothouber-Graatsma \(Conway\) puzzles][sg-puzzles] in [Clojure].
* [VotingLib] (Fall 2016, as student of [Harvey Mudd College][hmc],
  MATH 189G: Mathematics of Voting; archived): [Java] library written
  for a short research project investigating the performance of
  different voting systems assuming voter satisfaction can be modeled
  as a high-dimensional Euclidean distance metric.
* [SortingAlgorithms] (Fall 2016; archived): Versions of common
  [sorting algorithms] that I wrote in [Java] to help me learn about
  them.
* [music-sorter] (Spring -- Summer 2017; abandoned): Elementary
  research into techniques for clustering musical tracks based on
  acoustic content and style.
* [Lucid] (Spring 2017; abandoned): Attempt to learn [Rust] and design
  a simple version-control system following the design of [Git]. Did
  not get very far.
* [cpp-playground] (Fall 2017; archived): Test programs I used to help
  myself learn C++.
* [Kalyn] (Spring 2020; unfinished): Compile a high-level functional
  programming language, inspired by [Haskell] but with [Lisp] syntax,
  all the way to [ELF] binaries targeting [x86-64] without using any
  pre-existing components such as the [GNU][] [linker] or [C standard
  library][cstdlib]. Has a nice [blog post][kalyn-post].

## Reverse engineering and web automation

* [Decryptonite] (Summer -- Winter 2021; abandoned): Exploratory work
  to access [WideVine L3][widevine] YouTube content streams using
  open-source software.
* [Messenger Mirror][mm] (Fall 2021; archived): Small [Python]
  application using [Selenium] to bypass Facebook Messenger's anti-bot
  protections and allow message notifications to be automatically
  forwarded to email. Part of my initiative to stop using the products
  of companies I despise. This was eventually blocked by Facebook.
* [Unzuckify] (Winter 2021; archived): Small [Python] application
  using [reverse-engineered][rev-eng] [Facebook] login and
  [GraphQL](https://graphql.org/) APIs to exfiltrate message
  notifications and forward them to email. Replaces [Messenger
  Mirror][mm] after Facebook blocked it. This project was blocked too,
  so I just fully deprecated Messenger ahead of schedule.
* [Claremont Spam Disabler] (Summer 2022): Tiny [Google Apps
  Script][gas] project that automatically filters and processes spammy
  emails sent to students by the [Claremont Colleges].
* [Venmo Auto Transfer] (Summer 2022; archived): Small [Python]
  application using [reverse-engineered][rev-eng] [Venmo] API to
  automatically transfer Venmo balance to linked bank account.
* [Squeaky Hinge] (Fall 2022; archived): Small [Python] application
  using [reverse-engineered][rev-eng] [Hinge] API to send more
  reliable notifications on inbox messages.
* [dontbeevilmirror] (Spring 2023; unfinished): Anonymizing proxy [CDN] for
  [Android] apps pulled from the [Google Play Store].
* [regex-accountant-config] (Summer 2023 -- Present): Configuration
  modules for [regex-accountant] that allow it to extract data from
  numerous reluctant websites, including Amazon, Cash App, Fidelity
  Investments, Patreon, PayPal, and Vanguard. Also includes a [Plaid]
  integration to support any financial institutions supported by
  Plaid.
* [Curlinate] (Summer 2023): Command-line and Python interface to make
  [HTTPS] requests with custom [ClientHello] signature forgery.
* [Zelle reverse engineering] (Summer -- Fall 2023): Full client for
  command-line authentication to now-defunct [Zelle] mobile API to
  retrieve transaction history.
* [Ticketlord] (Fall 2023 -- Spring 2025): Extract [Ticketmaster]
  rotating barcode secrets from both the web and Android APIs, to
  avoid needing to use their cesspool of an unreliable mobile app for
  event access.
* [Nebulous] (Winter 2023; unfinished): Open-source [Nebula] client
  that has better support for managing downloaded videos.
* [Fuck Venmo] (Winter 2023 -- Spring 2025; archived): Software that
  fully automates the process of arguing with [Venmo]'s sociopathic
  customer support department multiple times per day so they agree to
  unlock your account that they keep locking without justification.
* [Venmo Auto Transfer Neue] (Summer 2024 -- Winter 2025): Wrapper for
  [venmo-auto-cashout] that also handles SMS OTP via my [Matrix]
  homeserver. Implementing the Matrix cryptography turned out to be
  the vast majority of the code for this project.
* [Outertube] (Fall 2024; abandoned): Open-source player for YouTube
  [WideVine L3][widevine] content streams. Based on work from
  [Decryptonite], but didn't get very far.
* [FTB Password Changer] (Summer 2024): Tool to automate the mandatory
  every-four-month password change that you have to do for
  California's [MyFTB] to avoid being permanently locked out of being
  able to pay taxes and file business documents.
* [Hotair] (Summer -- Winter 2025; unfinished): Open-source [Steam]
  client that can actually run games, including save data
  synchronization and online play. No dependencies on the proprietary
  client.
* [Blue Rover] (Spring 2026; unfinished): Automatically accept
  substitute teaching positions listed on [Red Rover] depending on
  availability.
* [Adobe File Downloader] (Summer 2026): Extract and synchronize files
  from Adobe's terrible "Your files" web interface, which doesn't
  provide a download option.

## System administration

* radian-local (Fall 2016 -- Present, private): Personal
  configurations on top of [Radian], and other very me-specific
  infrastructure and scripts.
* [Dotman] (Summer 2017 -- Summer 2018; abandoned): A very silly idea
  I had to write a unified package manager (with [Ruby] DSL) for my
  entire system configuration (e.g. software installation,
  configuration, dotfiles, misc scripts, etc.). This was abandoned
  when I realized I could just manually write down what I did to
  configure my laptop. If you actually want declarative system
  configuration, you should probably be using [Nix].
* [wdx] (Fall 2017): Simpler and more robust alternative to [wd],
  written in [Python].
* [backup-manager] (Summer 2018 -- Spring 2025; archived):
  Orchestration tooling for personal backups, file replication, and
  monitoring, based on [Borg] and [rclone].
* [misc-scripts] (Summer 2018 -- Present): Miscellaneous utility
  scripts that I have on my shell path and might be useful to others.
* [Madeline] (Summer 2018; archived): Novel approach to directory
  syncing, used to maintain complementary mirroring of two filesystem
  trees via SSH. This idea, while interesting, never served my use
  case terribly well in the end, and the implementation is terrible. I
  now use a smaller and better-targeted personal script to serve a
  similar function.
* [Debbie] (Winter 2020 -- Winter 2025; archived): Tooling and package
  definitions for installing and managing third-party software on
  [Debian]-based distributions when not supported in the official
  repositories, similar to Arch Linux [PKGBUILD]s. Eventually, I just
  switched to Arch and maintain packages on the [AUR] where
  appropriate.
* OpsWorks deprecation (Summer 2021 -- Summer 2024, as employee of
  [Plaid], proprietary): Zero-downtime migration of several hundred
  production-critical legacy systems out of [AWS OpsWorks][opsworks]
  before its retirement.
* [apt-get-unfuck] (Summer 2022; abandoned): Tooling to record and
  rollback old package versions from [Debian]-based repositories
  without relying on online data sources. I eventually switched to
  [BTRFS] instead.
* [pass-ln] (Fall 2022): [Pass] extension for creating [symbolic
  links][symlinks].
* [Dominion Strategy server upgrade] (Winter 2023): I did a server
  upgrade for the [Dominion Strategy forum] folks from Ubuntu 10.04 to
  24.04, and documented the process. I also previously retrofitted
  proper TLS onto the old server the year prior.
* system-upgrade (Winter 2023 -- Present): Operator-present server,
  laptop, and phone upgrade manager across highly heterogeneous device
  fleet.

## Web apps and services, browser extensions

* [Ecofasten] and [Alpine Snowboards] pricing calculators (Summer
  2015, as employee at ThinkTopic, proprietary): Frontend and backend
  work on existing [Clojure]/[ClojureScript]/[Datomic] web
  applications for generating price quotes for roof-mounted solar
  panels and alpine snowboards. *Teammates: [Charles
  Gruenwald][charles], [Keren Megory-Cohen][keren].*
* [Tidier] (Spring 2019): Small application to auto-close abandoned
  GitHub issues by label and activity.
* [Hyperschedule Prime] (Summer 2017; abandoned): First attempt at an
  improved course scheduling tool for the [Claremont Colleges]. I
  didn't finish it in time for course registration.
* [Hyposchedule] (Winter 2017; archived): Small script to do personal
  course scheduling for the [Claremont Colleges].
* [Hyperschedule] (Winter 2017 -- Fall 2019): Fast and powerful course
  scheduler for the [Claremont Colleges], still used. [Frontend source
  here][hyperschedule-source], [backend source
  here][hyperschedule-api] (since replaced). *Current maintainer:
  [ASHMC](https://www.hmc.edu/ashmc/).*
* [Hyperschedule Scrapers] (Summer 2019; abandoned): Attempt to extend
  Hyperschedule to support other institutions, including the
  [University of Colorado][ucb]. This is probably still doable and
  could be a successful idea, but my priorities shifted over time.
* [whales.life] (Spring 2019, as student of [Harvey Mudd
  College][hmc], CS 121: Software Development; archived): Simple
  webapp for playing [chess] against an AI using [minimax] and [neural
  networks]. [Source here][whales.life-source]. *Teammates: [Ben
  Baral][ben], [Max Treutelaar][max], [Miles President][miles],
  [Shannon Collier][shannon].*
* [GitHub Email Backlog][geb] (Summer 2020; archived): Simple [Chrome
  extension][chrome-ext] which abuses the [GitHub notifications
  API][github-notifications] to automatically update my profile status
  with an estimate of how long you will wait for a response when you
  report an issue. This is deprecated since I have gotten my personal
  life in order and can provide a more reliable base response time.
* [Riju] (Summer 2020 -- Summer 2022): Extremely fast online
  playground for every programming language. Currently working on port
  to [Kubernetes] to improve maintainability. [Source
  here][riju-source].
* [Python in a Box][pib] (Summer 2021): Interactive online Python REPL
  in 30 lines of JavaScript. [Source here][pib-source].
* [Veidt Legacy] (Summer -- Fall 2021; abandoned): Online webcomic
  aggregator, as a web server. I decided it was insufficiently ethical
  this way and decided on a [different architecture][veidt] instead.
* [riju-k8s] (Winter 2021; abandoned): Attempt to re-write [Riju]
  based on [Kubernetes]. Has some useful infrastructure setup but no
  real progress.
* [Tinyku] (Spring 2022; abandoned): Experiment in making a simple
  replacement for Heroku after they eliminated the ability to run
  small-scale applications cheaply.
* [Veidt] (Summer 2022; abandoned): Webcomic reader and progress
  tracker, as a browser extension. I ended up using [Mihon] personally
  instead.
* [riju-neue] (Summer 2022; unfinished): Another attempt to re-write
  [Riju] based on [Kubernetes]. Also has not gotten very far.
* [Hypercast] (Winter 2022; unfinished): Free, no-hassle watch parties
  on every streaming platform. Implemented as Chrome and Firefox
  extension.
* [GNSSMS] (Summer 2023; archived): Silly Mother's Day present that
  allowed you to text a [Twilio] number and get back GPS orbit data
  from the [gnss-reflections][gnssrefl] API formerly featured on my
  [mother's website][gnss-website].
* [Radian Transfer] (Summer 2024; abandoned): Replacement for Venmo,
  abandoned when I found out that it is essentially impossible to do
  business with any money movement provider unless you already have a
  huge corporation. I still ended up writing most of the REST logic
  for account signup and login, though.
* [dontbeeviltube] (Fall 2024; unfinished): Open-source client and
  proxy for free YouTube content based on [yt-dlp], as alternative to
  [Invidious] with improved stability.
* [PhotoPrismProxy] (Fall 2025): Simple proxy webserver that allows
  more easily uploading individual photos and albums to a [PhotoPrism]
  instance.

## Writing

* [*Calculus: Intuitive Explanations*][cie] (Summer -- Fall 2015;
  [source][cie-source]): 67 pages of [LaTeX] content, from limits to
  vector analysis, with 35 [Ti*k*Z][tikz] figures. [Source
  here][cie-source].
* [Calculus Bowl: Expert Edition][cbee] (Spring 2016): Strange
  multiple-choice questions from single-variable calculus, somewhat in
  the vein of the [Rocky Mountain Area Calculus Bowl][cb].
* [*Differential Equation Solution Strategies*][dess] (Spring 2016):
  Summary of strategies for solving different types of [differential
  equations], with proofs. [Source here][dess-source].
* [*Linear Algebra Summary Sheet*][lass] (Spring 2016): Quick
  reference for important [linear algebra] theorems, grouped so that
  making connections is easy. [Source here][lass-source].
* [`intuitiveexplanations.com`][ie] (Spring 2017 -- Present): Personal
  website built on [GitHub Actions][gha] using [Make], [Eleventy],
  [LaTeX], and hosted on [Vercel].
* [mla-tex] (Spring 2017 -- Fall 2018): [LaTeX][latex] [document
  class] for typesetting papers to [MLA] formatting standards.
* [Surveying Trigonometry Worksheet] (Spring 2017, as student of
  [Harvey Mudd College][hmc], MATH 196: Independent Study - Motivation
  in Mathematics): Math worksheet trying (poorly) to show some
  applications of trigonometry to the real world.
* [pset] (Fall 2017; abandoned): Configurable templating system for
  university problem sets typeset in LaTeX. Will never be finished
  because I am no longer a college student.
* [Talk for Students Speak][students-speak] (Fall 2019): Some remarks
  on mental health and the [paradoxical theory of change] that I
  delivered as a student panelist at a [Scripps College] student
  event.
* [example-website] (Summer 2020; archived): Simple template to set up
  a [static site] similar to my personal website, for my friends who
  were interested in making similar websites for themselves.
* [How Replit used legal threats to kill my open-source
  project][replit-post] (Summer 2021): Exposé on abusive behavior by a
  former employer which successfully shut down legal threats from them
  via the court of public opinion. At the time, seventh most upvoted
  post of all time [on Hacker News][replit-hn].
* [Reverse engineering the Facebook Messenger API][messenger-post]
  (Winter 2021): Tutorial for how to reverse engineer web
  applications, using Facebook Messenger as a case study.
* [PhotoPrism setup guide][pp-setup] (Winter 2023): Setup and
  migration guide for people moving from Google Photos to
  [PhotoPrism].

[2048-game]: https://play2048.co/
[2048]: https://github.com/radian-software/2048
[acc]: https://github.com/radian-software/acc
[adobe file downloader]: https://github.com/radian-software/adobe-file-downloader
[alertmanager]: https://prometheus.io/docs/alerting/latest/alertmanager/
[alpine snowboards]: https://www.sgsnowboards.com/
[android]: https://en.wikipedia.org/wiki/Android_(operating_system)
[apheleia]: https://github.com/radian-software/apheleia
[applescript]: https://en.wikipedia.org/wiki/AppleScript
[apt-get-unfuck]: https://github.com/radian-software/apt-get-unfuck
[artifactory]: https://jfrog.com/artifactory/
[aur]: https://wiki.archlinux.org/title/Arch_User_Repository
[aws]: https://en.wikipedia.org/wiki/Amazon_Web_Services
[backup-manager]: https://github.com/radian-software/backup-manager
[ben]: https://dspacemainprd01.lib.uwaterloo.ca/server/api/core/bitstreams/d25680c2-9f7f-4828-bb97-f6e882240eca/content
[bhs]: https://boh.bvsd.org/
[big-o reminders]: https://github.com/radian-software/big-o-reminders
[birthday filter]: https://github.com/radian-software/birthday-filter
[blackout]: https://github.com/radian-software/blackout
[blue rover]: https://github.com/radian-software/blue-rover
[borg]: https://www.borgbackup.org/
[bradley]: https://cmsathletics.org/sports/mens-swimming-and-diving/roster/bradley-newton/14845
[brogue]: https://sites.google.com/site/broguegame/
[btrfs]: https://en.wikipedia.org/wiki/Btrfs
[c++]: https://en.wikipedia.org/wiki/C%2B%2B
[caldav]: https://en.wikipedia.org/wiki/CalDAV
[calendar redacter]: https://github.com/radian-software/calendar-redacter
[calfw-blocks]: https://github.com/ml729/calfw-blocks
[calmerge]: https://github.com/radian-software/calmerge
[carddav]: https://en.wikipedia.org/wiki/CardDAV
[cas]: https://github.com/radian-software/CAS
[cb]: http://coyec.org/Zcalcbowl2016story/
[cbee]: /math/calculus-bowl-expert-edition
[cdn]: https://en.wikipedia.org/wiki/Content_delivery_network
[cf]: https://en.wikipedia.org/wiki/Collaborative_filtering
[charles]: https://web.archive.org/web/20260131174938/https://techascent.com/
[chess]: https://en.wikipedia.org/wiki/Chess
[christmas rogue]: https://github.com/radian-software/ChristmasRogue
[chrome-ext]: https://developer.chrome.com/extensions
[chrono count]: https://github.com/radian-software/chrono-count
[ci]: https://en.wikipedia.org/wiki/Continuous_integration
[cie-source]: https://github.com/raxod502/intuitive-explanations/blob/main/doc/tex/documents/CalculusIntuitiveExplanations/CalculusIntuitiveExplanations.tex
[cie]: /math/calculus-intuitive-explanations
[circleci]: https://circleci.com/
[claremont colleges]: http://www.claremont.edu/
[claremont spam disabler]: https://github.com/radian-software/claremont-spam-disabler
[clemera]: https://github.com/clemera
[clienthello]: https://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art059
[clinic-bench-id]: https://github.com/raxod502/juniper-tools/blob/master/benchmarking/draft/final.pdf
[clinic-bench]: https://github.com/raxod502/juniper-tools/tree/master/benchmarking
[clinic-frag-id]: https://tools.ietf.org/html/draft-bonica-intarea-lossless-pmtud-01
[clinic-frag]: https://github.com/raxod502/juniper-tools/tree/master/fragmentation
[clinic-slides]: https://nextcloud.intuitiveexplanations.com/s/M9DAew6BWR7z5Q8
[clinic]: https://www.cs.hmc.edu/clinic/
[clojure]: https://clojure.org/
[clojurescript]: https://clojurescript.org/
[complex numbers]: https://en.wikipedia.org/wiki/Complex_number
[computer algebra system]: https://en.wikipedia.org/wiki/Computer_algebra_system
[contact]: /about/contacting
[conway]: https://github.com/raxod502/conway
[copymantle]: https://github.com/radian-software/copymantle
[corona updown]: https://github.com/radian-software/corona-updown
[cortex.optimise]: https://github.com/raxod502/cortex/tree/master/examples/optimise
[cpp-playground]: https://github.com/radian-software/cpp-playground
[crh]: https://tools.ietf.org/html/draft-bonica-6man-comp-rtg-hdr-22
[cstdlib]: https://en.wikipedia.org/wiki/C_standard_library
[ctrlf]: https://github.com/radian-software/ctrlf
[curlinate]: https://github.com/radian-software/curlinate
[datomic]: https://www.datomic.com/
[debbie]: https://github.com/radian-software/debbie
[debian]: https://en.wikipedia.org/wiki/Debian
[declarative]: https://en.wikipedia.org/wiki/Declarative_programming
[decryptonite]: https://github.com/radian-software/decryptonite
[delight.el]: https://elpa.gnu.org/packages/delight.html
[dess-source]: https://github.com/raxod502/intuitive-explanations/blob/main/doc/tex/documents/DifferentialEquationSolutionStrategies/DifferentialEquationSolutionStrategies.tex
[dess]: /math/differential-equation-solution-strategies
[dfa]: https://github.com/raxod502/dfa
[dfas]: https://en.wikipedia.org/wiki/Deterministic_finite_automaton
[diary-manager]: https://github.com/radian-software/diary-manager
[differential equations]: https://en.wikipedia.org/wiki/Differential_equation
[dim.el]: https://github.com/alezost/dim.el
[diminish.el]: https://github.com/myrjola/diminish.el
[document class]: https://en.wikibooks.org/wiki/LaTeX/Document_Structure#Document_classes
[dominion strategy forum]: https://forum.dominionstrategy.com/
[dominion strategy server upgrade]: https://wiki.dominionstrategy.com/index.php/Ubuntu_upgrade_2023-11-15
[dontbeevilmirror]: https://github.com/radian-software/dontbeevilmirror
[dontbeeviltube]: https://github.com/radian-software/dontbeeviltube
[dotman]: https://github.com/radian-software/dotman/tree/e0ee7c8ba99477fd8c554a0757449b1ed6179fa4
[drift]: https://github.com/radian-software/drift
[dumbparens]: https://github.com/radian-software/dumbparens
[dynamic programming]: https://en.wikipedia.org/wiki/Dynamic_programming
[ec2 instance]: https://en.wikipedia.org/wiki/Amazon_Elastic_Compute_Cloud
[ecofasten]: https://ecofastensolar.com/
[el-patch]: https://github.com/radian-software/el-patch
[electric-pair-mode]: https://www.gnu.org/software/emacs/manual/html_node/emacs/Matching.html
[eleventy]: https://11ty.dev/
[elf]: https://en.wikipedia.org/wiki/Executable_and_Linkable_Format
[elint]: https://github.com/radian-software/elint
[elisp]: https://en.wikipedia.org/wiki/Emacs_Lisp
[emacs]: https://www.gnu.org/software/emacs/
[emacsmirror]: https://emacsmirror.net/
[empty]: https://github.com/radian-software/empty
[emtas]: https://github.com/radian-software/emtas
[enterprise fizzbuzz]: https://github.com/EnterpriseQualityCoding/FizzBuzzEnterpriseEdition
[etunes]: https://github.com/radian-software/etunes
[example-website]: https://github.com/raxod502/example-website
[exthdr]: https://en.wikipedia.org/wiki/IPv6_packet#Extension_headers
[facebook messenger]: https://www.messenger.com/
[facebook]: https://www.facebook.com/
[fastmail]: https://www.fastmail.com/
[flashcraft legacy]: https://github.com/radian-software/flashcraft-legacy
[flashcraft]: https://github.com/radian-software/flashcraft
[flask]: https://flask.palletsprojects.com/en/1.1.x/
[fmd healthcheck]: https://github.com/radian-software/fmd-healthcheck
[fmd]: https://fmd-foss.org/
[fstunes]: https://github.com/radian-software/fstunes
[ftb password changer]: https://github.com/radian-software/ftb_password_changer
[fuck venmo]: https://github.com/radian-software/fuck-venmo
[funwithframes]: https://github.com/raxod502/funwithframes
[gas]: https://developers.google.com/apps-script
[geb]: https://github.com/radian-software/github-email-backlog
[generative art]: https://en.wikipedia.org/wiki/Generative_art
[genetic algorithm]: https://en.wikipedia.org/wiki/Genetic_algorithm
[gha]: https://github.com/features/actions
[git lfs]: https://git-lfs.github.com/
[git]: https://git-scm.com/
[github-notifications]: https://developer.github.com/v3/activity/notifications/
[github]: https://github.com/raxod502
[gnome keyloop]: https://github.com/radian-software/gnome-keyloop
[gnome keyring]: https://en.wikipedia.org/wiki/GNOME_Keyring
[gnss-website]: https://gnss-reflections.org/
[gnssms]: https://github.com/radian-software/GNSSMS
[gnssrefl]: https://intuitiveexplanations.com
[gnu-elpa-mirror]: https://github.com/radian-software/gnu-elpa-mirror
[gnu-elpa]: https://elpa.gnu.org/
[gnu]: https://www.gnu.org/home.en.html
[go]: https://go.dev/
[google calendar]: https://calendar.google.com/
[google play store]: https://en.wikipedia.org/wiki/Google_Play
[gradient descent]: https://en.wikipedia.org/wiki/Gradient_descent
[graphql]: https://graphql.org/
[gravity]: https://github.com/radian-software/Gravity
[hakan]: https://www.hmc.edu/clinic/2020/optimizing-router-performance/
[hangman2232]: https://github.com/radian-software/Hangman2232
[hangman]: https://en.wikipedia.org/wiki/Hangman_(game)
[hangouts]: https://hangouts.google.com/
[haskell]: https://www.haskell.org/
[helm]: https://github.com/emacs-helm/helm
[heroku-buildpack-emacs]: https://github.com/radian-software/heroku-buildpack-emacs
[heroku-buildpack-git-lfs]: https://github.com/radian-software/heroku-buildpack-git-lfs
[heroku]: https://www.heroku.com/
[hinge]: https://hinge.co/
[hmc]: https://www.hmc.edu/
[hotair]: https://github.com/radian-software/hotair
[http server]: https://en.wikipedia.org/wiki/Web_server
[https]: https://en.wikipedia.org/wiki/HTTPS
[hwttp]: https://github.com/radian-software/hwttp
[hypercast]: https://github.com/radian-software/hypercast
[hyperschedule prime]: https://github.com/radian-software/hyperschedule-prime
[hyperschedule scrapers]: https://github.com/hyperschedule/hyperschedule-scrapers
[hyperschedule-api]: https://github.com/hyperschedule/hyperschedule-api
[hyperschedule-source]: https://github.com/hyperschedule/hyperschedule
[hyperschedule]: https://hyperschedule.io
[hyposchedule]: https://github.com/radian-software/hyposchedule
[ics]: https://en.wikipedia.org/wiki/ICalendar
[ie]: https://github.com/raxod502/intuitive-explanations
[invidious]: https://invidious.io/
[ios]: https://www.apple.com/ios/
[isearch]: https://www.gnu.org/software/emacs/manual/html_node/emacs/Incremental-Search.html
[ishikk]: https://github.com/radian-software/ishikk
[ivy]: https://github.com/abo-abo/swiper#ivy
[java]: https://www.java.com/
[jflap autograder]: https://github.com/raxod502/HMC-Grader/blob/master/app/plugins/autograder/newjflapgrader.py
[jflap-tester]: https://github.com/raxod502/jflap-tester
[jflap]: http://www.jflap.org/
[kalyn-post]: https://intuitiveexplanations.com/tech/kalyn
[kalyn]: https://github.com/radian-software/kalyn
[kenken]: https://en.wikipedia.org/wiki/KenKen
[keren]: https://github.com/kmegoryc
[kernel]: https://en.wikipedia.org/wiki/Linux_kernel
[kubernetes]: https://kubernetes.io/
[kye]: https://github.com/kwshi
[lam]: https://github.com/raxod502/life-after-mudd
[lass-source]: https://github.com/raxod502/intuitive-explanations/blob/main/doc/tex/documents/LinearAlgebraSummarySheet/LinearAlgebraSummarySheet.tex
[lass]: /math/linear-algebra-summary-sheet
[latex]: https://www.latex-project.org/
[layerize-inspiration]: https://github.com/radian-software/layerize/blob/f9d598b5d15c47045729505cc1b7a3d3e077bb11/Inspiration.pdf
[layerize]: https://github.com/radian-software/layerize
[lazy-map]: https://github.com/raxod502/lazy-map
[legacy-music-scripts]: https://github.com/radian-software/legacy-music-scripts
[leiningen]: https://leiningen.org/
[linear algebra]: https://en.wikipedia.org/wiki/Linear_algebra
[linker]: https://en.wikipedia.org/wiki/Linker_(computing)
[lisp]: https://en.wikipedia.org/wiki/Lisp_(programming_language)
[lucid]: https://github.com/radian-software/lucid
[lunch money]: https://lunchmoney.app/
[madeline]: https://github.com/radian-software/madeline
[make]: https://www.gnu.org/software/make/
[map]: https://en.wikipedia.org/wiki/Associative_array
[mathematica]: https://www.wolfram.com/mathematica/
[mathviewers]: https://github.com/raxod502/MathViewers
[matrix]: https://matrix.org/
[max]: https://mwt365.github.io/
[mazegen neue]: https://github.com/radian-software/MazeGenNeue
[mazegen]: https://github.com/radian-software/MazeGen
[melaan]: https://github.com/radian-software/melaan
[mercury]: https://github.com/radian-software/mercury
[messenger-post]: /tech/messenger
[micropython]: https://micropython.org/
[mihon]: https://mihon.app/
[miles]: https://tsl.news/miles-president-of-cms-basketball-talks-crossing-the-1000-point-mark/
[minecraft]: https://en.wikipedia.org/wiki/Minecraft
[minimal-webapp]: https://github.com/radian-software/minimal-webapp
[minimax]: https://en.wikipedia.org/wiki/Minimax
[misc-scripts]: https://github.com/radian-software/misc-scripts
[mla-tex]: https://github.com/radian-software/mla-tex
[mla]: https://web.archive.org/web/20180729195443/https://owl.english.purdue.edu/owl/resource/747/24/
[mm]: https://github.com/radian-software/messenger-mirror
[mood-tracker]: https://github.com/raxod502/mood-tracker
[mothers-day-2013]: https://github.com/raxod502/mothers-day-2013
[mtls]: https://en.wikipedia.org/wiki/Mutual_authentication#mTLS
[music-sorter]: https://github.com/raxod502/music-sorter
[myftb]: https://www.ftb.ca.gov/myftb/index.asp
[n-body]: https://en.wikipedia.org/wiki/N-body_simulation
[nanoma]: https://github.com/radian-software/nanoma
[nebula]: https://en.wikipedia.org/wiki/Nebula_(streaming_service)
[nebulous]: https://github.com/radian-software/nebulous
[neural networks]: https://en.wikipedia.org/wiki/Artificial_neural_network
[nfas]: https://en.wikipedia.org/wiki/Nondeterministic_finite_automaton
[nix]: https://nixos.org/
[node.js]: https://nodejs.org/en/
[ocr]: https://en.wikipedia.org/wiki/Optical_character_recognition
[opsworks]: https://web.archive.org/web/20250627034309/https://docs.aws.amazon.com/opsworks/latest/userguide/stacks-eol-faqs.html
[org-emacs]: https://github.com/raxod502/org-emacs
[org]: https://orgmode.org/
[osscount]: https://github.com/radian-software/osscount
[outertube]: https://github.com/radian-software/outertube
[paradoxical theory of change]: https://gestalt.org/arnie.htm
[paredit]: http://danmidwood.com/content/2014/11/21/animated-paredit.html
[pass-ln]: https://github.com/radian-software/pass-ln
[pass]: https://www.passwordstore.org/
[photoprism]: https://www.photoprism.app/
[photoprismproxy]: https://github.com/radian-software/photoprismproxy
[pib-source]: https://github.com/radian-software/python-in-a-box
[pib]: https://python-in-a-box.radian.codes/
[picow]: https://web.archive.org/web/20260518125619/https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html
[pipenv]: https://pipenv.pypa.io/en/latest/
[pkgbuild]: https://wiki.archlinux.org/title/PKGBUILD
[plaid]: https://plaid.com/
[planetation v1]: https://github.com/radian-software/planetation-v1
[planetation v2]: https://github.com/radian-software/planetation-v2
[pm]: https://en.wikipedia.org/wiki/Package_manager
[pmtud]: https://en.wikipedia.org/wiki/Path_MTU_Discovery
[postfix]: https://en.wikipedia.org/wiki/Postfix_(software)
[pp-setup]: https://github.com/radian-software/photoprism-setup-guide
[prescient.el]: https://github.com/radian-software/prescient.el
[processing]: https://processing.org/
[progfolio]: https://github.com/progfolio
[project finder]: https://github.com/radian-software/project-finder
[projectile simulator]: https://github.com/radian-software/ProjectileSimulator
[projectile-motion]: https://en.wikipedia.org/wiki/Projectile_motion
[promql]: https://prometheus.io/docs/prometheus/latest/querying/basics/
[pset]: https://github.com/radian-software/pset
[puzzle hunt]: https://blog.vero.site/post/puzzlehunts
[puzzle-hunt-1]: /puzzles
[puzzles]: https://github.com/raxod502/puzzles
[pyrelight]: https://github.com/radian-software/pyrelight
[python]: https://www.python.org/
[quantcast]: https://www.quantcast.com/
[radian llc financials]: https://github.com/radian-software/financials
[radian llc]: https://radian.codes/
[radian transfer]: https://github.com/radian-software/radian-transfer
[radian-github]: https://github.com/radian-software
[radian]: https://github.com/radian-software/radian
[railway backdoor]: https://github.com/radian-software/railway-backdoor
[railway]: https://railway.com/
[rclone]: https://rclone.org/
[rcs patches]: https://tools.ietf.org/doc/tcllib/html/rcs.html#section4
[red rover]: https://www.redroverk12.com/
[regex-accountant-config]: https://github.com/radian-software/regex-accountant-config
[regex-accountant]: https://github.com/radian-software/regex-accountant
[replit-hn]: https://web.archive.org/web/20260520003438/https://news.ycombinator.com/item?id=27424195
[replit-post]: /tech/replit
[replit]: https://intuitiveexplanations.com/tech/replit/
[rev-eng]: https://en.wikipedia.org/wiki/Reverse_engineering
[rh0]: https://tools.ietf.org/html/rfc2460#section-4.4
[riju-k8s]: https://github.com/radian-software/riju-k8s
[riju-neue]: https://github.com/radian-software/riju-neue
[riju-source]: https://github.com/radian-software/riju
[riju]: https://riju.codes/
[roguelike]: https://en.wikipedia.org/wiki/Roguelike
[ruby]: https://www.ruby-lang.org/en/
[rust]: https://rust-lang.org/
[sat]: https://en.wikipedia.org/wiki/Boolean_satisfiability_problem
[science-fair]: https://github.com/raxod502/ScienceFair
[scripps college]: https://en.wikipedia.org/wiki/Scripps_College
[sdl]: https://en.wikipedia.org/wiki/Simple_DirectMedia_Layer
[selectrum]: https://github.com/radian-software/selectrum
[selenium]: https://www.selenium.dev/
[semantle]: https://semantle.org/
[sfml]: https://www.sfml-dev.org/
[sg-puzzles]: http://mathworld.wolfram.com/Slothouber-GraatsmaPuzzle.html
[shallan-scripts]: https://github.com/radian-software/shallan-scripts
[shallan]: https://github.com/radian-software/shallan
[shannon]: https://www.flows.cv/shannoncollier
[signal]: https://signal.org/
[silhouette]: https://github.com/radian-software/silhouette
[sleeping beauty]: https://github.com/radian-software/sleeping-beauty
[smarter-playlist]: https://github.com/radian-software/smarter-playlist
[smartparens]: https://github.com/Fuco1/smartparens
[sorting algorithms]: https://en.wikipedia.org/wiki/Sorting_algorithm
[sortingalgorithms]: https://github.com/radian-software/SortingAlgorithms
[space-grid]: https://github.com/raxod502/space-grid
[squeaky hinge]: https://github.com/radian-software/squeaky-hinge
[srh]: https://tools.ietf.org/html/rfc8754
[star relic]: http://www.ifgdb.com/play/star-relic/
[static site]: https://en.wikipedia.org/wiki/Static_web_page
[steam]: https://en.wikipedia.org/wiki/Steam_(service)
[straight.el]: https://github.com/radian-software/straight.el
[students-speak]: /mental-health/students-speak
[sudoku]: https://en.wikipedia.org/wiki/Sudoku
[summit]: https://sum.bvsd.org/
[surveying trigonometry worksheet]: https://github.com/raxod502/SurveyingTrigonometryWorksheet
[swiper]: https://github.com/abo-abo/swiper#swiper
[symlinks]: https://en.wikipedia.org/wiki/Symbolic_link
[syntax tables]: https://www.gnu.org/software/emacs/manual/html_node/elisp/Syntax-Tables.html
[tabcrush]: https://github.com/radian-software/tabcrush
[tc-hn]: https://web.archive.org/web/20250107063533/https://news.ycombinator.com/item?id=15460851
[terraform]: https://en.wikipedia.org/wiki/Terraform_(software)
[terraria]: https://terraria.org/
[terrariaclone]: https://github.com/radian-software/TerrariaClone
[terrariacloneclone]: https://github.com/radian-software/TCC
[tetris-processing]: https://github.com/radian-software/tetris-processing
[tetris-python]: https://github.com/radian-software/tetris-python
[tetris]: https://en.wikipedia.org/wiki/Tetris
[the hashinator]: https://github.com/radian-software/the-hashinator
[ti-84-programs]: https://github.com/raxod502/TI84
[ti-84]: https://en.wikipedia.org/wiki/TI-84_Plus_series#TI-84_Plus_Silver_Edition
[ticketlord]: https://github.com/radian-software/ticketlord
[ticketmaster]: https://en.wikipedia.org/wiki/Ticketmaster#Criticism_and_controversies
[tidier]: https://github.com/radian-software/tidier
[tikz]: https://en.wikipedia.org/wiki/PGF/TikZ
[tinyku]: https://github.com/radian-software/tinyku
[tkinter]: https://docs.python.org/3/library/tkinter.html
[tls]: https://en.wikipedia.org/wiki/Transport_Layer_Security
[tmux]: https://tmux.github.io/
[transmission]: https://github.com/raxod502/transmission
[turing machines]: https://en.wikipedia.org/wiki/Turing_machine
[twilio]: https://en.wikipedia.org/wiki/Twilio
[ucb]: https://en.wikipedia.org/wiki/University_of_Colorado_Boulder
[unix filesystem]: https://en.wikipedia.org/wiki/Unix_filesystem
[unix philosophy]: https://en.wikipedia.org/wiki/Unix_philosophy
[unzuckify]: https://github.com/radian-software/unzuckify
[upm]: https://github.com/replit/upm
[use-package]: https://www.gnu.org/software/emacs/manual/html_mono/use-package.html
[utunes-scripts]: https://github.com/radian-software/utunes-scripts
[utunes]: https://github.com/radian-software/utunes
[veidt legacy]: https://github.com/radian-software/veidt-legacy
[veidt]: https://github.com/radian-software/veidt
[venmo auto transfer neue]: https://github.com/radian-software/venmo-auto-transfer-neue
[venmo auto transfer]: https://github.com/radian-software/venmo-auto-transfer
[venmo-auto-cashout]: https://github.com/evanpurkhiser/venmo-auto-cashout
[venmo]: https://venmo.com/
[vercel]: https://vercel.com/
[version control]: https://en.wikipedia.org/wiki/Version_control
[vertico]: https://github.com/minad/vertico
[votinglib]: https://github.com/raxod502/VotingLib
[watching paint dry]: https://github.com/raxod502/Watching-Paint-Dry
[wd]: https://github.com/mfaerevaag/wd
[wdr-slides]: https://nextcloud.intuitiveexplanations.com/s/ZzNJW26CiMFB2T4
[wdr-source]: https://github.com/raxod502/cs121-hello
[wdr]: https://link.intuitiveexplanations.com/cs121-hello
[wdx]: https://github.com/radian-software/wdx
[webcomic]: https://en.wikipedia.org/wiki/Webcomic
[whales.life-source]: https://github.com/raxod502/cs121-whales
[whales.life]: https://whales.intuitiveexplanations.com/
[widevine]: https://en.wikipedia.org/wiki/Widevine
[wind's pleasure]: https://github.com/radian-software/winds-pleasure
[with-feature]: https://github.com/radian-software/with-feature
[worm timeline reference]: https://github.com/radian-software/worm-timeline-reference
[worm]: https://en.wikipedia.org/wiki/Worm_(web_serial)
[x86-64]: https://en.wikipedia.org/wiki/X86-64
[yt-dlp]: https://github.com/yt-dlp/yt-dlp
[ytm]: https://music.youtube.com/
[zelle reverse engineering]: https://github.com/radian-software/zelle-app-notes
[zelle]: https://en.wikipedia.org/wiki/Zelle
[zsh]: http://www.zsh.org/
