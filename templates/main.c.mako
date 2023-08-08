#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define OPTIMIZER_HIDE_VAR(var) __asm__ __volatile__("" : "=r" (var) : "0" (var))
#define OPTIMIZER_BARRIER() __asm__ __volatile__("" ::: "memory", "cc")

extern int ${tested_function}(${', '.join(tested_arguments)});

%if check_calling_convention:
    #define MAGIC_0 ${random_magic_number_generator()}L
    #define MAGIC_1 ${random_magic_number_generator()}L
    #define MAGIC_2 ${random_magic_number_generator()}L
    #define MAGIC_3 ${random_magic_number_generator()}L
    #define MAGIC_4 ${random_magic_number_generator()}L
    #define MAGIC_5 ${random_magic_number_generator()}L
    #define MAGIC_6 ${random_magic_number_generator()}L
    #define MAGIC_7 ${random_magic_number_generator()}L
    #define MAGIC_8 ${random_magic_number_generator()}L
    #define MAGIC_9 ${random_magic_number_generator()}L
    #define MAGIC_10 ${random_magic_number_generator()}L
% endif

int main(int argc, char *argv[]) {
    /* Usage: ./main <testid> */
    if (argc != 2) {
        return 1;
    }

    int test_id = atoi(argv[1]);

    /* For loop inside the branch so we minimize the overhead for the loop */
    % for test_id, test in enumerate(plan.tests):
        if (test_id == ${test_id}) {
            % if check_calling_convention:
                #ifdef __x86_64__
                    register long rbx __asm__("%rbx");
                    register long r12 __asm__("%r12");
                    register long r13 __asm__("%r13");
                    register long r14 __asm__("%r14");
                    register long r15 __asm__("%r15");
                    rbx = MAGIC_0;
                    r12 = MAGIC_1;
                    r13 = MAGIC_2;
                    r14 = MAGIC_3;
                    r15 = MAGIC_4;
                    OPTIMIZER_HIDE_VAR(rbx);
                    OPTIMIZER_HIDE_VAR(r12);
                    OPTIMIZER_HIDE_VAR(r13);
                    OPTIMIZER_HIDE_VAR(r14);
                    OPTIMIZER_HIDE_VAR(r15);
                    long rbp_backup;
                    __asm__ __volatile__("movq %%rbp, %0" : "=r" (rbp_backup));
                    OPTIMIZER_HIDE_VAR(rbp_backup);
                    (void) ${tested_function}(${format_arguments(test.arguments)});
                    OPTIMIZER_BARRIER();
                    long rbp_current;
                    __asm__ __volatile__("movq %%rbp, %0" : "=r" (rbp_current));
                    long rbx_current = rbx;
                    long r12_current = r12;
                    long r13_current = r13;
                    long r14_current = r14;
                    long r15_current = r15;
                    int count = 0;
                    count += rbx_current != MAGIC_0;
                    count += r12_current != MAGIC_1;
                    count += r13_current != MAGIC_2;
                    count += r14_current != MAGIC_3;
                    count += r15_current != MAGIC_4;
                    count += rbp_current != rbp_backup;
                    if (count > 0) {
                        fprintf(stderr, "%d register%s: ", count, count > 1 ? "s" : "");
                        if (rbx_current != MAGIC_0) { fprintf(stderr, "rbx"); if (--count > 0) fprintf(stderr, ", "); }
                        if (r12_current != MAGIC_1) { fprintf(stderr, "r12"); if (--count > 0) fprintf(stderr, ", "); }
                        if (r13_current != MAGIC_2) { fprintf(stderr, "r13"); if (--count > 0) fprintf(stderr, ", "); }
                        if (r14_current != MAGIC_3) { fprintf(stderr, "r14"); if (--count > 0) fprintf(stderr, ", "); }
                        if (r15_current != MAGIC_4) { fprintf(stderr, "r15"); if (--count > 0) fprintf(stderr, ", "); }
                        if (rbp_current != rbp_backup) { fprintf(stderr, "rbp"); }
                    }
                #elif defined(__i386__)
                    register int ebx __asm__("%ebx");
                    register int esi __asm__("%esi");
                    register int edi __asm__("%edi");
                    ebx = (int) MAGIC_0;
                    esi = (int) MAGIC_1;
                    edi = (int) MAGIC_2;
                    OPTIMIZER_HIDE_VAR(ebx);
                    OPTIMIZER_HIDE_VAR(esi);
                    OPTIMIZER_HIDE_VAR(edi);
                    int ebp_backup;
                    __asm__ __volatile__("movl %%ebp, %0" : "=r" (ebp_backup));
                    OPTIMIZER_HIDE_VAR(ebp_backup);
                    (void) ${tested_function}(${format_arguments(test.arguments)});
                    OPTIMIZER_BARRIER();
                    int ebp_current;
                    __asm__ __volatile__("movl %%ebp, %0" : "=r" (ebp_current));
                    int ebx_current = ebx;
                    int esi_current = esi;
                    int edi_current = edi;
                    int count = 0;
                    count += ebx_current != (int) MAGIC_0;
                    count += esi_current != (int) MAGIC_1;
                    count += edi_current != (int) MAGIC_2;
                    count += ebp_current != ebp_backup;
                    if (count > 0) {
                        fprintf(stderr, "%d register%s: ", count, count > 1 ? "s" : "");
                        if (ebx_current != (int) MAGIC_0) { fprintf(stderr, "ebx"); if (--count > 0) fprintf(stderr, ", "); }
                        if (esi_current != (int) MAGIC_1) { fprintf(stderr, "esi"); if (--count > 0) fprintf(stderr, ", "); }
                        if (edi_current != (int) MAGIC_2) { fprintf(stderr, "edi"); if (--count > 0) fprintf(stderr, ", "); }
                        if (ebp_current != ebp_backup) { fprintf(stderr, "ebp"); }
                    }
                #elif defined(__arm__)
                    register int r4 __asm__("%r4");
                    register int r5 __asm__("%r5");
                    register int r6 __asm__("%r6");
                    register int r7 __asm__("%r7");
                    register int r8 __asm__("%r8");
                    register int r9 __asm__("%r9");
                    register int r10 __asm__("%r10");
                    register int r11 __asm__("%r11");
                    r4 = (int) MAGIC_7;
                    r5 = (int) MAGIC_0;
                    r6 = (int) MAGIC_1;
                    r7 = (int) MAGIC_2;
                    r8 = (int) MAGIC_3;
                    r9 = (int) MAGIC_4;
                    r10 = (int) MAGIC_5;
                    r11 = (int) MAGIC_6;
                    OPTIMIZER_HIDE_VAR(r4);
                    OPTIMIZER_HIDE_VAR(r5);
                    OPTIMIZER_HIDE_VAR(r6);
                    OPTIMIZER_HIDE_VAR(r7);
                    OPTIMIZER_HIDE_VAR(r8);
                    OPTIMIZER_HIDE_VAR(r9);
                    OPTIMIZER_HIDE_VAR(r10);
                    OPTIMIZER_HIDE_VAR(r11);
                    (void) ${tested_function}(${format_arguments(test.arguments)});
                    OPTIMIZER_BARRIER();
                    int r4_current = r4;
                    int r5_current = r5;
                    int r6_current = r6;
                    int r7_current = r7;
                    int r8_current = r8;
                    int r9_current = r9;
                    int r10_current = r10;
                    int r11_current = r11;
                    int count = 0;
                    count += r4_current != (int) MAGIC_7;
                    count += r5_current != (int) MAGIC_0;
                    count += r6_current != (int) MAGIC_1;
                    count += r7_current != (int) MAGIC_2;
                    count += r8_current != (int) MAGIC_3;
                    count += r9_current != (int) MAGIC_4;
                    count += r10_current != (int) MAGIC_5;
                    count += r11_current != (int) MAGIC_6;
                    if (count > 0) {
                        fprintf(stderr, "%d register%s: ", count, count > 1 ? "s" : "");
                        if (r4_current != (int) MAGIC_7) { fprintf(stderr, "r4"); if (--count > 0) fprintf(stderr, ", "); }
                        if (r5_current != (int) MAGIC_0) { fprintf(stderr, "r5"); if (--count > 0) fprintf(stderr, ", "); }
                        if (r6_current != (int) MAGIC_1) { fprintf(stderr, "r6"); if (--count > 0) fprintf(stderr, ", "); }
                        if (r7_current != (int) MAGIC_2) { fprintf(stderr, "r7"); if (--count > 0) fprintf(stderr, ", "); }
                        if (r8_current != (int) MAGIC_3) { fprintf(stderr, "r8"); if (--count > 0) fprintf(stderr, ", "); }
                        if (r9_current != (int) MAGIC_4) { fprintf(stderr, "r9"); if (--count > 0) fprintf(stderr, ", "); }
                        if (r10_current != (int) MAGIC_5) { fprintf(stderr, "r10"); if (--count > 0) fprintf(stderr, ", "); }
                        if (r11_current != (int) MAGIC_6) { fprintf(stderr, "r11"); }
                    }
                #elif defined(__aarch64__)
                    register long x19 __asm__("%x19");
                    register long x20 __asm__("%x20");
                    register long x21 __asm__("%x21");
                    register long x22 __asm__("%x22");
                    register long x23 __asm__("%x23");
                    register long x24 __asm__("%x24");
                    register long x25 __asm__("%x25");
                    register long x26 __asm__("%x26");
                    register long x27 __asm__("%x27");
                    register long x28 __asm__("%x28");
                    register long x29 __asm__("%x29");
                    x19 = MAGIC_10;
                    x20 = MAGIC_0;
                    x21 = MAGIC_1;
                    x22 = MAGIC_2;
                    x23 = MAGIC_3;
                    x24 = MAGIC_4;
                    x25 = MAGIC_5;
                    x26 = MAGIC_6;
                    x27 = MAGIC_7;
                    x28 = MAGIC_8;
                    x29 = MAGIC_9;
                    OPTIMIZER_HIDE_VAR(x19);
                    OPTIMIZER_HIDE_VAR(x20);
                    OPTIMIZER_HIDE_VAR(x21);
                    OPTIMIZER_HIDE_VAR(x22);
                    OPTIMIZER_HIDE_VAR(x23);
                    OPTIMIZER_HIDE_VAR(x24);
                    OPTIMIZER_HIDE_VAR(x25);
                    OPTIMIZER_HIDE_VAR(x26);
                    OPTIMIZER_HIDE_VAR(x27);
                    OPTIMIZER_HIDE_VAR(x28);
                    OPTIMIZER_HIDE_VAR(x29);
                    (void) ${tested_function}(${format_arguments(test.arguments)});
                    OPTIMIZER_BARRIER();
                    long x19_current = x19;
                    long x20_current = x20;
                    long x21_current = x21;
                    long x22_current = x22;
                    long x23_current = x23;
                    long x24_current = x24;
                    long x25_current = x25;
                    long x26_current = x26;
                    long x27_current = x27;
                    long x28_current = x28;
                    long x29_current = x29;
                    long count = 0;
                    count += x19_current != MAGIC_10;
                    count += x20_current != MAGIC_0;
                    count += x21_current != MAGIC_1;
                    count += x22_current != MAGIC_2;
                    count += x23_current != MAGIC_3;
                    count += x24_current != MAGIC_4;
                    count += x25_current != MAGIC_5;
                    count += x26_current != MAGIC_6;
                    count += x27_current != MAGIC_7;
                    count += x28_current != MAGIC_8;
                    count += x29_current != MAGIC_9;
                    if (count > 0) {
                        fprintf(stderr, "%d register%s: ", count, count > 1 ? "s" : "");
                        if (x19_current != MAGIC_10) { fprintf(stderr, "x19"); if (--count > 0) fprintf(stderr, ", "); }
                        if (x20_current != MAGIC_0) { fprintf(stderr, "x20"); if (--count > 0) fprintf(stderr, ", "); }
                        if (x21_current != MAGIC_1) { fprintf(stderr, "x21"); if (--count > 0) fprintf(stderr, ", "); }
                        if (x22_current != MAGIC_2) { fprintf(stderr, "x22"); if (--count > 0) fprintf(stderr, ", "); }
                        if (x23_current != MAGIC_3) { fprintf(stderr, "x23"); if (--count > 0) fprintf(stderr, ", "); }
                        if (x24_current != MAGIC_4) { fprintf(stderr, "x24"); if (--count > 0) fprintf(stderr, ", "); }
                        if (x25_current != MAGIC_5) { fprintf(stderr, "x25"); if (--count > 0) fprintf(stderr, ", "); }
                        if (x26_current != MAGIC_6) { fprintf(stderr, "x26"); if (--count > 0) fprintf(stderr, ", "); }
                        if (x27_current != MAGIC_7) { fprintf(stderr, "x27"); if (--count > 0) fprintf(stderr, ", "); }
                        if (x28_current != MAGIC_8) { fprintf(stderr, "x28"); if (--count > 0) fprintf(stderr, ", "); }
                        if (x29_current != MAGIC_9) { fprintf(stderr, "x29"); }
                    }
                #endif
                fflush(stderr);
                OPTIMIZER_BARRIER();
            % endif

            int result;
            for (int i = 0; i < ${test_iterations}; ++i) {
                result = ${tested_function}(${format_arguments(test.arguments)});
            }
            printf("%d", result);
        }
    % endfor

    fflush(stdout);
    return 0;
}
