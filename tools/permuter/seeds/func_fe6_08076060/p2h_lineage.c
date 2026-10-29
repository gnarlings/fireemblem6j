// plain-C climber descended from fe7u_port.c (score 2290)
void func_fe6_08076060(struct UnitListScreenProc *proc)
{
  int new_var;
  int r4;
  unsigned short new_var6;
  int r5;
  int new_var4;
  struct UnitListScreenProc *new_var7;
  u16 (*new_var5)[0x20];
  int new_var3;
  int r3;
  u8 *new_var8;
  u8 *new_var2;
  proc->unk_38 += gUnk_08678722[proc->unk_3E];
  new_var4 = 0x20;
  if (proc->unk_38 > 20)
  {
    proc->unk_38 = 20;
  }
  proc->unk_3E++;
  new_var7 = proc;
  if (proc->page_target > proc->unk_37)
  {
    for (r5 = 0; r5 < new_var7->unk_38; r5++)
    {
      for (r4 = proc->unk_40 / 8; r4 < ((proc->unk_40 / 8) + 12); r4++)
      {
        new_var3 = r5 + 8;
        r3 = r4 & 0x1F;
        gBg0Tm[(r3 * 0x20) + (inline_fn(r5) - proc->unk_38)] = gUnk_0200CD3A[r3][new_var3];
      }

      for (r4 = 0; r4 < 2; r4++)
      {
        gBg2Tm[((r4 + 5) * 0x20) + (inline_fn(r5) - proc->unk_38)] = gUnk_0200D53A[r4][r5 + 8];
        proc->unk_37 = proc->unk_37;
      }

    }

  }
  else
  {
    proc = proc;
    new_var2 = &proc->unk_38;
    for (r5 = 0; r5 < (*new_var2); r5++)
    {
      new_var6 = 12;
      new_var8 = new_var2;
      ;
      for (r4 = proc->unk_40 / 8; r4 < ((proc->unk_40 / 8) + new_var6); r4++)
      {
        new_var6 = r4 & 0x1F;
        r3 = new_var6;
        new_var3 = 8 & 0xFFFFFFFFFFFFFFFFu;
        gBg0Tm[((r3 * 0x20) + new_var3) + r5] = gUnk_0200CD3A[r3][inline_fn(r5) - (*new_var8)];
      }

      r3 = r5 + 0x1C;
      for (r4 = 0; r4 < 2; r4++)
      {
        new_var = r3;
        gBg2Tm[(((r4 + 5) * 0x20) + r5) + 8] = gUnk_0200D53A[r4][new_var - (*new_var8)];
      }

    }

  }
  EnableBgSync(BG0_SYNC_BIT | BG2_SYNC_BIT);
  if ((*new_var8) >= 20)
  {
    Proc_Break(proc);
  }
}
