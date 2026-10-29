// FE7U's matched sub_0808A92C, ported with plain C in place of its ({ }) expressions
void func_fe6_08076060(struct UnitListScreenProc * proc)
{
    int r4, r5, r3;

    proc->unk_38 += gUnk_08678722[proc->unk_3E];

    if (proc->unk_38 > 20)
        proc->unk_38 = 20;

    proc->unk_3E++;

    if (proc->page_target > proc->unk_37)
    {
        for (r5 = 0; r5 < proc->unk_38; r5++)
        {
            for (r4 = proc->unk_40 / 8; r4 < proc->unk_40 / 8 + 12; r4++)
            {
                r3 = r4 & 0x1F;
                gBg0Tm[r3 * 0x20 + ((r5 + 0x1C) - proc->unk_38)] = gUnk_0200CD3A[r3][r5 + 8];
            }

            for (r4 = 0; r4 < 2; r4++)
            {
                gBg2Tm[(r4 + 5) * 0x20 + ((r5 + 0x1C) - proc->unk_38)] = gUnk_0200D53A[r4][r5 + 8];
            }
        }
    }
    else
    {
        for (r5 = 0; r5 < proc->unk_38; r5++)
        {
            for (r4 = proc->unk_40 / 8; r4 < proc->unk_40 / 8 + 12; r4++)
            {
                r3 = r4 & 0x1F;
                gBg0Tm[(r3 * 0x20 + 8) + r5] = gUnk_0200CD3A[r3][(r5 + 0x1C) - proc->unk_38];
            }

            for (r4 = 0; r4 < 2; r4++)
            {
                gBg2Tm[(r4 + 5) * 0x20 + r5 + 8] = gUnk_0200D53A[r4][(r5 + 0x1C) - proc->unk_38];
            }
        }
    }

    EnableBgSync(BG0_SYNC_BIT | BG2_SYNC_BIT);

    if (proc->unk_38 >= 20)
        Proc_Break(proc);
}
