// p2g's plain-C best after the handoff (score 635)
void func_fe6_08076060(struct UnitListScreenProc *proc)
{
  int new_var;
  int r4;
  int new_var3;
  int new_var4;
  int r3;
  short new_var2;
  proc->unk_38 += gUnk_08678722[proc->unk_3E];
  new_var = 0x1C;
  new_var3 = 0x1F;
  if (proc->unk_38 > 20)
  {
    proc->unk_38 = 20;
  }
  proc->unk_3E++;
  if (proc->page_target > proc->unk_37)
  {
    for (new_var3 = 0; new_var3 < proc->unk_38; new_var3++)
    {
      for (r4 = proc->unk_40 / 8; r4 < ((proc->unk_40 / 8) + 12); r4++)
      {
        r3 = r4 & 0x1F;
        gBg0Tm[(r3 * 0x20) + ((new_var3 + new_var) - proc->unk_38)] = gUnk_0200CD3A[r3][new_var3 + 8];
      }

      for (r4 = 0; r4 < 2; r4++)
      {
        gBg2Tm[((r4 + 5) * 0x20) + ((new_var3 + new_var) - proc->unk_38)] = gUnk_0200D53A[r4][new_var3 + 8];
      }

    }

  }
  else
  {
    for (new_var3 = 0; new_var3 < proc->unk_38; new_var3++)
    {
      new_var4 = new_var3;
      new_var4 = proc->unk_40 / 8;
      for (r4 = new_var4; r4 < ((proc->unk_40 / 8) + 12); r4++)
      {
        r3 = new_var3;
        r3 = r4 & r3;
        new_var2 = ((r3 * 0x20) + 8) + new_var4;
        gBg0Tm[new_var2] = gUnk_0200CD3A[r3][(new_var3 + new_var) - proc->unk_38];
      }

      for (r4 = 0; r4 < 2; r4++)
      {
        gBg2Tm[(((r4 + 5) * 0x20) + new_var3) + 8] = gUnk_0200D53A[r4][(new_var3 + new_var) - proc->unk_38];
      }

    }

  }
  EnableBgSync(BG0_SYNC_BIT | BG2_SYNC_BIT);
  if (proc->unk_38 >= 20)
  {
    Proc_Break(proc);
  }
}
