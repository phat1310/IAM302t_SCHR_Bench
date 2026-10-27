/* SCHR-Bench controlled-function research suite. Pure local logic; no OS modifications. */
#if defined(_MSC_VER)
#define KEEP __declspec(noinline)
#else
#define KEEP __attribute__((noinline))
#endif

KEEP int target(int a,int b,int c) { (void)c; unsigned x=(unsigned)a^0x6dU; x=(x+((unsigned)b&7U))&255U; return x==0x5eU; }
