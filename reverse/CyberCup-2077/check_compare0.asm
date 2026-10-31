
BLOCK 14060fdb0
14060fdb0: jmp 0x1412d5a2f
1412d5a2f: and dword ptr [r8 + 0x350], 0
1412d5a37: xadd r9w, r9w
1412d5a3c: and r9b, 0x44
1412d5a40: sbb r9b, 0x97
1412d5a44: xor dword ptr [r8 + 0x350], 0xc47eb41e
1412d5a4f: add r9b, r10b
1412d5a52: pushfq 
1412d5a53: xor r9d, r9d
1412d5a56: or r9d, dword ptr [r8 + 0x348]
1412d5aa8: popfq 
1412d5aa9: mov dword ptr [r8], r9d
1412d5aac: jmp 0x141470520
141470520: xor r9d, r9d
141470523: jmp 0x14147056b
14147056b: xor r9d, dword ptr [r8 + 0x350]
141470572: jmp 0x1412761b8
1412761b8: sub r11, r11
1412761bb: stc 
1412761bc: cmp bpl, r13b
1412761bf: xor r11d, dword ptr [r8 + 4]
1412761c3: xor r11d, r9d
1412761c6: shld r9w, di, 0x40
1412761cc: xor dword ptr [r8 + 4], r11d
1412761d0: add r9b, r8b
1412761d3: shl r9, 0xf6
1412761d7: pushfq 
1412761d8: xor r9d, r9d
1412761db: or r9d, 0
14127622d: popfq 
14127622e: xor r11, r11
141276231: test r8, 0x574a08fa
141276238: xor r11b, r9b
14127623b: jmp 0x141357d8c
141357d8c: xor r11b, byte ptr [r8]
141357d8f: xor r9b, r11b
141357d92: xor r11, r11
141357d95: cmp r12b, 0xb5
141357d99: xor r11, r10
141357d9c: xor r11, qword ptr [rip - 0x42484b]
141357da3: cmp r12w, r13w
141357da7: xor r10, r11
141357daa: stc 
141357dab: jmp 0x1414abb6d
1414abb6d: xor r11, r11
1414abb70: jmp 0x14132f467
14132f467: xor r11, qword ptr [r10 + r9*8]
14132f46b: xchg r11, r10
14132f46e: stc 
14132f46f: xor r11, r11
14132f472: test r8, 0x62cf005b
14132f479: cmp spl, 0x12
14132f47d: xor r11d, r9d
14132f480: cmp r12b, r13b
14132f483: cmp esi, 0x1c742dd6
14132f489: xor r11d, 0
14132f48d: test bl, sil
14132f490: xor r9d, r11d
14132f493: sub r11, r11
14132f496: cmc 
14132f497: stc 
14132f498: xor r11b, r9b
14132f49b: cmp r11w, r9w
14132f49f: clc 
14132f4a0: jmp 0x141282996
141282996: xor r11b, byte ptr [r8 + 4]
14128299a: test al, r10b
14128299d: xor r9b, r11b
1412829a0: test r13b, 0x37
1412829a4: test ax, r12w
1412829a8: cmp cx, bx
1412829ab: xor r11, r11
1412829ae: xor r11b, byte ptr [r10 + r9]
1412829b2: test r9, 0x80f2ed9
1412829b9: xchg r11b, r9b
1412829bc: test r11b, 0xcd
1412829c0: mov byte ptr [r8 + 8], r9b
1412829c4: cmp r9w, 0xcf5
1412829ca: test bp, 0x1d29
1412829cf: jmp 0x14132f4f3
14132f4f3: sub r9d, r9d
14132f4f6: xor r9d, 0
14132f4fa: and r9b, 0
14132f4fe: clc 
14132f4ff: xor r9b, byte ptr [r8 + 1]
14132f503: sub r10, r10
14132f506: or r10, qword ptr [rip - 0x3fbfb5]
14132f50d: jmp 0x141445e85
141445e85: mov r10, qword ptr [r10 + r9*8]
141445e89: pushfq 
141445e8a: xor r9d, r9d
141445e8d: or r9d, 0
141445edf: popfq 
141445ee0: mov r9b, byte ptr [r8 + 5]
141445ee4: cmc 
141445ee5: mov r9b, byte ptr [r10 + r9]
141445ee9: xor r10b, 0x99
141445eed: add r10, rbp
141445ef0: cmc 
141445ef1: mov byte ptr [r8 + 9], r9b
141445ef5: bsr r10w, si
141445efa: bswap r10w
141445efe: shl r10b, cl
141445f01: sub r11, r11
141445f04: bts r10w, r12w
141445f09: test al, dh
141445f0b: btr r10w, 0x59
141445f11: xor r11d, r9d
141445f14: sbb r10b, 0xaf
141445f18: xadd r10d, r10d
141445f1c: xor r11d, 0
141445f20: bt r10w, 0xfe
141445f26: rcr r10b, 0xdb
141445f2a: xor r9d, r11d
141445f2d: xadd r10w, r10w
141445f32: and r10w, r13w
141445f36: xor r11, r11
141445f39: cmovs r10, rsp
141445f3d: xor r10b, 0x20
141445f41: xor r11b, r9b
141445f44: xor r11b, byte ptr [r8 + 2]
141445f48: shr r10b, cl
141445f4b: shl r10b, cl
141445f4e: adc r10w, r9w
141445f52: xor r9b, r11b
141445f55: mov r10, qword ptr [rip - 0x512a04]
141445f5c: stc 
141445f5d: sub r11, r11
141445f60: stc 
141445f61: xor r11, qword ptr [r10 + r9*8]
141445f65: test al, 0x1a
141445f67: jmp 0x1412ad578
1412ad578: xor r11, r10
1412ad57b: test r11w, bx
1412ad57f: xor r10, r11
1412ad582: stc 
1412ad583: sub r9d, r9d
1412ad586: or r9d, 0
1412ad58a: neg r9b
1412ad58d: adc r9b, dil
1412ad590: rcl r9b, 3
1412ad594: mov r9b, byte ptr [r8 + 6]
1412ad598: xor r11, r11
1412ad59b: xor r11b, byte ptr [r10 + r9]
1412ad59f: xchg r11b, r9b
1412ad5a2: bt r10d, r11d
1412ad5a6: ror r10w, cl
1412ad5aa: movzx r10d, bx
1412ad5ae: and byte ptr [r8 + 0xa], 0
1412ad5b3: or byte ptr [r8 + 0xa], r9b
1412ad5b7: movsxd r10, r11d
1412ad5ba: pushfq 
1412ad5bb: and r9d, 0
1412ad5c2: xor r9d, 0
1412ad5fa: popfq 
1412ad5fb: and r9b, 0
1412ad5ff: btc r10w, r8w
1412ad604: inc r10d
1412ad607: bt r10d, r12d
1412ad60b: xor r9b, byte ptr [r8 + 3]
1412ad60f: add r10b, 0xc2
1412ad613: mov r10, qword ptr [rip - 0x37a0c2]
1412ad61a: jmp 0x141302c06
141302c06: xor r11, r11
141302c09: test r8b, dl
141302c0c: test r8b, 0x71
141302c10: xor r11, qword ptr [r10 + r9*8]
141302c14: xor r11, r10
141302c17: xor r10, r11
141302c1a: clc 
141302c1b: xor r9d, r9d
141302c1e: or r9d, 0
141302c22: test r11b, 0x60
141302c26: cmc 
141302c27: and r9b, 0
141302c2b: cmp r13b, r11b
141302c2e: or r9b, byte ptr [r8 + 7]
141302c32: sub r11, r11
141302c35: clc 
141302c36: cmp ebx, r10d
141302c39: xor r11b, byte ptr [r10 + r9]
141302c3d: jmp 0x14137ae10
14137ae10: xor r11b, r9b
14137ae13: test r12b, r8b
14137ae16: xor r9b, r11b
14137ae19: clc 
14137ae1a: cmp rbx, r15
14137ae1d: sub r11, r11
14137ae20: xor r11b, byte ptr [r8 + 0xb]
14137ae24: clc 
14137ae25: xor r11b, r9b
14137ae28: movzx r9, r8w
14137ae2c: rcr r9w, cl
14137ae30: xor byte ptr [r8 + 0xb], r11b
14137ae34: bt r9, rbp
14137ae38: and r9b, sil
14137ae3b: clc 
14137ae3c: pushfq 
14137ae3d: xor r9d, r9d
14137ae40: or r9d, dword ptr [r8 + 8]
14137ae8f: popfq 
14137ae90: and dword ptr [r8 + 0x354], 0
14137ae98: xor dword ptr [r8 + 0x354], r9d
14137ae9f: jmp 0x14128891c
14128891c: and dword ptr [r8 + 0x358], 0
141288924: xor dword ptr [r8 + 0x358], 0x638acb6f
14128892f: test r10b, r15b
141288932: test r10d, 0x171f3629
141288939: sub r11, r11
14128893c: test r12w, r9w
141288940: jmp 0x1412b2f8e
1412b2f8e: xor r11d, r9d
1412b2f91: xor r11d, dword ptr [r8 + 0x34c]
1412b2f98: cmp spl, 0xf7
1412b2f9c: cmp spl, r12b
1412b2f9f: xor r9d, r11d
1412b2fa2: cmp r11w, r14w
1412b2fa6: cmc 
1412b2fa7: test r9b, 0x9d
1412b2fab: mov dword ptr [r8], r9d
1412b2fae: xor r9d, r9d
1412b2fb1: xor r9d, dword ptr [r8 + 0x358]
1412b2fb8: cmc 
1412b2fb9: cmp sp, ax
1412b2fbc: and dword ptr [r8 + 4], 0
1412b2fc1: clc 
1412b2fc2: cmc 
1412b2fc3: xor dword ptr [r8 + 4], r9d
1412b2fc7: test ax, 0x7173
1412b2fcb: sub r9d, r9d
1412b2fce: or r9d, 0
1412b2fd2: jmp 0x141477447
141477447: and r9b, 0
14147744b: xor r9b, byte ptr [r8]
14147744e: test si, 0x2738
141477453: stc 
141477454: xor r10, r10
141477457: jmp 0x1413854cf
1413854cf: or r10, qword ptr [rip - 0x451f7e]
1413854d6: stc 
1413854d7: test r14, 0x7d85380d
1413854de: xor r11, r11
1413854e1: xor r11, qword ptr [r10 + r9*8]
1413854e5: jmp 0x141374b25
141374b25: xor r11, r10
141374b28: test bpl, 0x37
141374b2c: jmp 0x1413e2b79
1413e2b79: xor r10, r11
1413e2b7c: cmc 
1413e2b7d: sub r11, r11
1413e2b80: xor r11d, r9d
1413e2b83: xor r11d, 0
1413e2b87: test r14w, sp
1413e2b8b: stc 
1413e2b8c: test si, 0xd95
1413e2b91: xor r9d, r11d
1413e2b94: cmp ax, r13w
1413e2b98: shr r9b, cl
1413e2b9b: adc r9b, r12b
1413e2b9e: mov r9b, byte ptr [r8 + 4]
1413e2ba2: cmp ax, r9w
1413e2ba6: cmp r15w, 0x40ba
1413e2bac: xor r11, r11
1413e2baf: xor r11b, byte ptr [r10 + r9]
1413e2bb3: cmc 
1413e2bb4: stc 
1413e2bb5: xchg r11b, r9b
1413e2bb8: mov byte ptr [r8 + 8], r9b
1413e2bbc: test sil, 0x8e
1413e2bc0: cmp r8, 0x17dc54da
1413e2bc7: sub r9d, r9d
1413e2bca: cmc 
1413e2bcb: clc 
1413e2bcc: or r9d, 0
1413e2bd0: stc 
1413e2bd1: and r9b, 0
1413e2bd5: stc 
1413e2bd6: cmp r9d, r13d
1413e2bd9: clc 
1413e2bda: xor r9b, byte ptr [r8 + 1]
1413e2bde: cmp r8b, 0xbd
1413e2be2: jmp 0x1413b1780
1413b1780: xor r10, r10
1413b1783: test r9b, r13b
1413b1786: or r10, qword ptr [rip - 0x47e235]
1413b178d: stc 
1413b178e: mov r10, qword ptr [r10 + r9*8]
1413b1792: jmp 0x14142f2ab
14142f2ab: xor r9d, r9d
14142f2ae: test sil, r10b
14142f2b1: cmp bpl, dl
14142f2b4: cmp r13d, 0x16ce4bd3
14142f2bb: or r9d, 0
14142f2bf: neg r9b
14142f2c2: or r9b, r11b
14142f2c5: mov r9b, byte ptr [r8 + 5]
14142f2c9: stc 
14142f2ca: mov r9b, byte ptr [r10 + r9]
14142f2ce: stc 
14142f2cf: sub r11, r11
14142f2d2: cmp r15b, 0xbb
14142f2d6: test r15w, 0xc77
14142f2dc: xor r11b, byte ptr [r8 + 9]
14142f2e0: cmp r14, rsi
14142f2e3: stc 
14142f2e4: xor r11b, r9b
14142f2e7: cmp dl, 0xe2
14142f2ea: xor byte ptr [r8 + 9], r11b
14142f2ee: cmp r9b, r10b
14142f2f1: sub r9d, r9d
14142f2f4: stc 
14142f2f5: xor r9d, 0
14142f2f9: mov r9b, byte ptr [r8 + 2]
14142f2fd: cmp r15b, r10b
14142f300: sub r11, r11
14142f303: test r8w, 0x4e33
14142f309: cmp bl, spl
14142f30c: xor r11, r10
14142f30f: cmp r13b, 0x3b
14142f313: xor r11, qword ptr [rip - 0x4fbdc2]
14142f31a: cmp dh, al
14142f31c: jmp 0x1413ded32
1413ded32: xor r10, r11
1413ded35: test r12b, r8b
1413ded38: stc 
1413ded39: xor r11, r11
1413ded3c: xor r11, qword ptr [r10 + r9*8]
1413ded40: xor r11, r10
1413ded43: test bh, 0xac
1413ded46: cmc 
1413ded47: xor r10, r11
1413ded4a: xor r9d, r9d
1413ded4d: clc 
1413ded4e: or r9d, 0
1413ded52: mov r9b, byte ptr [r8 + 6]
1413ded56: cmc 
1413ded57: sub r11, r11
1413ded5a: clc 
1413ded5b: cmp r13b, 0x79
1413ded5f: xor r11b, byte ptr [r10 + r9]
1413ded63: ror r10, cl
1413ded66: xchg r11b, r9b
1413ded69: sal r10b, cl
1413ded6c: bt r10w, ax
1413ded71: cmp r8b, r9b
1413ded74: sub r11, r11
1413ded77: mov r10b, bl
1413ded7a: rcr r10b, 0x5a
1413ded7e: mov r10, 0x340c47f0
1413ded85: xor r11b, byte ptr [r8 + 0xa]
1413ded89: adc r10b, 0x6d
1413ded8d: xor r11b, r9b
1413ded90: sar r9b, 0x95
1413ded94: xor byte ptr [r8 + 0xa], r11b
1413ded98: movsx r10w, r15b
1413ded9d: sbb r9b, 4
1413deda1: pushfq 
1413deda2: xor r9d, r9d
1413deda5: or r9d, 0
1413dedf7: popfq 
1413dedf8: mov r9b, byte ptr [r8 + 3]
1413dedfc: adc r10b, 0xf
1413dee00: sal r10b, cl
1413dee03: rol r10w, 0xa7
1413dee08: mov r10, qword ptr [rip - 0x4ab8b7]
1413dee0f: cmp sil, r8b
1413dee12: stc 
1413dee13: cmc 
1413dee14: xor r11, r11
1413dee17: xor r11, qword ptr [r10 + r9*8]
1413dee1b: xor r11, r10
1413dee1e: test bpl, bl
1413dee21: xor r10, r11
1413dee24: test bpl, al
1413dee27: xor r11, r11
1413dee2a: cmp r14b, dl
1413dee2d: xor r11d, r9d
1413dee30: cmc 
1413dee31: xor r11d, 0
1413dee35: xor r9d, r11d
1413dee38: jmp 0x14132ed19
14132ed19: xor r11, r11
14132ed1c: cmp r12b, 0xf9
14132ed20: xor r11b, r9b
14132ed23: stc 
14132ed24: xor r11b, byte ptr [r8 + 7]
14132ed28: test bpl, 0x7d
14132ed2c: test bp, r8w
14132ed30: xor r9b, r11b
14132ed33: sub r11, r11
14132ed36: xor r11b, byte ptr [r10 + r9]
14132ed3a: mov r10w, bp
14132ed3e: ror r10b, cl
14132ed41: xor r11b, r9b
14132ed44: movsx r10, r11w
14132ed48: xor r9b, r11b
14132ed4b: cmp di, r15w
14132ed4f: bswap r10d
14132ed52: cmp r12b, 2
14132ed56: mov byte ptr [r8 + 0xb], r9b
14132ed5a: shrd r10d, r15d, 0xda
14132ed5f: neg r10b
14132ed62: xor r11, r11
14132ed65: sar r10b, 0x75
14132ed69: xadd r10b, r10b
14132ed6d: jmp 0x141314ba6
141314ba6: xor r11d, r9d
141314ba9: bts r10d, ebp
141314bad: xor r11d, dword ptr [r8 + 8]
141314bb1: shl r10b, cl
141314bb4: xor r9d, r11d
141314bb7: sub r11, r11
141314bba: movsx r10d, r15w
141314bbe: adc r10b, 0x1d
141314bc2: shr r10w, cl
141314bc6: xor r11d, dword ptr [r8 + 0x35c]
141314bcd: shrd r10d, esp, 0x48
141314bd2: xor r11d, r9d
141314bd5: sar r10b, 0xd9
141314bd9: bts r10, rsi
141314bdd: xor dword ptr [r8 + 0x35c], r11d
141314be4: not r10d
141314be7: sub r11, r11
141314bea: test dl, r12b
141314bed: shrd r10w, r12w, 0xc9
141314bf3: xor r11d, r9d
141314bf6: xor r11d, dword ptr [r8 + 0x334]
141314bfd: jmp 0x141311c41
141311c41: xor r9d, r11d
141311c44: and dword ptr [r8], 0
141311c48: cmovno r10w, bx
141311c4d: adc r10w, 0x5774
141311c53: movsx r10w, cl
141311c58: xor dword ptr [r8], r9d
141311c5b: not r10d
141311c5e: xor r9d, r9d
141311c61: rcr r10b, cl
141311c64: xor r9d, dword ptr [r8 + 0x354]
141311c6b: rcl r10b, cl
141311c6e: or r10b, 0xcc
141311c72: shr r10b, cl
141311c75: sub r11, r11
141311c78: bt r10w, 0xba
141311c7e: dec r10
141311c81: sal r10w, 0x4d
141311c86: xor r11d, dword ptr [r8 + 4]
141311c8a: sar r10d, cl
141311c8d: xor r11d, r9d
141311c90: bt r10, r9
141311c94: ror r10, cl
141311c97: sub r10b, r15b
141311c9a: xor dword ptr [r8 + 4], r11d
141311c9e: rcr r10b, cl
141311ca1: xor r10w, bx
141311ca5: cmp r11w, 0x20e7
141311cab: sub r9d, r9d
141311cae: or r9d, 0
141311cb2: or r10w, sp
141311cb6: sbb r10w, r15w
141311cba: sal r10b, cl
141311cbd: and r9b, 0
141311cc1: xor r9b, byte ptr [r8]
141311cc4: neg r10d
141311cc7: dec r10
141311cca: mov r10, qword ptr [rip - 0x3de779]
141311cd1: sub r11, r11
141311cd4: xor r11, qword ptr [r10 + r9*8]
141311cd8: cmc 
141311cd9: xor r11, r10
141311cdc: clc 
141311cdd: xor r10, r11
141311ce0: stc 
141311ce1: sub r9d, r9d
141311ce4: test r12d, 0x6ba56f48
141311ceb: xor r9d, 0
141311cef: jmp 0x1412fac81
1412fac81: xor r11, r11
1412fac84: test rbp, 0x2b4566ca
1412fac8b: clc 
1412fac8c: xor r11b, r9b
1412fac8f: cmc 
1412fac90: cmp ch, 0xf8
1412fac93: cmp r12w, ax
1412fac97: xor r11b, byte ptr [r8 + 4]
1412fac9b: cmc 
1412fac9c: cmp r8b, r9b
1412fac9f: xor r9b, r11b
1412faca2: jmp 0x1412c7109
1412c7109: mov r9b, byte ptr [r10 + r9]
1412c710d: and byte ptr [r8 + 8], 0
1412c7112: jmp 0x14125f4f0
14125f4f0: or byte ptr [r8 + 8], r9b
14125f4f4: xor r11, r11
14125f4f7: cmp r15b, 0x70
14125f4fb: stc 
14125f4fc: cmp spl, r8b
14125f4ff: xor r11d, r9d
14125f502: cmp cl, bpl
14125f505: xor r11d, 0
14125f509: cmp rbx, r8
14125f50c: test rcx, 0x104b0dca
14125f513: xor r9d, r11d
14125f516: stc 
14125f517: test dil, r11b
14125f51a: and r9b, 0
14125f51e: cmp r8b, 0xa9
14125f522: cmc 
14125f523: stc 
14125f524: xor r9b, byte ptr [r8 + 1]
14125f528: xor r10, r10
14125f52b: or r10, qword ptr [rip - 0x32bfda]
14125f532: test dil, r13b
14125f535: clc 
14125f536: stc 
14125f537: sub r11, r11
14125f53a: cmp bpl, dl
14125f53d: stc 
14125f53e: xor r11, qword ptr [r10 + r9*8]
14125f542: stc 
14125f543: test r12w, r9w
14125f547: test r11b, 0xf6
14125f54b: xchg r11, r10
14125f54e: sub r11, r11
14125f551: clc 
14125f552: xor r11d, r9d
14125f555: test al, sil
14125f558: clc 
14125f559: xor r11d, 0
14125f55d: cmc 
14125f55e: cmp r12w, 0x57b6
14125f564: cmp r12w, bp
14125f568: xor r9d, r11d
14125f56b: and r9b, 0
14125f56f: xor r9b, byte ptr [r8 + 5]
14125f573: sub r11, r11
14125f576: jmp 0x1412e761d
1412e761d: xor r11b, byte ptr [r10 + r9]
1412e7621: cmp bl, dil
1412e7624: test cl, 0xbb
1412e7627: xchg r11b, r9b
1412e762a: and byte ptr [r8 + 9], 0
1412e762f: jmp 0x14147a769
14147a769: xor byte ptr [r8 + 9], r9b
14147a76d: and r9b, r12b
14147a770: adc r9, r13
14147a773: shr r9b, cl
14147a776: pushfq 
14147a777: xor r9d, r9d
14147a77a: or r9d, 0
14147a7cc: popfq 
14147a7cd: and r9b, 0
14147a7d1: or r9b, byte ptr [r8 + 2]
14147a7d5: xor r11, r11
14147a7d8: cmp r13w, 0x6e31
14147a7de: xor r11, r10
14147a7e1: cmc 
14147a7e2: test ecx, ebp
14147a7e4: clc 
14147a7e5: xor r11, qword ptr [rip - 0x547294]
14147a7ec: cmp r10d, 0x64b869fa
14147a7f3: xor r10, r11
14147a7f6: mov r10, qword ptr [r10 + r9*8]
14147a7fa: test esi, 0x77df4172
14147a800: cmp r10d, 0x3c53115f
14147a807: sub r9d, r9d
14147a80a: test cl, r10b
14147a80d: clc 
14147a80e: or r9d, 0
14147a812: cmp r12b, 0x13
14147a816: clc 
14147a817: xor r11, r11
14147a81a: xor r11b, r9b
14147a81d: clc 
14147a81e: xor r11b, byte ptr [r8 + 6]
14147a822: jmp 0x14128cb05
14128cb05: xor r9b, r11b
14128cb08: sub r11, r11
14128cb0b: test rdi, 0xdc344db
14128cb12: xor r11b, byte ptr [r10 + r9]
14128cb16: cmc 
14128cb17: xor r11b, r9b
14128cb1a: clc 
14128cb1b: xor r9b, r11b
14128cb1e: clc 
14128cb1f: stc 
14128cb20: and byte ptr [r8 + 0xa], 0
14128cb25: or byte ptr [r8 + 0xa], r9b
14128cb29: cmc 
14128cb2a: sub r9d, r9d
14128cb2d: clc 
14128cb2e: or r9d, 0
14128cb32: test sp, bx
14128cb35: clc 
14128cb36: xor r11, r11
14128cb39: xor r11b, r9b
14128cb3c: xor r11b, byte ptr [r8 + 3]
14128cb40: jmp 0x1413900bc
1413900bc: xor r9b, r11b
1413900bf: xor r11, r11
1413900c2: xor r11, r10
1413900c5: xor r11, qword ptr [rip - 0x45cb74]
1413900cc: xor r10, r11
1413900cf: test r13w, ax
1413900d3: mov r10, qword ptr [r10 + r9*8]
1413900d7: xor r11, r11
1413900da: xor r11d, r9d
1413900dd: cmp r12, r14
1413900e0: xor r11d, 0
1413900e4: test r14b, spl
1413900e7: stc 
1413900e8: test bh, 0xd6
1413900eb: xor r9d, r11d
1413900ee: stc 
1413900ef: clc 
1413900f0: xor r11, r11
1413900f3: cmc 
1413900f4: clc 
1413900f5: xor r11b, r9b
1413900f8: xor r11b, byte ptr [r8 + 7]
1413900fc: cmp bpl, 0x6a
141390100: cmc 
141390101: clc 
141390102: xor r9b, r11b
141390105: xor r11, r11
141390108: xor r11b, byte ptr [r10 + r9]
14139010c: test ax, 0x76ae
141390110: xchg r11b, r9b
141390113: sub r11, r11
141390116: test r8d, 0x66f00992
14139011d: cmp r8b, r11b
141390120: xor r11b, byte ptr [r8 + 0xb]
141390124: xor r11b, r9b
141390127: shr r9d, 0x9a
14139012b: xor byte ptr [r8 + 0xb], r11b
14139012f: pushfq 
141390130: xor r9d, r9d
141390133: or r9d, dword ptr [r8 + 8]
141390180: popfq 
141390181: mov dword ptr [r8 + 0x360], r9d
141390188: clc 
141390189: and dword ptr [r8 + 0x364], 0
141390191: clc 
141390192: cmc 
141390193: xor dword ptr [r8 + 0x364], 0
14139019b: cmp r11w, 0x7d43
1413901a1: xor r11, r11
1413901a4: xor r11d, r9d
1413901a7: test sp, bx
1413901aa: stc 
1413901ab: xor r11d, dword ptr [r8 + 0x364]
1413901b2: xor r9d, r11d
1413901b5: cmp sil, 0x6d
1413901b9: cmc 
1413901ba: mov dword ptr [r8], r9d
1413901bd: sub r9d, r9d
1413901c0: stc 
1413901c1: test edx, ebp
1413901c3: or r9d, dword ptr [r8 + 0x360]
1413901ca: jmp 0x1413ee424
1413ee424: and dword ptr [r8 + 4], 0
1413ee429: test sp, di
1413ee42c: or dword ptr [r8 + 4], r9d
1413ee430: cmp dil, r12b
1413ee433: test ax, 0x116e
1413ee437: xor r9d, r9d
1413ee43a: cmp r8w, 0x325
1413ee440: or r9d, 0
1413ee444: jmp 0x141425462
141425462: xor r11, r11
141425465: cmp rbx, rsp
141425468: jmp 0x141416b56
141416b56: xor r11b, r9b
141416b59: xor r11b, byte ptr [r8]
141416b5c: xor r9b, r11b
141416b5f: sub r11, r11
141416b62: test r15, r10
141416b65: xor r11, r10
141416b68: test r14, 0x39763b65
141416b6f: clc 
141416b70: stc 
141416b71: xor r11, qword ptr [rip - 0x4c2600]
141416b78: clc 
141416b79: cmp di, r10w
141416b7d: cmp r14w, 0x4cac
141416b83: xor r10, r11
141416b86: cmp cl, r10b
141416b89: stc 
141416b8a: sub r11, r11
141416b8d: clc 
141416b8e: test bl, r9b
141416b91: xor r11, qword ptr [r10 + r9*8]
141416b95: test r12b, dil
141416b98: cmp r13b, r9b
141416b9b: xor r11, r10
141416b9e: xor r10, r11
141416ba1: sub r9d, r9d
141416ba4: jmp 0x1414094b5
1414094b5: xor r9d, 0
1414094b9: xor r11, r11
1414094bc: xor r11b, r9b
1414094bf: cmp rdx, 0x18e2017f
1414094c6: xor r11b, byte ptr [r8 + 4]
1414094ca: cmp spl, r14b
1414094cd: jmp 0x1413eac87
1413eac87: xor r9b, r11b
1413eac8a: test r8b, 0x58
1413eac8e: cmc 
1413eac8f: sub r11, r11
1413eac92: clc 
1413eac93: cmc 
1413eac94: xor r11b, byte ptr [r10 + r9]
1413eac98: cmc 
1413eac99: jmp 0x141461fb9
141461fb9: xor r11b, r9b
141461fbc: test r10w, 0x715f
141461fc2: xor r9b, r11b
141461fc5: test r13b, 0xe7
141461fc9: cmp esi, r10d
141461fcc: xor r11, r11
141461fcf: jmp 0x141471898
141471898: xor r11b, byte ptr [r8 + 8]
14147189c: xor r11b, r9b
14147189f: clc 
1414718a0: xor byte ptr [r8 + 8], r11b
1414718a4: test ch, bl
1414718a6: clc 
1414718a7: cmc 
1414718a8: xor r11, r11
1414718ab: test bp, dx
1414718ae: clc 
1414718af: jmp 0x14127a4d5
14127a4d5: xor r11d, r9d
14127a4d8: xor r11d, 0
14127a4dc: clc 
14127a4dd: xor r9d, r11d
14127a4e0: cmc 
14127a4e1: sub r11, r11
14127a4e4: clc 
14127a4e5: xor r11b, r9b
14127a4e8: test r10, rax
14127a4eb: cmp dx, 0x2bf6
14127a4f0: xor r11b, byte ptr [r8 + 1]
14127a4f4: xor r9b, r11b
14127a4f7: xor r10, r10
14127a4fa: stc 
14127a4fb: jmp 0x1412835b4
1412835b4: or r10, qword ptr [rip - 0x32f043]
1412835bb: cmp r12w, 0x5f65
1412835c1: jmp 0x141299ac4
141299ac4: xor r11, r11
141299ac7: cmp r10w, 0x309f
141299acd: xor r11, qword ptr [r10 + r9*8]
141299ad1: xchg r11, r10
141299ad4: test r11, 0x7070227c
141299adb: cmc 
141299adc: stc 
141299add: sub r11, r11
141299ae0: test r13w, bp
141299ae4: xor r11d, r9d
141299ae7: cmp rbp, 0x475c2947
141299aee: jmp 0x1412d37c6
1412d37c6: xor r11d, 0
1412d37ca: clc 
1412d37cb: cmc 
1412d37cc: cmp esp, 0x460e47ad
1412d37d2: xor r9d, r11d
1412d37d5: cmp r15, r10
1412d37d8: xor r11, r11
1412d37db: test sil, r10b
1412d37de: xor r11b, r9b
1412d37e1: clc 
1412d37e2: test r14b, 0xc6
1412d37e6: xor r11b, byte ptr [r8 + 5]
1412d37ea: test dl, 0x65
1412d37ed: clc 
1412d37ee: xor r9b, r11b
1412d37f1: xor r11, r11
1412d37f4: cmc 
1412d37f5: clc 
1412d37f6: xor r11b, byte ptr [r10 + r9]
1412d37fa: cmp r15d, 0xb544904
1412d3801: cmc 
1412d3802: xor r11b, r9b
1412d3805: test ax, ax
1412d3808: xor r9b, r11b
1412d380b: mov byte ptr [r8 + 9], r9b
1412d380f: jmp 0x14124b00d
14124b00d: sub r9d, r9d
14124b010: stc 
14124b011: jmp 0x141423b96
141423b96: or r9d, 0
141423b9a: and r9b, 0
141423b9e: test r11b, 0x70
141423ba2: jmp 0x14136a5c5
14136a5c5: or r9b, byte ptr [r8 + 2]
14136a5c9: stc 
14136a5ca: sub r10, r10
14136a5cd: stc 
14136a5ce: jmp 0x1413595b8
1413595b8: or r10, qword ptr [rip - 0x405047]
1413595bf: mov r10, qword ptr [r10 + r9*8]
1413595c3: xor r11, r11
1413595c6: clc 
1413595c7: cmp r10w, sp
1413595cb: xor r11d, r9d
1413595ce: stc 
1413595cf: jmp 0x1413451bc
1413451bc: xor r11d, 0
1413451c0: jmp 0x141431de0
141431de0: xor r9d, r11d
141431de3: test bpl, 0x15
141431de7: cmc 
141431de8: jmp 0x14138128c
14138128c: xor r11, r11
14138128f: test r8b, 0xd6
141381293: xor r11b, r9b
141381296: xor r11b, byte ptr [r8 + 6]
14138129a: cmp rbx, 0x7d581ece
1413812a1: clc 
1413812a2: xor r9b, r11b
1413812a5: cmp al, 0x8e
1413812a7: test r8w, 0x22d4
1413812ad: test dl, r11b
1413812b0: mov r9b, byte ptr [r10 + r9]
1413812b4: test spl, dl
1413812b7: cmp r10w, bx
1413812bb: mov byte ptr [r8 + 0xa], r9b
1413812bf: xor r9d, r9d
1413812c2: test edi, esi
1413812c4: stc 
1413812c5: cmp r15b, 0xf6
1413812c9: or r9d, 0
1413812cd: clc 
1413812ce: cmc 
1413812cf: xor r11, r11
1413812d2: cmc 
1413812d3: jmp 0x14132c6e4
14132c6e4: xor r11b, r9b
14132c6e7: test r13b, 0xf8
14132c6eb: test sil, r15b
14132c6ee: cmc 
14132c6ef: xor r11b, byte ptr [r8 + 3]
14132c6f3: clc 
14132c6f4: xor r9b, r11b
14132c6f7: test bpl, 0xa1
14132c6fb: clc 
14132c6fc: cmp r12, r15
14132c6ff: xor r10, r10
14132c702: xor r10, qword ptr [rip - 0x3d8191]
14132c709: cmp r14b, r8b
14132c70c: xor r11, r11
14132c70f: cmp ah, dl
14132c711: test r14b, 0xec
14132c715: cmp r9w, 0x11
14132c71b: xor r11, qword ptr [r10 + r9*8]
14132c71f: xor r11, r10
14132c722: or r9b, 0x75
14132c726: stc 
14132c727: xor r9w, r8w
14132c72b: xor r10, r11
14132c72e: pushfq 
14132c72f: xor r9d, r9d
14132c732: or r9d, 0
14132c786: popfq 
14132c787: mov r9b, byte ptr [r8 + 7]
14132c78b: test r12b, r15b
14132c78e: mov r9b, byte ptr [r10 + r9]
14132c792: test r11d, r10d
14132c795: sub r11, r11
14132c798: btr r10w, bx
14132c79d: bsf r10w, di
14132c7a2: movsx r10d, di
14132c7a6: xor r11b, byte ptr [r8 + 0xb]
14132c7aa: bsr r10w, si
14132c7af: xor r10, rax
14132c7b2: xor r11b, r9b
14132c7b5: sar r10d, cl
14132c7b8: add r10, r11
14132c7bb: xor byte ptr [r8 + 0xb], r11b
14132c7bf: xor r10b, 0x5d
14132c7c3: test r8b, r14b
14132c7c6: ror r10w, 0x9e
14132c7cb: xor r9d, r9d
14132c7ce: movsxd r10, edx
14132c7d1: sar r10w, 0xea
14132c7d6: or r9d, dword ptr [r8 + 8]
14132c7da: shl r10w, cl
14132c7de: mov r10w, bp
14132c7e2: movzx r10w, al
14132c7e7: and dword ptr [r8 + 0x368], 0
14132c7ef: sal r10b, cl
14132c7f2: or dword ptr [r8 + 0x368], r9d
14132c7f9: sub r9d, r9d
14132c7fc: inc r10d
14132c7ff: or r9d, dword ptr [r8 + 0x344]
14132c806: cmp rax, rbp
14132c809: sub r11, r11
14132c80c: ror r10d, cl
14132c80f: setno r10b
14132c813: sbb r10, 0x6d3f7966
14132c81a: xor r11d, dword ptr [r8]
14132c81d: bt r10d, 0xc8
14132c822: xor r11d, r9d
14132c825: mov r10d, 0x63f41569
14132c82b: xor dword ptr [r8], r11d
14132c82e: adc r10b, 0x71
14132c832: bsr r10w, r15w
14132c837: clc 
14132c838: xor r9d, r9d
14132c83b: rcr r10b, 0x19
14132c83f: xor r9d, dword ptr [r8 + 0x35c]
14132c846: ror r10w, 0xd1
14132c84b: and r10d, 0x2ebd2207
14132c852: and dword ptr [r8 + 4], 0
14132c857: btr r10w, dx
14132c85c: xor dword ptr [r8 + 4], r9d
14132c860: sal r10b, cl
14132c863: sbb r10w, bx
14132c867: xor r9d, r9d
14132c86a: sal r10b, 0x5f
14132c86e: btr r10, 0x2a
14132c873: or r9d, 0
14132c877: jmp 0x141395986
141395986: mov r9b, byte ptr [r8]
141395989: bsr r10d, r11d
14139598d: mov r10, qword ptr [rip - 0x46243c]
141395994: cmp r13w, 0x2987
14139599a: sub r11, r11
14139599d: test r10, 0x33e56e4f
1413959a4: xor r11, qword ptr [r10 + r9*8]
1413959a8: cmp dx, r9w
1413959ac: test r15, 0x82031a7
1413959b3: xor r11, r10
1413959b6: stc 
1413959b7: test r12w, r14w
1413959bb: clc 
1413959bc: xor r10, r11
1413959bf: xor r9d, r9d
1413959c2: xor r9d, 0
1413959c6: xor r11, r11
1413959c9: jmp 0x1412b53fb
1412b53fb: xor r11b, r9b
1412b53fe: xor r11b, byte ptr [r8 + 4]
1412b5402: test dx, 0x2cc1
1412b5407: xor r9b, r11b
1412b540a: xor r11, r11
1412b540d: jmp 0x1413c8247
1413c8247: xor r11b, byte ptr [r10 + r9]
1413c824b: or r10w, r15w
1413c824f: sal r10w, 0x72
1413c8254: xor r11b, r9b
1413c8257: rcr r10b, cl
1413c825a: movzx r10w, bpl
1413c825f: xor r10w, ax
1413c8263: xor r9b, r11b
1413c8266: sar r10d, 0x23
1413c826a: mov byte ptr [r8 + 8], r9b
1413c826e: xor r9d, r9d
1413c8271: inc r10w
1413c8275: shl r10w, cl
1413c8279: bts r10w, r10w
1413c827e: xor r9d, 0
1413c8282: mov r9b, byte ptr [r8 + 1]
1413c8286: movzx r10w, sil
1413c828b: and r10, rax
1413c828e: mov r10, qword ptr [rip - 0x494d3d]
1413c8295: cmc 
1413c8296: clc 
1413c8297: mov r10, qword ptr [r10 + r9*8]
1413c829b: sub r11, r11
1413c829e: test r12, 0x5cf83bd8
1413c82a5: clc 
1413c82a6: xor r11d, r9d
1413c82a9: jmp 0x1412e4ce9
1412e4ce9: xor r11d, 0
1412e4ced: test r8d, eax
1412e4cf0: xor r9d, r11d
1412e4cf3: shl r9b, 0x12
1412e4cf7: mov r9b, byte ptr [r8 + 5]
1412e4cfb: clc 
1412e4cfc: xor r11, r11
1412e4cff: xor r11b, byte ptr [r10 + r9]
1412e4d03: stc 
1412e4d04: xchg r11b, r9b
1412e4d07: cmp dh, 0xdc
1412e4d0a: mov byte ptr [r8 + 9], r9b
1412e4d0e: sub r11, r11
1412e4d11: clc 
1412e4d12: xor r11d, r9d
1412e4d15: xor r11d, 0
1412e4d19: xor r9d, r11d
1412e4d1c: mov r9b, byte ptr [r8 + 2]
1412e4d20: xor r11, r11
1412e4d23: stc 
1412e4d24: jmp 0x1414874f0
1414874f0: xor r11, r10
1414874f3: test r15, 0x616617bc
1414874fa: clc 
1414874fb: cmc 
1414874fc: xor r11, qword ptr [rip - 0x553fab]
141487503: cmc 
141487504: test r11b, 0xd5
141487508: xor r10, r11
14148750b: test r8b, r10b
14148750e: xor r11, r11
141487511: cmp r13d, r15d
141487514: xor r11, qword ptr [r10 + r9*8]
141487518: stc 
141487519: cmp ah, 0
14148751c: xchg r11, r10
14148751f: xor r9d, r9d
141487522: or r9d, 0
141487526: and r9b, 0
14148752a: clc 
14148752b: test dl, r10b
14148752e: xor r9b, byte ptr [r8 + 6]
141487532: test r12, 0x3035440d
141487539: stc 
14148753a: sub r11, r11
14148753d: xor r11b, byte ptr [r10 + r9]
141487541: rcl r10, 0x4b
141487545: xchg r10b, r10b
141487548: xor r11b, r9b
14148754b: shl r10w, cl
14148754f: add r10d, 0x11047a6e
141487556: xor r9b, r11b
141487559: jmp 0x14130fcab
14130fcab: sub r11, r11
14130fcae: or r10b, bpl
14130fcb1: xor r11b, byte ptr [r8 + 0xa]
14130fcb5: xadd r10b, r10b
14130fcb9: movsx r10d, si
14130fcbd: xor r11b, r9b
14130fcc0: movsx r10, r15w
14130fcc4: xor byte ptr [r8 + 0xa], r11b
14130fcc8: movsx r10w, r12b
14130fccd: mov r10b, 0xbe
14130fcd0: sub r11, r11
14130fcd3: sal r10b, 0xde
14130fcd7: xor r10b, spl
14130fcda: jmp 0x141464203
141464203: xor r11d, r9d
141464206: add r10b, 0xe5
14146420a: shrd r10w, sp, 0x5c
141464210: xor r11d, 0
141464214: mov r10b, cl
141464217: not r10b
14146421a: rcr r10b, 0x2c
14146421e: xor r9d, r11d
141464221: xchg r10w, r10w
141464225: dec r10w
141464229: xadd r10b, r10b
14146422d: xor r11, r11
141464230: bsr r10, rbx
141464234: rcr r10b, cl
141464237: xor r11b, r9b
14146423a: xor r11b, byte ptr [r8 + 3]
14146423e: jmp 0x14141c0a6
14141c0a6: xor r9b, r11b
14141c0a9: xadd r10w, r10w
14141c0ae: dec r10w
14141c0b2: test r12b, r8b
14141c0b5: mov r10, qword ptr [rip - 0x4e8b64]
14141c0bc: sub r11, r11
14141c0bf: cmc 
14141c0c0: xor r11, qword ptr [r10 + r9*8]
14141c0c4: stc 
14141c0c5: cmp r9d, 0x6c2257d3
14141c0cc: xchg r11, r10
14141c0cf: xor r11, r11
14141c0d2: cmp r13d, r11d
14141c0d5: cmc 
14141c0d6: xor r11d, r9d
14141c0d9: test r12, r10
14141c0dc: cmp r11b, r15b
14141c0df: xor r11d, 0
14141c0e3: cmc 
14141c0e4: stc 
14141c0e5: xor r9d, r11d
14141c0e8: clc 
14141c0e9: and r9b, 0
14141c0ed: xor r9b, byte ptr [r8 + 7]
14141c0f1: cmc 
14141c0f2: test r12, r15
14141c0f5: mov r9b, byte ptr [r10 + r9]
14141c0f9: jmp 0x14136ca5c
14136ca5c: xor r11, r11
14136ca5f: jmp 0x14144aa87
14144aa87: xor r11b, byte ptr [r8 + 0xb]
14144aa8b: cmc 
14144aa8c: stc 
14144aa8d: xor r11b, r9b
14144aa90: xor byte ptr [r8 + 0xb], r11b
14144aa94: clc 
14144aa95: jmp 0x141278d71
141278d71: xor r11, r11
141278d74: cmp r8b, al
141278d77: test r14b, 1
141278d7b: xor r11d, r9d
141278d7e: jmp 0x14133dcf2
14133dcf2: xor r11d, dword ptr [r8 + 8]
14133dcf6: test bh, 0xc6
14133dcf9: xor r9d, r11d
14133dcfc: test r10b, bl
14133dcff: and dword ptr [r8 + 0x36c], 0
14133dd07: clc 
14133dd08: xor dword ptr [r8 + 0x36c], r9d
14133dd0f: jmp 0x1412d5f31
1412d5f31: sub r9d, r9d
1412d5f34: test dx, r14w
1412d5f38: cmc 
1412d5f39: xor r9d, dword ptr [r8 + 0x368]
1412d5f40: test r10w, r11w
1412d5f44: mov dword ptr [r8], r9d
1412d5f47: clc 
1412d5f48: not r9b
1412d5f4b: pushfq 
1412d5f4c: xor r9d, r9d
1412d5f4f: or r9d, dword ptr [r8 + 0x36c]
1412d5fa1: popfq 
1412d5fa2: mov dword ptr [r8 + 4], r9d
1412d5fa6: pushfq 
1412d5fa7: xor r9d, r9d
1412d5faa: or r9d, 0
1412d5ffc: popfq 
1412d5ffd: mov r9b, byte ptr [r8]
1412d6000: test r8, 0x3285191a
1412d6007: xor r11, r11
1412d600a: clc 
1412d600b: xor r11, r10
1412d600e: test r9w, 0x4c30
1412d6014: cmc 
1412d6015: xor r11, qword ptr [rip - 0x381aa4]
1412d601c: clc 
1412d601d: cmp cl, 2
1412d6020: xor r10, r11
1412d6023: cmp r10w, 0x7f19
1412d6029: cmp dx, ax
1412d602c: sub r11, r11
1412d602f: xor r11, qword ptr [r10 + r9*8]
1412d6033: cmp r13b, 0xf4
1412d6037: xor r11, r10
1412d603a: cmp al, r11b
1412d603d: xor r10, r11
1412d6040: jmp 0x1413729f5
1413729f5: sub r9d, r9d
1413729f8: test sil, 0x9a
1413729fc: xor r9d, 0
141372a00: test r12b, r8b
141372a03: and r9b, 0
141372a07: clc 
141372a08: test eax, r14d
141372a0b: xor r9b, byte ptr [r8 + 4]
141372a0f: xor r11, r11
141372a12: cmp rdx, r13
141372a15: xor r11b, byte ptr [r10 + r9]
141372a19: cmc 
141372a1a: stc 
141372a1b: test r9b, bl
141372a1e: xchg r11b, r9b
141372a21: test di, r13w
141372a25: clc 
141372a26: xor r11, r11
141372a29: cmp dil, 0x48
141372a2d: test dl, 0xdd
141372a30: xor r11b, byte ptr [r8 + 8]
141372a34: xor r11b, r9b
141372a37: xor byte ptr [r8 + 8], r11b
141372a3b: sub r9d, r9d
141372a3e: stc 
141372a3f: cmp bl, cl
141372a41: or r9d, 0
141372a45: test r9w, 0x597f
141372a4b: clc 
141372a4c: and r9b, 0
141372a50: test r10b, 0x81
141372a54: or r9b, byte ptr [r8 + 1]
141372a58: test bp, dx
141372a5b: clc 
141372a5c: cmp bp, r12w
141372a60: sub r10, r10
141372a63: or r10, qword ptr [rip - 0x41e4f2]
141372a6a: sub r11, r11
141372a6d: xor r11, qword ptr [r10 + r9*8]
141372a71: jmp 0x141492adf
141492adf: xchg r11, r10
141492ae2: jmp 0x1413fbec8
1413fbec8: xor r11, r11
1413fbecb: cmp r10b, r10b
1413fbece: xor r11d, r9d
1413fbed1: clc 
1413fbed2: xor r11d, 0
1413fbed6: test r8b, 0x4e
1413fbeda: cmp r11b, bl
1413fbedd: clc 
1413fbede: xor r9d, r11d
1413fbee1: stc 
1413fbee2: and r9b, 0
1413fbee6: test ebp, esi
1413fbee8: jmp 0x1412ca87c
1412ca87c: or r9b, byte ptr [r8 + 5]
1412ca880: jmp 0x141250c32
141250c32: xor r11, r11
141250c35: cmp rax, r10
141250c38: xor r11b, byte ptr [r10 + r9]
141250c3c: xor r11b, r9b
141250c3f: cmp cx, r13w
141250c43: cmp si, 0x87d
141250c48: xor r9b, r11b
141250c4b: jmp 0x1414ac51f
1414ac51f: and byte ptr [r8 + 9], 0
1414ac524: test r11b, 0x11
1414ac528: test bpl, r13b
1414ac52b: xor byte ptr [r8 + 9], r9b
1414ac52f: clc 
1414ac530: test dil, 0x2d
1414ac534: sub r11, r11
1414ac537: cmp dil, bpl
1414ac53a: xor r11d, r9d
1414ac53d: cmc 
1414ac53e: test cl, 0x67
1414ac541: xor r11d, 0
1414ac545: xor r9d, r11d
1414ac548: jmp 0x1412dfbc9
1412dfbc9: mov r9b, byte ptr [r8 + 2]
1412dfbcd: cmp rdx, r14
1412dfbd0: xor r10, r10
1412dfbd3: or r10, qword ptr [rip - 0x38b662]
1412dfbda: cmp r14w, 0x2990
1412dfbe0: xor r11, r11
1412dfbe3: cmp dil, 0xa2
1412dfbe7: clc 
1412dfbe8: xor r11, qword ptr [r10 + r9*8]
1412dfbec: jmp 0x14144cf02
14144cf02: xor r11, r10
14144cf05: cmp bp, 0x5628
14144cf0a: test ah, 0xa7
14144cf0d: xor r10, r11
14144cf10: cmc 
14144cf11: sub r9d, r9d
14144cf14: test si, 0x7934
14144cf19: or r9d, 0
14144cf1d: cmp r10, rbx
14144cf20: xor r11, r11
14144cf23: cmp r15b, 0x21
14144cf27: test r10d, r12d
14144cf2a: xor r11b, r9b
14144cf2d: xor r11b, byte ptr [r8 + 6]
14144cf31: jmp 0x1413063e8
1413063e8: xor r9b, r11b
1413063eb: cmp bx, si
1413063ee: xor r11, r11
1413063f1: test ch, 0x9f
1413063f4: xor r11b, byte ptr [r10 + r9]
1413063f8: xchg r11b, r9b
1413063fb: rcr r10b, 0xf0
1413063ff: sub r11, r11
141306402: or r10w, 0x30db
141306408: btr r10w, bp
14130640d: xor r11b, byte ptr [r8 + 0xa]
141306411: cmovle r10w, r15w
141306416: xor r11b, r9b
141306419: xor byte ptr [r8 + 0xa], r11b
14130641d: sbb r10w, 0x37b5
141306423: cmc 
141306424: sub r11, r11
141306427: xor r11d, r9d
14130642a: xor r11d, 0
14130642e: stc 
14130642f: xor r9d, r11d
141306432: sub r11, r11
141306435: sbb r10b, cl
141306438: xor r11b, r9b
14130643b: movsxd r10, eax
14130643e: xor r11b, byte ptr [r8 + 3]
141306442: xor r9b, r11b
141306445: shld r10d, r10d, 0x17
14130644a: or r10b, 0xc7
14130644e: bts r10, rsp
141306452: mov r10, qword ptr [rip - 0x3b1ee1]
141306459: clc 
14130645a: xor r11, r11
14130645d: jmp 0x14132069e
14132069e: xor r11, qword ptr [r10 + r9*8]
1413206a2: sar r9d, 0x40
1413206a6: rcl r9, 0xd6
1413206aa: xor r11, r10
1413206ad: btr r9, r12
1413206b1: xor r10, r11
1413206b4: mov r9w, 0x4ce2
1413206b9: cmp r9b, bpl
1413206bc: dec r9w
1413206c0: pushfq 
1413206c1: xor r9d, r9d
1413206c4: or r9d, 0
14132070a: popfq 
14132070b: sub r11, r11
14132070e: clc 
14132070f: jmp 0x14126429e
14126429e: xor r11b, r9b
1412642a1: stc 
1412642a2: xor r11b, byte ptr [r8 + 7]
1412642a6: cmp r11b, r10b
1412642a9: test rsi, r8
1412642ac: clc 
1412642ad: xor r9b, r11b
1412642b0: cmp bl, 0xe0
1412642b3: stc 
1412642b4: xor r11, r11
1412642b7: test spl, r12b
1412642ba: cmp r14w, r10w
1412642be: test cx, 0x5d59
1412642c3: xor r11b, byte ptr [r10 + r9]
1412642c7: cmp cx, 0x38f8
1412642cc: stc 
1412642cd: xchg r11b, r9b
1412642d0: clc 
1412642d1: and byte ptr [r8 + 0xb], 0
1412642d6: cmp r13b, r14b
1412642d9: test esp, ebp
1412642db: or byte ptr [r8 + 0xb], r9b
1412642df: pushfq 
1412642e0: xor r9d, r9d
1412642e3: or r9d, dword ptr [r8 + 8]
141264332: popfq 
141264333: and dword ptr [r8 + 0x370], 0
14126433b: cmp r9b, dil
14126433e: xor dword ptr [r8 + 0x370], r9d
141264345: test eax, 0x1e996227
14126434a: sub r9d, r9d
14126434d: stc 
14126434e: xor r9d, 0
141264352: test r12b, 0xb8
141264356: xor r11, r11
141264359: test rsp, 0x419b4bc3
141264360: cmc 
141264361: xor r11b, r9b
141264364: cmp al, r11b
141264367: xor r11b, byte ptr [r8 + 0x347]
14126436e: clc 
14126436f: test r14b, 0x91
141264373: xor r9b, r11b
141264376: stc 
141264377: cmc 
141264378: sub r10, r10
14126437b: cmp edx, r15d
14126437e: jmp 0x141261a68
141261a68: xor r10, qword ptr [rip - 0x2baca7]
141261a6f: xor r11, r11
141261a72: xor r11, qword ptr [r10 + r9*8]
141261a76: cmp r13w, r11w
141261a7a: test r15, 0xa4d347e
141261a81: xchg r11, r10
141261a84: jmp 0x1412912a7
1412912a7: sub r11, r11
1412912aa: cmp r14, 0x53e434f1
1412912b1: xor r11d, r9d
1412912b4: cmc 
1412912b5: test r14b, 0x66
1412912b9: clc 
1412912ba: xor r11d, 0
1412912be: xor r9d, r11d
1412912c1: test spl, r10b
1412912c4: xor r11, r11
1412912c7: jmp 0x1413f93e9
1413f93e9: xor r11b, r9b
1413f93ec: cmc 
1413f93ed: clc 
1413f93ee: xor r11b, byte ptr [r8 + 0x346]
1413f93f5: xor r9b, r11b
1413f93f8: cmp r9w, r10w
1413f93fc: stc 
1413f93fd: xor r11, r11
1413f9400: xor r11b, byte ptr [r10 + r9]
1413f9404: cmp r10w, r8w
1413f9408: xor r11b, r9b
1413f940b: xor r9b, r11b
1413f940e: jmp 0x1412bbb95
1412bbb95: and byte ptr [r8 + 0x374], 0
1412bbb9d: or byte ptr [r8 + 0x374], r9b
1412bbba4: sub r9d, r9d
1412bbba7: clc 
1412bbba8: xor r9d, 0
1412bbbac: jmp 0x14136c433
14136c433: xor r11, r11
14136c436: test bpl, 0xc
14136c43a: xor r11b, r9b
14136c43d: xor r11b, byte ptr [r8 + 0x344]
14136c444: xor r9b, r11b
14136c447: test r9w, 0x3ab2
14136c44d: cmc 
14136c44e: sub r11, r11
14136c451: xor r11, r10
14136c454: cmp r14w, 0x5eba
14136c45a: xor r11, qword ptr [rip - 0x3c5699]
14136c461: xor r10, r11
14136c464: cmp sil, 0xb1
14136c468: xor r11, r11
14136c46b: cmp r15w, 0x2e45
14136c471: xor r11, qword ptr [r10 + r9*8]
14136c475: xor r11, r10
14136c478: cmc 
14136c479: clc 
14136c47a: xor r10, r11
14136c47d: stc 
14136c47e: sub r11, r11
14136c481: jmp 0x1412954e2
1412954e2: xor r11d, r9d
1412954e5: test si, 0x6fb4
1412954ea: cmp r15w, ax
1412954ee: xor r11d, 0
1412954f2: cmp cl, spl
1412954f5: stc 
1412954f6: cmp di, 0x4d53
1412954fb: xor r9d, r11d
1412954fe: stc 
1412954ff: xor r11, r11
141295502: jmp 0x1414539ed
1414539ed: xor r11b, r9b
1414539f0: xor r11b, byte ptr [r8 + 0x347]
1414539f7: xor r9b, r11b
1414539fa: mov r9b, byte ptr [r10 + r9]
1414539fe: clc 
1414539ff: and byte ptr [r8 + 0x375], 0
141453a07: xor byte ptr [r8 + 0x375], r9b
141453a0e: stc 
141453a0f: xor r11, r11
141453a12: xor r11d, r9d
141453a15: test r10b, 0x13
141453a19: cmp r8b, r12b
141453a1c: xor r11d, 0
141453a20: cmc 
141453a21: cmp al, r10b
141453a24: xor r9d, r11d
141453a27: test r9b, 0x58
141453a2b: jmp 0x141317d4b
141317d4b: and r9b, 0
141317d4f: cmc 
141317d50: test sp, r13w
141317d54: xor r9b, byte ptr [r8 + 0x345]
141317d5b: jmp 0x1412d9dc3
1412d9dc3: xor r10, r10
1412d9dc6: cmp r8b, bl
1412d9dc9: stc 
1412d9dca: xor r10, qword ptr [rip - 0x333009]
1412d9dd1: clc 
1412d9dd2: jmp 0x1414925e3
1414925e3: xor r11, r11
1414925e6: jmp 0x14139944e
14139944e: xor r11, qword ptr [r10 + r9*8]
141399452: xor r11, r10
141399455: test dh, 0x4d
141399458: clc 
141399459: xor r10, r11
14139945c: test r15b, 0x5f
141399460: test bl, r8b
141399463: xor r9d, r9d
141399466: test r14w, 0x18f1
14139946c: xor r9d, 0
141399470: stc 
141399471: jmp 0x141405deb
141405deb: and r9b, 0
141405def: test rsp, r11
141405df2: or r9b, byte ptr [r8 + 0x344]
141405df9: xor r11, r11
141405dfc: test r10d, 0x565a1cce
141405e03: stc 
141405e04: xor r11b, byte ptr [r10 + r9]
141405e08: cmp r12w, r14w
141405e0c: xchg r11b, r9b
141405e0f: xor r11, r11
141405e12: jmp 0x14148e294
14148e294: xor r11b, byte ptr [r8 + 0x376]
14148e29b: stc 
14148e29c: jmp 0x1414a230c
1414a230c: xor r11b, r9b
1414a230f: test r15b, sil
1414a2312: xor byte ptr [r8 + 0x376], r11b
1414a2319: sub r9d, r9d
1414a231c: test r12w, 0x60e
1414a2322: jmp 0x14132f1ce
14132f1ce: or r9d, 0
14132f1d2: mov r9b, byte ptr [r8 + 0x346]
14132f1d9: sub r10, r10
14132f1dc: or r10, qword ptr [rip - 0x38841b]
14132f1e3: stc 
14132f1e4: jmp 0x141338938
141338938: xor r11, r11
14133893b: xor r11, qword ptr [r10 + r9*8]
14133893f: bts r9w, ax
141338944: xor r11, r10
141338947: xor r10, r11
14133894a: pushfq 
14133894b: xor r9d, r9d
14133894e: or r9d, 0
1413389a0: popfq 
1413389a1: mov r9b, byte ptr [r8 + 0x345]
1413389a8: cmp r15w, 0x103a
1413389ae: clc 
1413389af: sub r11, r11
1413389b2: xor r11b, byte ptr [r10 + r9]
1413389b6: cmc 
1413389b7: clc 
1413389b8: cmp r14b, 1
1413389bc: xchg r11b, r9b
1413389bf: sub r11, r11
1413389c2: cmp dx, r13w
1413389c6: clc 
1413389c7: xor r11b, byte ptr [r8 + 0x377]
1413389ce: stc 
1413389cf: xor r11b, r9b
1413389d2: shrd r9d, r14d, 0xa5
1413389d7: xor byte ptr [r8 + 0x377], r11b
1413389de: xchg r9b, r9b
1413389e1: cmp dl, spl
1413389e4: pushfq 
1413389e5: and r9d, 0
1413389ec: xor r9d, dword ptr [r8 + 0x334]
141338a24: popfq 
141338a25: mov dword ptr [r8], r9d
141338a28: sub r11, r11
141338a2b: xor r11d, r9d
141338a2e: test r14b, 0xba
141338a32: clc 
141338a33: cmp eax, 0x4ad457ab
141338a38: xor r11d, dword ptr [r8 + 0x374]
141338a3f: xor r9d, r11d
141338a42: cmp r10b, 0x41
141338a46: sub r11, r11
141338a49: xor r11d, dword ptr [r8 + 4]
141338a4d: stc 
141338a4e: xor r11d, r9d
141338a51: rcl r9w, cl
141338a55: xor dword ptr [r8 + 4], r11d
141338a59: movsx r9w, r10b
141338a5e: movzx r9d, ax
141338a62: pushfq 
141338a63: xor r9d, r9d
141338a66: or r9d, 0
141338aba: popfq 
141338abb: mov r9b, byte ptr [r8]
141338abe: sub r11, r11
141338ac1: xor r11, r10
141338ac4: test r12b, bpl
141338ac7: cmc 
141338ac8: xor r11, qword ptr [rip - 0x405577]
141338acf: xor r10, r11
141338ad2: sub r11, r11
141338ad5: clc 
141338ad6: stc 
141338ad7: xor r11, qword ptr [r10 + r9*8]
141338adb: test al, bpl
141338ade: cmp r8b, sil
141338ae1: xchg r11, r10
141338ae4: stc 
141338ae5: clc 
141338ae6: cmc 
141338ae7: sub r9d, r9d
141338aea: cmp r14b, 0xe1
141338aee: jmp 0x1412c0755
1412c0755: or r9d, 0
1412c0759: xor r11, r11
1412c075c: jmp 0x14147101a
14147101a: xor r11b, r9b
14147101d: stc 
14147101e: cmc 
14147101f: xor r11b, byte ptr [r8 + 4]
141471023: test sil, bpl
141471026: jmp 0x141263a88
141263a88: xor r9b, r11b
141263a8b: xor r11, r11
141263a8e: cmp r8w, 0x45eb
141263a94: xor r11b, byte ptr [r10 + r9]
141263a98: clc 
141263a99: cmp r8b, 0xd1
141263a9d: xchg r11b, r9b
141263aa0: mov byte ptr [r8 + 8], r9b
141263aa4: xor r9d, r9d
141263aa7: xor r9d, 0
141263aab: cmc 
141263aac: test ax, 0x2a22
141263ab0: and r9b, 0
141263ab4: clc 
141263ab5: stc 
141263ab6: test r9w, r10w
141263aba: xor r9b, byte ptr [r8 + 1]
141263abe: cmp r12, 0x60951cfd
141263ac5: jmp 0x14125a0ab
14125a0ab: xor r11, r11
14125a0ae: test r14w, 0x1a67
14125a0b4: xor r11, r10
14125a0b7: xor r11, qword ptr [rip - 0x326b66]
14125a0be: cmp r15b, r15b
14125a0c1: jmp 0x141370dbc
141370dbc: xor r10, r11
141370dbf: cmp r15w, bp
141370dc3: sub r11, r11
141370dc6: test r14b, 0x3e
141370dca: test spl, r8b
141370dcd: xor r11, qword ptr [r10 + r9*8]
141370dd1: jmp 0x1413c1ea7
1413c1ea7: xor r11, r10
1413c1eaa: test r12d, 0x25f02241
1413c1eb1: xor r10, r11
1413c1eb4: cmc 
1413c1eb5: test r11b, 0x17
1413c1eb9: xor r9d, r9d
1413c1ebc: or r9d, 0
1413c1ec0: mov r9b, byte ptr [r8 + 5]
1413c1ec4: xor r11, r11
1413c1ec7: jmp 0x14131e5ab
14131e5ab: xor r11b, byte ptr [r10 + r9]
14131e5af: xor r11b, r9b
14131e5b2: xor r9b, r11b
14131e5b5: stc 
14131e5b6: cmc 
14131e5b7: sub r11, r11
14131e5ba: xor r11b, byte ptr [r8 + 9]
14131e5be: cmc 
14131e5bf: cmp cl, r10b
14131e5c2: xor r11b, r9b
14131e5c5: test bx, r14w
14131e5c9: xor byte ptr [r8 + 9], r11b
14131e5cd: sub r11, r11
14131e5d0: cmp ax, r12w
14131e5d4: cmc 
14131e5d5: xor r11d, r9d
14131e5d8: jmp 0x1412532e6
1412532e6: xor r11d, 0
1412532ea: test r9w, 0x4d28
1412532f0: test r15b, dil
1412532f3: xor r9d, r11d
1412532f6: sub r11, r11
1412532f9: stc 
1412532fa: xor r11b, r9b
1412532fd: test r9w, cx
141253301: cmc 
141253302: xor r11b, byte ptr [r8 + 2]
141253306: xor r9b, r11b
141253309: xor r11, r11
14125330c: test r11w, 0x65e6
141253312: xor r11, r10
141253315: test cx, 0x291e
14125331a: cmc 
14125331b: xor r11, qword ptr [rip - 0x31fdca]
141253322: cmp bpl, 0x47
141253326: jmp 0x1413c62b4
1413c62b4: xor r10, r11
1413c62b7: cmc 
1413c62b8: sub r11, r11
1413c62bb: test r10, r11
1413c62be: xor r11, qword ptr [r10 + r9*8]
1413c62c2: cmc 
1413c62c3: xchg r11, r10
1413c62c6: xor r9d, r9d
1413c62c9: cmp dl, bl
1413c62cb: xor r9d, 0
1413c62cf: test r12w, 0x1c7e
1413c62d5: jmp 0x1412548e8
1412548e8: and r9b, 0
1412548ec: test rdi, r12
1412548ef: cmp edx, r9d
1412548f2: test bp, 0x2e1d
1412548f7: xor r9b, byte ptr [r8 + 6]
1412548fb: mov r9b, byte ptr [r10 + r9]
1412548ff: mov r10w, 0x46fa
141254904: sub r11, r11
141254907: xor r11b, byte ptr [r8 + 0xa]
14125490b: bswap r10
14125490e: xor r11b, r9b
141254911: xor byte ptr [r8 + 0xa], r11b
141254915: cmovle r10d, r12d
141254919: stc 
14125491a: xor r9d, r9d
14125491d: cmc 
14125491e: movsx r10, r9w
141254922: or r9d, 0
141254926: rol r10b, 0xdf
14125492a: xchg r10w, r10w
14125492e: cmp r9b, 0x6a
141254932: sub r11, r11
141254935: add r10w, r10w
141254939: xor r11b, r9b
14125493c: xor r11b, byte ptr [r8 + 3]
141254940: sub r10w, r12w
141254944: bts r10w, cx
141254949: xor r9b, r11b
14125494c: movzx r10w, r11b
141254951: movsx r10d, si
141254955: btr r10w, 0x8c
14125495b: mov r10, qword ptr [rip - 0x32140a]
141254962: xor r11, r11
141254965: clc 
141254966: stc 
141254967: xor r11, qword ptr [r10 + r9*8]
14125496b: adc r9, rbx
14125496e: xchg r11, r10
141254971: test dil, 0xef
141254975: sal r9d, 0xfb
141254979: bsr r9, r10
14125497d: pushfq 
14125497e: and r9d, 0
141254985: xor r9d, 0
1412549bd: popfq 
1412549be: and r9b, 0
1412549c2: cmp dil, r13b
1412549c5: or r9b, byte ptr [r8 + 7]
1412549c9: test ebx, 0x52712ae5
1412549cf: cmp al, 0xe4
1412549d1: clc 
1412549d2: xor r11, r11
1412549d5: cmc 
1412549d6: xor r11b, byte ptr [r10 + r9]
1412549da: jmp 0x1413dfd86
1413dfd86: xchg r11b, r9b
1413dfd89: jmp 0x1413b818d
1413b818d: sub r11, r11
1413b8190: xor r11b, byte ptr [r8 + 0xb]
1413b8194: xor r11b, r9b
1413b8197: xor byte ptr [r8 + 0xb], r11b
1413b819b: pushfq 
1413b819c: and r9d, 0
1413b81a3: xor r9d, dword ptr [r8 + 8]
1413b81d8: popfq 
1413b81d9: mov dword ptr [r8 + 0x378], r9d
1413b81e0: sub r9d, r9d
1413b81e3: or r9d, dword ptr [r8 + 0x378]
1413b81ea: jmp 0x1413e98c1
1413e98c1: and dword ptr [r8], 0
1413e98c5: jmp 0x14149919b
14149919b: xor dword ptr [r8], r9d
14149919e: sub r9d, r9d
1414991a1: xor r9d, dword ptr [r8 + 0x2c]
1414991a5: stc 
1414991a6: cmp r15w, 0x12fd
1414991ac: mov dword ptr [r8 + 4], r9d
1414991b0: test r10b, r11b
1414991b3: xor r9d, r9d
1414991b6: or r9d, 0
1414991ba: cmp bx, r8w
1414991be: xor r11, r11
1414991c1: cmp r8b, 0x8c
1414991c5: cmp r15b, al
1414991c8: jmp 0x141367aad
141367aad: xor r11b, r9b
141367ab0: cmc 
141367ab1: cmp r9w, r13w
141367ab5: xor r11b, byte ptr [r8]
141367ab8: test dl, dil
141367abb: cmp rbp, r12
141367abe: clc 
141367abf: xor r9b, r11b
141367ac2: sub r10, r10
141367ac5: clc 
141367ac6: cmp ecx, r9d
141367ac9: or r10, qword ptr [rip - 0x434578]
141367ad0: sub r11, r11
141367ad3: xor r11, qword ptr [r10 + r9*8]
141367ad7: xor r11, r10
141367ada: jmp 0x1412c35a2
1412c35a2: xor r10, r11
1412c35a5: xor r9d, r9d
1412c35a8: jmp 0x1413d7c47
1413d7c47: or r9d, 0
1413d7c4b: and r9b, 0
1413d7c4f: cmp r9, r14
1413d7c52: cmc 
1413d7c53: test r10w, 0x1d8c
1413d7c59: xor r9b, byte ptr [r8 + 4]
1413d7c5d: stc 
1413d7c5e: jmp 0x141451ac0
141451ac0: sub r11, r11
141451ac3: jmp 0x14149e021
14149e021: xor r11b, byte ptr [r10 + r9]
14149e025: stc 
14149e026: xor r11b, r9b
14149e029: cmp dl, 0x65
14149e02c: cmc 
14149e02d: cmp r13b, bpl
14149e030: xor r9b, r11b
14149e033: and byte ptr [r8 + 8], 0
14149e038: clc 
14149e039: or byte ptr [r8 + 8], r9b
14149e03d: jmp 0x1412ccbca
1412ccbca: sub r11, r11
1412ccbcd: clc 
1412ccbce: xor r11d, r9d
1412ccbd1: xor r11d, 0
1412ccbd5: stc 
1412ccbd6: xor r9d, r11d
1412ccbd9: and r9b, 0
1412ccbdd: xor r9b, byte ptr [r8 + 1]
1412ccbe1: test spl, 0x47
1412ccbe5: cmp r14w, cx
1412ccbe9: jmp 0x1412912cc
1412912cc: sub r11, r11
1412912cf: cmp r9, 0x172267fc
1412912d6: xor r11, r10
1412912d9: cmp di, 0x7b25
1412912de: xor r11, qword ptr [rip - 0x35dd8d]
1412912e5: clc 
1412912e6: test cl, r12b
1412912e9: xor r10, r11
1412912ec: test r8b, r15b
1412912ef: mov r10, qword ptr [r10 + r9*8]
1412912f3: not r9b
1412912f6: sal r9b, 0xdf
1412912fa: pushfq 
1412912fb: xor r9d, r9d
1412912fe: or r9d, 0
141291344: popfq 
141291345: sub r11, r11
141291348: cmp r9b, 0xc4
14129134c: xor r11b, r9b
14129134f: cmp r8b, cl
141291352: clc 
141291353: xor r11b, byte ptr [r8 + 5]
141291357: xor r9b, r11b
14129135a: jmp 0x14149a4db
14149a4db: sub r11, r11
14149a4de: cmp r11w, 0x33a0
14149a4e4: test r14, rcx
14149a4e7: xor r11b, byte ptr [r10 + r9]
14149a4eb: xchg r11b, r9b
14149a4ee: xor r11, r11
14149a4f1: clc 
14149a4f2: cmc 
14149a4f3: test bp, 0x3fb5
14149a4f8: xor r11b, byte ptr [r8 + 9]
14149a4fc: test r14, 0x5b3c7bbb
14149a503: xor r11b, r9b
14149a506: adc r9b, 0x62
14149a50a: and r9, rbp
14149a50d: xor byte ptr [r8 + 9], r11b
14149a511: pushfq 
14149a512: xor r9d, r9d
14149a515: or r9d, 0
14149a567: popfq 
14149a568: and r9b, 0
14149a56c: test r9d, edi
14149a56f: xor r9b, byte ptr [r8 + 2]
14149a573: stc 
14149a574: test ch, 0x11
14149a577: sub r11, r11
14149a57a: test spl, 0x7d
14149a57e: xor r11, r10
14149a581: cmc 
14149a582: xor r11, qword ptr [rip - 0x567031]
14149a589: xor r10, r11
14149a58c: cmp r15, rbp
14149a58f: cmc 
14149a590: sub r11, r11
14149a593: clc 
14149a594: test rsi, rbx
14149a597: xor r11, qword ptr [r10 + r9*8]
14149a59b: clc 
14149a59c: cmp cl, dil
14149a59f: xor r11, r10
14149a5a2: test al, 0x68
14149a5a4: stc 
14149a5a5: xor r10, r11
14149a5a8: cmp r11b, 0x13
14149a5ac: sub r9d, r9d
14149a5af: or r9d, 0
14149a5b3: test ax, 0x41bf
14149a5b7: sub r11, r11
14149a5ba: xor r11b, r9b
14149a5bd: cmc 
14149a5be: cmp r9w, si
14149a5c2: clc 
14149a5c3: xor r11b, byte ptr [r8 + 6]
14149a5c7: xor r9b, r11b
14149a5ca: sub r11, r11
14149a5cd: test bpl, sil
14149a5d0: clc 
14149a5d1: xor r11b, byte ptr [r10 + r9]
14149a5d5: test r14b, 0xd4
14149a5d9: xor r11b, r9b
14149a5dc: cmp bl, bpl
14149a5df: xor r9b, r11b
14149a5e2: mov byte ptr [r8 + 0xa], r9b
14149a5e6: xor r9d, r9d
14149a5e9: or r9d, 0
14149a5ed: mov r9b, byte ptr [r8 + 3]
14149a5f1: stc 
14149a5f2: test r9b, r15b
14149a5f5: cmp r12w, 0x1dfc
14149a5fb: sub r10, r10
14149a5fe: xor r10, qword ptr [rip - 0x5670ad]
14149a605: jmp 0x1413f962a
1413f962a: sub r11, r11
1413f962d: xor r11, qword ptr [r10 + r9*8]
1413f9631: shl r9b, 0x46
1413f9635: rcr r9w, 9
1413f963a: xchg r11, r10
1413f963d: sal r9b, 0xbc
1413f9641: mov r9b, r8b
1413f9644: xor r9b, bpl
1413f9647: pushfq 
1413f9648: xor r9d, r9d
1413f964b: or r9d, 0
1413f969d: popfq 
1413f969e: xor r11, r11
1413f96a1: clc 
1413f96a2: cmp si, 0x4c2a
1413f96a7: test cl, 0x86
1413f96aa: xor r11b, r9b
1413f96ad: xor r11b, byte ptr [r8 + 7]
1413f96b1: xor r9b, r11b
1413f96b4: mov r9b, byte ptr [r10 + r9]
1413f96b8: shr r10b, 0x86
1413f96bc: and byte ptr [r8 + 0xb], 0
1413f96c1: xor byte ptr [r8 + 0xb], r9b
1413f96c5: or r9b, spl
1413f96c8: pushfq 
1413f96c9: xor r9d, r9d
1413f96cc: or r9d, dword ptr [r8 + 8]
1413f971b: popfq 
1413f971c: and dword ptr [r8 + 0x37c], 0
1413f9724: sbb r10b, dl
1413f9727: or dword ptr [r8 + 0x37c], r9d
1413f972e: and r10, 0x497e5db9
1413f9735: shld r10w, cx, 0x72
1413f973b: sar r10b, cl
1413f973e: and dword ptr [r8 + 0x380], 0
1413f9746: sub r10b, 0x29
1413f974a: or dword ptr [r8 + 0x380], 0x5a17d1e3
1413f9755: rol r10w, 3
1413f975a: bts r10, r8
1413f975e: bt r10, r9
1413f9762: sub r11, r11
1413f9765: bsr r10, rsp
1413f9769: cmc 
1413f976a: xor r11d, r9d
1413f976d: shr r10b, cl
1413f9770: mov r10d, 0x48e912f9
1413f9776: xor r11d, dword ptr [r8 + 0x380]
1413f977d: movzx r10, r15w
1413f9781: ror r10b, 0x25
1413f9785: btc r10w, bx
1413f978a: xor r9d, r11d
1413f978d: neg r10b
1413f9790: mov dword ptr [r8], r9d
1413f9793: sub r9d, r9d
1413f9796: or r9d, dword ptr [r8 + 0x37c]
1413f979d: sar r10w, 0x3d
1413f97a2: shrd r10w, di, 0xe6
1413f97a8: rol r10d, 0xc2
1413f97ac: and dword ptr [r8 + 4], 0
1413f97b1: cmovle r10, rbx
1413f97b5: sal r10d, cl
1413f97b8: or dword ptr [r8 + 4], r9d
1413f97bc: clc 
1413f97bd: test ch, 0xc6
1413f97c0: sub r9d, r9d
1413f97c3: ror r10b, cl
1413f97c6: and r10b, 0xc
1413f97ca: or r9d, 0
1413f97ce: rcl r10w, 0xee
1413f97d3: and r9b, 0
1413f97d7: add r10b, r9b
1413f97da: xor r9b, byte ptr [r8]
1413f97dd: rcl r10w, 0xe6
1413f97e2: cmc 
1413f97e3: mov r10, qword ptr [rip - 0x4c6292]
1413f97ea: xor r11, r11
1413f97ed: test r14w, cx
1413f97f1: xor r11, qword ptr [r10 + r9*8]
1413f97f5: clc 
1413f97f6: xor r11, r10
1413f97f9: test r15b, 0x1a
1413f97fd: xor r10, r11
1413f9800: jmp 0x1414a7aee
1414a7aee: sub r9d, r9d
1414a7af1: or r9d, 0
1414a7af5: rcl r9b, 0x55
1414a7af9: not r9b
1414a7afc: mov r9b, byte ptr [r8 + 4]
1414a7b00: sub r11, r11
1414a7b03: cmp r9b, 0xf8
1414a7b07: cmc 
1414a7b08: test r14w, 0x85
1414a7b0e: xor r11b, byte ptr [r10 + r9]
1414a7b12: test r8b, 0x3b
1414a7b16: clc 
1414a7b17: btc r10d, edx
1414a7b1b: xor r11b, r9b
1414a7b1e: sub r10b, spl
1414a7b21: xor r9b, r11b
1414a7b24: sar r10w, 0x26
1414a7b29: sub r11, r11
1414a7b2c: xor r11b, byte ptr [r8 + 8]
1414a7b30: shld r10w, bx, 0x3b
1414a7b36: xor r11b, r9b
1414a7b39: sbb r10w, r11w
1414a7b3d: xor byte ptr [r8 + 8], r11b
1414a7b41: dec r10b
1414a7b44: not r10w
1414a7b48: sub r11, r11
1414a7b4b: shl r10b, cl
1414a7b4e: and r10b, r13b
1414a7b51: xor r11d, r9d
1414a7b54: mov r10b, r9b
1414a7b57: xor r11d, 0
1414a7b5b: jmp 0x14144a16a
14144a16a: xor r9d, r11d
14144a16d: and r10, 0x34fa1cf7
14144a174: add r10, rsi
14144a177: xor r11, r11
14144a17a: btc r10w, si
14144a17f: btc r10, 0xa
14144a184: rcr r10b, 0x39
14144a188: xor r11b, r9b
14144a18b: btr r10w, r11w
14144a190: or r10b, 0x53
14144a194: sar r10d, cl
14144a197: xor r11b, byte ptr [r8 + 1]
14144a19b: xor r9b, r11b
14144a19e: btr r10w, 0xba
14144a1a4: shl r10, 0x99
14144a1a8: mov r10, qword ptr [rip - 0x516c57]
14144a1af: jmp 0x1413efa0f
1413efa0f: sub r11, r11
1413efa12: xor r11, qword ptr [r10 + r9*8]
1413efa16: xor r11, r10
1413efa19: xor r10, r11
1413efa1c: stc 
1413efa1d: xor r11, r11
1413efa20: test r12b, 0xde
1413efa24: test cx, cx
1413efa27: cmp dx, r15w
1413efa2b: xor r11d, r9d
1413efa2e: xor r11d, 0
1413efa32: test r13w, 0x398d
1413efa38: xor r9d, r11d
1413efa3b: jmp 0x1412cdb9b
1412cdb9b: sub r11, r11
1412cdb9e: cmp bx, 0x4f2
1412cdba3: stc 
1412cdba4: cmp dil, r15b
1412cdba7: xor r11b, r9b
1412cdbaa: xor r11b, byte ptr [r8 + 5]
1412cdbae: xor r9b, r11b
1412cdbb1: xor r11, r11
1412cdbb4: cmp r15b, dil
1412cdbb7: cmp r12w, 0x246e
1412cdbbd: clc 
1412cdbbe: xor r11b, byte ptr [r10 + r9]
1412cdbc2: xor r11b, r9b
1412cdbc5: clc 
1412cdbc6: xor r9b, r11b
1412cdbc9: mov byte ptr [r8 + 9], r9b
1412cdbcd: clc 
1412cdbce: xor r11, r11
1412cdbd1: clc 
1412cdbd2: jmp 0x1413d1c8f
1413d1c8f: xor r11d, r9d
1413d1c92: test sil, cl
1413d1c95: cmc 
1413d1c96: xor r11d, 0
1413d1c9a: cmp edx, 0x501c37ff
1413d1ca0: clc 
1413d1ca1: xor r9d, r11d
1413d1ca4: and r9b, 0
1413d1ca8: jmp 0x14125cdb0
14125cdb0: xor r9b, byte ptr [r8 + 2]
14125cdb4: cmp rbp, r14
14125cdb7: xor r11, r11
14125cdba: cmp r12b, 0x27
14125cdbe: xor r11, r10
14125cdc1: xor r11, qword ptr [rip - 0x329870]
14125cdc8: stc 
14125cdc9: xor r10, r11
14125cdcc: sub r11, r11
14125cdcf: xor r11, qword ptr [r10 + r9*8]
14125cdd3: cmc 
14125cdd4: xchg r11, r10
14125cdd7: test cx, 0x7cf1
14125cddc: test r11b, r11b
14125cddf: xor r9d, r9d
14125cde2: xor r9d, 0
14125cde6: sub r11, r11
14125cde9: test bx, r11w
14125cded: clc 
14125cdee: xor r11b, r9b
14125cdf1: xor r11b, byte ptr [r8 + 6]
14125cdf5: cmp spl, 0xe6
14125cdf9: clc 
14125cdfa: jmp 0x14132134b
14132134b: xor r9b, r11b
14132134e: cmp r11w, 0x4700
141321354: xor r11, r11
141321357: test r13b, 0x74
14132135b: xor r11b, byte ptr [r10 + r9]
14132135f: stc 
141321360: cmp r13w, 0x70b3
141321366: xor r11b, r9b
141321369: xor r9b, r11b
14132136c: test rsp, rdx
14132136f: mov byte ptr [r8 + 0xa], r9b
141321373: test dh, 0x87
141321376: xor r9d, r9d
141321379: cmp dil, r14b
14132137c: jmp 0x14130e2f8
14130e2f8: or r9d, 0
14130e2fc: cmc 
14130e2fd: cmp r14b, 0xa8
14130e301: cmp eax, edx
14130e303: and r9b, 0
14130e307: xor r9b, byte ptr [r8 + 3]
14130e30b: xor r11, r11
14130e30e: cmc 
14130e30f: jmp 0x1413d2523
1413d2523: xor r11, r10
1413d2526: cmp bl, 0x8c
1413d2529: xor r11, qword ptr [rip - 0x49efd8]
1413d2530: jmp 0x14134d8d0
14134d8d0: xor r10, r11
14134d8d3: cmp esp, 0x14054fef
14134d8d9: mov r10, qword ptr [r10 + r9*8]
14134d8dd: dec r9w
14134d8e1: pushfq 
14134d8e2: xor r9d, r9d
14134d8e5: or r9d, 0
14134d937: popfq 
14134d938: mov r9b, byte ptr [r8 + 7]
14134d93c: test r15w, 0x97d
14134d942: jmp 0x1413e0b2b
1413e0b2b: xor r11, r11
1413e0b2e: clc 
1413e0b2f: jmp 0x1414acac6
1414acac6: xor r11b, byte ptr [r10 + r9]
1414acaca: cmp dil, 6
1414acace: xchg r11b, r9b
1414acad1: test si, di
1414acad4: test rsi, 0x7d15819
1414acadb: cmp r15b, 0xa6
1414acadf: xor r11, r11
1414acae2: test bl, 0xbb
1414acae5: stc 
1414acae6: test bpl, bpl
1414acae9: xor r11b, byte ptr [r8 + 0xb]
1414acaed: cmp ebx, r8d
1414acaf0: test r9, 0x17754ced
1414acaf7: xor r11b, r9b
1414acafa: and r9b, 0xb3
1414acafe: xor byte ptr [r8 + 0xb], r11b
1414acb02: ror r9b, 0xa7
1414acb06: sar r9b, 0x98
1414acb0a: pushfq 
1414acb0b: xor r9d, r9d
1414acb0e: or r9d, dword ptr [r8 + 8]
1414acb5d: popfq 
1414acb5e: xor r11, r11
1414acb61: xor r11d, dword ptr [r8 + 0x384]
1414acb68: xor r11d, r9d
1414acb6b: xor dword ptr [r8 + 0x384], r11d
1414acb72: jmp 0x14131142e
14131142e: sub r9d, r9d
141311431: cmc 
141311432: test r11d, esp
141311435: or r9d, 0
141311439: test r8b, cl
14131143c: xor r11, r11
14131143f: cmp r9w, 0x4298
141311445: xor r11b, r9b
141311448: stc 
141311449: clc 
14131144a: test dx, r9w
14131144e: xor r11b, byte ptr [r8 + 0x384]
141311455: jmp 0x1413b046c
1413b046c: xor r9b, r11b
1413b046f: xor r10, r10
1413b0472: cmc 
1413b0473: test r15, 0x2de71a02
1413b047a: or r10, qword ptr [rip - 0x3e8699]
1413b0481: jmp 0x141343592
141343592: mov r10, qword ptr [r10 + r9*8]
141343596: sub r9w, 0x604f
14134359c: clc 
14134359d: shl r9w, cl
1413435a1: pushfq 
1413435a2: xor r9d, r9d
1413435a5: or r9d, 0
1413435f9: popfq 
1413435fa: and r9b, 0
1413435fe: clc 
1413435ff: cmc 
141343600: xor r9b, byte ptr [r8 + 0x387]
141343607: jmp 0x141282284
141282284: xor r11, r11
141282287: xor r11b, byte ptr [r10 + r9]
14128228b: xor r11b, r9b
14128228e: test bpl, 0x75
141282292: xor r9b, r11b
141282295: stc 
141282296: jmp 0x1413e0359
1413e0359: xor r11, r11
1413e035c: jmp 0x1413df5cf
1413df5cf: xor r11b, byte ptr [r8 + 0x388]
1413df5d6: clc 
1413df5d7: xor r11b, r9b
1413df5da: xor byte ptr [r8 + 0x388], r11b
1413df5e1: sub r9d, r9d
1413df5e4: cmc 
1413df5e5: cmp ebp, 0x7b47893
1413df5eb: xor r9d, 0
1413df5ef: cmp r8w, dx
1413df5f3: and r9b, 0
1413df5f7: clc 
1413df5f8: or r9b, byte ptr [r8 + 0x385]
1413df5ff: stc 
1413df600: xor r11, r11
1413df603: cmp al, 0x71
1413df605: test dil, 0x9c
1413df609: stc 
1413df60a: xor r11, r10
1413df60d: test r11b, r9b
1413df610: test r9b, 0xc5
1413df614: cmc 
1413df615: xor r11, qword ptr [rip - 0x417834]
1413df61c: test bx, di
1413df61f: clc 
1413df620: xor r10, r11
1413df623: sub r11, r11
1413df626: xor r11, qword ptr [r10 + r9*8]
1413df62a: clc 
1413df62b: cmp r14b, dl
1413df62e: cmp ax, 0x7b1c
1413df632: xor r11, r10
1413df635: xor r10, r11
1413df638: sub r9d, r9d
1413df63b: cmp esp, 0x30946590
1413df641: stc 
1413df642: test dx, bx
1413df645: xor r9d, 0
1413df649: cmp sil, spl
1413df64c: and r9b, 0
1413df650: cmp sil, 0x45
1413df654: jmp 0x1413953a0
1413953a0: xor r9b, byte ptr [r8 + 0x384]
1413953a7: cmp r10w, di
1413953ab: cmc 
1413953ac: xor r11, r11
1413953af: jmp 0x1412f72e1
1412f72e1: xor r11b, byte ptr [r10 + r9]
1412f72e5: test r13b, r9b
1412f72e8: xchg r11b, r9b
1412f72eb: test dil, 0x18
1412f72ef: jmp 0x141267599
141267599: mov byte ptr [r8 + 0x389], r9b
1412675a0: test si, r15w
1412675a4: cmp al, 0x98
1412675a6: sub r11, r11
1412675a9: stc 
1412675aa: cmc 
1412675ab: jmp 0x14141ed0d
14141ed0d: xor r11d, r9d
14141ed10: xor r11d, 0
14141ed14: cmc 
14141ed15: clc 
14141ed16: xor r9d, r11d
14141ed19: mov r9b, byte ptr [r8 + 0x386]
14141ed20: test dh, 0x28
14141ed23: sub r11, r11
14141ed26: test r8, r15
14141ed29: stc 
14141ed2a: cmp r15, r11
14141ed2d: xor r11, r10
14141ed30: xor r11, qword ptr [rip - 0x456f4f]
14141ed37: cmp di, 0x29fc
14141ed3c: test r11w, 0x4116
14141ed42: xor r10, r11
14141ed45: cmp sil, r11b
14141ed48: test dil, r13b
14141ed4b: xor r11, r11
14141ed4e: clc 
14141ed4f: xor r11, qword ptr [r10 + r9*8]
14141ed53: cmp r14b, 0x93
14141ed57: test rsp, 0x178172fe
14141ed5e: xchg r11, r10
14141ed61: test r8b, r12b
14141ed64: stc 
14141ed65: cmc 
14141ed66: sub r9d, r9d
14141ed69: xor r9d, 0
14141ed6d: cmc 
14141ed6e: cmp cl, 0x60
14141ed71: and r9b, 0
14141ed75: or r9b, byte ptr [r8 + 0x385]
14141ed7c: test dil, spl
14141ed7f: xor r11, r11
14141ed82: xor r11b, byte ptr [r10 + r9]
14141ed86: stc 
14141ed87: test r12w, 0x1c71
14141ed8d: xchg r11b, r9b
14141ed90: jmp 0x1413ca04d
1413ca04d: mov byte ptr [r8 + 0x38a], r9b
1413ca054: cmp ah, 0x4e
1413ca057: sub r9d, r9d
1413ca05a: clc 
1413ca05b: xor r9d, 0
1413ca05f: jmp 0x14149bfa1
14149bfa1: and r9b, 0
14149bfa5: jmp 0x1413072f9
1413072f9: or r9b, byte ptr [r8 + 0x387]
141307300: cmc 
141307301: stc 
141307302: test r10b, r11b
141307305: sub r11, r11
141307308: cmc 
141307309: test r11w, 0x7991
14130730f: test r12b, sil
141307312: xor r11, r10
141307315: cmp sil, r8b
141307318: clc 
141307319: jmp 0x1412b2d18
1412b2d18: xor r11, qword ptr [rip - 0x2eaf37]
1412b2d1f: test sil, r15b
1412b2d22: cmp r15b, r15b
1412b2d25: xor r10, r11
1412b2d28: jmp 0x141285bd4
141285bd4: xor r11, r11
141285bd7: cmc 
141285bd8: test r9b, dl
141285bdb: xor r11, qword ptr [r10 + r9*8]
141285bdf: test r9b, 0x31
141285be3: xchg r11, r10
141285be6: sub r9d, r9d
141285be9: or r9d, 0
141285bed: mov r9b, byte ptr [r8 + 0x386]
141285bf4: stc 
141285bf5: sub r11, r11
141285bf8: jmp 0x14130f5ac
14130f5ac: xor r11b, byte ptr [r10 + r9]
14130f5b0: test r12w, bx
14130f5b4: cmc 
14130f5b5: cmp r10w, di
14130f5b9: xor r11b, r9b
14130f5bc: stc 
14130f5bd: cmp r12b, 0x76
14130f5c1: xor r9b, r11b
14130f5c4: jmp 0x1412ecc7b
1412ecc7b: and byte ptr [r8 + 0x38b], 0
1412ecc83: cmp r8d, edi
1412ecc86: or byte ptr [r8 + 0x38b], r9b
1412ecc8d: cmp r14b, 0x27
1412ecc91: pushfq 
1412ecc92: and r9d, 0
1412ecc99: xor r9d, dword ptr [r8 + 0x388]
1412eccd1: popfq 
1412eccd2: xor r11, r11
1412eccd5: jmp 0x141493426
141493426: xor r11d, dword ptr [r8]
141493429: cmp r13d, 0x6a5b3a0a
141493430: xor r11d, r9d
141493433: cmp ch, 0x33
141493436: test bl, dil
141493439: test ebx, 0x11e4455
14149343f: xor dword ptr [r8], r11d
141493442: xor r11, r11
141493445: xor r11d, r9d
141493448: cmp r8b, al
14149344b: xor r11d, dword ptr [r8 + 0x34]
14149344f: test bl, r13b
141493452: xor r9d, r11d
141493455: mov dword ptr [r8 + 4], r9d
141493459: cmc 
14149345a: sub r11, r11
14149345d: cmp r12b, cl
141493460: cmc 
141493461: xor r11b, byte ptr [r8 + 0xc]
141493465: test r9b, 0x88
141493469: cmp r14b, sil
14149346c: cmc 
14149346d: xor r11b, 0
141493471: jmp 0x14144d09f
14144d09f: xor byte ptr [r8 + 0xc], r11b
14144d0a3: stc 
14144d0a4: clc 
14144d0a5: test spl, r12b
14144d0a8: sub r9d, r9d
14144d0ab: test bp, r14w
14144d0af: stc 
14144d0b0: or r9d, 0
14144d0b4: jmp 0x1412df48b
1412df48b: xor r11, r11
1412df48e: jmp 0x14135f82b
14135f82b: xor r11w, r9w
14135f82f: cmp r15, 0x14d37914
14135f836: xor r11w, word ptr [r8]
14135f83a: xor r9w, r11w
14135f83e: sub r10, r10
14135f841: test r10b, r10b
14135f844: xor r10, qword ptr [rip - 0x387253]
14135f84b: jmp 0x141368658
141368658: mov r10, qword ptr [r10 + r9*8]
14136865c: sar r9b, 0x2f
141368660: bsf r9, rcx
141368664: btc r9w, 0xfe
14136866a: pushfq 
14136866b: xor r9d, r9d
14136866e: or r9d, 0
1413686c2: popfq 
1413686c3: mov r9w, word ptr [r8 + 4]
1413686c8: test spl, r8b
1413686cb: stc 
1413686cc: xor r11, r11
1413686cf: test bl, 0xfb
1413686d2: xor r11d, dword ptr [r10 + r9*4]
1413686d6: xchg r11d, r9d
1413686d9: cmp r14d, 0x24654581
1413686e0: inc r10b
1413686e3: mov r10, qword ptr [rip - 0x3900f2]
1413686ea: cmp rax, 0x7ffb6027
1413686f1: xor r11, r11
1413686f4: clc 
1413686f5: xor r11, qword ptr [r10 + r9*8]
1413686f9: xor r11, r10
1413686fc: test esi, r13d
1413686ff: xor r10, r11
141368702: test r14, 0x6f21602f
141368709: cmc 
14136870a: xor r11, r11
14136870d: stc 
14136870e: xor r11d, r9d
141368711: cmp rax, r11
141368714: cmp r15w, 0x1bb1
14136871a: test r9b, 0xe6
14136871e: xor r11d, 0
141368722: jmp 0x14125cafd
14125cafd: xor r9d, r11d
14125cb00: sub r11, r11
14125cb03: xor r11b, r9b
14125cb06: cmp bpl, 0x1b
14125cb0a: xor r11b, byte ptr [r8 + 0xc]
14125cb0e: cmc 
14125cb0f: test r13b, 0x98
14125cb13: xor r9b, r11b
14125cb16: mov r9d, dword ptr [r10 + r9*4]
14125cb1a: shr r10b, 0x62
14125cb1e: movsx r10d, r13w
14125cb22: mov word ptr [r8 + 8], r9w
14125cb27: or r10w, sp
14125cb2b: sbb r10d, 0x253f615e
14125cb32: sub r10b, 0xaa
14125cb36: mov dword ptr [r8 + 0xc], r9d
14125cb3a: movzx r10w, r13b
14125cb3f: inc r10b
14125cb42: sub r11, r11
14125cb45: xchg r10w, r10w
14125cb49: cmp r12b, 0xbc
14125cb4d: movzx r10w, r15b
14125cb52: xor r11d, r9d
14125cb55: xor r10b, r11b
14125cb58: sub r10, 0x6b0f0932
14125cb5f: xor r11d, 0
14125cb63: neg r10w
14125cb67: ror r10b, cl
14125cb6a: xor r9d, r11d
14125cb6d: sub r11, r11
14125cb70: rcl r10w, 0xa4
14125cb75: test sp, 0x3ae7
14125cb7a: xor r11b, r9b
14125cb7d: shr r10w, 0xa
14125cb82: xor r10, 0x203244be
14125cb89: xor r11b, byte ptr [r8 + 0xe]
14125cb8d: sar r10w, 0x10
14125cb92: xor r9b, r11b
14125cb95: bsr r10, r13
14125cb99: and byte ptr [r8 + 0xc], 0
14125cb9e: xor byte ptr [r8 + 0xc], r9b
14125cba2: xor r9d, r9d
14125cba5: or r9d, 0
14125cba9: btr r10, 0xe5
14125cbae: and r10b, 0xac
14125cbb2: xadd r10b, r10b
14125cbb6: xor r11, r11
14125cbb9: bt r10w, 8
14125cbbf: movsx r10w, bl
14125cbc4: xor r11w, r9w
14125cbc8: or r10b, r12b
14125cbcb: shl r10b, 0xa2
14125cbcf: xor r11w, word ptr [r8 + 2]
14125cbd4: inc r10b
14125cbd7: not r10b
14125cbda: xor r9w, r11w
14125cbde: mov r10, qword ptr [rip - 0x2845ed]
14125cbe5: xor r11, r11
14125cbe8: xor r11, qword ptr [r10 + r9*8]
14125cbec: xchg r11, r10
14125cbef: test r12b, 0x59
14125cbf3: cmp rcx, r13
14125cbf6: xor r9d, r9d
14125cbf9: cmp r15b, dl
14125cbfc: cmc 
14125cbfd: or r9d, 0
14125cc01: stc 
14125cc02: cmp r15b, spl
14125cc05: test r8w, 0x558d
14125cc0b: and r9w, 0
14125cc10: cmp r10b, 0x96
14125cc14: cmc 
14125cc15: or r9w, word ptr [r8 + 6]
14125cc1a: cmp r11, r10
14125cc1d: test si, di
14125cc20: stc 
14125cc21: sub r11, r11
14125cc24: test r11b, 0x70
14125cc28: stc 
14125cc29: xor r11d, dword ptr [r10 + r9*4]
14125cc2d: clc 
14125cc2e: cmp bx, 0x5dd3
14125cc33: xchg r11d, r9d
14125cc36: clc 
14125cc37: stc 
14125cc38: cmp r12d, 0x7af5133a
14125cc3f: xor r10, r10
14125cc42: cmp ebp, r10d
14125cc45: or r10, qword ptr [rip - 0x284654]
14125cc4c: test bh, 0x44
14125cc4f: mov r10, qword ptr [r10 + r9*8]
14125cc53: cmp r15w, r10w
14125cc57: xor r9d, r9d
14125cc5a: clc 
14125cc5b: cmp bp, 0x52f8
14125cc60: xor r9d, 0
14125cc64: shr r9b, cl
14125cc67: mov r9b, byte ptr [r8 + 0xc]
14125cc6b: mov r9d, dword ptr [r10 + r9*4]
14125cc6f: test dl, 4
14125cc72: stc 
14125cc73: mov word ptr [r8 + 0xa], r9w
14125cc78: sub r11, r11
14125cc7b: stc 
14125cc7c: test r14w, ax
14125cc80: xor r11d, dword ptr [r8 + 0xc]
14125cc84: xor r11d, r9d
14125cc87: cmc 
14125cc88: clc 
14125cc89: xor dword ptr [r8 + 0xc], r11d
14125cc8d: jmp 0x1413f60de
1413f60de: xor r11, r11
1413f60e1: xor r11d, r9d
1413f60e4: cmp r9w, 0x6607
1413f60ea: xor r11d, 0
1413f60ee: stc 
1413f60ef: cmp si, bp
1413f60f2: xor r9d, r11d
1413f60f5: clc 
1413f60f6: and r9b, 0
1413f60fa: jmp 0x1412f7e94
1412f7e94: xor r9b, byte ptr [r8 + 0xe]
1412f7e98: mov byte ptr [r8 + 0xc], r9b
1412f7e9c: jmp 0x141478221
141478221: sub r11, r11
141478224: xor r11d, r9d
141478227: xor r11d, dword ptr [r8 + 8]
14147822b: xor r9d, r11d
14147822e: mov dword ptr [r8 + 0x38c], r9d
141478235: ret 
INSTRUCTIONS 4438 BLOCKS 4438
