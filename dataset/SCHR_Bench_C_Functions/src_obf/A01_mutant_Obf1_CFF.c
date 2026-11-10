/* SCHR-Bench controlled-function research suite. Pure local logic; no OS modifications. */
#if defined(_MSC_VER)
#define KEEP __declspec(noinline)
#else
#define KEEP __attribute__((noinline))
#endif

KEEP int target(int a, int b, int c) {
    volatile int _cff_state = 0x37a1;
    while (_cff_state != 0) {
        if (_cff_state == 0x37a1) {
            _cff_state = 0x59b2;
        } else if (_cff_state == 0x59b2) {
            (void)b;(void)c; if(a==0) return 0; return 1; 
        }
    }
    return 0;
}
