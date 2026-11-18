#pragma once
#include <stddef.h>
#include <ctype.h>
#include <string.h>
#include <limits.h>
namespace embedded_env {
enum Result { Valid, Missing, Malformed, InvalidRule };
enum Kind { NonEmpty, Integer, Boolean, HttpUrl };
inline Result check(const char* value,Kind kind,size_t maxLength=256){
 if(!maxLength||maxLength>4096||kind<NonEmpty||kind>HttpUrl)return InvalidRule;
 if(!value||!*value)return Missing;
 const size_t n=strlen(value);if(n>maxLength)return Malformed;
 if(kind==NonEmpty)return Valid;
 if(kind==Boolean)return (!strcmp(value,"true")||!strcmp(value,"false")||!strcmp(value,"1")||!strcmp(value,"0"))?Valid:Malformed;
 if(kind==HttpUrl){
  const char* p=nullptr;
  if(!strncmp(value,"https://",8))p=value+8;
  else if(!strncmp(value,"http://",7))p=value+7;
  if(!p||!*p||*p=='/'||*p=='?'||*p=='#')return Malformed;
  const char* hostEnd=p;
  while(*hostEnd&&*hostEnd!='/'&&*hostEnd!='?'&&*hostEnd!='#'){
   const unsigned char ch=(unsigned char)*hostEnd;
   if(ch<=32||ch>=127||ch=='@'||ch==92)return Malformed;
   ++hostEnd;
  }
  if(hostEnd==p)return Malformed;
  for(const char* q=hostEnd;*q;++q){const unsigned char ch=(unsigned char)*q;if(ch<=32||ch>=127||ch==92)return Malformed;}
  return Valid;
 }
 size_t i=(value[0]=='-'||value[0]=='+')?1:0;
 if(i==n)return Malformed;
 unsigned long long acc=0;const bool neg=value[0]=='-';
 const unsigned long long limit=neg?(unsigned long long)LONG_MAX+1ULL:(unsigned long long)LONG_MAX;
 for(;i<n;++i){if(value[i]<'0'||value[i]>'9')return Malformed;
  unsigned digit=(unsigned)(value[i]-'0');if(acc>(limit-digit)/10ULL)return Malformed;acc=acc*10ULL+digit;}
 return Valid;
}
}