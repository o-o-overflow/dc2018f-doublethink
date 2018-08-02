# babelcode

Babelcode is a polyglot challenge.

## Architectures

```
|	arch		|	CPU	|	deb	| ready	| Byte Width	| Word Width	| fs access	|	bin	|			notes					|
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DEC PDP-1		| PDP-1		| simh		| [X]	| 18		| 18		| No		|		|								|
| DEC PDP-8		| PDP-8		| simh		| [X]	| 12		| 12		| No		|		|								|
| DEC PDP-10		| PDP-10	| simh		| [X]	| 36		| 36		| No		|		|								|
| IBM 1401		| IBM 1401	| simh		| [X]	| 7		| 7		| No		|		| https://en.wikipedia.org/wiki/IBM\_1401			|
| Data General Nova	| Nova		| simh		| [X]	| 16		| 16		| No		|		|								|
| LGP-30		| LGP-30	| simh		| [X]	| 31		| 31		| No		|		|								|
| MIX			| MIX		| mdk		| [X]	| 6		| 30		| No		|		|								|
| MMIX			| MMIX		| 		| [X]	| 6		| 32		| Yes		|		|								|
| Hexagon		| Hexagon	|		| [X]	| 8		| 32		| Yes   	|		|								|
| RISC-V		| RISCV		|		| [X]	| 8		| 64		| Yes   	|		|								|
| cLEMENCy		| cLEMENCy	|		| [X]	| 9		| 27		| No	   	|		|								|
| AMD64			| AMD64		|		| [X]	| 8		| 64		| Yes	   	|		|								|
| 8051			|		| emu8051	|	|		| 		|       	|		|								|
| Atari2600		|		| stella	|	|		| 		|       	|		|								|
| Atari800		|		| atari800	|	|		| 		|       	|		|								|
| Commodore 64		|		|		|	|		| 		|       	|		|								|
| DEC PDP-11		|		| simh		|	|		| 		|       	|		|								|
| DEC PDP-15		|		| simh		|	|		| 		|       	|		|								|
| DEC PDP-4		|		| simh		|	|		| 		|       	|		|								|
| DEC PDP-7		|		| simh		|	|		| 		|       	|		|								|
| DEC PDP-9		|		| simh		|	|		| 		|       	|		|								|
| DEC VAX		|		| simh		|	|		| 		|       	|		|								|
| ESA/390		|		| hercules	|	|		| 		|       	|		|								|
| Eclipse		|		| simh		|	|		| 		|       	|		|								|
| GRI-909		|		| simh		|	|		| 		|       	|		|								|
| Gameboy		|		|		|	|		| 		|       	|		|								|
| Genesis		|		|		|	|		| 		|       	|		|								|
| HP 2100		|		| simh		|	|		| 		|       	|		|								|
| Honeywell 316		|		| simh		|	|		| 		|       	|		|								|
| Honeywell 516		|		| simh		|	|		| 		|       	|		|								|
| IBM 1620 Model 1	|		| simh		|	|		| 		|       	|		|								|
| IBM 1620 Model 2	|		| simh		|	|		| 		|       	|		|								|
| IBM 3270		|		|		|	|		| 		|       	|		|								|
| IBM 7094		|		| simh		|	|		| 		|       	|		|								|
| IBM System 3 Model 10	|		| simh		|	|		| 		|       	|		|								|
| Interdata 3		|		| simh		|	|		| 		|       	|		|								|
| Interdata 4		|		| simh		|	|		| 		|       	|		|								|
| Interdata 5		|		| simh		|	|		| 		|       	|		|								|
| Interdata 7/16	|		| simh		|	|		| 		|       	|		|								|
| Interdata 7/32	|		| simh		|	|		| 		|       	|		|								|
| Interdata 70		|		| simh		|	|		| 		|       	|		|								|
| Interdata 8/16	|		| simh		|	|		| 		|       	|		|								|
| Interdata 8/16E	|		| simh		|	|		| 		|       	|		|								|
| Interdata 8/32	|		| simh		|	|		| 		|       	|		|								|
| Interdata 80		|		| simh		|	|		| 		|       	|		|								|
| KC85			|		| kcemu		|	|		| 		|       	|		|								|
| LGP-21		|		| simh		|	|		| 		|       	|		|								|
| MIPS R2000		|		| spim		|	|		| 		|       	|		|								|
| MIPS R3000		|		| spim		|	|		| 		|       	|		|								|
| MSX			|		| openmsx	|	|		| 		|       	|		|								|
| Master System		|		|		|	|		| 		|       	|		|								|
| N64			|		|		|	|		| 		|       	|		|								|
| NES			|		|		|	|		| 		|       	|		|								|
| PDP-11		|		| simh		|	|		| 		|       	|		|								|
| PIC			|		| gpsim		|	|		| 		|       	|		|								|
| PS2			|		|		|	|		| 		|       	|		|								|
| PS3 (Cell)		|		|		|	|		| 		|       	|		|								|
| SDS 940		|		| simh		|	|		| 		|       	|		|								|
| SNES			|		|		|	|		| 		|       	|		|								|
| Saturn		|		|		|	|		| 		|       	|		|								|
| System/370		|		| hercules	|	|		| 		|       	|		|								|
| TRS80 (Z80)		|		|		|	|		| 		|       	|		|								|
| ZX Spectrum		|		|		|	|		| 		|       	|		|								|
| cris			|		| qemu-static	|	|		| 		|       	|		|								|
| itanium		|		|		|	|		| 		|       	|		|								|
| m68k			|		|		|	|		| 		|       	|		|								|
| microblaze		|		| qemu-static	|	|		| 		|       	|		|								|
| microblazeel		|		| qemu-static	|	|		| 		|       	|		|								|
| pr3287		|		|		|	|		| 		|       	|		|								|
| s390x			|		| qemu-static	|	|		| 		|       	|		|								|
| sh4			|		| qemu-static	|	|		| 		|       	|		|								|
| sh4eb			|		| qemu-static	|	|		| 		|       	|		|								|
| z/Architecture	|		| hercules	|	|		| 		|       	|		|								|
+-----------------------+---------------+---------------+-------+---------------+---------------+---------------+---------------+---------------------------------------------------------------+
```

# useful links

## 1401
http://aei.pitt.edu/91112/1/2637.3.pdf

## Nova
http://users.rcn.com/crfriend/museum/doco/DG/Nova/base-instr.html
https://ia800204.us.archive.org/22/items/usersguidefordat00ralp/usersguidefordat00ralp.pdf
https://archive.org/stream/usersguidefordat00ralp/usersguidefordat00ralp_djvu.txt

## LGP-30
http://ed-thelen.org/comp-hist/lgp-30.html
http://computermuseum.informatik.uni-stuttgart.de/dev_en/lgp30/lgp30_1.html
http://bitsavers.trailing-edge.com/pdf/royalPrecision/LGP-30/LGP-30_Subroutine_Manual_Oct60.pdf
http://obsolescenceguaranteed.blogspot.com/2016/06/using-simh-lgp-30-emulator.html

## PDP-10
http://pdp10.nocrew.org/docs/instruction-set/Jumps.html
https://esolangs.org/wiki/MIX_(Knuth)#Character_codes
