import sys, numpy as np
from PIL import Image, ImageFilter, ImageDraw
S=sys.argv[1]; OUT=sys.argv[2]
tracks={
 'dark': ({114:(1478,700),120:(1535,716),126:(1605,726),132:(1695,747),138:(1822,770),144:(1950,793)}, 116, 142),
 'white':({90:(1428,695),96:(1482,704),102:(1537,713),108:(1592,722),114:(1672,733),120:(1770,745),124:(1853,756),128:(1936,767)}, 90, 127),
}
def interp(k,f):
    ks=sorted(k)
    for a,b in zip(ks,ks[1:]):
        if a<=f<=b:
            t=(f-a)/(b-a); return (k[a][0]+(k[b][0]-k[a][0])*t, k[a][1]+(k[b][1]-k[a][1])*t)
done=0
for f in range(90,145):
    im=Image.open(f"{S}/orig/frame_{f:04d}.webp").convert('RGB'); changed=False
    for name,(k,f0,f1) in tracks.items():
        if not (f0<=f<=f1): continue
        x,y=interp(k,f)
        if x>1920+10: continue
        r = 9 + (f-f0)/(f1-f0)*9   # grows with the push-in
        R=int(r*3)
        box=(int(x-R),int(y-R),int(x+R),int(y+R))
        box=(max(0,box[0]),max(0,box[1]),min(1920,box[2]),min(1080,box[3]))
        c=im.crop(box)
        size=int(r*2)|1
        fill=c.filter(ImageFilter.MedianFilter(min(size,31))).filter(ImageFilter.GaussianBlur(1.5))
        m=Image.new('L',c.size,0); d=ImageDraw.Draw(m)
        cx,cy=x-box[0],y-box[1]
        d.ellipse([cx-r*0.8,cy-r*1.15,cx+r*0.8,cy+r*1.15],fill=255)
        m=m.filter(ImageFilter.GaussianBlur(r*0.3))
        c.paste(fill,(0,0),m); im.paste(c,box[:2]); changed=True
    if changed:
        im.save(f"{OUT}/frame_{f:04d}.webp",quality=82,method=6); done+=1
print('patched',done)
