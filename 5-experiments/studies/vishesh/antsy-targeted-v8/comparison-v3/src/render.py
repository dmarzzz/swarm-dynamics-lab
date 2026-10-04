"""Result visualization from saved policy rows, never inferred missing results."""
def render(summary,path):
    from PIL import Image,ImageDraw
    image=Image.new('RGB',(1600,1000),'#101925');d=ImageDraw.Draw(image)
    def text(x,y,value,size=24,color='white'):d.text((x,y),str(value),fill=color,font_size=size)
    text(45,30,'Antsy | does another reader earn its cost?',38)
    text(45,90,summary['attempt']+' | '+summary['stop'],26)
    text(45,135,f"Physical OCR calls: {summary['started_calls']}/{summary['assigned_calls']} started; {summary['unstarted_calls']} unstarted",25)
    colors={'correct':'#4bcfa4','wrong':'#fa736f','abstain':'#eab45f','unscorable':'#8991c9','failed_or_missing':'#66717e'}
    for index,(policy,counts) in enumerate(summary['policies'].items()):
        y=225+index*170;text(45,y,policy.replace('_',' '),27)
        total=max(1,counts['assigned']);x=45
        for category,color in colors.items():
            width=1400*counts[category]/total
            if width:d.rectangle((x,y+45,x+width,y+90),fill=color)
            x+=width
        text(45,y+105,' | '.join(f'{k}: {counts[k]}' for k in colors),21)
    text(45,770,f"Selective fallback: {summary['rescues']} correct rescues; {summary['introduced_wrong_accepts']} wrong accepts introduced",26)
    text(45,820,f"Same wrong value from both readers: {summary['same_wrong_value']} | trace status: {summary['trace_status']}",24)
    text(45,880,'Unit: receipt. Policy replays share OCR observations; they are not independent samples.',22)
    text(45,925,'Native compute includes both readers; selective service-time estimates are not throughput measurements.',21)
    image.save(path)
