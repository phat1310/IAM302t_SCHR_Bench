/* SCHR-Bench controlled-function research suite. Pure local logic; no OS modifications. */
#if defined(_MSC_VER)
#define KEEP __declspec(noinline)
#else
#define KEEP __attribute__((noinline))
#endif

KEEP int target(int a,int b,int c) { (void)b;(void)c; int n=0; for(int i=0;i<a && i<32;i++) n+=(i&1); return n; }
