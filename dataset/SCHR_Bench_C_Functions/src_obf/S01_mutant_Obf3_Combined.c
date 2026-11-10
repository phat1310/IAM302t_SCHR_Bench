/* SCHR-Bench controlled-function research suite. Pure local logic; no OS modifications. */
#if defined(_MSC_VER)
#define KEEP __declspec(noinline)
#else
#define KEEP __attribute__((noinline))
#endif

KEEP int target(int a, int b, int c) {
    volatile unsigned int _dispatch = (((unsigned int)a * ((unsigned int)a + 1U)) & 1U) ^ 0x7f01U;
    while (_dispatch != 0U) {
        if (_dispatch == 0x7f01U) {
            (void)b;(void)c; return ((a^0x2b)&255)==0x41; 
        }
        _dispatch = 0U;
    }
    return 0;
}
