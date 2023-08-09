#include <stdio.h>
#include <stdint.h>

/* TODO: ability to provide types */
extern int ${tested_function}();

int main(int argc, char *argv[]) {
    /* Usage: ./main <testid> */
    if (argc != 2) {
        return 1;
    }

    int test_id = atoi(argv[1]);

    /* For loop inside the branch so we minimize the overhead for the loop */
    % for test_id, test in enumerate(plan.tests):
        if (test_id == ${test_id}) {
            int result;
            for (int i = 0; i < ${test_iterations}; ++i) {
                result = narayana(${', '.join(map(str, test.arguments))});
            }
            printf("%d", result);
        }
    % endfor

    fflush(stdout);
    return 0;
}
