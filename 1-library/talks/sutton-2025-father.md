---
id: sutton-2025-father
type: talk
title: "Richard Sutton – Father of RL thinks LLMs are a dead end"
authors: [Richard Sutton, Dwarkesh Patel]
year: 2025
url: https://www.dwarkesh.com/p/richard-sutton
venue: Dwarkesh Podcast (video and transcript), published 2025-09-26
topics: [fork-merge-security, llm-agent-swarms, meta]
added_by: dmarz/fm-sutton
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

A 66-minute interview in which Sutton argues that LLMs lack goals and ground truth and that the scalable path is continual learning from experience. This is the primary source for the fork-merge corruption idea dmarz attributes to him. Read in full from the official transcript on dwarkesh.com. Two passages matter.

At 00:26:11, answering Patel's question about aggregating knowledge across copies of a continually learning agent, Sutton says:

> "You'd have copies and many instances. Sure, you'd want to share knowledge across the instances. There would be lots of possibilities for doing that. Today, you have one child grow up and learn about the world, and then every new child has to repeat that process. Whereas with AIs, with a digital intelligence, you could hope to do it once and then copy it into the next one as a starting place."

At 00:49:51 (section "Will The Bitter Lesson still apply after AGI?", just before the 00:53:48 "Succession to AI" chapter), Sutton raises the fork-merge question and the corruption risk:

> "An interesting question is, you're an AI, you get some more computer power. Should you use it to make yourself more computationally capable? Or should you use it to spawn off a copy of yourself to go learn something interesting on the other side of the planet or on some other topic and then report back to you?"

> "More questions, will it be possible to really spawn it off, send it out, learn something new, something perhaps very new, and then will it be able to be reincorporated into the original? Or will it have changed so much that it can't really be done? [...] You spawn off many, many copies, do different things, highly decentralized, but report back to the central master. This will be such a powerful thing."

> "This is my attempt to add something to this view. A big issue will become corruption. If you really could just get information from anywhere and bring it into your central mind, you could become more and more powerful. It's all digital and they all speak some internal digital language. Maybe it'll be easy and possible. But it will not be as easy as you're imagining because you can lose your mind this way. If you pull in something from the outside and build it into your inner thinking, it could take over you, it could change you, it could be your destruction rather than your increment in knowledge."

> "I think this will become a big concern, particularly when you're like, 'Oh, he's figured out all about how to play some new game or he's studied Indonesia, and you want to incorporate that into your mind.' You could think, 'Oh, just read it all in, and that'll be fine.' But no, you've just read a whole bunch of bits into your mind, and they could have viruses in them, they could have hidden goals, they can warp you and change you. This will become a big thing. How do you have cybersecurity in the age of digital spawning and re-reforming again?"

"This view" refers to a Dwarkesh Patel video Sutton says he watched, linked in the transcript as "one of your videos" (https://youtu.be/bJD1NpdMY5s, titled "What will automated firms look like?"; the essay version is [[dwarkesh-2025-what]]). Elsewhere Sutton states his four-part argument that succession to AI is inevitable (00:54:03) and says that in a continual learning setup knowledge "just goes into the weights" rather than a context window.

What is measured: nothing. Sutton offers this as an open question and a prediction ("I'm not sure what the answer is"). He does not propose a mechanism, a defence or a threshold.

## Relevance to us

This is the origin quote for the whole fork-merge-security topic, and it is more specific than the paraphrase in the task brief in three ways. First, Sutton frames the merge as reincorporation into a "central master" from "many, many copies", which is a star topology with one root, so it is the setting of Q1 and Q2 directly. Second, his threat is content-borne: "viruses", "hidden goals" in "a whole bunch of bits" read into the mind. That is a Q3 statement in which the payload rides on the learned knowledge itself, not on an external attacker seizing the copy; he names both an exogenous route ("pull in something from the outside") and drift ("will it have changed so much that it can't really be done?"). Third, he frames the defence as "cybersecurity", not as alignment, which licenses borrowing from Byzantine aggregation and supply-chain security for Q2. He says nothing about hiding which copy returns (Q1) or about k-of-n thresholds (Q2); both are our extensions. His geographic example is "the other side of the planet" and "Indonesia", not China. Sutton also argues for decentralized cooperation over centralized control in [[sutton-2024-perspective]], which sits in some tension with the "central master" picture here. Related framings: [[dwarkesh-2025-what]] (mega-Sundar spawning and reabsorbing copies), [[silver-2025-welcome]] (agents learning from their own streams of experience, the setting in which merged knowledge goes into weights).
