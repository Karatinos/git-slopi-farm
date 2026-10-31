"""Pure model of cybercup.sys capability API (RVA 0x315c) and ticket math.
This models state transitions for user-mode emulation; timeouts/locking omitted.
"""
MASK = (1 << 64) - 1

def rol(x, n, bits=64):
    mask=(1 << bits)-1
    return ((x << n) | (x >> (bits-n))) & mask

def siphash24(key0, key1, word0, word1, word2):
    v=[key0 ^ 0x736f6d6570736575, key1 ^ 0x646f72616e646f6d,
       key0 ^ 0x6c7967656e657261, key1 ^ 0x7465646279746573]
    def rnd():
        v[0]=(v[0]+v[1]) & MASK; v[1]=rol(v[1],13)^v[0]; v[0]=rol(v[0],32)
        v[2]=(v[2]+v[3]) & MASK; v[3]=rol(v[3],16)^v[2]
        v[0]=(v[0]+v[3]) & MASK; v[3]=rol(v[3],21)^v[0]
        v[2]=(v[2]+v[1]) & MASK; v[1]=rol(v[1],17)^v[2]; v[2]=rol(v[2],32)
    for m in [word0,word1,word2,0x1800000000000000]:
        v[3]^=m
        rnd();rnd()
        v[0]^=m
    v[2]^=0xff
    for _ in range(4): rnd()
    return v[0]^v[1]^v[2]^v[3]

def ticket_transform(operation, value):
    assert operation in (0x2077,0x2078)
    return (rol((value & 0xffffffff)^0xa3c59ac3,9,32) + operation*0x045d9f3b) & 0xffffffff

class Capabilities:
    def __init__(self,key0=0,key1=0):
        self.key=(key0,key1);self.counter=0;self.sessions={}
    def hash(self,*words): return siphash24(*self.key,*words)
    def token(self,x): return (x & 0x7ffffffffffffffd)|2
    def call(self,pid,op,arg=0,token=0,extra=0):
        if op==0x30ff and not arg and not token:return 0x10000
        if op==0x30fe and not arg and not token:return 0xf
        if op==0x3000 and arg and not token:
            self.counter+=1
            token=self.token(self.hash(self.counter,pid,arg^0x4846564c4f50454e))
            self.sessions[pid,token]={'nonce':arg,'state':self.hash(token,pid,arg),'step':1,'code':0,'code2':0,'pred':0}
            return token
        allowed=(0x3001,0x3002,0x3003,0x3010,0x3011,0x3021,0x3030,0x3040,0x3041)
        s=self.sessions.get((pid,token))
        if op not in allowed or not s:return MASK
        if op in (0x3010,0x3040):
            which='code' if op==0x3010 else 'code2'
            if extra or arg < 0x10000 or arg > 0x7fffffffffff or s[which]:return MASK
            s[which]=arg;return 0
        if op==0x3030:
            if extra or s['step']==1 or s['pred']:return MASK
            s['pred']=1
            return self.hash(s['state'],arg^0x4856505245443031,token)&3
        if op in (0x3002,0x3003):
            if op==0x3002 and s['step']<=1:return MASK
            del self.sessions[pid,token];return 0
        if op==0x3011 and (not extra or s['code']!=extra):return MASK
        if op==0x3041 and (not extra or s['code2']!=extra):return MASK
        if op==0x3021 and extra!=MASK:return MASK
        if arg>>32!=s['step'] or s['step']>4:return MASK
        s['state']=self.hash(s['state'],arg,token^s['nonce'])
        new=self.token(self.hash(s['state'],token,0x4846564c53544550))
        if new==token:new^=4
        s['step']+=1;s['code']=s['code2']=s['pred']=0
        del self.sessions[pid,token];self.sessions[pid,new]=s
        return new

class CheckSessions(Capabilities):
    """Nine-step choice API at driver RVA 0x2e64; opaque token remains fixed."""
    def call(self,pid,op,arg=0,token=0,process=None):
        owner=pid if process is None else (pid,process)
        if op==0x305f and not arg and not token:return 0x10000
        if op==0x3050 and arg and not token:
            self.counter+=1
            token=self.token(self.hash(self.counter,pid,arg^0x434845434b4f504e))
            self.sessions[owner,token]={'nonce':arg,'state':self.hash(token,pid,arg),'step':0,'lastarg':0,'lastresult':0}
            return token
        s=self.sessions.get((owner,token))
        if not 0x3051<=op<=0x305b or not s:return MASK
        if op in (0x305a,0x305b):
            result=0 if op==0x305b or (not arg and s['step']==9) else MASK
            del self.sessions[owner,token]
            return result
        step=op-0x3051
        if step+1==s['step'] and arg==s['lastarg']:return s['lastresult']
        if step!=s['step'] or step>=9:return MASK
        s['state']=self.hash(s['state'],arg,(0x434845434b535445+step)^s['nonce'])
        result=(s['state']^(s['state']>>32))&3
        s['step']+=1;s['lastarg']=arg;s['lastresult']=result
        return result

class Tickets:
    """Ticket/version services from RVA 0x36c4; expiration omitted."""
    def __init__(self):self.counter=0;self.sessions={}
    def call(self,pid,op,arg=0,token=0):
        if op==0:return 0x20000
        if op==1 and arg==0x2077 and not token:
            self.counter=(self.counter+1)&MASK
            if self.counter in (0,MASK):self.counter=(self.counter+1)&MASK
            self.sessions[pid,self.counter]=2
            return self.counter
        state=self.sessions.get((pid,token))
        if not state:return MASK
        if op==2:del self.sessions[pid,token];return 0
        if op==0x2077 and state==2:
            self.sessions[pid,token]=4
            return ticket_transform(op,arg)
        if op==0x2078 and state==4:
            del self.sessions[pid,token]
            return ticket_transform(op,arg)
        return MASK
