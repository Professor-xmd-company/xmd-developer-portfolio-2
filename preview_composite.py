from PIL import Image, ImageDraw
import numpy as np, cv2, re, os
A='assets'; OUT='.'
def load(p): return Image.open(os.path.join(A,p)).convert('RGBA')

def wave_image(W,H,top,scale_name):
    s=open('/home/user/uploads/Star Wave.html').read()
    m=re.search(r'const D=\[(.*?)\];',s,re.S); D=list(map(int,m.group(1).split(',')))
    pal=re.search(r'const PAL=\[(.*?)\];',s,re.S).group(1)
    PAL=[x.strip().strip('"') for x in pal.split(',')]
    k=W/784.0
    img=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(img,'RGBA')
    for i in range(0,len(D),3):
        x=D[i]+.5;y=D[i+1]+.5;p=D[i+2]
        size=p//1000;col=PAL[(p%1000)//10];a=(p%10)/9
        col=tuple(int(col[j:j+2],16) for j in (1,3,5))
        al=min(1,a*1.35)
        X=x*k;Y=top+y*k;L=max(0.6,size/2*k)
        if size==0:
            rr=max(.6,.85*k);d.ellipse((X-rr,Y-rr,X+rr,Y+rr),fill=col+(int(255*al),))
        else:
            d.rectangle((X-L,Y-max(.5,k/2),X+L,Y+max(.5,k/2)),fill=col+(int(255*al),))
            d.rectangle((X-max(.5,k/2),Y-L,X+max(.5,k/2),Y+L),fill=col+(int(255*al),))
            if size>=8:
                al2=min(1,a*.9);d.rectangle((X-.9*k,Y-.9*k,X+.9*k,Y+.9*k),fill=(255,255,255,int(255*al2)))
    return img

def screen(bg,fg):
    b=np.asarray(bg).astype(np.float32)/255; f=np.asarray(fg).astype(np.float32)/255
    a=f[...,3:4]; rgb=1-(1-b[...,:3])*(1-f[...,:3])
    out=b[...,:3]*(1-a)+rgb*a
    return Image.fromarray((np.clip(out,0,1)*255).astype(np.uint8)).convert('RGBA')

for name,ref,size,top,portrait_box in [
    ('desktop','/home/user/uploads/file_000000005db08211b2da00fa115ebcd9.png',(1536,1024),134,(788,71)),
    ('mobile','/home/user/uploads/file_00000000524882119afd50bf0ad3a936.png',(1024,1536),430,(524,153))]:
    W,H=size
    comp=Image.new('RGBA',(W,H),(0,3,14,255))
    comp.alpha_composite(load(f'bg-{name}.png'))
    comp=screen(comp,load(f'wave-glow-{name}.png'))
    comp.alpha_composite(wave_image(W,H,0, name).crop((0,0,W,min(H,top+int(W*150/784))))) # placeholder
    # redraw with top included directly
    comp2=Image.new('RGBA',(W,H),(0,3,14,255));comp2.alpha_composite(load(f'bg-{name}.png'));comp2=screen(comp2,load(f'wave-glow-{name}.png'))
    wave=wave_image(W,H,0,name)
    # wave_image already includes top; move it to canvas via paste at top
    wave_full=Image.new('RGBA',(W,H),(0,0,0,0)); wave_full.paste(wave,(0,top))
    comp2.alpha_composite(wave_full)
    p=load(f'portrait-{name}.png'); comp2.alpha_composite(p,portrait_box)
    comp2.alpha_composite(load(f'overlay-{name}.png'))
    comp2.convert('RGB').save(f'composite-{name}.png')
    # side-by-side with reference
    refim=Image.open(ref).convert('RGB')
    side=Image.new('RGB',(W*2,H));side.paste(refim,(0,0));side.paste(comp2.convert('RGB'),(W,0));side.save(f'comparison-{name}.png')
print('done')
