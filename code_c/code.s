	.text
	.syntax unified
	.eabi_attribute	67, "2.09"	@ Tag_conformance
	.cpu	cortex-m0
	.eabi_attribute	6, 12	@ Tag_CPU_arch
	.eabi_attribute	7, 77	@ Tag_CPU_arch_profile
	.eabi_attribute	8, 0	@ Tag_ARM_ISA_use
	.eabi_attribute	9, 1	@ Tag_THUMB_ISA_use
	.eabi_attribute	34, 0	@ Tag_CPU_unaligned_access
	.eabi_attribute	17, 1	@ Tag_ABI_PCS_GOT_use
	.eabi_attribute	20, 1	@ Tag_ABI_FP_denormal
	.eabi_attribute	21, 0	@ Tag_ABI_FP_exceptions
	.eabi_attribute	23, 3	@ Tag_ABI_FP_number_model
	.eabi_attribute	24, 1	@ Tag_ABI_align_needed
	.eabi_attribute	25, 1	@ Tag_ABI_align_preserved
	.eabi_attribute	38, 1	@ Tag_ABI_FP_16bit_format
	.eabi_attribute	18, 4	@ Tag_ABI_PCS_wchar_t
	.eabi_attribute	26, 2	@ Tag_ABI_enum_size
	.eabi_attribute	14, 0	@ Tag_ABI_PCS_R9_use
	.file	"code.c"
	.globl	run                             @ -- Begin function run
	.p2align	2
	.type	run,%function
	.code	16                              @ @run
	.thumb_func
run:
	.fnstart
@ %bb.0:
	.pad	#88
	sub	sp, #88
	@APP
	sub	sp, #508
	@NO_APP
	@APP
	sub	sp, #452
	@NO_APP
	movs	r0, #1
	str	r0, [sp]
	b	.LBB0_1
.LBB0_1:                                @ =>This Inner Loop Header: Depth=1
	ldr	r1, [sp]
	ldr	r0, .LCPI0_0
	muls	r0, r1, r0
	ldr	r1, .LCPI0_1
	adds	r0, r0, r1
	ldr	r1, .LCPI0_2
	cmp	r0, r1
	blo	.LBB0_3
	b	.LBB0_2
.LBB0_2:                                @   in Loop: Header=BB0_1 Depth=1
	ldr	r0, [sp]
	adds	r0, r0, #1
	str	r0, [sp]
	b	.LBB0_1
.LBB0_3:
	ldr	r0, [sp]
	str	r0, [sp, #28]
	b	.LBB0_4
.LBB0_4:
	b	.LBB0_5
.LBB0_5:                                @ =>This Inner Loop Header: Depth=1
	b	.LBB0_5
	.p2align	2
@ %bb.6:
.LCPI0_0:
	.long	3067833783                      @ 0xb6db6db7
.LCPI0_1:
	.long	306783378                       @ 0x12492492
.LCPI0_2:
	.long	613566757                       @ 0x24924925
.Lfunc_end0:
	.size	run, .Lfunc_end0-run
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 18.1.8"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 6	@ Tag_ABI_optimization_goals
