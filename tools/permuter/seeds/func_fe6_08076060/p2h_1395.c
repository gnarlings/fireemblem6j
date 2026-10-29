// plain-C climber descended from fe7u_port.c, using a permuter inline_fn helper (score 1395)
inline int inline_fn(int arg0)
{
  return arg0 + 0x1C;
}

void func_fe6_08076060(struct UnitListScreenProc *proc)
{
  int new_var;
  unsigned int new_var11;
  int r4;
  unsigned short new_var6;
  int r5;
  int new_var4;
  u8 new_var13;
  struct UnitListScreenProc *new_var7;
  u8 new_var9;
  u16 (*new_var5)[0x20];
  int new_var3;
  int r3;
  u8 *new_var8;
  struct UnitListScreenProc *new_var12;
  int new_var10;
  u8 *new_var2;
  proc->unk_38 += gUnk_08678722[proc->unk_3E];
  new_var4 = 0x20;
  if (proc->unk_38 > 20)
  {
    proc->unk_38 = 20;
  }
  proc->unk_3E++;
  new_var12 = proc;
  new_var13 = new_var12->page_target;
  new_var7 = new_var12;
  new_var9 = new_var12->unk_37;
  if (new_var13 > new_var9)
  {
    for (r5 = 0; r5 < new_var7->unk_38; r5++)
    {
      for (r4 = new_var12->unk_40 / 8; r4 < ((new_var12->unk_40 / 8) + 12); r4++)
      {
        new_var3 = r5 + 8;
        r3 = r4 & 0x1F;
        gBg0Tm[(r3 * 0x20) + (inline_fn(r5) - new_var12->unk_38)] = gUnk_0200CD3A[r3][new_var3];
      }

      new_var10 = r5 + 8;
      for (r4 = 0; r4 < 2; r4++)
      {
        gBg2Tm[((r4 + 5) * 0x20) + (inline_fn(r5) - new_var12->unk_38)] = gUnk_0200D53A[r4][new_var10];
        new_var12->unk_37 = new_var12->unk_37;
      }

    }

  }
  else
  {
    r5 = 0;
    proc = proc;
    new_var2 = &proc->unk_38;
    for (r5 = 0; r5 < (*new_var2); r5++)
    {
      ;
      new_var8 = new_var2;
      ;
      for (r4 = proc->unk_40 / 8; r4 < ((proc->unk_40 / 8) + 12); r4++)
      {
        new_var6 = r4 & 0x1F;
        new_var11 = 0xFFFFFFFFu;
        r3 = new_var6;
        new_var3 = 8 & new_var11;
        gBg0Tm[((r3 * 0x20) + new_var3) + r5] = gUnk_0200CD3A[r3][(new_var = inline_fn(r5)) - (*new_var2)];
      }

      r3 = r5 + 0x1C;
      for (r4 = 0; r4 < 2; r4++)
      {
        new_var = r3;
        gBg2Tm[(((r4 + 5) * 0x20) + r5) + 8] = gUnk_0200D53A[r4][new_var - (*new_var2)];
      }

    }

  }
  EnableBgSync((r3 = BG0_SYNC_BIT) | BG2_SYNC_BIT);
  if ((*new_var8) >= 20)
  {
    Proc_Break(proc);
  }
}
