#!/usr/bin/env python3

import json
import os
from pathlib import Path
import re
import subprocess
import time
import traceback
import urllib.parse

import requests

os.chdir(Path(__file__).parent.parent)


def drop_unbalanced_parens(url):
    nesting = 0
    for idx, char in enumerate(url):
        if char == "(":
            nesting += 1
        if char == ")":
            nesting -= 1
        if nesting < 0:
            return url[:idx]
    return url


try:
    with open(".url-cache.json") as f:
        url_cache = json.load(f)
except FileNotFoundError:
    url_cache = {}


all_urls = set()


for relpath in subprocess.run(
    ["git", "ls-files"], stdout=subprocess.PIPE, check=True, encoding="utf-8"
).stdout.splitlines():
    if not relpath.endswith(".md"):
        continue
    with open(relpath) as f:
        text = f.read()
        for re_match in re.finditer(r"https?://[^*][^] \n<>;#[]+", text):
            url = re_match.group()
            url = drop_unbalanced_parens(url)
            url = re.sub(r"^([^(]+)\).*", r"\1", url)
            url = url.rstrip(".,;:\"'`")
            if relpath == "src/tech/messenger.md":
                if "fbcdn.net" in url:
                    continue
                if "messenger.com" in url:
                    continue
                if url == "https://httpbin.org/post":
                    url = "https://httpbin.org/get"
            if relpath == "src/tech/replit/evidence.md":
                if url == "https://code.labstack.com/":
                    continue
            all_urls.add(url)


special_options = {
    "www.minecraft.net": {
        "headers": {
            "User-Agent": "HTTPie/3.2.4",
        },
    },
    "archiveofourown.org": {
        "headers": {
            "User-Agent": "HTTPie/3.2.4",
        }
    },
    "archive.is": {
        "headers": {
            "User-Agent": "HTTPie/3.2.4",
        }
    },
}


try:
    for url in sorted(all_urls):
        if data := url_cache.get(url):
            if time.time() - data["last_check"] < 86400 * 30 * 3:
                continue
        print(f"Testing {url} ...")
        try:
            headers = {
                "User-Agent": "https://github.com/radian-software/intuitive-explanations/blob/main/tools/check_external_links.py"
            }
            if opts := special_options.get(urllib.parse.urlparse(url).netloc):
                headers.update(opts.get("headers", {}))
            resp = requests.get(
                url,
                timeout=30,
                headers=headers,
            )
            data = {
                "result": "response",
                "status_code": resp.status_code,
                "last_check": int(time.time()),
            }
        except Exception as e:
            data = {
                "result": "error",
                "error": str(e),
                "last_check": int(time.time()),
            }
        url_cache[url] = data
finally:
    with open(".url-cache.json.tmp", "w") as f:
        json.dump(url_cache, f, indent=2)
        f.write("\n")
    os.rename(".url-cache.json.tmp", ".url-cache.json")


for url in sorted(all_urls):
    data = url_cache[url]
    if data["result"] == "error":
        print(f"Error: {url}")
    if data["result"] == "response":
        if data["status_code"] < 200 or data["status_code"] >= 300:
            print(f"Status code {data['status_code']}: {url}")
