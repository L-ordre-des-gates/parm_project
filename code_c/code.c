#include "parm.h"
void run()
{
    BEGIN();
    int nombre = 1;
    while (nombre % 7 != 0) {
        nombre++;
    }
    RES = nombre;
    END();
}