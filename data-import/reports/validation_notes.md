# MDDS Dataset Validation Notes

## Validation Summary

A total of 30 MDDS 2011 state/UT datasets were validated.

* Total datasets: 30
* PASS: 29
* REVIEW: 1
* FAIL: 0

The validation checked dataset structure, missing values, duplicate rows, MDDS state codes, district codes, sub-district codes, village codes, and hierarchy consistency.

## Assam Dataset Review

Dataset:

`Rdir_2011_18_ASSAM.xls`

Validation result:

`REVIEW`

Details:

* Total rows: 26,762
* Missing values: 2
* Duplicate rows: 0
* Affected record: MDDS PLCN `302048`
* Area Name: `Kharija Dalaigaon Pt.2 (Part)`
* District: `Chirang`
* Missing fields:

  * `MDDS Sub_DT`
  * `SUB-DISTRICT NAME`

The missing values occur in the source dataset itself. The source record has been identified and flagged for review rather than assigning an unverified sub-district value.

## Conclusion

The dataset validation process completed successfully for all 30 input files.

29 datasets passed validation with no detected missing values or duplicate rows.

1 dataset (Assam) was flagged for review because of a single source record containing two missing hierarchical fields.

No datasets failed validation.

The Assam record should be verified against the authoritative MDDS source before assigning or modifying its sub-district information.
