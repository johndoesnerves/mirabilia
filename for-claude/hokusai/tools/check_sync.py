import numpy as np, subprocess, sys
SR=16000
def onsets(path):
    raw=subprocess.run(['ffmpeg','-v','error','-i',path,'-ac','1','-ar',str(SR),'-f','s16le','-'],capture_output=True).stdout
    x=np.frombuffer(raw,np.int16).astype(float)/32768
    hop=160; rms=np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2)) for i in range(len(x)//hop)])
    v=rms>10**(-35/20); out=[]; i=0
    while i<len(v):
        if v[i] and v[i:i+8].mean()>0.8 and (i<15 or not v[i-15:i].any()): out.append(i*hop/SR); i+=8
        else: i+=1
    return np.array(out)
o=onsets(sys.argv[1]); f=onsets(sys.argv[2])
d=[f[np.argmin(abs(f-t/1.3))]-t/1.3 for t in o]
d=np.array(d); print(sys.argv[2].split('/')[-1], 'onsets', len(o), 'max |diff| %.3f  median %.3f' % (np.max(np.abs(d)), np.median(d)))
