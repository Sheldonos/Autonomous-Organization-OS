---
name: ncfb-sqlcode-805
description: >
  Use when an NCFB developer, DBA, or mainframe operator receives SQLCODE -805 on z/OS Db2.
  Walks through the full root-cause diagnosis and resolution: DBRM not found in plan, package
  not bound, timestamp mismatch, wrong plan name, environment mismatch (DEV vs QA vs PROD),
  and the BIND/REBIND steps required to fix it. Triggers on phrases like "SQLCODE -805",
  "DBRM not found", "program not bound", "rebind required", "-805 error", or
  "package not found in plan".
---

# NCFB SQLCODE -805 Troubleshooting

SQLCODE -805 means: **"The DBRM or package named in the SQL was not found in the plan or package collection."**

The program compiled and linked successfully, but the SQL inside it was never — or not recently —
bound into the Db2 plan that the job is running under. Nothing executes until this is resolved.

Follow every step in order. Do not skip to the fix before completing the diagnosis.

---

## Step 1 — Capture the Full Error Message

Ask the user to retrieve the complete SQLSTATE and Db2 message text from the job output.

In SDSF:
```
1. Type SDSF → press Enter
2. Type ST on the command line → find the failed job
3. Type S next to the job → scroll to the failed step
4. Look for the full DSNT408I or DSNT418I message near the -805 return code
5. Copy the DBRM name, collection ID, and plan name from the message
```

The message will contain:
- **DBRM name** — the name of the program's compiled SQL module
- **Plan name** — the Db2 plan that was referenced at runtime
- **Collection ID** — (if using packages) the package collection the program expected

Record all three before continuing.

---

## Step 2 — Identify the Root Cause

There are four distinct causes. Check them in this order:

### Cause A — Program Was Never Bound

The program was compiled and linked, but BIND was never run.

**Check:** Ask the developer — was BIND executed after the most recent compile?
- If no BIND was ever run → **go to Step 3 (BIND the DBRM)**.

### Cause B — Program Was Recompiled But Not Rebound

The source code was changed, recompiled, and linked — but the old DBRM (or a new one) was never
rebound into the plan. This is the most common cause at NCFB batch shops.

**Check:** Compare the DBRM timestamp to the load module timestamp:
- If they differ → SQLCODE **-818** will often appear alongside -805, or -805 alone indicates
  the new DBRM is not in the plan at all.
- **Go to Step 3 (REBIND).**

### Cause C — Wrong Plan Name in the JCL or Application

The job is connecting to a Db2 plan that does not contain this program's DBRM.

**Check:** Look at the JCL for the failed job step:
```jcl
//DSNHDECP DD DSN=...
//SYSPRINT  DD SYSOUT=*
```
Or look at the `PARM=` on the EXEC statement — does the plan name match the plan that was bound?

```
[CONFIRM WITH DBA — what is the correct NCFB plan name for CLAIMS batch? POLICY batch?]
```
- If the plan name is wrong → correct the JCL and resubmit. No BIND needed.

### Cause D — Wrong Environment (DEV/QA/PROD Mismatch)

The program was bound in DEV but is running in QA or PROD where the bind has not been promoted.

**Check:** Ask — which Db2 subsystem is the job connecting to?
```
[CONFIRM WITH DBA — NCFB Db2 subsystem IDs for DEV, QA, and PROD]
```
- If the BIND exists in DEV but not in PROD → the BIND package promotion was skipped.
- The DBA must run the BIND in the target environment, or the change management process must
  promote it.
- **Do not rebind directly in PROD without change management approval.**

---

## Step 3 — Execute the Fix

### Fix for Causes A and B: BIND or REBIND the DBRM

The DBA or authorized developer must run a BIND job. Provide this template:

```jcl
//BIND805  JOB (ACCT),'BIND FIX -805',CLASS=A,MSGCLASS=X
//*
//BINDSTEP EXEC PGM=IKJEFT01
//SYSTSPRT DD SYSOUT=*
//SYSPRINT DD SYSOUT=*
//SYSTSIN  DD *
  DSN SYSTEM(ssid)
  BIND PACKAGE(collection-id) -
       MEMBER(dbrm-name)       -
       LIBRARY('NCFB.DEV.DBRM') -
       ACTION(REPLACE)          -
       VALIDATE(BIND)           -
       ISOLATION(CS)
  END
/*
```

Replace:
- `ssid` → Db2 subsystem ID `[CONFIRM WITH DBA]`
- `collection-id` → Collection ID from the -805 error message
- `dbrm-name` → DBRM name from the -805 error message
- `NCFB.DEV.DBRM` → actual DBRM library `[CONFIRM WITH DBA — NCFB DBRM PDS naming]`

> ⚠️ For PROD: BIND must go through change management. Do not run directly.
> `[CONFIRM WITH DBA — NCFB change management process for PROD BIND]`

### Fix for Cause C: Correct the JCL Plan Name

Update the plan name reference in the JCL or PARM= to match the plan that contains the program's
DBRM. Resubmit the job. No BIND is needed.

### Fix for Cause D: Promote the BIND to the Target Environment

Raise a change management request to promote the BIND package from DEV/QA into PROD.
The DBA executes the BIND in PROD after approval.
`[CONFIRM — NCFB BIND promotion process and who approves]`

---

## Step 4 — Verify the Fix

After BIND/REBIND completes, verify before resubmitting the production job:

```sql
-- Confirm the package now exists in the Db2 catalog
SELECT COLLID, NAME, VERSION, VALID, OPERATIVE, TIMESTAMP
FROM   SYSIBM.SYSPACKAGE
WHERE  NAME   = 'dbrm-name'
  AND  COLLID = 'collection-id';
```

Expected result:
- `VALID = 'Y'` — package is valid
- `OPERATIVE = 'Y'` — package is operative (usable)
- `TIMESTAMP` matches the load module timestamp (resolves any -818 risk)

If `VALID = 'N'` → the BIND succeeded but found dependency errors. Call the DBA — the package
needs investigation before the job runs.

---

## Step 5 — Escalation Triggers

Stop and involve the DBA immediately if any of these are true:

| Trigger | Why |
|---|---|
| Error is in a PROD job during a live batch window | Business impact — DBA must authorize any PROD BIND |
| BIND completes but `VALID = 'N'` in SYSPACKAGE | Unresolved dependency — DBA investigation required |
| Multiple programs are failing with -805 simultaneously | May indicate a plan-level DROP or mass environment issue |
| You cannot identify the DBRM name from the error message | Incomplete diagnostic — do not guess; get the DBA |
| Change management process applies | Any PROD BIND requires a ticket `[CONFIRM NCFB CM tool]` |

---

## Quick Reference

| Term | Meaning |
|---|---|
| **DBRM** | Database Request Module — the compiled SQL extracted from the source program at compile time |
| **BIND** | The process that takes the DBRM and registers it into a Db2 plan or package so it can execute |
| **REBIND** | Re-running BIND for an already-bound DBRM — required after recompile |
| **Plan** | A Db2 object that groups one or more DBRMs/packages for execution |
| **Package** | A finer-grained alternative to plans — one DBRM per package, grouped into a collection |
| **Collection ID** | The namespace that groups related packages — analogous to a library |
| **-818** | Timestamp mismatch — load module and DBRM were compiled at different times — always rebind |
| **SYSPACKAGE** | Db2 catalog table — lists all bound packages and their validity status |
| **NCFB.DEV.DBRM** | Placeholder — confirm actual DBRM PDS with DBA |
