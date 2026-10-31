#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using U=uint32_t; using Q=uint64_t;
struct Params {int kind; U a,b,ta,tb; std::array<U,8> m,p,q;};
const std::string alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_";
U key(const Params &p,int i,U c) {
  U x=c^p.m[i];
  if ((p.kind==2 && (i&1)) || (p.kind==3 && !(i&1))) x=(c+p.p[i])&255;
  return x+257+65*i;
}
U qbyte(const Params &p,int i,U c) {return (c^p.m[i])^((c+p.p[i])&255)^p.q[i];}
U rbyte(const Params &p,int i,U c) {return (qbyte(p,i,c)+c)&255;}
void forward(U &a,U &b,U k,int i) {
  a=std::rotl((a^k)+b,5+i%7);
  b=a^std::rotl(b+(a^k),11+i%5);
}
void backward(U &a,U &b,U k,int i) {
  b=std::rotr(b^a,11+i%5)-(a^k);
  a=(std::rotr(a,5+i%7)-b)^k;
}
Q left(const Params&p,U chars) {
  U a=p.a,b=p.b,q=0;
  for(int i=0;i<4;i++) {
    U c=(chars>>(8*i))&255,k=key(p,i,c);
    q|=qbyte(p,i,c)<<(8*i);
    if (p.kind==0) forward(a,b,k,i);
    if (p.kind==2) a=std::rotl(a^(b+k),5+i);
    if (p.kind==3) a=std::rotl(a+k,9+i)^(b^k);
  }
  return Q(a)|(Q(p.kind==0?b:q)<<32);
}
Q right(const Params&p,U chars) {
  U a=p.ta,b=p.tb;
  if (p.kind==0) {
    for(int i=7;i>=4;i--) backward(a,b,key(p,i,(chars>>(8*(i-4)))&255),i);
    return Q(a)|(Q(b)<<32);
  }
  U r=0;
  for(int i=4;i<8;i++) r|=rbyte(p,i,(chars>>(8*(i-4)))&255)<<(8*(i-4));
  a^=r;b=p.b;
  for(int i=4;i<8;i++) {
    U k=key(p,i,(chars>>(8*(i-4)))&255);
    if (p.kind==2) b=std::rotl(b+k,13+i%7)^a;
    if (p.kind==3) b=std::rotl(b^k,11+i%5)+(a^k);
  }
  return Q(a)|(Q(b^p.tb)<<32);
}
Q hash(Q x) {x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;x*=0x94d049bb133111ebULL;return x^(x>>31);}
std::string str(U x) {std::string s(4,' ');for(int i=0;i<4;i++)s[i]=char(x>>(8*i));return s;}
int main(int argc,char**argv) {
  std::ifstream in("cc3_mitm_params.txt");std::array<Params,8> ps;
  for(auto&p:ps){in>>p.kind>>p.a>>p.b>>p.ta>>p.tb;for(auto&x:p.m)in>>x;for(auto&x:p.p)in>>x;for(auto&x:p.q)in>>x;}
  if(!in){std::cerr<<"Invalid parameters\n";return 1;}
  const size_t cap=1ULL<<25,mask=cap-1;
  std::vector<Q> keys(cap);std::vector<U> vals(cap);
  for(int arg=1;arg<argc;arg++) {
    int block=std::stoi(argv[arg]);const auto&p=ps.at(block);
    if(p.kind==1){std::cerr<<"Unsupported family 1\n";return 2;}
    std::fill(vals.begin(),vals.end(),0);
    auto start=std::chrono::steady_clock::now();
    for(U a:alphabet)for(U b:alphabet)for(U c:alphabet)for(U d:alphabet) {
      U chars=a|(b<<8)|(c<<16)|(d<<24);Q k=left(p,chars);size_t pos=hash(k)&mask;
      while(vals[pos])pos=(pos+1)&mask;
      keys[pos]=k;vals[pos]=chars;
    }
    std::cerr<<"Block "<<block<<": forward table built\n";
    size_t found=0;
    for(U a:alphabet)for(U b:alphabet)for(U c:alphabet)for(U d:alphabet) {
      U chars=a|(b<<8)|(c<<16)|(d<<24);Q k=right(p,chars);size_t pos=hash(k)&mask;
      while(vals[pos]) {
        if(keys[pos]==k) {found++;std::cout<<"{\"block\":"<<block<<",\"value\":\""<<str(vals[pos])<<str(chars)<<"\"}\n"<<std::flush;}
        pos=(pos+1)&mask;
      }
    }
    auto seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    std::cerr<<"Block "<<block<<": "<<found<<" candidates; "<<seconds<<" seconds\n";
  }
}
