#include <string.h>
#include <stdio.h>


const int order = 16;
const unsigned long polynom = 0x1021;
const unsigned long crcinit = 0x0000;
const unsigned long crcxor = 0x0000;
const int refin = 1;
const int refout = 1;

unsigned long crcmask;
unsigned long crchighbit;
unsigned long crcinit_nondirect;

unsigned long reflect(unsigned long crc, int bitnum) {
	unsigned long i, j=1, crcout=0;

	for (i=(unsigned long)1<<(bitnum-1); i; i>>=1) {
		if (crc & i) crcout|=j;
		j<<= 1;
	}
	return (crcout);
}

void init_values() {
    int i;
	unsigned long bit, crc;

	crcmask = ((((unsigned long)1<<(order-1))-1)<<1)|1;
	crchighbit = (unsigned long)1<<(order-1);

    crcinit_nondirect = crcinit;
    crc = crcinit;
    for (i=0; i<order; i++) {

        bit = crc & crchighbit;
        crc<<= 1;
        if (bit) crc^= polynom;
    }
    crc&= crcmask;
}

unsigned long crcbitbybit(unsigned char* p, unsigned long len) {

    init_values();

	unsigned long i, j, c, bit;
	unsigned long crc = crcinit_nondirect;

	for (i=0; i<len; i++) {

		c = (unsigned long)*p++;
		if (refin) c = reflect(c, 8);

		for (j=0x80; j; j>>=1) {

			bit = crc & crchighbit;
			crc<<= 1;
			if (c & j) crc|= 1;
			if (bit) crc^= polynom;
		}
	}	

	for (i=0; i<order; i++) {

		bit = crc & crchighbit;
		crc<<= 1;
		if (bit) crc^= polynom;
	}

	if (refout) crc=reflect(crc, order);
	crc^= crcxor;
	crc&= crcmask;

	return(crc);
}

