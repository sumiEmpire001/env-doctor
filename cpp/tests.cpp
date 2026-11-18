#include "core.hpp"
#include <cassert>
int main(){using namespace embedded_env;
 assert(check(nullptr,NonEmpty)==Missing);
 assert(check("42",Integer)==Valid);
 assert(check("12x",Integer)==Malformed);
 assert(check("999999999999999999999999999",Integer)==Malformed);
 assert(check("true",Boolean)==Valid);
 assert(check("yes",Boolean)==Malformed);
 assert(check("https://example.org",HttpUrl)==Valid);
 assert(check("ftp://example.org",HttpUrl)==Malformed);
 assert(check("abc",NonEmpty,2)==Malformed);
}