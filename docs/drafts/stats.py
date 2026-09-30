#!/usr/bin/env python3
"""Render the ASCII stats block in README.md from live GitHub data.
Runs in the profile repo's daily workflow. Lines stay under 40 columns for phones.
Needs GITHUB_TOKEN (or GH_TOKEN) in the environment."""
import json, os, re, sys, urllib.request

USER = "RamenFast"
WIDTH = 38  # inner width of the frame

QUERY = """{ user(login:"%s"){
  followers{totalCount}
  repositories(first:100,ownerAffiliations:OWNER,privacy:PUBLIC,isFork:false){
    totalCount nodes{stargazerCount languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name}}}}}
  contributionsCollection{contributionCalendar{totalContributions}}
}}""" % USER

def gql():
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not tok: sys.exit("GITHUB_TOKEN missing")
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": QUERY}).encode(),
                                 headers={"Authorization": f"bearer {tok}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))["data"]["user"]

def bar(frac, width):
    full = int(round(frac * width))
    return "█" * full + "░" * (width - full)

def render(u):
    repos = u["repositories"]["nodes"]
    stars = sum(r["stargazerCount"] for r in repos)
    langs = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda x: -x[1])[:5]
    contribs = u["contributionsCollection"]["contributionCalendar"]["totalContributions"]

    def row(s=""): return "│ " + s.ljust(WIDTH - 2) + " │"
    lines = ["┌" + "─" * WIDTH + "┐",
             row("STATION STATUS".center(WIDTH - 2)),
             row("─" * (WIDTH - 2)),
             row(f"public repos   {u['repositories']['totalCount']:>4}"),
             row(f"stars          {stars:>4}"),
             row(f"followers      {u['followers']['totalCount']:>4}"),
             row(f"contribs / yr  {contribs:>4}"),
             row("─" * (WIDTH - 2)),
             row("BEAM MIX".center(WIDTH - 2))]
    for name, size in top:
        frac = size / total
        lines.append(row(f"{name[:10]:<10} {bar(frac, 18)} {int(round(frac*100)):>3}%"))
    lines.append("└" + "─" * WIDTH + "┘")
    return "\n".join(lines)

def main():
    block = "```text\n" + render(gql()) + "\n```"
    path = os.path.join(os.path.dirname(__file__), "README.md")
    s = open(path, encoding="utf-8").read()
    new = re.sub(r"<!-- stats:start -->.*?<!-- stats:end -->",
                 "<!-- stats:start -->\n" + block + "\n<!-- stats:end -->", s, flags=re.S)
    if new == s: print("no change"); return
    open(path, "w", encoding="utf-8").write(new); print("README updated")

if __name__ == "__main__": main()
