/* SCHR-Bench controlled-function research suite. Pure local logic; no OS modifications. */
#if defined(_MSC_VER)
#define KEEP __declspec(noinline)
#else
#define KEEP __attribute__((noinline))
#endif

KEEP int target(int a, int b, int c) {
    volatile int _mba_mask = (b & ~b);
    (void)_mba_mask;
    (void)c; return a>b?1:0; 
}
