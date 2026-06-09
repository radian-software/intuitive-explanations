---
title: |
  Reverse engineering the Facebook Messenger API
date: 2021-12-06
---

*Note:* The focus of this article is to explain the process of reverse
engineering, and it is not continually updated to reflect ongoing
changes in Facebook APIs. If you are looking for updated details,
consider basing your work on open-source projects like
[mautrix/meta](https://github.com/mautrix/meta), which is developed by
my employer [Beeper](https://www.beeper.com/).

I recently had occasion to reverse engineer the [Facebook
Messenger](https://www.messenger.com/) API for personal use, and
realized the case study would make a great tutorial. This blog post
lays out how I deciphered the API, and explains the reverse
engineering techniques I used, so that you can go forth and do the
same. The required background knowledge is fairly minimal.

**Remember:** Reverse engineering is ethical, pro-democratic, and
protected under US law, but you still need to exercise integrity and
responsibility when interacting with any online system. Examples of
irresponsible behavior include:

* Sending automated (or non-automated) spam to other users
* Downloading people's data without their consent
* Putting undue load on infrastructure you are not paying for

This kind of behavior is inappropriate regardless of how it is
accomplished. But when put to the right use, reverse engineering is a
way to give yourself and others greater agency, freedom, and
creativity online. For example, you could use it to develop an
alternative interface to an online system which would otherwise be
inaccessible to users with disabilities. Or you could adjust an
application to be runnable on older systems that are no longer
supported, which would benefit users who cannot afford to buy new
hardware.

**Warning:** Notwithstanding the above, Facebook loves to
automatically suspend and/or ban people who look at their API funny,
even if you aren't doing anything bad. Explore with caution.

**Table of contents**

<!-- toc -->

- [Goal](#goal)
- [Get the email and password](#get-the-email-and-password)
- [Inspect the login form](#inspect-the-login-form)
- [Replicate the login request](#replicate-the-login-request)
- [Simplify the login request](#simplify-the-login-request)
- [Track down hidden login parameters](#track-down-hidden-login-parameters)
- [Parse the HTML response](#parse-the-html-response)
- [Make the login request](#make-the-login-request)
- [Find the inbox request](#find-the-inbox-request)
- [Make the inbox request more readable](#make-the-inbox-request-more-readable)
- [Find hidden inbox query parameters](#find-hidden-inbox-query-parameters)
- [Extract the inbox query parameters](#extract-the-inbox-query-parameters)
- [Decipher the inbox data response](#decipher-the-inbox-data-response)
- [Examine the behavior of the inbox data response](#examine-the-behavior-of-the-inbox-data-response)
- [Parse the inbox data response](#parse-the-inbox-data-response)
- [Find the send-message request](#find-the-send-message-request)
- [Replicate the send-message request](#replicate-the-send-message-request)
- [Clean up the send-message request](#clean-up-the-send-message-request)
- [What next?](#what-next)

<!-- tocstop -->

## Goal

Our goal here will be to develop a command-line program called
Messyger that allows:

* Seeing your most recent conversations, and which ones have unread
  messages.
* Sending a message to a conversation.

Of course, this isn't enough for a full Messenger client, but it's
enough to show off the techniques without having too much busywork. To
practice your own skills, you could add more capabilities after
reading this post.

We'll use Python because it makes the code concise and easy to read.

The full code from this blog post is available [on
GitHub](https://github.com/raxod502/messyger).

## Get the email and password

Step 1 of using Messenger is providing your email address and password
to log in. The same will be true of Messyger:

```python
import argparse

parser = argparse.ArgumentParser("messyger")
parser.add_argument("-u", "--email", required=True)
parser.add_argument("-p", "--password", required=True)
args = parser.parse_args()

print("email:", args.email)
print("password:", args.password)
```

([Read more about
argparse](https://docs.python.org/3/library/argparse.html).)

And usage:

```
% python3 messyger.py -u camilla.woodward@protonmail.com -p 0aSPlneurgscxzpuEZb9
email: camilla.woodward@protonmail.com
password: 0aSPlneurgscxzpuEZb9
```

And before you ask, no, none of these credentials are valid. Because
Facebook banned all of the accounts for having too much suspicious
activity...

## Inspect the login form

![Messenger login UI](/assets/messenger/login-ui.png)

So what happens when we click the login button? We can find out by
opening the developer tools in Chrome (or its equivalent in other
browsers; any will suffice) and switching to the Network tab to see
the list of all HTTP requests made by the browser while loading the
page.

![Network tab on login UI](/assets/messenger/login-ui-requests.png)

When we click the login button, what we see (assuming we first check
the "Preserve log" checkbox) is a new request showing up at the bottom
of the log, to the relevant-seeming URL
`https://www.messenger.com/login/password/`.

![Login request in Network
tab](/assets/messenger/login-request-overview.png)

This is a POST request, which means that data is being submitted to
the server, which is what we expect for a request to log in. ([Read
more about HTTP request
methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods).)
If we scroll down, Chrome will show us the form data that was
submitted as part of this request, which indeed includes the email and
password:

![Form data for login request](/assets/messenger/login-form-data.png)

([Read more about form
data](https://developer.mozilla.org/en-US/docs/Learn/Forms/Sending_and_retrieving_form_data#the_post_method).)

There are also a bunch of other parameters here, so we'll have to
figure out what those mean, and if they're important. But first, we
should figure out how making this request actually results in us being
logged in.

Typically, logins are handled using cookies, so you'll provide your
username and password, and the server will give you some cookies for
the browser to store. ([Read more about
cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies).)
Then, the cookies are included in all subsequent requests, allowing
the server to verify that you have already logged in.

If we scroll up and look at the response headers, we can see that
indeed the response uses the `Set-Cookie` header to pass some cookies
back to the browser.

![Set-Cookie headers in login
response](/assets/messenger/login-cookie-headers.png)

([Read more about HTTP response
headers](https://developer.mozilla.org/en-US/docs/Glossary/Response_header).)

## Replicate the login request

Now that we've identified the request that is used to log in, we'll
want to replicate it outside of the browser, so that we have full
control over it. The goal is to take the email and password, and
exchange them for the cookies that will allow us to make subsequent
authenticated requests.

Luckily, Chrome (and other browsers) provide an easy way to do this.
You can right-click the request and extract a cURL command that will
do the same thing as the browser did, but from the command line.

![Copy as cURL right-click menu](/assets/messenger/copy-as-curl.png)

([Read more about cURL](https://curl.se/).)

Here's what that looks like:

```
% curl 'https://www.messenger.com/login/password/' \
    -H 'authority: www.messenger.com' \
    -H 'pragma: no-cache' \
    -H 'cache-control: no-cache' \
    -H 'sec-ch-ua: "Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"' \
    -H 'sec-ch-ua-mobile: ?0' \
    -H 'sec-ch-ua-platform: "Linux"' \
    -H 'origin: https://www.messenger.com' \
    -H 'upgrade-insecure-requests: 1' \
    -H 'dnt: 1' \
    -H 'content-type: application/x-www-form-urlencoded' \
    -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36' \
    -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
    -H 'sec-fetch-site: same-origin' \
    -H 'sec-fetch-mode: navigate' \
    -H 'sec-fetch-user: ?1' \
    -H 'sec-fetch-dest: document' \
    -H 'referer: https://www.messenger.com/' \
    -H 'accept-language: en-US,en;q=0.9' \
    -H 'cookie: wd=1010x980; dpr=2; datr=UqKaYf_W73hoTmwXhi8ZqzZ4' \
    --data-raw 'jazoest=2913&lsd=AVrs5S09Cjw&initial_request_id=APeMI6-a6r5592s5ETA6Zr5&timezone=480&lgndim=eyJ3IjoxOTIwLCJoIjoxMDgwLCJhdyI6MTkyMCwiYWgiOjEwNTMsImMiOjI0fQ%3D%3D&lgnrnd=114743_C4xH&lgnjs=n&email=camilla.woodward%40protonmail.com&pass=0aSPlneurgscxzpuEZb9&login=1&persistent=1&default_persistent=' \
    --compressed
```

When we run this command, we'll see that it finishes successfully but
does not print anything. This is because cURL does not print response
headers by default, and this request only returns headers (no body
content). We can [add the `-i` option to display response
headers](https://catonmat.net/cookbooks/curl/print-response-headers),
which do appear to have the cookies we were expecting:

```
HTTP/2 302
set-cookie: sb=ja6aYcS61HGuWo-I6JaD_8G3; expires=Tue, 21-Nov-2023 20:39:41 GMT; Max-Age=63072000; path=/; domain=.messenger.com; secure; httponly; SameSite=None
set-cookie: c_user=100075402451059; expires=Mon, 21-Nov-2022 20:39:40 GMT; Max-Age=31535999; path=/; domain=.messenger.com; secure; SameSite=None
set-cookie: xs=36%3Adbs1ryav8jfpEg%3A2%3A1637527181%3A-1%3A-1; expires=Mon, 21-Nov-2022 20:39:40 GMT; Max-Age=31535999; path=/; domain=.messenger.com; secure; httponly; SameSite=None
location: https://www.messenger.com/
content-security-policy-report-only: default-src https: data: wss: blob: chrome-extension: 'unsafe-inline' 'unsafe-eval';block-all-mixed-content;report-uri https://www.facebook.com/csp/reporting/?minimize=0;
content-security-policy: default-src data: blob: https://*.fbcdn.net https://*.facebook.com *.fbsbx.com *.messenger.com;script-src *.facebook.com *.fbcdn.net *.facebook.net *.google-analytics.com *.google.com 127.0.0.1:* 'unsafe-inline' 'unsafe-eval' blob: data: 'self' connect.facebook.net *.messenger.com;style-src data: blob: 'unsafe-inline' *.facebook.com *.fbcdn.net *.messenger.com;connect-src *.facebook.com facebook.com *.fbcdn.net *.facebook.net wss://*.facebook.com:* wss://*.whatsapp.com:* attachment.fbsbx.com ws://localhost:* blob: *.cdninstagram.com 'self' *.messenger.com wss://*.messenger.com www.messenger.com www.google-analytics.com wss://*.messenger.com:*;font-src *.messenger.com *.facebook.com https://*.fbcdn.net data: *.gstatic.com;img-src *.fbcdn.net https://*.facebook.com cdninstagram.com *.cdninstagram.com *.tenor.co *.tenor.com *.giphy.com data: *.fbsbx.com *.messenger.com messenger.com blob: android-webview-video-poster: *.xx.fbcdn.net https://messenger.com;media-src *.messenger.com *.facebook.com https://*.fbcdn.net data: *.fbsbx.com *.fbcdn.net *.cdninstagram.com https://*.giphy.com blob:;frame-src *.messenger.com *.facebook.com https://*.fbcdn.net data: *.fbsbx.com *.fbcdn.net *.cdninstagram.com blob: *.doubleclick.net;
report-to: {"max_age":86400,"endpoints":[{"url":"https:\/\/www.facebook.com\/browser_reporting\/?minimize=0"}],"group":"coep_report"}
x-fb-rlafr: 0
document-policy: force-load-at-top
cross-origin-resource-policy: same-origin
cross-origin-embedder-policy-report-only: require-corp;report-to="coep_report"
cross-origin-opener-policy: same-origin-allow-popups
pragma: no-cache
cache-control: private, no-cache, no-store, must-revalidate
expires: Sat, 01 Jan 2000 00:00:00 GMT
x-content-type-options: nosniff
x-xss-protection: 0
x-frame-options: DENY
access-control-expose-headers: X-FB-Debug, X-Loader-Length
access-control-allow-methods: OPTIONS
access-control-allow-credentials: true
access-control-allow-origin: https://www.messenger.com
vary: Origin
strict-transport-security: max-age=15552000; preload; includeSubDomains
content-type: text/html; charset="utf-8"
x-fb-debug: niLVdyLSHPRUwRyAzfXpDUEgukRqEdXXNZ1yK3fO1yjJG1z8FrzwfA1OMfo1QbiSxCnBZx72f1nk6HEXi44NDg==
content-length: 0
date: Sun, 21 Nov 2021 20:39:42 GMT
priority: u=3,i
alt-svc: h3=":443"; ma=3600, h3-29=":443"; ma=3600
```

However, cURL syntax is a little annoying, and I personally prefer to
use [HTTPie](https://httpie.io/) instead. Fortunately there is a nice
tool called [CurliPie](https://curlipie.open-api.vn) that converts
cURL syntax to HTTPie. That gives us this:

```
% http -f https://www.messenger.com/login/password/ \
    Authority:www.messenger.com \
    Pragma:no-cache \
    Cache-Control:no-cache \
    Sec-Ch-Ua:'"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"' \
    Sec-Ch-Ua-Mobile:'?0' \
    Sec-Ch-Ua-Platform:Linux \
    Origin:https://www.messenger.com \
    Upgrade-Insecure-Requests:1 \
    Dnt:1 \
    Content-Type:application/x-www-form-urlencoded \
    User-Agent:'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36' \
    Accept:'text/html, application/xhtml+xml, application/xml;q=0.9, image/avif, image/webp, image/apng, */*;q=0.8, application/signed-exchange;v=b3;q=0.9' \
    Sec-Fetch-Site:same-origin \
    Sec-Fetch-Mode:navigate \
    Sec-Fetch-User:'?1' \
    Sec-Fetch-Dest:document \
    Referer:https://www.messenger.com/ \
    Accept-Language:'en-US, en;q=0.9' \
    Cookie:'wd=1010x980; dpr=2; datr=UqKaYf_W73hoTmwXhi8ZqzZ4' \
    jazoest=2913 \
    lsd=AVrs5S09Cjw \
    initial_request_id=APeMI6-a6r5592s5ETA6Zr5 \
    timezone=480 \
    lgndim=eyJ3IjoxOTIwLCJoIjoxMDgwLCJhdyI6MTkyMCwiYWgiOjEwNTMsImMiOjI0fQ== \
    lgnrnd=114743_C4xH \
    lgnjs=n \
    email=camilla.woodward@protonmail.com \
    pass=0aSPlneurgscxzpuEZb9 \
    login=1 \
    persistent=1
```

Notice how now the email and password are separated out into different
arguments, instead of crammed into a big long string under
`--data-raw`.

Running the HTTPie command above shows us the headers in a nice format
by default, including (again) the cookies:

```
HTTP/1.1 302 Found
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: OPTIONS
Access-Control-Allow-Origin: https://www.messenger.com
Access-Control-Expose-Headers: X-FB-Debug, X-Loader-Length
Alt-Svc: h3=":443"; ma=3600, h3-29=":443"; ma=3600
Cache-Control: private, no-cache, no-store, must-revalidate
Connection: keep-alive
Content-Length: 0
Content-Type: text/html; charset="utf-8"
Date: Sun, 21 Nov 2021 20:56:53 GMT
Expires: Sat, 01 Jan 2000 00:00:00 GMT
Location: https://www.messenger.com/
Pragma: no-cache
Priority: u=3,i
Set-Cookie: sb=lLKaYbQYjhQ1r-tdd337y6b6; expires=Tue, 21-Nov-2023 20:56:52 GMT; Max-Age=63072000; path=/; domain=.messenger.com; secure; httponly; SameSite=None
Set-Cookie: c_user=100075402451059; expires=Mon, 21-Nov-2022 20:56:50 GMT; Max-Age=31535998; path=/; domain=.messenger.com; secure; SameSite=None
Set-Cookie: xs=36%3AxbGwJByz_Zpfag%3A2%3A1637528212%3A-1%3A-1; expires=Mon, 21-Nov-2022 20:56:50 GMT; Max-Age=31535998; path=/; domain=.messenger.com; secure; httponly; SameSite=None
Strict-Transport-Security: max-age=15552000; preload; includeSubDomains
Vary: Origin
X-Content-Type-Options: nosniff
X-FB-Debug: vR9/wct/iva6TWZRO48tsnEYT1xrMyIErMwNH0P47uFA65WrEtUiMR38CY6p8NLdT2aIh1nXbSszogNuHE6Bng==
X-Frame-Options: DENY
X-XSS-Protection: 0
content-security-policy: default-src data: blob: https://*.fbcdn.net https://*.facebook.com *.fbsbx.com *.messenger.com;script-src *.facebook.com *.fbcdn.net *.facebook.net *.google-analytics.com *.google.com 127.0.0.1:* 'unsafe-inline' 'unsafe-eval' blob: data: 'self' connect.facebook.net *.messenger.com;style-src data: blob: 'unsafe-inline' *.facebook.com *.fbcdn.net *.messenger.com;connect-src *.facebook.com facebook.com *.fbcdn.net *.facebook.net wss://*.facebook.com:* wss://*.whatsapp.com:* attachment.fbsbx.com ws://localhost:* blob: *.cdninstagram.com 'self' *.messenger.com wss://*.messenger.com www.messenger.com www.google-analytics.com wss://*.messenger.com:*;font-src *.messenger.com *.facebook.com https://*.fbcdn.net data: *.gstatic.com;img-src *.fbcdn.net https://*.facebook.com cdninstagram.com *.cdninstagram.com *.tenor.co *.tenor.com *.giphy.com data: *.fbsbx.com *.messenger.com messenger.com blob: android-webview-video-poster: *.xx.fbcdn.net https://messenger.com;media-src *.messenger.com *.facebook.com https://*.fbcdn.net data: *.fbsbx.com *.fbcdn.net *.cdninstagram.com https://*.giphy.com blob:;frame-src *.messenger.com *.facebook.com https://*.fbcdn.net data: *.fbsbx.com *.fbcdn.net *.cdninstagram.com blob: *.doubleclick.net;
content-security-policy-report-only: default-src https: data: wss: blob: chrome-extension: 'unsafe-inline' 'unsafe-eval';block-all-mixed-content;report-uri https://www.facebook.com/csp/reporting/?minimize=0;
cross-origin-embedder-policy-report-only: require-corp;report-to="coep_report"
cross-origin-opener-policy: same-origin-allow-popups
cross-origin-resource-policy: same-origin
document-policy: force-load-at-top
report-to: {"max_age":86400,"endpoints":[{"url":"https:\/\/www.facebook.com\/browser_reporting\/?minimize=0"}],"group":"coep_report"}
x-fb-rlafr: 0
```

Notice that the response says `302 Found`, and includes a `Location:
https://www.messenger.com`. This instructs the browser (after setting
the relevant cookies) to redirect the user to
`https://www.messenger.com`, where you now will see your
conversations. ([Read more about HTTP response
codes](https://httpstatuses.com/).)

## Simplify the login request

That HTTP request has a lot of parameters in it! Browsers send a lot
of headers by default, and websites will usually add on a bunch more
for good measure, but usually most of the headers (and even form
parameters) are unneeded.

Once we have a working request in HTTPie, we can strip out parameters
one at a time to see which ones are actually required. For example, if
we change the password, it stops working:

```
% http -f https://www.messenger.com/login/password/ \
    Authority:www.messenger.com \
    Pragma:no-cache \
    Cache-Control:no-cache \
    Sec-Ch-Ua:'"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"' \
    Sec-Ch-Ua-Mobile:'?0' \
    Sec-Ch-Ua-Platform:Linux \
    Origin:https://www.messenger.com \
    Upgrade-Insecure-Requests:1 \
    Dnt:1 \
    Content-Type:application/x-www-form-urlencoded \
    User-Agent:'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36' \
    Accept:'text/html, application/xhtml+xml, application/xml;q=0.9, image/avif, image/webp, image/apng, */*;q=0.8, application/signed-exchange;v=b3;q=0.9' \
    Sec-Fetch-Site:same-origin \
    Sec-Fetch-Mode:navigate \
    Sec-Fetch-User:'?1' \
    Sec-Fetch-Dest:document \
    Referer:https://www.messenger.com/ \
    Accept-Language:'en-US, en;q=0.9' \
    Cookie:'wd=1010x980; dpr=2; datr=UqKaYf_W73hoTmwXhi8ZqzZ4' \
    jazoest=2913 \
    lsd=AVrs5S09Cjw \
    initial_request_id=APeMI6-a6r5592s5ETA6Zr5 \
    timezone=480 \
    lgndim=eyJ3IjoxOTIwLCJoIjoxMDgwLCJhdyI6MTkyMCwiYWgiOjEwNTMsImMiOjI0fQ== \
    lgnrnd=114743_C4xH \
    lgnjs=n \
    email=camilla.woodward@protonmail.com \
    pass=thisiswrong \
    login=1 \
    persistent=1

HTTP/1.1 200 OK
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: OPTIONS
Access-Control-Allow-Origin: https://www.messenger.com
Access-Control-Expose-Headers: X-FB-Debug, X-Loader-Length
Alt-Svc: h3=":443"; ma=3600, h3-29=":443"; ma=3600
Cache-Control: private, no-cache, no-store, must-revalidate
Connection: keep-alive
Content-Encoding: gzip
Content-Type: text/html; charset="utf-8"
Date: Sun, 21 Nov 2021 22:33:31 GMT
Expires: Sat, 01 Jan 2000 00:00:00 GMT
Pragma: no-cache
Priority: u=3,i
Set-Cookie: sb=O8maYf6WN7nBh2pODWFo9bTa; expires=Tue, 21-Nov-2023 22:33:31 GMT; Max-Age=63072000; path=/; domain=.messenger.com; secure; httponly; SameSite=None
Strict-Transport-Security: max-age=15552000; preload; includeSubDomains
Transfer-Encoding: chunked
Vary: Origin
Vary: Accept-Encoding
X-Content-Type-Options: nosniff
X-FB-Debug: 1JwQc9JQPTRqGrUzIfY/OED6es6VSkBWrdeTj8XQ3BOF6nbEtDsuPSsQ52lfVuYvS/8Xz1BNlQadiGzFgGzisQ==
X-Frame-Options: DENY
X-XSS-Protection: 0
content-security-policy: default-src data: blob: https://*.fbcdn.net https://*.facebook.com *.fbsbx.com *.messenger.com;script-src *.facebook.com *.fbcdn.net *.facebook.net *.google-analytics.com *.google.com 127.0.0.1:* 'unsafe-inline' 'unsafe-eval' blob: data: 'self' connect.facebook.net *.messenger.com;style-src data: blob: 'unsafe-inline' *.facebook.com *.fbcdn.net *.messenger.com;connect-src *.facebook.com facebook.com *.fbcdn.net *.facebook.net wss://*.facebook.com:* wss://*.whatsapp.com:* attachment.fbsbx.com ws://localhost:* blob: *.cdninstagram.com 'self' *.messenger.com wss://*.messenger.com www.messenger.com www.google-analytics.com wss://*.messenger.com:*;font-src *.messenger.com *.facebook.com https://*.fbcdn.net data: *.gstatic.com;img-src *.fbcdn.net https://*.facebook.com cdninstagram.com *.cdninstagram.com *.tenor.co *.tenor.com *.giphy.com data: *.fbsbx.com *.messenger.com messenger.com blob: android-webview-video-poster: *.xx.fbcdn.net https://messenger.com;media-src *.messenger.com *.facebook.com https://*.fbcdn.net data: *.fbsbx.com *.fbcdn.net *.cdninstagram.com https://*.giphy.com blob:;frame-src *.messenger.com *.facebook.com https://*.fbcdn.net data: *.fbsbx.com *.fbcdn.net *.cdninstagram.com blob: *.doubleclick.net;
content-security-policy-report-only: default-src https: data: wss: blob: chrome-extension: 'unsafe-inline' 'unsafe-eval';block-all-mixed-content;report-uri https://www.facebook.com/csp/reporting/?minimize=0;
cross-origin-embedder-policy-report-only: require-corp;report-to="coep_report"
cross-origin-opener-policy: same-origin-allow-popups
cross-origin-resource-policy: same-origin
document-policy: force-load-at-top
report-to: {"max_age":86400,"endpoints":[{"url":"https:\/\/www.facebook.com\/browser_reporting\/?minimize=0"}],"group":"coep_report"}
x-fb-rlafr: 0

<!DOCTYPE html>
<html lang="en" id="facebook" class="no_js">
... a bunch of HTML ...
```

Notice how we now get a `200 OK` response instead of `302 Found`, and
the `c_user` and `xs` cookies aren't getting set anymore, which means
our login attempt is failing. (We might expect to see `401
Unauthorized` or `403 Forbidden` instead of `200 OK` for a failed
login attempt, but servers don't always return the most sensible
status codes.)

If we go through removing each parameter that can be removed without
losing the cookies, then this is what we end up with:

```
% http -f https://www.messenger.com/login/password/ \
    Cookie:'datr=UqKaYf_W73hoTmwXhi8ZqzZ4' \
    lsd=AVrs5S09Cjw \
    initial_request_id=APeMI6-a6r5592s5ETA6Zr5 \
    email=camilla.woodward@protonmail.com \
    pass=0aSPlneurgscxzpuEZb9
```

## Track down hidden login parameters

We've now simplified the login command a lot, but what are these
`datr`, `lsd`, and `initial_request_id` values? In general, when
seeing parameters like these in outgoing requests, there are three
possibilities:

1. The client got the value from the server on a previous request, and
   is just sending it back.
2. The client is generating the value from scratch (e.g. based on the
   current timestamp, or a random number generator).
3. Some combination of the two (the client gets a value from the
   server and then modifies it in some way before sending it back).

A lot of reverse engineering is making educated guesses and seeing if
they pan out. Let's make a guess that case (1) is what's happening
here. This seems especially likely because `initial_request_id` sounds
like it is referring to a previous request. There's really only one
significant request that happens before the login request, which is
the initial HTML page containing the login form. So, a natural place
to start is to take a look at that page to see if it has anything that
looks relevant.

To do so, we can open a new private browsing window and load up
Messenger again. Then, we can go to the Sources tab to see the HTML
that is being used to display the current page. (You might need to
reload the page if you loaded it before opening the developer tools.)

![Source tab for login form](/assets/messenger/login-form-source.png)

Fortunately, Chrome (as with other browsers) has a neat feature where
they can reformat code in the Sources tab to be easier to read. (If
there isn't a popup telling you about it, it's the button labeled `{}`
in the lower-left of the text pane.)

In the reformatted HTML, if we search for `initial_request_id`, check
out what we find:

![Search results for initial\_request\_id in login form
source](/assets/messenger/initial-request-id-search.png)

Not only is there a suspicious-looking value for `initial_request_id`
included in the HTML (`AovnGK3QdvNgThxCxYXmSDz`), but just a little
above it is a value for `lsd` (`AVpERbgkGxw`)! If we refresh the page,
we'll find that these values change every time. Since the values are
included as `<input>` tags in the `<form>` for the login button,
they'll automatically get submitted along with the email address and
password, just like we saw in the Network tab earlier.

Elsewhere in the page is a value for `datr`
(`a26cYYDoj0oHu9oca8jmB8W6`):

![Search results for datr in login form
source](/assets/messenger/datr-search.png)

If we want to confirm these values are used the way we think, we can
click the login button and see that the values in the POST request
match up as expected:

![Form data matching up with parameters extracted from
HTML](/assets/messenger/initial-request-id-form-data.png)

There's a little gotcha that I ran into the first time I investigated
this. If you reload the page before logging in, mysteriously the
`datr` value goes away from the HTML! Correspondingly, by switching to
the Application tab and selecting `https://www.messenger.com` under
Cookies, you can see that there are no cookies the first time we load
the page:

![No cookies set before
reloading](/assets/messenger/cookies-empty.png)

But then after we reload... suddenly, cookies!

![Cookies set after
reloading](/assets/messenger/cookies-populated.png)

This is particularly tricky because you wouldn't expect the HTML
response to magically change just by reloading the page. If I had to
guess, there's some JavaScript on the frontend that detects when
you're about to leave the page (e.g. by reloading), and sets the
`datr` cookie. Then, that cookie value is automatically included in
the new request, which causes the server to modify the HTML to no
longer include a `js_datr` value for some reason.

## Parse the HTML response

Okay, now we know how to log in to Messenger:

1. Fetch the HTML page at `https://www.messenger.com`
2. Extract values for `initial_request_id`, `lsd`, and `datr` from
   various places in the HTML
3. Make a POST request to `https://www.messenger.com/login/password/`
   with those values alongside the email address and password
4. Extract the `xs`, `sb`, and `c_user` cookies from the response
   headers

Let's finally get back to Messyger and implement these steps. We'll
use the [Requests](https://docs.python-requests.org/en/latest/)
library to simplify our HTTP requests.

Step 1 is fairly easy with Requests. We make a request, check that
there was no error, and then get the HTML text:

```python
import requests

html_resp = requests.get("https://www.messenger.com")
html_resp.raise_for_status()
html_page = html_resp.text

print(html_page)
```

For step 2, we'll want to start by looking in the raw HTML that we
just printed to see where the values are located that we want to
extract. Let's start with `initial_request_id`:

```html
<input type="hidden" autocomplete="off" id="initial_request_id" name="initial_request_id" value="AS49ZKW_DYimevm1SD-qQ9Q" />
```

The part that we really care about is
`value="AS49ZKW_DYimevm1SD-qQ9Q"`. However, the text `value=` shows up
a lot of times in the HTML, so we also need the preceding
`name="initial_request_id"` to be sure we're looking at the right
value.

Now that we know what we're looking for (i.e. something like
`name="initial_request_id" value="AS49ZKW_DYimevm1SD-qQ9Q"`), we can
write a [regular expression](https://www.regular-expressions.info/) to
search for this pattern. That looks like this:

```python
import re

initial_request_id = re.search(
    r'name="initial_request_id" value="([^"]+)"',
    html_page
).group(1)

print(initial_request_id)
```

([Read more about the Python `re`
module](https://docs.python.org/3/library/re.html).)

In this regular expression, `[^"]` stands for any character other than
a double quote, `+` means one or more, and the parentheses create a
sub-expression whose value can be returned by calling the `.group()`
method.

The `lsd` parameter occurs in HTML that looks like this:

```html
<input type="hidden" name="lsd" value="AVosEZyGrXU" autocomplete="off" />
```

We can write a similar regular expression to extract its value:

```python
lsd = re.search(
    r'name="lsd" value="([^"]+)"',
    html_page
).group(1)

print(lsd)
```

The `datr` parameter looks a bit different:

```javascript
["_js_datr","-nacYQnDcFLPM5Sc66w7KQKG",63072000000,"/",true]
```

However, it's not too much more difficult to extract it:

```python
datr = re.search(
    r'"_js_datr","([^"]+)"',
    html_page
).group(1)

print(datr)
```

## Make the login request

Now that we have all the necessary parameters, we can use the Requests
module to actually perform the login request to Messenger. As a
reminder, the login request using HTTPie looks like this:

```
% http -f https://www.messenger.com/login/password/ \
    Cookie:'datr=UqKaYf_W73hoTmwXhi8ZqzZ4' \
    lsd=AVrs5S09Cjw \
    initial_request_id=APeMI6-a6r5592s5ETA6Zr5 \
    email=camilla.woodward@protonmail.com \
    pass=0aSPlneurgscxzpuEZb9
```

We can replicate it in Python like so:

```python
login = requests.post(
    "https://www.messenger.com/login/password/",
    cookies={"datr": datr},
    data={
        "lsd": lsd,
        "initial_request_id": initial_request_id,
        "email": args.email,
        "pass": args.password
    },
    allow_redirects=False  # do not follow 302
)
assert login.status_code == 302

print(login.cookies)
```

(The `.cookies` property in a Requests response contains the values
that were set by the `Set-Cookie` headers in the response.)

And here's what we get from running the whole script so far:

```
% python3 messyger.py -u camilla.woodward@protonmail.com -p 0aSPlneurgscxzpuEZb9
{'c_user': '100075402451059', 'sb': 'yXmcYTct5V-EAvEuXfPrArCj', 'xs': '49%3AZuqoxpqqnfwF_A%3A2%3A1637644745%3A-1%3A-1'}
```

Success!

## Find the inbox request

Now that we've logged in, we should be able to fetch data about our
Messenger account. We'll start by trying to get the information shown
in the left-hand side of the Messenger interface: your list of
conversations.

![Requests after logging in](/assets/messenger/logged-in-requests.png)

Since Messenger is a highly interactive application, it's pretty
unlikely for it to send that information encoded as raw HTML (although
we could check by searching for a string like `Hi Camilla` in the HTML
response). Rather, it's more likely that the information will be
fetched asynchronously via JavaScript. For various historical reasons,
this is called an XHR request, where XHR stands for XMLHttpRequest
despite having nothing to do with XML. ([Read more about the different
types of asynchronous requests in
JavaScript](https://archive.is/y48hO).) We can filter for XHR requests
in the Network tab:

![XHR requests in Network
inspector](/assets/messenger/xhr-requests.png)

However, there are a bunch of them, so it would be a pain to look at
each one and try to figure out if it has the data we're looking for.
To deal with this problem, we can download all the request and
response data as an HTTP Archive (HAR), so that we can search through
them all at the same time:

![Right-click menu for "Save all as HAR with
content"](/assets/messenger/save-as-har.png)

The HAR format is actually just JSON, so we can use a tool like
[jq](https://stedolan.github.io/jq/) to search through it. First we'll
check the list of all the URLs that the browser made requests to:

```
% cat inbox-requests.har | jq '.log.entries | map(.request.url)'
[
  "https://www.messenger.com/login/password/",
  "https://www.messenger.com/",
  "https://www.messenger.com/t/100007424414992/",
  ... a bunch more URLs ...
  "https://www.messenger.com/ajax/bnzai?__a=1&__ccg=EXCELLENT&__comet_req=1&__hs=18957.HYP%3Amessengerdotcom_comet_pkg.2.1.0.0.&__hsi=0-0&__jssesw=1&__req=g&__rev=1004771992&__s=lryd0q%3Amohw6t%3Axnxaps&__spin_b=trunk&__spin_r=1004771992&__spin_t=1637886944&__user=100075402451059&dpr=2&fb_dtsg=AQE4bjFlv-4P3Xs%3A50%3A1637886942&jazoest=21949&lsd=M237eS5ouvAFHBqYl3StT7&ph=C3",
  "https://www.messenger.com/ajax/webstorage/process_keys/?state=0",
  "https://www.messenger.com/ajax/webstorage/process_keys/?state=0"
]
```

([Read more about how to use
jq](https://earthly.dev/blog/jq-select/).)

The jq command above is equivalent to the following Python code, and
you could do it this way too, if it feels more comfortable:

```python
import json
with open("inbox-requests.har") as f:
    requests = json.load(f)

urls = []
for entry in requests["log"]["entries"]:
    urls.append(entry["request"]["url"])

print(json.dumps(urls, indent=2))
```

([Read more about the Python `json`
module](https://docs.python.org/3/library/json.html).)

However, I like jq because once you learn how to use it, it's a lot
faster than writing Python or searching through JSON by hand.

Now, rather than printing every URL, let's print only the ones whose
responses contained the string `Hi Camilla`. This should allow us to
identify which ones have the data that shows up in the sidebar:

```
% cat inbox-requests.har \
    | jq '.log.entries
            | map(select(.response.content.text | .?
                           | contains("Hi Camilla"))
                    | .request.url)'
[
  "https://www.messenger.com/api/graphql/"
]
```

Or equivalently:

```python
urls = []
for entry in requests["log"]["entries"]:
    try:
        if "Hi Camilla" in entry["response"]["content"]["text"]:
            urls.append(entry["request"]["url"])
    except KeyError:  # ignoring missing keys is ".?" in jq
        continue

print(json.dumps(urls, indent=2))
```

Great! There's a request to `https://www.messenger.com/api/graphql/`
that returns the data we want. Unfortunately, the HAR download doesn't
have a convenient "Copy as cURL" option, so we'll go back to the
browser to do that.

The main tricky bit is there are actually a bunch of different
requests to this same endpoint, and we need to know which one to copy.
I'm sure there are plenty of smart ways to get around this, but I just
did it the straightforward way by printing out the requests that came
before and after it, so I could match them up visually.

```python
% cat inbox-requests.har \
    | jq '.log.entries
            | map({ url: .request.url,
                    hasMyData: (.response.content.text | .?
                                  | contains("Hi Camilla"))})'
... bunch of requests ...
  {
    "url": "https://static.xx.fbcdn.net/rsrc.php/v3/yy/r/DeeNYB34aTG.js?_nc_x=0OMkmbJTxss",
    "hasMyData": false
  },
  {
    "url": "https://static.xx.fbcdn.net/rsrc.php/ym/r/YQbyhl59TWY.ico",
    "hasMyData": false
  },
  {
    "url": "https://www.messenger.com/api/graphql/",
    "hasMyData": true
  },
  {
    "url": "https://www.messenger.com/api/graphql/",
    "hasMyData": false
  },
  {
    "url": "https://www.messenger.com/ajax/bootloader-endpoint/?modules=TransportSelectingClientSingleton%2CRequestStreamCommonRequestStreamCommonTypes&__user=100075402451059&__a=1&__dyn=7AzHJ16U9ob8ng569yaxG4VuC0BVU98nwgU7SbGbwSwAyUcoeU5W2Sawba1DwUx60GE3Qwb-q7oc81xoswMwto886C1nzUO0n2US2G3i0Boy1PwBgK7o6C0Mo5W3S1lwlE-Uqw8y4UaEW0D8qBwJK5Umxm5o7GmdUlwhEe88o5i7-2K0_UbpEbUGdG0HE5d0&__csr=gacABdkJnqAlZjhsGiaCOR5PrKBrfh7KJd9qzbl5iKQJlQqQ_K8HBl6HJCzayXDyqiBHw75w5Iw3M40ju0578b81v81DFFQ9Ew0z-0MUeo4O0w9E1589ro3ew5TyU-3Sq0FFEymS2B0to2Lw1c2bw2t85W0B80jfw3ZU0wa0mq0vO0hi08uw8Grw3WE0we0hG054o4Yw4qh4xKex11WE2SWw3Eo0Pi0Yk0v-0WU0BG0fIGiq0mp1Slock2uey9d9wAwl8O19gtwhUx0Dwywj8W3-7Gjzp87Op2r80OpXz8qwhoC22l4xu448U4-4Uuwd279FU6-1owe62qywg8S1ew3dU4a5U3Awaa16xS0CQ9xO5t1O7XgoxSuE622e0F83ww6-wNwposw7uwae1oy9cBe0lu1zAG2e6o7S1gwWwZwn8aUoxeimFrxR6w5GwNyo0xO8w6zxu1awj8kw45wXw4im0wU2sxi3ulrw9-U1HUWuq514R0bi0ru581UA2m0d5woE2nwrpE1qAby4-iAldi2qm0hS16ge85G3K2q0nml06Vw8p02Pu2S0t20boway&__req=3&__hs=18957.HYP%3Amessengerdotcom_comet_pkg.2.1.0.0.&dpr=2&__ccg=EXCELLENT&__rev=1004771992&__s=lryd0q%3Amohw6t%3Axnxaps&__hsi=0-0&__comet_req=1&fb_dtsg_ag=AQyUiaFmn4dTZRTOD6xvQejSbiWCOkwF_hArsm6-mgIByBR7%3A50%3A1637886942&jazoest=25004&__spin_r=1004771992&__spin_b=trunk&__spin_t=1637886944&__jssesw=1",
    "hasMyData": false
  },
... bunch of requests ...
```

Then it was just a matter of finding the corresponding place in the
browser Network tab (note that the Network tab only shows the last bit
of each URL, after the last or second-to-last slash):

![Copying the login request as
cURL](/assets/messenger/copy-inbox-request.png)

That gives us this:

```
% curl 'https://www.messenger.com/api/graphql/' \
    -H 'authority: www.messenger.com' \
    -H 'pragma: no-cache' \
    -H 'cache-control: no-cache' \
    -H 'sec-ch-ua: "Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"' \
    -H 'dnt: 1' \
    -H 'sec-ch-ua-mobile: ?0' \
    -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36' \
    -H 'x-fb-friendly-name: LSPlatformGraphQLLightspeedRequestQuery' \
    -H 'x-fb-lsd: M237eS5ouvAFHBqYl3StT7' \
    -H 'content-type: application/x-www-form-urlencoded' \
    -H 'sec-ch-ua-platform: "Linux"' \
    -H 'accept: */*' \
    -H 'origin: https://www.messenger.com' \
    -H 'sec-fetch-site: same-origin' \
    -H 'sec-fetch-mode: cors' \
    -H 'sec-fetch-dest: empty' \
    -H 'referer: https://www.messenger.com/t/100007424414992/' \
    -H 'accept-language: en-US,en;q=0.9' \
    -H 'cookie: wd=1074x980; dpr=2; datr=0SugYWovp6j2RMqGVQqOqQwr; sb=3iugYaVtLi-qyDF0VndcCAKs; c_user=100075402451059; xs=50%3Aq86l0PoxUG0qew%3A2%3A1637886942%3A-1%3A-1' \
    --data-raw 'av=100075402451059&__user=100075402451059&__a=1&__dyn=7AzHJ16U9ob8ng569yaxG4VuC0BVU98nwgU7SbGbwSwAyUcoeU5W2Sawba1DwUx60GE3Qwb-q7oc81xoswMwto886C1nzUO0n2US2G3i0Boy1PwBgK7o6C0Mo5W3S1lwlE-Uqw8y4UaEW0D8qBwJK5Umxm5o7GmdUlwhEe88o5i7-2K0_UbpEbUGdG0HE5d0&__csr=gacABdkJnqAlZjhsGiaCOR5PrKBrfh7KJd9qzbl5iKQJlQqQ_K8HBl6HJCzayXDyqiBHw75w5Iw3M40ju0578b81v81DFFQ9Ew0z-0MUeo4O0w9E1589ro3ew5TyU-3Sq0FFEymS2B0to2Lw1c2bw2t85W0B80jfw3ZU0wa0mq0vO0hi08uw8Grw3WE0we0hG054o4Yw4qh4xKex11WE2SWw3Eo0Pi0Yk0v-0WU0BG0fIGiq0mp1Slock2uey9d9wAwl8O19gtwhUx0Dwywj8W3-7Gjzp87Op2r80OpXz8qwhoC22l4xu448U4-4Uuwd279FU6-1owe62qywg8S1ew3dU4a5U3Awaa16xS0CQ9xO5t1O7XgoxSuE622e0F83ww6-wNwposw7uwae1oy9cBe0lu1zAG2e6o7S1gwWwZwn8aUoxeimFrxR6w5GwNyo0xO8w6zxu1awj8kw45wXw4im0wU2sxi3ulrw9-U1HUWuq514R0bi0ru581UA2m0d5woE2nwrpE1qAby4-iAldi2qm0hS16ge85G3K2q0nml06Vw8p02Pu2S0t20boway&__req=1&__hs=18957.HYP%3Amessengerdotcom_comet_pkg.2.1.0.0.&dpr=2&__ccg=EXCELLENT&__rev=1004771992&__s=lryd0q%3Amohw6t%3Axnxaps&__hsi=0-0&__comet_req=1&fb_dtsg=AQE4bjFlv-4P3Xs%3A50%3A1637886942&jazoest=21949&lsd=M237eS5ouvAFHBqYl3StT7&__spin_r=1004771992&__spin_b=trunk&__spin_t=1637886944&__jssesw=1&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=LSPlatformGraphQLLightspeedRequestQuery&variables=%7B%22deviceId%22%3A%226a9252cb-2145-4f81-9d69-1834b84ba614%22%2C%22requestId%22%3A0%2C%22requestPayload%22%3A%22%7B%5C%22database%5C%22%3A1%2C%5C%22version%5C%22%3A4680497022042598%2C%5C%22sync_params%5C%22%3A%5C%22%7B%5C%5C%5C%22scale%5C%5C%5C%22%3A1%2C%5C%5C%5C%22preview_height%5C%5C%5C%22%3A200%2C%5C%5C%5C%22preview_width%5C%5C%5C%22%3A150%2C%5C%5C%5C%22preview_height_large%5C%5C%5C%22%3A400%2C%5C%5C%5C%22preview_width_large%5C%5C%5C%22%3A300%2C%5C%5C%5C%22full_height%5C%5C%5C%22%3A200%2C%5C%5C%5C%22snapshot_num_threads_per_page%5C%5C%5C%22%3A15%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%7D%5C%22%2C%5C%22epoch_id%5C%22%3A0%2C%5C%22last_applied_cursor%5C%22%3Anull%7D%22%2C%22requestType%22%3A1%7D&server_timestamps=true&doc_id=4476599072415612' \
    --compressed
```

If we run that cURL command and search in the output (for example, by
putting `| grep -o "Hi Camilla"` on the end; [read more about grep
options](https://vishnuch.tech/grep-cheatsheet)), we can see that the
response does indeed have the data we're looking for.

## Make the inbox request more readable

Although the cURL command works, that `--data-raw` parameter is
absolutely disgusting, so let's convert it to HTTPie syntax using
[CurliPie](https://curlipie.open-api.vn):

```
% http -f https://www.messenger.com/api/graphql/ \
    Authority:www.messenger.com \
    Pragma:no-cache \
    Cache-Control:no-cache \
    Sec-Ch-Ua:'"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"' \
    Dnt:1 \
    Sec-Ch-Ua-Mobile:'?0' \
    User-Agent:'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36' \
    X-Fb-Friendly-Name:LSPlatformGraphQLLightspeedRequestQuery \
    X-Fb-Lsd:M237eS5ouvAFHBqYl3StT7 \
    Content-Type:application/x-www-form-urlencoded \
    Sec-Ch-Ua-Platform:Linux \
    Accept:'*/*' \
    Origin:https://www.messenger.com \
    Sec-Fetch-Site:same-origin \
    Sec-Fetch-Mode:cors \
    Sec-Fetch-Dest:empty \
    Referer:https://www.messenger.com/t/100007424414992/ \
    Accept-Language:'en-US, en;q=0.9' \
    Cookie:'wd=1074x980; dpr=2; datr=0SugYWovp6j2RMqGVQqOqQwr; sb=3iugYaVtLi-qyDF0VndcCAKs; c_user=100075402451059; xs=50%3Aq86l0PoxUG0qew%3A2%3A1637886942%3A-1%3A-1' \
    av=100075402451059 \
    __user=100075402451059 \
    __a=1 \
    __dyn=7AzHJ16U9ob8ng569yaxG4VuC0BVU98nwgU7SbGbwSwAyUcoeU5W2Sawba1DwUx60GE3Qwb-q7oc81xoswMwto886C1nzUO0n2US2G3i0Boy1PwBgK7o6C0Mo5W3S1lwlE-Uqw8y4UaEW0D8qBwJK5Umxm5o7GmdUlwhEe88o5i7-2K0_UbpEbUGdG0HE5d0 \
    __csr=gacABdkJnqAlZjhsGiaCOR5PrKBrfh7KJd9qzbl5iKQJlQqQ_K8HBl6HJCzayXDyqiBHw75w5Iw3M40ju0578b81v81DFFQ9Ew0z-0MUeo4O0w9E1589ro3ew5TyU-3Sq0FFEymS2B0to2Lw1c2bw2t85W0B80jfw3ZU0wa0mq0vO0hi08uw8Grw3WE0we0hG054o4Yw4qh4xKex11WE2SWw3Eo0Pi0Yk0v-0WU0BG0fIGiq0mp1Slock2uey9d9wAwl8O19gtwhUx0Dwywj8W3-7Gjzp87Op2r80OpXz8qwhoC22l4xu448U4-4Uuwd279FU6-1owe62qywg8S1ew3dU4a5U3Awaa16xS0CQ9xO5t1O7XgoxSuE622e0F83ww6-wNwposw7uwae1oy9cBe0lu1zAG2e6o7S1gwWwZwn8aUoxeimFrxR6w5GwNyo0xO8w6zxu1awj8kw45wXw4im0wU2sxi3ulrw9-U1HUWuq514R0bi0ru581UA2m0d5woE2nwrpE1qAby4-iAldi2qm0hS16ge85G3K2q0nml06Vw8p02Pu2S0t20boway \
    __req=1 \
    __hs=18957.HYP:messengerdotcom_comet_pkg.2.1.0.0. \
    dpr=2 \
    __ccg=EXCELLENT \
    __rev=1004771992 \
    __s=lryd0q:mohw6t:xnxaps \
    __hsi=0-0 \
    __comet_req=1 \
    fb_dtsg=AQE4bjFlv-4P3Xs:50:1637886942 \
    jazoest=21949 \
    lsd=M237eS5ouvAFHBqYl3StT7 \
    __spin_r=1004771992 \
    __spin_b=trunk \
    __spin_t=1637886944 \
    __jssesw=1 \
    fb_api_caller_class=RelayModern \
    fb_api_req_friendly_name=LSPlatformGraphQLLightspeedRequestQuery \
    variables='{"deviceId":"6a9252cb-2145-4f81-9d69-1834b84ba614","requestId":0,"requestPayload":"{\"database\":1,\"version\":4680497022042598,\"sync_params\":\"{\\\"scale\\\":1,\\\"preview_height\\\":200,\\\"preview_width\\\":150,\\\"preview_height_large\\\":400,\\\"preview_width_large\\\":300,\\\"full_height\\\":200,\\\"snapshot_num_threads_per_page\\\":15,\\\"locale\\\":\\\"en_US\\\"}\",\"epoch_id\":0,\"last_applied_cursor\":null}","requestType":1}' \
    server_timestamps=true \
    doc_id=4476599072415612
```

Now if we run this command, we'll actually see that it produces a
*different* result than the cURL one, which shouldn't happen! Namely:

```
{
    "data": {
        "viewer": {
            "lightspeed_web_request": null
        }
    },
    "errors": [
        {
            "message": "A server error missing_required_variable_value occured. Check server logs for details.",
            "severity": "WARNING"
        },
... a bunch more scary text ...
```

Well, we can't check the server logs, but presumably something about
the conversion from cURL to HTTPie messed up the request. How can we
debug things when something like this happens?

Well, one way is to use a service like [httpbin](https://httpbin.org/)
to check what requests your tools are *actually* sending out to the
internet. Here's an example of sending ostensibly the same request to
httpbin using cURL and HTTPie, and seeing that the two requests were
actually not quite identical (e.g., the `User-Agent` header was
different):

```
% curl https://httpbin.org/post \
       -H 'example-header: foobar' \
       --data-raw 'param1=baz&param2=quux'
{
  "args": {},
  "data": "",
  "files": {},
  "form": {
    "param1": "baz",
    "param2": "quux"
  },
  "headers": {
    "Accept": "*/*",
    "Content-Length": "22",
    "Content-Type": "application/x-www-form-urlencoded",
    "Example-Header": "foobar",
    "Host": "httpbin.org",
    "User-Agent": "curl/7.74.0",
    "X-Amzn-Trace-Id": "Root=1-61a036e4-21a4901c0f5a2bc9091cab5a"
  },
  "json": null,
  "origin": "67.180.179.80",
  "url": "https://httpbin.org/post"
}

% http -f https://httpbin.org/post \
    example-header:foobar \
    param1=baz \
    param2=quux
{
    "args": {},
    "data": "",
    "files": {},
    "form": {
        "param1": "baz",
        "param2": "quux"
    },
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": "22",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Example-Header": "foobar",
        "Host": "httpbin.org",
        "User-Agent": "HTTPie/2.2.0",
        "X-Amzn-Trace-Id": "Root=1-61a03726-478a4c12219627695c0d62e9"
    },
    "json": null,
    "origin": "67.180.179.80",
    "url": "https://httpbin.org/post"
}
```

By replacing `https://www.messenger.com/api/graphql/` with
`https://httpbin.org/post` in our cURL and HTTPie commands above, then
carefully comparing the output (maybe with the aid of a command like
`git diff --no-index` to highlight differences between two files;
[read more about `git diff
--no-index`](https://stackoverflow.com/a/17194704)), we can find out
that HTTPie is doing something peculiar to the backslashes in the
`variables=` argument. Here's a simpler example to show the behavior:

```
% curl -s https://httpbin.org/post \
       --data-urlencode backslashes='\\\\' \
    | jq .form.backslashes -r
\\\\

% http -f https://httpbin.org/post \
          backslashes='\\\\' \
    | jq .form.backslashes -r
\\
```

(Using `-r` tells jq to print the value as a raw string, instead of as
a JSON string with quotes. Using `--data-urlencode` instead of
`--data-raw` means we don't have to worry about [URL
encoding](https://en.wikipedia.org/wiki/Percent-encoding) ourselves.
Using `-s` prevents cURL from printing out a progress bar.)

With cURL, it's four backslashes in, four backslashes out. But with
HTTPie, it's four backslashes in, *only two backslashes out*! Why?
Well, if we Google, we end up finding [this GitHub
issue](https://github.com/httpie/cli/issues/654#issuecomment-367301035)
that mentions HTTPie allows the use of backslash-escaping in form
parameters. This feature has the implication that if you *actually*
want to include a backslash in your form parameters, you need to
double it (use two backslashes instead of one). Indeed:

```
% http -f https://httpbin.org/post \
          backslashes='\\\\\\\\' \
    | jq .form.backslashes -r
\\\\
```

So, if we double every backslash in the request, we end up with a
*working* HTTPie command line to fetch our inbox data:

```
% http -f https://www.messenger.com/api/graphql/ \
    Authority:www.messenger.com \
    Pragma:no-cache \
    Cache-Control:no-cache \
    Sec-Ch-Ua:'"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"' \
    Dnt:1 \
    Sec-Ch-Ua-Mobile:'?0' \
    User-Agent:'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36' \
    X-Fb-Friendly-Name:LSPlatformGraphQLLightspeedRequestQuery \
    X-Fb-Lsd:M237eS5ouvAFHBqYl3StT7 \
    Content-Type:application/x-www-form-urlencoded \
    Sec-Ch-Ua-Platform:Linux \
    Accept:'*/*' \
    Origin:https://www.messenger.com \
    Sec-Fetch-Site:same-origin \
    Sec-Fetch-Mode:cors \
    Sec-Fetch-Dest:empty \
    Referer:https://www.messenger.com/t/100007424414992/ \
    Accept-Language:'en-US, en;q=0.9' \
    Cookie:'wd=1074x980; dpr=2; datr=0SugYWovp6j2RMqGVQqOqQwr; sb=3iugYaVtLi-qyDF0VndcCAKs; c_user=100075402451059; xs=50%3Aq86l0PoxUG0qew%3A2%3A1637886942%3A-1%3A-1' \
    av=100075402451059 \
    __user=100075402451059 \
    __a=1 \
    __dyn=7AzHJ16U9ob8ng569yaxG4VuC0BVU98nwgU7SbGbwSwAyUcoeU5W2Sawba1DwUx60GE3Qwb-q7oc81xoswMwto886C1nzUO0n2US2G3i0Boy1PwBgK7o6C0Mo5W3S1lwlE-Uqw8y4UaEW0D8qBwJK5Umxm5o7GmdUlwhEe88o5i7-2K0_UbpEbUGdG0HE5d0 \
    __csr=gacABdkJnqAlZjhsGiaCOR5PrKBrfh7KJd9qzbl5iKQJlQqQ_K8HBl6HJCzayXDyqiBHw75w5Iw3M40ju0578b81v81DFFQ9Ew0z-0MUeo4O0w9E1589ro3ew5TyU-3Sq0FFEymS2B0to2Lw1c2bw2t85W0B80jfw3ZU0wa0mq0vO0hi08uw8Grw3WE0we0hG054o4Yw4qh4xKex11WE2SWw3Eo0Pi0Yk0v-0WU0BG0fIGiq0mp1Slock2uey9d9wAwl8O19gtwhUx0Dwywj8W3-7Gjzp87Op2r80OpXz8qwhoC22l4xu448U4-4Uuwd279FU6-1owe62qywg8S1ew3dU4a5U3Awaa16xS0CQ9xO5t1O7XgoxSuE622e0F83ww6-wNwposw7uwae1oy9cBe0lu1zAG2e6o7S1gwWwZwn8aUoxeimFrxR6w5GwNyo0xO8w6zxu1awj8kw45wXw4im0wU2sxi3ulrw9-U1HUWuq514R0bi0ru581UA2m0d5woE2nwrpE1qAby4-iAldi2qm0hS16ge85G3K2q0nml06Vw8p02Pu2S0t20boway \
    __req=1 \
    __hs=18957.HYP:messengerdotcom_comet_pkg.2.1.0.0. \
    dpr=2 \
    __ccg=EXCELLENT \
    __rev=1004771992 \
    __s=lryd0q:mohw6t:xnxaps \
    __hsi=0-0 \
    __comet_req=1 \
    fb_dtsg=AQE4bjFlv-4P3Xs:50:1637886942 \
    jazoest=21949 \
    lsd=M237eS5ouvAFHBqYl3StT7 \
    __spin_r=1004771992 \
    __spin_b=trunk \
    __spin_t=1637886944 \
    __jssesw=1 \
    fb_api_caller_class=RelayModern \
    fb_api_req_friendly_name=LSPlatformGraphQLLightspeedRequestQuery \
    variables='{"deviceId":"6a9252cb-2145-4f81-9d69-1834b84ba614","requestId":0,"requestPayload":"{\\"database\\":1,\\"version\\":4680497022042598,\\"sync_params\\":\\"{\\\\\\"scale\\\\\\":1,\\\\\\"preview_height\\\\\\":200,\\\\\\"preview_width\\\\\\":150,\\\\\\"preview_height_large\\\\\\":400,\\\\\\"preview_width_large\\\\\\":300,\\\\\\"full_height\\\\\\":200,\\\\\\"snapshot_num_threads_per_page\\\\\\":15,\\\\\\"locale\\\\\\":\\\\\\"en_US\\\\\\"}\\",\\"epoch_id\\":0,\\"last_applied_cursor\\":null}","requestType":1}' \
    server_timestamps=true \
    doc_id=4476599072415612
```

And with this in hand, we can pare out unneeded data and parameters to
arrive at the following minimal request that gets us what we want:

```
% http -f https://www.messenger.com/api/graphql/ \
    Cookie:'c_user=100075402451059; xs=50%3Aq86l0PoxUG0qew%3A2%3A1637886942%3A-1%3A-1' \
    fb_dtsg=AQE4bjFlv-4P3Xs:50:1637886942 \
    doc_id=4476599072415612 \
    variables='{"deviceId":"6a9252cb-2145-4f81-9d69-1834b84ba614","requestId":0,"requestPayload":"{\\"database\\":1,\\"version\\":4680497022042598,\\"sync_params\\":\\"{}\\"}","requestType":1}'
```

Lovely!

## Find hidden inbox query parameters

So now we have the request we need to make. However, once again we
have a bunch of parameters whose values seem inscrutable:

* `fb_dtsg` (`AQE4bjFlv-4P3Xs:50:1637886942`)
* `doc_id` (`4476599072415612`)
* `deviceId` (`6a9252cb-2145-4f81-9d69-1834b84ba614`)
* `version` (`4680497022042598`)

We'll start, arbitrarily, with `fb_dtsg`. Since we have the whole HAR
in one place, we know we don't have to worry about the value of the
parameter changing out from under us when we reload the page. So, we
can just search directly for the value of the parameter:

```
% cat inbox-requests.har \
    | jq '.log.entries
            | map(select(.response.content.text | .?
                           | contains("AQE4bjFlv-4P3Xs:50:1637886942"))
                    | .request.url)'
[
  "https://www.messenger.com/t/100007424414992/"
]
```

Apparently, once again we get parameter values for free just by
looking at the initial HTML response! Let's extract that response from
the HAR and run it through [Prettier](https://prettier.io/) to make
the HTML more readable:

```
% cat inbox-requests.har \
    | jq '.log.entries
            | map(select(.response.content.text | .?
                           | contains("AQE4bjFlv-4P3Xs:50:1637886942")))
            | .[0].response.content.text' -r \
    > inbox.html
% prettier inbox.html > inbox-pretty.html
```

Searching through `inbox-pretty.html` with our favorite text editor,
look what we find for `fb_dtsg`:

```javascript
                [
                  "DTSGInitialData",
                  [],
                  { token: "AQE4bjFlv-4P3Xs:50:1637886942" },
                  258,
                ],
```

And while we're at it, why not search for the other values too? Turns
out there are two of them just lying around (`deviceId` and
`version`):

```javascript
                  {
                    syncScripts: [],
                    deviceId: "6a9252cb-2145-4f81-9d69-1834b84ba614",
                    schemaVersion: "4680497022042598",
                    schemaVersionV2: null,
                    accountKey: "",
                  },
```

That knocks out three parameter values, leaving only `doc_id`. Since
its value, `4476599072415612`, tragically doesn't show up in the HTML,
let's go back to the HAR:

```
% cat inbox-requests.har \
    | jq '.log.entries
            | map(select(.response.content.text | .?
                           | contains("4476599072415612"))
                    | .request.url)'
[
  "https://static.xx.fbcdn.net/rsrc.php/v3iRYC4/y8/l/en_US/d0FzJm8Jr_2GGVI9daGiZfL5MEKqrgHqVIWF0joMj2QgTM4YRSBq4b1LW25pZd7TC-AjrHzCyljakIj8QgziINDKiIZu6XPLjKZJ_v74SDWO8lfwQznT2vHDG_5hUHYYOcBO0v0LGrADQfsxLTta97k6SMq0QFmd6lLAcfPeULHpocMm0pQ6ZiqCb9aFMEaLXT3_o_DtviHOB3GX1Isgz-QZRkiA16JwTjqxIM9tg2HGk3jOqpo4M8-E4se5OLtvP_50qxVk.js?_nc_x=0OMkmbJTxss"
]
```

Apparently, it's in one of those random, inscrutably-named JavaScript
files. Let's check it out:

```
% cat inbox-requests.har \
    | jq '.log.entries
            | map(select(.response.content.text | .?
                           | contains("4476599072415612")))
            | .[0].response.content.text' -r \
    > docid.js
% prettier docid.js > docid-pretty.js
```

Aha, here it is, seeming to be part of the definition of something
called `LSPlatformGraphQLLightspeedRequestQuery`:

```javascript
        params: {
          id: "4476599072415612",
          metadata: {},
          name: "LSPlatformGraphQLLightspeedRequestQuery",
          operationKind: "query",
          text: null,
        },
```

But we also need to know how to pick this particular script out of the
many that are loaded as part of the page. Let's take a look at where
this script is referenced in the HTML page. It looks like this:

```html
    <script
      src="https://static.xx.fbcdn.net/rsrc.php/v3/y1/r/HRDukpAcyqY.js?_nc_x=0OMkmbJTxss"
      data-bootloader-hash="LWwZBAL"
      async="1"
      crossorigin="anonymous"
      data-p=":1"
      data-c="1"
      onload='_btldr["LWwZBAL"]=1'
      onerror='_btldr["LWwZBAL"]=1'
      nonce="nW7qla6Q"
    ></script>
    <link
      rel="preload"
      href="https://static.xx.fbcdn.net/rsrc.php/v3iRYC4/y8/l/en_US/d0FzJm8Jr_2GGVI9daGiZfL5MEKqrgHqVIWF0joMj2QgTM4YRSBq4b1LW25pZd7TC-AjrHzCyljakIj8QgziINDKiIZu6XPLjKZJ_v74SDWO8lfwQznT2vHDG_5hUHYYOcBO0v0LGrADQfsxLTta97k6SMq0QFmd6lLAcfPeULHpocMm0pQ6ZiqCb9aFMEaLXT3_o_DtviHOB3GX1Isgz-QZRkiA16JwTjqxIM9tg2HGk3jOqpo4M8-E4se5OLtvP_50qxVk.js?_nc_x=0OMkmbJTxss"
      as="script"
      crossorigin="anonymous"
      nonce="nW7qla6Q"
    />
    <script
      src="https://static.xx.fbcdn.net/rsrc.php/v3iRYC4/y8/l/en_US/d0FzJm8Jr_2GGVI9daGiZfL5MEKqrgHqVIWF0joMj2QgTM4YRSBq4b1LW25pZd7TC-AjrHzCyljakIj8QgziINDKiIZu6XPLjKZJ_v74SDWO8lfwQznT2vHDG_5hUHYYOcBO0v0LGrADQfsxLTta97k6SMq0QFmd6lLAcfPeULHpocMm0pQ6ZiqCb9aFMEaLXT3_o_DtviHOB3GX1Isgz-QZRkiA16JwTjqxIM9tg2HGk3jOqpo4M8-E4se5OLtvP_50qxVk.js?_nc_x=0OMkmbJTxss"
      data-bootloader-hash="Ll9z/Tq"
      async="1"
      crossorigin="anonymous"
      data-p=":8,11,62,45,43,13,9,65,41,56,27,21,19,59,31,35,25,33,61,37,39,29,4,20"
      data-c="1"
      onload='_btldr["Ll9z\/Tq"]=1'
      onerror='_btldr["Ll9z\/Tq"]=1'
      nonce="nW7qla6Q"
    ></script>
    <link
      rel="preload"
      href="https://static.xx.fbcdn.net/rsrc.php/v3i7Mx4/ya/l/en_US/xovCaG3pRYkBA-zL6eV7sA_kvzFwGGA0iA_Y451ymmdRYKi3JNddo5uNTBXcpfVOaa67G_e6QNkiMZSz44Fa4IsHe1jJJzzjA8TXc-buPNEADH6ljxd0XkWPBzDnUKHZdnKhP0dmjvw4e8cHQ-wygr9Dbce6gKQUJ7j-7IAZomrkiSS24Cf0iRHhPpBbS9Mb_8VDsyKoohBoYL6MVOPJYEcxdVAvTH8o9Vk041xqiSJOXCzZm0UD5J6h5tubWo2SOY3BEhtTcw9z37VDEGPcTjrwwtNcGZfLak_UlVUiSZsFRYeVECK6mZFE3Bk1R6vYlIoidhMWzP.js?_nc_x=0OMkmbJTxss"
      as="script"
      crossorigin="anonymous"
      nonce="nW7qla6Q"
    />
    <script
      src="https://static.xx.fbcdn.net/rsrc.php/v3i7Mx4/ya/l/en_US/xovCaG3pRYkBA-zL6eV7sA_kvzFwGGA0iA_Y451ymmdRYKi3JNddo5uNTBXcpfVOaa67G_e6QNkiMZSz44Fa4IsHe1jJJzzjA8TXc-buPNEADH6ljxd0XkWPBzDnUKHZdnKhP0dmjvw4e8cHQ-wygr9Dbce6gKQUJ7j-7IAZomrkiSS24Cf0iRHhPpBbS9Mb_8VDsyKoohBoYL6MVOPJYEcxdVAvTH8o9Vk041xqiSJOXCzZm0UD5J6h5tubWo2SOY3BEhtTcw9z37VDEGPcTjrwwtNcGZfLak_UlVUiSZsFRYeVECK6mZFE3Bk1R6vYlIoidhMWzP.js?_nc_x=0OMkmbJTxss"
      data-bootloader-hash="2abuuwv"
      async="1"
      crossorigin="anonymous"
      data-p=":3,50,26,24,16,7,64,53,18,14,12,15,17,34,2,44,32,60,28,51,5,55,36,63,23,52,22,10,57,6"
      data-c="1"
      onload='_btldr["2abuuwv"]=1'
      onerror='_btldr["2abuuwv"]=1'
      nonce="nW7qla6Q"
    ></script>
```

Unfortunately, there appear to be a huge number of similarly
inscrutably-named scripts all listed in the same section. But no
matter, we can always just download all of them and then see which one
has the content we're looking for.

## Extract the inbox query parameters

By now we have a procedure for constructing the inbox request:

1. Fetch the HTML page for our Messenger inbox once logged in.
2. Extract the parameters for `fb_dtsg`, `deviceId`, and `version`
   from the HTML.
3. Get a list of all the scripts referenced in the HTML, and download
   each of those.
4. Find the script that defines
   `LSPlatformGraphQLLightspeedRequestQuery`, and extract the
   parameter for `doc_id`.
5. Construct a POST request using these parameters, and fetch the
   response.

We now need to replicate each of these steps in Python. Step 1 is
fairly straightforward; it's the same as the first request we made,
except now we're logged in and can provide cookies to authenticate
ourselves:

```python
inbox_html_resp = requests.get(
    "https://www.messenger.com",
    cookies=login.cookies
)
inbox_html_resp.raise_for_status()
inbox_html_page = inbox_html_resp.text

print(inbox_html_page)
```

Step 2 is just a repeat of our earlier work writing regular
expressions to extract parameters from HTML:

```python
dtsg = re.search(
    r'"DTSGInitialData",\[\],\{"token":"([^"]+)"',
    inbox_html_page
).group(1)

device_id = re.search(
    r'"deviceId":"([^"]+)"',
    inbox_html_page
).group(1)

schema_version = re.search(
    r'"schemaVersion":"([0-9]+)"',
    inbox_html_page
).group(1)

print("dtsg:", dtsg)
print("device_id:", device_id)
print("schema_version:", schema_version)
```

Here we're escaping the brackets and curly braces in the `dtsg`
regular expression to avoid them being interpreted as regular
expression operators, and using `[0-9]` to mean any digit zero through
nine.

For step 3, we'll want to start by using regular expressions to get a
list of all the scripts that (like the one we're looking for) have
`rsrc.php` in their URL and end in `.js`:

```python
script_urls = re.findall(
  r'"([^"]+rsrc\.php/[^"]+\.js[^"]+)"',
  inbox_html_page
)
```

Then we'll want to fetch each of them:

```python
scripts = []
for url in script_urls:
    resp = requests.get(url)
    resp.raise_for_status()
    scripts.append(resp.text)
```

Next up, for step 4, we want to find the script that defines
`LSPlatformGraphQLLightspeedRequestQuery`, and extract `doc_id` from
it:

```python
for script in scripts:
    if "LSPlatformGraphQLLightspeedRequestQuery" not in script:
        continue
    doc_id = re.search(
        r'id:"([0-9]+)",metadata:\{\},name:"LSPlatformGraphQLLightspeedRequestQuery"',
        script
    ).group(1)
    break

print("doc_id:", doc_id)
```

Here's what the parameter extraction looks like in action:

```
% python3 messyger.py -u camilla.woodward@protonmail.com -p 0aSPlneurgscxzpuEZb9
dtsg: AQE0GKhvCGqVF3E:14:1637897352
device_id: 86fbb4b2-fe0e-43e9-8bd5-cd58f7bb763b
schema_version: 4680497022042598
doc_id: 4476599072415612
```

Finally, for step 5, we need to recreate the following HTTPie request
in Python, using our extracted parameters:

```
% http -f https://www.messenger.com/api/graphql/ \
    Cookie:'c_user=100075402451059; xs=50%3Aq86l0PoxUG0qew%3A2%3A1637886942%3A-1%3A-1' \
    fb_dtsg=AQE4bjFlv-4P3Xs:50:1637886942 \
    doc_id=4476599072415612 \
    variables='{"deviceId":"6a9252cb-2145-4f81-9d69-1834b84ba614","requestId":0,"requestPayload":"{\\"database\\":1,\\"version\\":4680497022042598,\\"sync_params\\":\\"{}\\"}","requestType":1}'
```

Here's what that looks like:

```python
import json

inbox_resp = requests.post(
    "https://www.messenger.com/api/graphql/",
    cookies=login.cookies,
    data={
        "fb_dtsg": dtsg,
        "doc_id": doc_id,
        "variables": json.dumps({
            "deviceId": device_id,
            "requestId": 0,
            "requestPayload": json.dumps({
                "database": 1,
                "version": schema_version,
                "sync_params": json.dumps({})
            }),
            "requestType": 1
        })
    }
)
inbox_resp.raise_for_status()

print(inbox_resp.text)
```

You might ask why the Messenger API expects a JSON string inside a
JSON string inside a JSON string inside an HTML form. You would have a
very good question. But at least it explains why we had so many
backslashes to deal with earlier.

## Decipher the inbox data response

Alright, now that we've successfully retrieved our inbox data... what
format is that data coming in, exactly? Well, here's the start of it:

```json
{
  "data": {
    "viewer": {
      "lightspeed_web_request": {
        "payload": "function f(){let inputs=arguments,LS=inputs[inputs.length-1],
```

Yep, that's right. It's a JSON object... *with a bunch of JavaScript
code inside it*! I can't claim to understand why, but [this Facebook
blog post about "Project
LightSpeed"](https://engineering.fb.com/2020/03/02/data-infrastructure/messenger/)
is probably related, given that this JSON object is apparently a
`lightspeed_web_request`. Apparently, in the new version of Messenger,
released in early 2020, the server directly sends JavaScript for the
client to blindly execute and update its local state.

In any case, let's take a look at this JavaScript and see what may lie
inside:

```
% cat inbox-resp.json \
    | jq .data.viewer.lightspeed_web_request.payload -r \
    > inbox-payload.js
% prettier inbox-payload.js > inbox-payload-pretty.js
```

It looks like things start out with a bunch of initialization, setting
up some kind of sequence of operations to operate as a single
[transaction](https://stackoverflow.com/q/974596) using a bunch of
[higher-order functions](https://archive.is/sK4Fn):

```javascript
function f() {
  let inputs = arguments,
    LS = inputs[inputs.length - 1],
    n = LS.n,
    m = [],
    output = [],
    U;
  return LS.seq([
    (_) =>
      LS.seq([
        (_) =>
          LS.sp(
            "executeFirstBlockForSyncTransaction",
            [0, 1],
            [-1, 4294967295],
            U,
            "HCwRAAAWlgEWlqOCxgETBAA",
            [0, 2],
            false,
            [0, 0],
            false,
            [0, 1],
            U
          ).then((r) => ([m[0]] = r)),
        (_) =>
          m[0]
            ? LS.seq([
                (_) =>
                  LS.seq([
                    (_) => LS.fe(LS.db.table(15).fetch(), (c) => c.delete()),
                    (_) => LS.fe(LS.db.table(18).fetch(), (c) => c.delete()),
                    (_) => LS.fe(LS.db.table(19).fetch(), (c) => c.delete()),
                    (_) => LS.fe(LS.db.table(20).fetch(), (c) => c.delete()),
                    (_) => LS.fe(LS.db.table(21).fetch(), (c) => c.delete()),
                    (_) => LS.fe(LS.db.table(22).fetch(), (c) => c.delete()),
                    (_) => LS.fe(LS.db.table(23).fetch(), (c) => c.delete()),
                    (_) => LS.fe(LS.db.table(24).fetch(), (c) => c.delete()),
                    ... lots more of this ...
```

After this boilerplate, however, the bulk of the script consists of
calls to the `LS.sp` function, like this:

```javascript
                (_) =>
                  LS.sp(
                    "addParticipantIdToGroupThread",
                    [23284, 3405894928],
                    [23284, 3405894928],
                    [381, 1262926839],
                    [381, 1262927046],
                    [381, 1262844841],
                    U,
                    false,
                    U,
                    [0, 0],
                    [0, 80],
                    U,
                    U
                  ),
```

This is where we have to start staring at code and making guesses. One
reasonable guess is that the first argument to `LS.sp` represents the
action to be taken (e.g. register a user as one of the participants in
a group conversation), and the remaining arguments are parameters for
that action (e.g., identifying which user and which conversation are
to be operated on).

One thing that would be helpful is understanding what some of these
argument values are. For example, what's `U`? Fortunately, that one is
pretty easy to figure out. From the beginning of the script:

```javascript
  let inputs = arguments,
    LS = inputs[inputs.length - 1],
    n = LS.n,
    m = [],
    output = [],
    U;
```

So `U` is actually just `undefined` (which is the default value of an
uninitialized variable in JavaScript); it looks like the code is using
the `U` alias to save characters.

What about these two-element arrays? They're actually all over the
place in the generated code, and strangely enough, every array has
exactly two integers, no more, no less. Even more strangely, there
aren't any normal integers! Numbers only show up inside two-element
arrays. Here are some examples of these arrays:

```javascript
[-1, 4294967295]
[0, 0]
[0, 1]
[0, 2]
[0, 80]
[0, 1640485980]
[381, 1262844841]
[381, 1262926839]
[381, 1262927029]
[381, 1262927046]
[23284, 3405894928]
[23300, 2664454259],
[368832, 2185323521]
[230687821, 2208225279]
```

Looking at these arrays, we can see a couple of notable properties:

* There are various "genres" of the arrays, which have different
  typical ranges. For example, there are a bunch that are `[0, <small
  integer>]`, then a bunch that are `[381, <large integer>]`, then
  some that are `[<integer around 23000>, <large integer>]`.
* We know that some of these values must somehow represent things like
  user IDs and conversation IDs, since functions like
  `addParticipantIdToGroupThread` don't take any arguments that could
  convey this information aside from the two-element arrays.
* Values like `[0, 0]` and `[0, 1]` show up a lot.
* The value `4294967295` that shows up in `[-1, 4294967295]` is
  exactly one less than 2 to the 32, or the maximum value of a 32-bit
  integer.

These properties are all suggestive, but the thing that gave me a
flash of insight was this code elsewhere in the script payload:

```
                        LS.i64.eq(i.a, [23284, 3405894928]) &&
                        LS.i64.eq([0, 0], [0, 0]) &&
                        LS.i64.eq(i.b, [381, 1262927029]) &&
```

The term `i64` typically refers to a 64-bit integer, so `i64.eq` would
be a function for comparing 64-bit integers for equality. Oh, so these
arrays must be representing 64-bit integers! The first integer must be
the high 32 bits (which would often be zero), and the second integer
is the low 32 bits. I would assume Messenger does this because
[JavaScript doesn't have 64-bit
integers](https://stackoverflow.com/a/307200).

For example, the recurring value `[23284, 3405894928]` would translate
to `2^32 * 23284 + 3405894928 = 100007424414992`. And what do you
know, that's exactly the value that was showing up in the URL
`https://www.messenger.com/t/100007424414992/` in our screenshots!

Armed with this knowledge, let's take a look at where `Hi Camilla` is
showing up, as that will probably have the inbox information we're
looking for. There turn out to be three occurrences:
`deleteThenInsertThread`, `upsertMessage`, and
`setMessageDisplayedContentTypes`. Well, we're looking to generate a
conversation list, so the first function sounds the most relevant.
Here are its arguments:

```javascript
                  LS.sp(
                    "deleteThenInsertThread",
                    [381, 1262897440],
                    [381, 1262897440],
                    "Hi Camilla!",
                    U,
                    "https://scontent-sjc3-1.xx.fbcdn.net/v/t1.30497-1/143086968_2856368904622192_1959732218791162458_n.png?_nc_cat=1&ccb=1-5&_nc_sid=dbb9e7&_nc_ohc=Q_Y6W2vdkywAX8eYoNq&_nc_ht=scontent-sjc3-1.xx&oh=8e70b2536bd14a3ecbe072f3753622a3&oe=61C56EF8",
                    U,
                    [0, 80],
                    [23300, 2492200183],
                    [0, 0],
                    [0, 1],
                    "inbox",
                    "/messaging/lightspeed/media_fallback/?entity_id=100075230196983&entity_type=10&width=200&height=200",
                    [0, 1640328952],
                    [0, 0],
                    [0, 0],
                    [0, 0],
                    false,
                    [23300, 2492200183],
                    U,
                    U,
                    ... lots more nulls and zeroes ...
```

Let's break down the arguments here based on what we know:

* `Hi Camilla!` would probably be the text that's displayed in the
  sidebar, i.e. the most recent message in its conversation.
* `[23300, 2492200183] = 100075402451059` is the ID that's displayed
  in the URL for the conversation with Kane Woods (who sent the `Hi
  Camilla!` message). This parameter is repeated twice in different
  places for some reason.
* `[381, 1262897440] = 1637645437216` is a [UNIX
  timestamp](https://en.wikipedia.org/wiki/Unix_time) for `Tuesday,
  November 23, 2021 5:30:37.216 AM GMT`, which is approximately the
  time that I'm writing this guide. UNIX timestamp is a super common
  format to represent dates and times, so it's worth remembering, and
  after you see it enough you'll be able to see an integer and say
  "that kinda looks like it's the right size to be a timestamp". You
  can use [an online tool](https://www.epochconverter.com/) to convert
  timestamps to human-readable representation, and vice versa. This
  parameter is also repeated twice in different places for some
  reason.
* The `https://scontent-sjc3-1.xx.fbcdn.net` URL can be opened
  directly in the browser and appears to be the profile picture
  displayed next to the conversation.
* `[0, 1640328952]` seems like another UNIX timestamp, `Friday,
  December 24, 2021 6:55:52 AM GMT` (this one in seconds rather than
  milliseconds), but that's a whole month after the first one, so the
  relevance of this one isn't totally clear.

## Examine the behavior of the inbox data response

This is a good start, but we need more information to be sure we
understand what these parameters really mean. For one thing, we could
be making bad assumptions, and for another, there are already
unanswered questions, such as why there are seemingly duplicated
parameters. They could be truly redundant, or the different copies
could have different meanings and just happen to have the same value
in this particular situation. One way we can resolve the confusion is
by collecting more data:

1. Reload the page and download the response data again. Compare it
   with the original (say, using `git diff --no-index` on the
   formatted JavaScript payloads) to see what changes between two
   subsequent requests for the same data.
2. Now make some change by interacting with Messenger, e.g. by sending
   a new message. Download the response data a third time and compare
   it with the original as well. Anything that's different now that
   wasn't different in the first comparison must be a change caused by
   your latest interaction. This might help to identify how the values
   of the parameters relate to the data being shown on the webpage.

Let's start by sending a new message from our test account in one of
its conversations. Here is how the invocation to
`deleteThenInsertThread` in the inbox API response changes:

```diff
                   LS.sp(
                     "deleteThenInsertThread",
-                    [381, 1262927029],
-                    [381, 1262927029],
-                    "Hey there Camilla!",
+                    [381, 1596534595],
+                    [381, 1596534595],
+                    "You: Hello, this is a response",
                     U,
                     "https://scontent-sjc3-1.xx.fbcdn.net/v/t31.18172-1/p200x200/13235223_1713693562221441_496736952870870067_o.jpg?_nc_cat=110&ccb=1-5&_nc_sid=dbb9e7&_nc_ohc=AlIiI4QhLQUAX_
FB-Bd&_nc_ht=scontent-sjc3-1.xx&oh=fc8dd918473653af963d198ea106e8eb&oe=61C7D45C",
                     U,
                     [0, 80],
                     [23284, 3405894928],
                     [0, 0],
                     [0, 1],
                     "inbox",
                     "/messaging/lightspeed/media_fallback/?entity_id=100007424414992&entity_type=10&width=200&height=200",
                     [0, 1640485980],
                     [0, 0],
                     [0, 0],
                     [0, 0],
                     false,
-                    [23284, 3405894928],
+                    [23300, 2664454259],
                     U,
                     U,
```

The UNIX timestamps at the top have changed from `[381, 1262927029] =
Tuesday, November 23, 2021 5:31:06.805 AM GMT` to `[381, 1596534595] =
Saturday, November 27, 2021 2:11:14.371 AM GMT`, with the new
timestamp being exactly the time when we sent the latest message. This
suggests that one or both of those timestamps corresponds to the time
of the last message or other update to the conversation. We'll need to
do more investigation to figure out the difference between the two
parameters.

The last-message string was updated from `Hey there Camilla!` to `You:
Hello, this is a response`, and the presence of `You:` in here
suggests that it's not the raw message, but actually corresponds to
the literal text shown in the inbox sidebar.

And finally, the ID at the bottom has changed. Note that previously
there were two instances of `[23284, 3405894928] = 100007424414992`
(the user ID of the person we were messaging), but now one of them has
changed to `[23300, 2664454259] = 100075402451059` (our own user ID,
which we can find by searching for ourselves in Messenger and checking
the URL). This behavior suggests that the first of the two IDs is the
ID of the person we're messaging, while the second is the ID of the
person who sent the last message (previously the other person, now
us).

Let's now explore read/unread behavior. We'll receive a new message
from another account, and then see how the API response changes when
we read that message (clearing its unread status).

Aha, this produces a difference between the two mysterious timestamps
passed to `deleteThenInsertThread`:

```diff
                   LS.sp(
                     "deleteThenInsertThread",
                     [381, 1597327774],
-                    [381, 1596534595],
+                    [381, 1597327774],
                     "Have you read this yet?",
                     U,
                     "https://scontent-sjc3-1.xx.fbcdn.net/v/t31.18172-1/p200x200/13235223_1713693562221441_496736952870870067_o.jpg?_nc_cat=110&ccb=1-5&_nc_sid=dbb9e7&_nc_ohc=AlIiI4QhLQUAX_FB-Bd&_nc_ht=scontent-sjc3-1.xx&oh=fc8dd918473653af963d198ea106e8eb&oe=61C7D45C",
```

Based on this information, it seems likely that the first timestamp is
when the most recent message was sent, whereas the second timestamp is
the timestamp of the most recent message that's been read so far. In
other words, the conversation has unread message(s) when these two
timestamps differ.

One last detail to clear up before we can construct our inbox view:
how do we actually translate from these user IDs back to human names
we can display? Well, searching for a name like `Kane Woods` in the
response shows that this information can be easily extracted from the
arguments to the `verifyContactRowExists` function:

```javascript
                  LS.sp(
                    "verifyContactRowExists",
                    [23300, 2492200183],
                    [0, 1],
                    "https://scontent-sjc3-1.xx.fbcdn.net/v/t1.30497-1/p100x100/143086968_2856368904622192_1959732218791162458_n.png?_nc_cat=1&ccb=1-5&_nc_sid=dbb9e7&_nc_ohc=Q_Y6W2vdkywAX9oSRfq&_nc_ht=scontent-sjc3-1.xx&oh=daaf26cd7b77fa48b5bc2aafc7ee8a0c&oe=61C90FD1",
                    "Kane Woods",
                    ... more arguments ...
```

## Parse the inbox data response

We now have a checklist of data to extract from the inbox data
response:

* Extract the embedded JavaScript snippet from the JSON response we
  get from Messenger.
* Look at calls to `deleteThenInsertThread` to get a list of
  conversations that would be displayed in the sidebar.
* Extract the last-sent message description from a string argument.
* Get the user ID of the person the conversation is with, as well as
  the user ID of the person who sent the last message.
* Compare the two timestamps in the initial arguments to determine
  whether the conversation is marked as unread or not.
* Look at calls to `verifyContactRowExists` to map user IDs back to
  human names.

However, this code seems like a huge mess to parse with regular
expressions, since the required data is stuck in specific positional
arguments of long function invocations, separated by lots of cruft we
don't care about. Another approach is called for.

The standard approach to parsing programming languages without regular
expressions is to use a tool to convert them into their [abstract
syntax tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree),
which allows manipulating the data embedded in the language without
needing to parse lots of syntax. We'll use the
[Esprima](https://github.com/Kronuz/esprima-python) library to parse
JavaScript from Python:

```python
import esprima

inbox_json = inbox_resp.json()
inbox_js = inbox_json["data"]["viewer"]["lightspeed_web_request"]["payload"]

ast = esprima.parseScript(inbox_js)

print(ast)
```

Now, instead of having to parse a function call like this:

```javascript
                  LS.sp(
                    "updateThreadsRangesV2",
                    "inbox",
                    [0, 0],
                    [0, 1],
                    [-2147483648, 0]
                  ),
```

We get a pre-parsed data structure like this, where all the arguments
are neatly identified for us and we can just loop over them in Python:

```javascript
{
    type: "CallExpression",
    callee: {
        type: "MemberExpression",
        computed: False,
        object: {
            type: "Identifier",
            name: "LS"
        },
        property: {
            type: "Identifier",
            name: "sp"
        }
    },
    arguments: [
        {
            type: "Literal",
            value: "updateThreadsRangesV2",
            raw: "\"updateThreadsRangesV2\""
        },
        {
            type: "Literal",
            value: "inbox",
            raw: "\"inbox\""
        },
        {
            type: "ArrayExpression",
            elements: [
                {
                    type: "Literal",
                    value: 0,
                    raw: "0"
                },
                {
                    type: "Literal",
                    value: 0,
                    raw: "0"
                }
            ]
        },
        {
            type: "ArrayExpression",
            elements: [
                {
                    type: "Literal",
                    value: 0,
                    raw: "0"
                },
                {
                    type: "Literal",
                    value: 1,
                    raw: "1"
                }
            ]
        },
        {
            type: "ArrayExpression",
            elements: [
                {
                    type: "UnaryExpression",
                    prefix: True,
                    operator: "-",
                    argument: {
                        type: "Literal",
                        value: 2147483648,
                        raw: "2147483648"
                    }
                },
                {
                    type: "Literal",
                    value: 0,
                    raw: "0"
                }
            ]
        }
    ]
},
```

Step 1 of processing the AST we get from Esprima will be to identify
all the uses of `LS.sp`. We can write a function to match this
pattern, based on looking at the AST snippet above:

```python
def is_lightspeed_call(node):
    return (
        node.type == "CallExpression"
        and node.callee.type == "MemberExpression"
        and node.callee.object.type == "Identifier"
        and node.callee.object.name == "LS"
        and node.callee.property.type == "Identifier"
        and node.callee.property.name == "sp"
    )
```

Then we'll want to transform the arguments into Python values rather
than the objects that appear in the AST, again by inspecting the AST
snippet above to see how things are represented:

```python
def parse_argument(node):
    if node.type == "Literal":
        return node.value
    if node.type == "ArrayExpression":
        assert len(node.elements) == 2
        high_bits, low_bits = map(parse_argument, node.elements)
        return (high_bits << 32) + low_bits
    if (
        node.type == "UnaryExpression" and
        node.prefix and
        node.operator == "-"
    ):
        return -parse_argument(node.argument)
```

(We're using `<< 32` to implement Messenger's multiply-by-2-to-the-32
operation; [read more about
`<<`](https://stackoverflow.com/a/141873).)

What we want to do now is go through every node in the AST, searching
for `LS.sp` invocations, and sort them by which function is being
called. Fortunately, this is exactly the sort of task that libraries
like Esprima are designed for. The typical way to do it is by writing
a function which the library will call for every node in the AST. Here
is what that looks like:

```python
import collections
fn_calls = collections.defaultdict(list)

def handle_node(node, meta):
    if not is_lightspeed_call(node):
        return

    args = [parse_argument(arg) for arg in node.arguments]
    (fn_name, *fn_args) = args

    fn_calls[fn_name].append(fn_args)

esprima.parseScript(inbox_js, delegate=handle_node)

print(json.dumps(fn_calls, indent=2))
```

Here's what that looks like:

```
% python3 messyger.py -u ailish.maldonado@yahoo.com -p 5155xKYdE1zi0KxGPMvF
{
  "executeFirstBlockForSyncTransaction": [
    [
      1,
      -1,
      null,
      "HCwRAAAWZhaql9XyAxMEAA",
      2,
      false,
      0,
      false,
      1,
      null
    ]
  ],
  "deleteThenInsertThread": [
    [
      1638035642666,
      1638035369213,
      "Totes agreed",
      null,
      "https://scontent-sjc3-1.xx.fbcdn.net/v/t1.30497-1/143086968_2856368904622192_1959732218791162458_n.png?_nc_cat=1&ccb=1-5&_nc_sid=dbb9e7&_nc_ohc=Q_Y6W2vdkywAX8I78V4&_nc_ht=scontent-sjc3-1.xx&oh=c780f73897ab04a260dbbd203a14e2e5&oe=61C96378",
      null,
      80,
      100075475206906,
      ... lots more ...
```

(You may notice we're using a different email address here, because
this is the point in the blog post where the original account I was
using for testing got banned for acting too suspicious.)

With this data in hand, we can finally assemble our parsed function
calls into a useful thread listing:

```python
conversations = collections.defaultdict(dict)

for args in fn_calls["deleteThenInsertThread"]:
    last_sent_ts, last_read_ts, last_msg, *rest = args
    user_id, last_msg_author = [
        arg for arg in rest if isinstance(arg, int) and arg > 1e14
    ]
    conversations[user_id]["unread"] = last_sent_ts != last_read_ts
    conversations[user_id]["last_message"] = last_msg
    conversations[user_id]["last_message_author"] = last_msg_author

for args in fn_calls["verifyContactRowExists"]:
    user_id, _, _, name, *rest = args
    conversations[user_id]["name"] = name

print(json.dumps(conversations, indent=2))
```

And, huzzah! Conversations listed from most to least recent, with our
own user ID available as the last entry in the dictionary. (That last
bit is admittedly a little weird, but it could always be cleaned up
later if desired.)

```
% python3 messyger.py -u ailish.maldonado@yahoo.com -p 5155xKYdE1zi0KxGPMvF
{
  "100075475206906": {
    "unread": true,
    "last_message": "Totes agreed",
    "last_message_author": 100075475206906,
    "name": "Kerri Blackmore"
  },
  "100075217039998": {
    "unread": false,
    "last_message": "You: How ya doin",
    "last_message_author": 100075103764938,
    "name": "Astrid Mccallum"
  },
  "100075103764938": {
    "name": "Ailish Maldonado"
  }
}
```

## Find the send-message request

Let's move on to the last planned feature of Messyger: sending a
message to a conversation. We can start by opening up Messenger with
the developer tools open and sending a message, to see what request(s)
it triggers:

![Requests triggered by sending a
message](/assets/messenger/send-message-requests.png)

Hmmm, something is odd here. In the right-hand column, labeled
Waterfall, we can see a visual representation of the time when each
request was made. Most of them were made at about the same time,
during the initial page load. The third-to-last request was made a
little bit after (it looks like the client makes a request like this
periodically, even if you don't do anything). And the last two
requests are the only two that were made after we sent the message.
But those last two requests aren't API requests, they're just requests
to fetch images! So how was the client able to tell the server to send
our message?

Well, if we scroll up in the Network tab, we can see there are a few
requests that are still listed as "Pending", meaning they haven't
finished transmitting data yet:

![Websocket requests shown as
Pending](/assets/messenger/websocket-request-pending.png)

Those connections are [websocket
connections](https://www.html5rocks.com/en/tutorials/websockets/basics/),
which are long-lasting HTTP connections that the server and client can
use to send data back and forth at any time. Indeed, if we click on
one of those connections, we can see that they have been hard at work
the entire time sending messages back and forth:

![List of messages sent over chat
websocket](/assets/messenger/websocket-messages.png)

Since we didn't see any new HTTP requests in the Network tab when
sending a message, it's possible that the client used one of its
websocket connections to communicate with the server instead. Indeed,
if we check the last few websocket messages that were exchanged after
we pressed Return, we find this one, which is a message from the
client to the server containing exactly the text of the message we
sent:

![Websocket message responsible for sending our
text](/assets/messenger/send-message-in-websocket.png)

To inspect the contents, we can download that message from Chrome (in
base64 since it's labeled as a "binary message"):

![Right-click menu for downloading the websocket
message](/assets/messenger/copy-as-base64.png)

Using a tool like [base64decode.org](https://www.base64decode.org/),
we can then inspect the contents:

![Using base64decode.org to decode the websocket
message](/assets/messenger/base64-decode.png)

It appears that there's a bit of junk at the beginning, but then the
rest is just a JSON object that looks awfully similar to the one that
we used when making our request to get the inbox data.

Here's the raw JSON:

```json
{
  "request_id": 76,
  "type": 3,
  "payload": "{\"version_id\":\"4680497022042598\",\"tasks\":[{\"label\":\"46\",\"payload\":\"{\\\"thread_id\\\":100075475206906,\\\"otid\\\":\\\"6870463702739115828\\\",\\\"source\\\":65537,\\\"send_type\\\":1,\\\"text\\\":\\\"Let's see how this message gets sent\\\",\\\"initiating_source\\\":1}\",\"queue_name\":\"100075475206906\",\"task_id\":10,\"failure_count\":null},{\"label\":\"21\",\"payload\":\"{\\\"thread_id\\\":100075475206906,\\\"last_read_watermark_ts\\\":1638046193775,\\\"sync_group\\\":1}\",\"queue_name\":\"100075475206906\",\"task_id\":11,\"failure_count\":null}],\"epoch_id\":6870463702858032614,\"data_trace_id\":\"#0Q0JVtIKTdGjTDCwodlbNg\"}",
  "app_id": "772021112871879"
}
```

Where the `payload` key is a JSON string that expands to this:

```json
{
  "version_id": "4680497022042598",
  "tasks": [
    {
      "label": "46",
      "payload": "{\"thread_id\":100075475206906,\"otid\":\"6870463702739115828\",\"source\":65537,\"send_type\":1,\"text\":\"Let's see how this message gets sent\",\"initiating_source\":1}",
      "queue_name": "100075475206906",
      "task_id": 10,
      "failure_count": null
    },
    {
      "label": "21",
      "payload": "{\"thread_id\":100075475206906,\"last_read_watermark_ts\":1638046193775,\"sync_group\":1}",
      "queue_name": "100075475206906",
      "task_id": 11,
      "failure_count": null
    }
  ],
  "epoch_id": 6870463702858032000,
  "data_trace_id": "#0Q0JVtIKTdGjTDCwodlbNg"
}
```

And the `payload` keys in *that* are JSON strings that expand to
these:

```json
{
  "thread_id": 100075475206906,
  "otid": "6870463702739115828",
  "source": 65537,
  "send_type": 1,
  "text": "Let's see how this message gets sent",
  "initiating_source": 1
}

{
  "thread_id": 100075475206906,
  "last_read_watermark_ts": 1638046193775,
  "sync_group": 1
}
```

## Replicate the send-message request

Now that we've identified the request that the client uses to send a
message, we want to replicate it outside the browser for testing.
However, this one is a bit more complicated, because we can't just
"Copy as cURL" for a websocket message. We could get the cURL command
to *open* the websocket, but then the server and client might need to
exchange a bunch of individual messages on the socket before we could
send the request we want.

However, if we look at the data in this websocket message, it seems
strangely similar to the HTTP request we made earlier when fetching
the inbox data. In particular:

* Both requests have an embedded string of JSON (called `payload` and
  `requestPayload` respectively).
* Both "payloads" have a top-level key that seems to specify some kind
  of schema version, with value `4680497022042598` (the key being
  called `version_id` and `version` respectively).
* Alongside the "payload" there is also a sibling key that specifies
  some kind of request type, with value `type: 3` in the websocket
  message and `requestType: 1` in the inbox request.

Is it possible that the Messenger API supports making the same request
in two different ways (via individual HTTP request or as a message on
an already-open websocket)? If so, it would make things easier for us,
because then instead of figuring out how to do the stuff with
websockets, we could just make this request the same way as we made
the inbox request.

We have no particular reason to believe this will work, since we don't
have a working example in the client to compare against, but if our
guess happens to be right, we could save a lot of time, so let's give
it a try. We'll start with our existing code to make the inbox
request:

```python
inbox_resp = requests.post(
    "https://www.messenger.com/api/graphql/",
    cookies=login.cookies,
    data={
        "fb_dtsg": dtsg,
        "doc_id": doc_id,
        "variables": json.dumps({
            "deviceId": device_id,
            "requestId": 0,
            "requestPayload": json.dumps({
                "database": 1,
                "version": schema_version,
                "sync_params": json.dumps({})
            }),
            "requestType": 1
        })
    }
)
inbox_resp.raise_for_status()
```

Then we'll modify it to substitute out its `requestPayload` for the
one we saw in the websocket message:

```python
send_message_resp = requests.post(
    "https://www.messenger.com/api/graphql/",
    cookies=login.cookies,
    data={
        "fb_dtsg": dtsg,
        "doc_id": doc_id,
        "variables": json.dumps({
            "deviceId": device_id,
            "requestId": 0,
            "requestPayload": json.dumps({
                "version_id": "4680497022042598",
                "tasks": [
                  {
                    "label": "46",
                    "payload": json.dumps({
                        "thread_id": 100075475206906,
                        "otid": "6870463702739115828",
                        "source": 65537,
                        "send_type": 1,
                        "text": "Let's see how this message gets sent",
                        "initiating_source": 1
                    }),
                    "queue_name": "100075475206906",
                    "task_id": 10,
                    "failure_count": None
                  },
                  {
                    "label": "21",
                    "payload": json.dumps({
                        "thread_id": 100075475206906,
                        "last_read_watermark_ts": 1638046193775,
                        "sync_group": 1
                    }),
                    "queue_name": "100075475206906",
                    "task_id": 11,
                    "failure_count": None
                  }
                ],
                "epoch_id": 6870463702858032000,
                "data_trace_id": "#0Q0JVtIKTdGjTDCwodlbNg"
            }),
            "requestType": 3  # to match type: 3 in websocket message
        })
    }
)
send_message_resp.raise_for_status()

print(send_message_resp.text)
```

If we run this, the results are mixed: it doesn't return an error
(instead it returns a bunch of embedded JavaScript just like the inbox
response), but it also doesn't actually send a message that shows up
in the Messenger interface. There are a couple different potential
explanations for why this could be; for example:

1. We might not be able to send messages using this API at all, and
   our original guess was wrong.
2. We could have a syntax error somewhere in our request, and the
   server might just ignore malformed requests and send back a generic
   response.
3. Unlike getting the inbox data, which is read-only, sending a
   message is a write operation. The API might have been designed so
   that repeating the same request more than once doesn't result in
   multiple messages getting sent.

From a design perspective, (3) actually makes a lot of sense. After
all, requests sometimes fail inside the network and need to be
retried, so it's best if repeating a request multiple times doesn't
result in action being taken multiple times.

One way to see if this is the case is by playing around with the
parameters of the request to see if one of them has to be modified
before the repeated request will be seen as a request to send a *new*
message, rather than be ignored as a duplicate.

And if we do this, we find that indeed, changing the `otid` value
(e.g., by adding 1 to it) results in a new copy of the message being
sent!

![Two copies of our message](/assets/messenger/duplicate-message.png)

Apparently, `otid` is some kind of unique identifier used to prevent
messages from accidentally getting sent twice (each message from the
client gets assigned a unique `otid`, and each `otid` can only be
processed once by the server).

## Clean up the send-message request

Now that we have a proof of concept for how to send messages, we can
clean it up by using variables instead of hardcoding in values. We'll
start by reading in command-line arguments for sending a message:

```python
parser.add_argument("-m", "--message")
parser.add_argument("-r", "--recipient", type=int)
```

Then we can replace `Let's see how this message gets sent` with
`args.message`, and `100075475206906` with `args.recipient`.

Most of the other parameters in the request look reasonably important,
so we'll leave most of them in. The only exception is `data_trace_id`,
which suggests something used for debugging, so we'll remove that.

There are a couple of leftover hardcoded numbers:

* `source` is set to `65537` (exactly one more than 2 to the 16th
  power). However, testing suggests that the value doesn't actually
  matter, so we'll just set it to 0 for now and revisit later if it
  causes issues.
* `label` is set to `46` and `21` respectively in the two elements of
  the `tasks` array. These values seem likely to be fixed ID numbers
  that are part of the API (`46` meaning "send message" and `21`
  meaning "update last-read indicator").
* `last_read_watermark_ts` is set to a UNIX timestamp that seems to be
  for the time the message was sent, which we can replace with one
  generated by our code.
* `task_id` is set to `10` and `11` respectively for the two `tasks`.
  Testing suggests that the values don't matter, so we'll set them to
  0 and 1, respectively.
* `requestType` is `3` and this comes from the websocket API request,
  so we'll leave that as is.

Here's what we end up with after making those substitutions:

```python
import datetime

timestamp = int(datetime.datetime.now().timestamp() * 1000)

send_message_resp = requests.post(
    "https://www.messenger.com/api/graphql/",
    cookies=login.cookies,
    data={
        "fb_dtsg": dtsg,
        "doc_id": doc_id,
        "variables": json.dumps(
            {
                "deviceId": device_id,
                "requestId": 0,
                "requestPayload": json.dumps(
                    {
                        "version_id": str(schema_version),
                        "tasks": [
                            {
                                "label": "46",
                                "payload": json.dumps(
                                    {
                                        "thread_id": args.recipient,
                                        "otid": "6870463702739115830",
                                        "source": 0,
                                        "send_type": 1,
                                        "text": args.message,
                                        "initiating_source": 1,
                                    }
                                ),
                                "queue_name": str(args.recipient),
                                "task_id": 0,
                                "failure_count": None,
                            },
                            {
                                "label": "21",
                                "payload": json.dumps(
                                    {
                                        "thread_id": args.recipient,
                                        "last_read_watermark_ts": timestamp,
                                        "sync_group": 1,
                                    }
                                ),
                                "queue_name": str(args.recipient),
                                "task_id": 1,
                                "failure_count": None,
                            },
                        ],
                        "epoch_id": 6870463702858032000,
                    }
                ),
                "requestType": 3,
            }
        ),
    },
)
```

All we have left now are the mysterious `otid` and `epoch_id`
parameters. Generating `otid` correctly is important for making sure
our messages are actually sent, so we'll want to understand how to do
it.

Since the `otid` is different for every message, it would most likely
have to be generated on the client side. Therefore, a reasonable place
to start would be to search the client-side JavaScript for mentions of
`otid`.

```
% cat inbox-requests.har \
    | jq '.log.entries
            | map(select(.response.content.text | .?
                           | contains("otid"))
                    | .request.url)'
[
  "https://static.xx.fbcdn.net/rsrc.php/v3iRYC4/y8/l/en_US/d0FzJm8Jr_2GGVI9daGiZfL5MEKqrgHqVIWF0joMj2QgTM4YRSBq4b1LW25pZd7TC-AjrHzCyljakIj8QgziINDKiIZu6XPLjKZJ_v74SDWO8lfwQznT2vHDG_5hUHYYOcBO0v0LGrADQfsxLTta97k6SMq0QFmd6lLAcfPeULHpocMm0pQ6ZiqCb9aFMEaLXT3_o_DtviHOB3GX1Isgz-QZRkiA16JwTjqxIM9tg2HGk3jOqpo4M8-E4se5OLtvP_50qxVk.js?_nc_x=0OMkmbJTxss
"
]
% cat inbox-requests.har \
    | jq '.log.entries
            | map(select(.response.content.text | .?
                           | contains("otid")))
            | .[0].response.content.text' -r \
    > otid.js
% prettier otid.js > otid-pretty.js
```

There are appearances of `otid` in this script. By themselves, none of
them are very explanatory, but context is everything. One of the
matches looks like this:

```javascript
                d[2].set("otid", c.i64.to_string(d[1])),
```

And if we look up at the top of the function where this statement
appears, we see it looks like this:

```javascript
__d(
  "LSCreateGroupThreadWithAdminText",
  [
    "LSCreateOfflineThreadingID",
    "LSIssueNewTask",
    "LSLocalApplyOptimisticGroupThread",
  ],
  function (a, b, c, d, e, f) {
```

Hey, wait, does `otid` stand for `OfflineThreadingID`? Boom, let's
search for the definition of this `LSCreateOfflineThreadingID`
function. Conveniently enough, it's even in the same file!

```javascript
__d(
  "LSCreateOfflineThreadingID",
  [],
  function (a, b, c, d, e, f) {
    a = function () {
      var a = arguments,
        b = a[a.length - 1];
      b.n;
      var c = [],
        d = [];
      return (
        (c[0] = b.i64.random()),
        (d[0] = b.i64.and_(
          b.i64.or_(
            b.i64.lsl_(a[0], b.i64.to_int32([0, 22])),
            b.i64.and_(c[0], [0, 4194303])
          ),
          [2147483647, 4294967295]
        )),
        b.resolve(d)
      );
    };
    e.exports = a;
  },
  null
);
```

By looking at this function, it seems like the algorithm is something
like:

1. Generate a random 64-bit integer (`b.i64.random()`).
2. Combine that with `4194303` using bitwise AND. Since `4194303`
   happens to be one less than 2 to the 22nd power, this has the
   effect of dropping all bits past the rightmost 22, which converts
   the value from step 1 into a random 22-bit integer.
3. Take the argument to `LSCreateOfflineThreadingID`, and shift it by
   22 bits to the left (`lsl` is a common abbreviation for *left shift
   logical*, which is usually written as `<<`).
4. Combine the preceding two values using bitwise OR. Since the first
   value has only the rightmost bits, while the second value has only
   the leftmost bits, this operation essentially concatenates the two
   numbers. Arithmetically, it works out to `(lefthand bits) * 2^22 +
   (righthand bits)`.

([Read more about bitwise
operators](https://en.wikipedia.org/wiki/Bitwise_operation).)

This raises the question: what actually *is* the argument passed to
`LSCreateOfflineThreadingID`? Well, if we look back at the original
function that mentioned `LSCreateOfflineThreadingID`, we can see that
this is where the call happens:

```javascript
            function (a) {
              return c
                .sp(b("LSCreateOfflineThreadingID"), c.i64.of_float(Date.now()))
                .then(function (a) {
                  return (a = a), (d[1] = a[0]), a;
                });
            },
```

Aha! The argument is just a UNIX timestamp generated by `Date.now()`.
So, with that in mind, we can generate our own "offline threading IDs"
in Python:

```python
timestamp = int(datetime.datetime.now().timestamp() * 1000)
otid = (timestamp << 22) + random.randrange(2 ** 22)
```

One last puzzle to resolve: what about `epoch_id`? Actually, it's
almost the same as `otid`! In the websocket message, we had `otid =
6870463702739115830` and `epoch_id = 6870463702858032000`. It seems
like `epoch_id` is just `otid` rounded down to some particular even
boundary. In fact, with a little more inspection, it turns out that
the boundary is just the same 22-bit boundary as above. So, this is
what's going on:

```python
import random

timestamp = int(datetime.datetime.now().timestamp() * 1000)
epoch = timestamp << 22
otid = epoch + random.randrange(2 ** 22)
```

At long last, we can add this code to Messyger and have a fully(?)
functioning Messenger client that can fetch our list of conversations,
and send a text message to any one of them. The full code is [on
GitHub](https://github.com/raxod502/messyger).

## What next?

Messyger is nowhere near a full Messenger client. I don't intend to
add any more features, because Messyger is an educational case study
rather than a practical application. However, if you want to practice
your skills, you might consider figuring out how to handle some of the
complexities that Messyger glosses over; for example:

* We only had direct messages here; what about group chats?
* How do you fetch past messages, in addition to the most recent one?
* How can you send and receive images, instead of just texts?
* How are emojis and reactions represented?
* How can you get information about when the *recipient* has read your
  message?

Or, you can find a website of your own that you wish exposed a better
API. Can you figure out how to make things work the way you want?

⛏️ Go forth and build something!
