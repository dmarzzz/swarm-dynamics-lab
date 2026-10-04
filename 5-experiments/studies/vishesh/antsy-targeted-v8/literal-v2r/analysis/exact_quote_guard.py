"""Retrospective additional gate; not part of frozen Q2 native execution."""
import re

def numeric_tokens(text):
 return set(re.findall(r'(?<![\w.,])\d+(?:[.,]\d+)*(?![\w.,])',text))

def verified_quote(proposal,response):
 return bool(response and response.get('verified') is True and isinstance(proposal.get('token'),str) and proposal['token'] in numeric_tokens(response.get('evidence','')))
