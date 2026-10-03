import json, glob, re, unicodedata, collections
P=json.load(open("papers.json"))
def norm(s): return unicodedata.normalize("NFKD",s).encode("ascii","ignore").decode().lower()
BOT=re.compile(r"arxiv|papers?$|daily|bot|digest|fly51fly|scifi|net_science|_akhaliq|huggingpapers|marktechpost|memoirs|computerpapers|statspapers|arxivbangers|pin$|^do$|wgov|january|gm8xx8",re.I)
tw={}
for f in sorted(glob.glob("raw/papers-*.json")):
    for t in json.load(open(f)):
        if t.get("isRetweet"): continue
        tw[t["id"]]=t
rows=[]
for t in tw.values():
    blob=json.dumps(t.get("entities",{}))+(t.get("fullText") or t.get("text") or "")
    hits=[ax for ax in P if ax in blob]
    if not hits: continue
    a=t["author"]; name=norm(a.get("name","")); handle=a["userName"].lower()
    for ax in hits:
        p=P[ax]; auth=norm(p["authors"])
        surn={w for w in re.findall(r"[a-z]{3,}",auth)} - {"and","the","etal","university","for"}
        toks=set(re.findall(r"[a-z]{3,}",name))|{handle}
        is_author=bool(toks & surn) or any(s in handle for s in surn if len(s)>=5)
        bot=bool(BOT.search(handle)) or bool(re.match(r"^\[(cs|lg|cl|ai)",(t.get("text") or "").lower()))
        rows.append(dict(ax=ax,pid=p["id"],rel=p["rel"],topics=p["topics"],id=t["id"],h=a["userName"],name=a.get("name"),fol=a.get("followers"),likes=t.get("likeCount",0),
            reply=t.get("isReply"),conv=t.get("conversationId"),author=is_author,bot=bot,date=t["createdAt"],text=(t.get("fullText") or t.get("text"))))
json.dump(rows,open("classified.json","w"),indent=1)
c=collections.Counter((r["author"],r["bot"]) for r in rows); print(len(tw),"tweets",len(rows),"paper-hits",c)
print("papers with any:",len({r['ax'] for r in rows}),"with author thread:",len({r['ax'] for r in rows if r['author'] and not r['bot']}))
