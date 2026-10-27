/* SCHR-Bench controlled-function research suite. Pure local logic; no OS modifications. */
#if defined(_MSC_VER)
#define KEEP __declspec(noinline)
#else
#define KEEP __attribute__((noinline))
#endif

KEEP int target(int a,int b,int c) { (void)c; int state=(a&1)?2:1; if(state==2 && b<5) return 0; return 1; }
