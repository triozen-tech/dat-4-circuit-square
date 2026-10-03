import sys
from PIL import Image, ImageDraw
S=sys.argv[1]; out=sys.argv[2]; items=[tuple(map(int,a.split(','))) for a in sys.argv[3:]]
tiles=[]
for f,cx,cy in items:
    im=Image.open(f"{S}/orig/frame_{f:04d}.webp").convert('RGB')
    x0,y0=cx-100,cy-75
    c=im.crop((x0,y0,x0+200,y0+150)).resize((600,450),Image.NEAREST)
    d=ImageDraw.Draw(c)
    for gx in range((x0//10+1)*10, x0+200, 10):
        X=(gx-x0)*3; d.line([(X,0),(X,450)],fill=(255,0,0) if gx%50==0 else (255,160,160),width=2 if gx%50==0 else 1)
    for gy in range((y0//10+1)*10, y0+150, 10):
        Y=(gy-y0)*3; d.line([(0,Y),(600,Y)],fill=(0,160,255) if gy%50==0 else (160,210,255),width=2 if gy%50==0 else 1)
    d.rectangle([0,0,150,22],fill='black'); d.text((4,4),f"f{f} x0={x0} y0={y0}",fill='white')
    tiles.append(c)
W=Image.new('RGB',(1200,450*((len(tiles)+1)//2)),'white')
for i,t in enumerate(tiles): W.paste(t,((i%2)*600,(i//2)*450))
W.save(out)
