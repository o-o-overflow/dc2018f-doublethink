XR r0, r0, r0
XR r1, r1, r1

lds r3, [r0 + 0x4010000]
sli r3, r3, 1
lds r4, [r0 + 0x4010001]
sri r4, r4, 7
or r3, r3, r4
sts r3, [r1 + 0x5010000]

lds r3, [r0 + 0x4010001]
sli r3, r3, 2
lds r4, [r0 + 0x4010002]
sri r4, r4, 6
or r3, r3, r4
sts r3, [r1 + 0x5010001]

lds r3, [r0 + 0x4010002]
sli r3, r3, 3
lds r4, [r0 + 0x4010003]
sri r4, r4, 5
or r3, r3, r4
sts r3, [r1 + 0x5010002]

lds r3, [r0 + 0x4010003]
sli r3, r3, 4
lds r4, [r0 + 0x4010004]
sri r4, r4, 4
or r3, r3, r4
sts r3, [r1 + 0x5010003]

lds r3, [r0 + 0x4010004]
sli r3, r3, 5
lds r4, [r0 + 0x4010005]
sri r4, r4, 3
or r3, r3, r4
sts r3, [r1 + 0x5010004]

lds r3, [r0 + 0x4010005]
sli r3, r3, 6
lds r4, [r0 + 0x4010006]
sri r4, r4, 2
or r3, r3, r4
sts r3, [r1 + 0x5010005]

lds r3, [r0 + 0x4010006]
sli r3, r3, 7
lds r4, [r0 + 0x4010007]
sri r4, r4, 1
or r3, r3, r4
sts r3, [r1 + 0x5010006]

lds r3, [r0 + 0x4010007]
sli r3, r3, 8
lds r4, [r0 + 0x4010008]
sri r4, r4, 0
or r3, r3, r4
sts r3, [r1 + 0x5010007]

lds r3, [r0 + 0x4010009]
sli r3, r3, 1
lds r4, [r0 + 0x401000a]
sri r4, r4, 7
or r3, r3, r4
sts r3, [r1 + 0x5010008]

lds r3, [r0 + 0x401000a]
sli r3, r3, 2
lds r4, [r0 + 0x401000b]
sri r4, r4, 6
or r3, r3, r4
sts r3, [r1 + 0x5010009]

lds r3, [r0 + 0x401000b]
sli r3, r3, 3
lds r4, [r0 + 0x401000c]
sri r4, r4, 5
or r3, r3, r4
sts r3, [r1 + 0x501000a]

lds r3, [r0 + 0x401000c]
sli r3, r3, 4
lds r4, [r0 + 0x401000d]
sri r4, r4, 4
or r3, r3, r4
sts r3, [r1 + 0x501000b]

lds r3, [r0 + 0x401000d]
sli r3, r3, 5
lds r4, [r0 + 0x401000e]
sri r4, r4, 3
or r3, r3, r4
sts r3, [r1 + 0x501000c]

lds r3, [r0 + 0x401000e]
sli r3, r3, 6
lds r4, [r0 + 0x401000f]
sri r4, r4, 2
or r3, r3, r4
sts r3, [r1 + 0x501000d]

lds r3, [r0 + 0x401000f]
sli r3, r3, 7
lds r4, [r0 + 0x4010010]
sri r4, r4, 1
or r3, r3, r4
sts r3, [r1 + 0x501000e]

lds r3, [r0 + 0x4010010]
sli r3, r3, 8
lds r4, [r0 + 0x4010011]
sri r4, r4, 0
or r3, r3, r4
sts r3, [r1 + 0x501000f]

;adi r0, r0, 1
;adi r1, r1, 1
;lds r3, [r0]
;sli r3, r3, 1
;sts r3, [r1]

XR r1, r1, r1
XR r2, r2, r2
ML r2, 0x1000
STT r2, [r1 + 0x5012000, 1]
