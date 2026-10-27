/* SCHR-Bench controlled-function research suite. Pure local logic; no OS modifications. */
#if defined(_MSC_VER)
#define KEEP __declspec(noinline)
#else
#define KEEP __attribute__((noinline))
#endif

KEEP int target(int a,int b,int c) { (void)c; unsigned x=((unsigned)a^0x17U)&255U; unsigned y=((unsigned)b^0x26U)&255U; return x==67U && y==84U; }
