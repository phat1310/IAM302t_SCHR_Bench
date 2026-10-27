/* SCHR-Bench controlled-function research suite. Pure local logic; no OS modifications. */
#if defined(_MSC_VER)
#define KEEP __declspec(noinline)
#else
#define KEEP __attribute__((noinline))
#endif

KEEP int target(int a,int b,int c) { int s=a&3; for(int i=0;i<3;i++) { if((b>>i)&1) s=(s+1)&3; else s=(s^1)&3; } return s==c; }
