"""Conservative saved-output guard for a declared Indonesian-locale workflow.

Does not repair answers or authenticate quoted text against pixels. A mismatch
forces referral; an agreement still needs source/label verification elsewhere.
"""
import re
from decimal import Decimal,InvalidOperation

def quoted_amounts(evidence):
    values=[]
    for token in re.findall(r'(?<![\w.,])\d+(?:[.,]\d+)*(?![\w.,])',evidence):
        if re.fullmatch(r'\d{1,3}(?:\.\d{3})+(?:,\d{1,2})?',token):clean=token.replace('.','').replace(',','.')
        elif re.fullmatch(r'\d{1,3}(?:,\d{3})+',token):clean=token.replace(',','')
        elif re.fullmatch(r'\d+(?:,\d{1,2})?',token):clean=token.replace(',','.')
        else:continue
        try:values.append(format(Decimal(clean),'.2f'))
        except InvalidOperation:pass
    return set(values)

def check(parsed):
    if not parsed or parsed.get('decision')!='accept':return 'refer'
    values=quoted_amounts(parsed.get('evidence',''))
    if len(values)!=1 or parsed.get('amount') not in values:return 'refer'
    return 'consistent_not_verified'
