/* SCHR-Bench controlled-function research suite. Pure local logic; no OS modifications. */
#if defined(_MSC_VER)
#define KEEP __declspec(noinline)
#else
#define KEEP __attribute__((noinline))
#endif

__attribute__((noinline)) static int mock_add(int state) { return state|1; }
__attribute__((noinline)) static int mock_remove(int state) { return state&~1; }
KEEP int target(int a,int b,int c) { (void)b;(void)c; return mock_remove(a); }
