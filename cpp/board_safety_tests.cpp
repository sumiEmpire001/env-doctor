#include "core.hpp"
#include <cassert>
int main(){
 using namespace embedded_env;
 assert(check("0",Integer)==Valid);
 assert(check("-42",Integer)==Valid);
 assert(check("+",Integer)==Malformed);
 assert(check("1.5",Integer)==Malformed);
 assert(check("FALSE",Boolean)==Malformed);
 assert(check("https://",HttpUrl)==Malformed);
 assert(check("https://example.org/path",HttpUrl)==Valid);
 assert(check("https://example.org bad",HttpUrl)==Malformed);
 assert(check("https://user@example.org",HttpUrl)==Malformed);
 assert(check("https://example.org\\\\bad",HttpUrl)==Malformed);
 assert(check("https:///missing-host",HttpUrl)==Malformed);
 assert(check("ftp://example.com",HttpUrl)==Malformed);
 assert(check("",NonEmpty)==Missing);
 assert(check("ok",NonEmpty,0)==InvalidRule);
 assert(check("ok",(Kind)99)==InvalidRule);
}