/* SCHR-Bench controlled-function research suite. Pure local logic; no OS modifications. */
#if defined(_MSC_VER)
#define KEEP __declspec(noinline)
#else
#define KEEP __attribute__((noinline))
#endif

KEEP int target(int a,int b,int c) { unsigned key=(((unsigned)a<<1)+(unsigned)b)&255U; unsigned v=((unsigned)c^key)&255U; return v==0x4dU; }
