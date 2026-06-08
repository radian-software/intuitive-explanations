#!/usr/bin/env python3

import os
import pathlib
import re
import subprocess
import sys

os.chdir(pathlib.Path(__file__).parent.parent)


def normalize(anchor):
    return re.sub(r"\s+", " ", anchor.lower())


def get_anchors_used(text):
    text = re.sub(r"```.+?```", "", text, flags=re.DOTALL)
    anchors = []
    for first, second, third in re.findall(
        r"\\\[|`.+?`|\[(.+?[^\\])\](?:\((.+?)\)|\[(.*?)\])?", text, re.DOTALL
    ):
        if second or not first:
            continue
        anchor = normalize(third or first)
        if anchor == "...":
            continue
        anchors.append(anchor)
    return anchors


def get_anchors_defined(text):
    anchors = []
    for first in re.findall(r"^\[(.+?)\]:", text, re.MULTILINE):
        anchors.append(normalize(first))
    return anchors


errors = []

for relpath in (
    subprocess.run(["git", "ls-files"], stdout=subprocess.PIPE, check=True)
    .stdout.decode()
    .splitlines()
):
    if relpath.endswith(".md"):
        with open(relpath) as f:
            text = f.read()
        text = re.sub(r"(?s)<script.*?</script>", "", text)
        anchors_used = get_anchors_used(text)
        anchors_defined = get_anchors_defined(text)
        dedupe_set = set()
        for anchor in anchors_defined:
            if anchor in dedupe_set:
                errors.append((relpath, "defined twice", anchor))
            dedupe_set.add(anchor)
        for anchor in set(anchors_used) - set(anchors_defined):
            errors.append((relpath, "used but not defined", anchor))
        for anchor in set(anchors_defined) - set(anchors_used):
            errors.append((relpath, "defined but not used", anchor))

for error in errors:
    print(": ".join(("check_links.py",) + error), file=sys.stderr)

if errors:
    sys.exit(1)
