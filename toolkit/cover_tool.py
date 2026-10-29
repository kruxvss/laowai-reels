"""Reel cover (banner) maker: python3 cover_tool.py photo.jpg out.png "Line one" "serif red line" "中文" """
import sys
from PIL import Image, ImageDraw, ImageFilter
from reel_lib import *
BRAND=(196,28,28); WHITE=(255,255,255)
def make(photo, l1, l2, zh, out, tag="DID YOU KNOW  你知道吗"):
    tag = sys.argv[6] if len(sys.argv)>6 else tag
    if photo in (None,"none"):
        import numpy as np
        yy,xx=np.mgrid[0:H,0:W]; r=np.sqrt(((xx-540)/1000)**2+((yy-800)/1300)**2); k=np.clip(r,0,1)[...,None]
        c0=np.array([226,52,44]); c1=np.array([120,8,10]); arr=(c0*(1-k)+c1*k).astype("uint8"); im=Image.fromarray(arr).convert("RGBA")
    else:
        im=Image.open(photo).convert("RGB"); iw,ih=im.size; s=max(W/iw,H/ih)
        im=im.resize((int(iw*s)+1,int(ih*s)+1),Image.LANCZOS); x=(im.size[0]-W)//2; y=(im.size[1]-H)//2
        im=im.crop((x,y,x+W,y+H)).convert("RGBA")
    ov=Image.new("RGBA",(W,H)); d=ImageDraw.Draw(ov)
    for yy in range(H):
        a=int(70+130*(abs(yy-H*0.5)/(H*0.5))**1.5+60*max(0,1-abs(yy-900)/500)); d.line((0,yy,W,yy),fill=(110,8,8,min(235,a)))
    im.alpha_composite(ov); d=ImageDraw.Draw(im,"RGBA")
    # central 3:4 safe zone is y 240..1680
    tw=text_w(tag,36,"mono"); d.rounded_rectangle((540-tw/2-34,420,540+tw/2+34,490),35,fill=BRAND+(255,)); draw_text(d,540,466,tag,36,"mono",WHITE,"m")
    for txt,wt,sz,col,yy in zip(l1.split("|")+[l2],["extrabold"]*len(l1.split("|"))+["serif"],[106]*len(l1.split("|"))+[150],[WHITE]*len(l1.split("|"))+[(255,214,208)],[720+i*125 for i in range(len(l1.split("|")))]+[720+len(l1.split("|"))*125+15]):
        L,A=text_layer(txt,sz,wt,col); 
        # shadow
        sh=L.copy(); sh.putalpha(L.getchannel("A").point(lambda v:int(v*0.45))); sh=sh.filter(ImageFilter.GaussianBlur(10))
        im.alpha_composite(sh,(int(540-A[0]),int(yy-A[1]+8))); im.alpha_composite(L,(int(540-A[0]),int(yy-A[1])))
    L,A=text_layer(zh,54,"extrabold",(255,236,232)); im.alpha_composite(L,(int(540-A[0]),int(1200-A[1])))
    # wordmark chip
    d=ImageDraw.Draw(im,"RGBA"); a=text_w("laowai",64,"extrabold"); b=text_w("吗",64,"extrabold")
    d.rounded_rectangle((540-(a+b)/2-44,1380,540+(a+b)/2+44,1490),55,fill=(255,255,255,245))
    draw_text(d,540-(a+b)/2,1458,"laowai",64,"extrabold",(31,27,22)); draw_text(d,540-(a+b)/2+a,1458,"吗",64,"extrabold",BRAND)
    L,A=text_layer("laowai.ma",40,"bold",(255,236,232)); im.alpha_composite(L,(int(540-A[0]),int(1570-A[1])))
    im.convert("RGB").save(out)
if __name__=="__main__": make(*sys.argv[1:6])
