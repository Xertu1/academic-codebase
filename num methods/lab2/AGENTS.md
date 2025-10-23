## System Prompt

**System prompt:**

> In the future, do not change anything in the program except what will be further specified in the prompt; if the user does not explicitly mention in the prompt the part of the code that needs to be changed for the program to work correctly, it can be changed, but the edits should be minimal.

---

## Purpose

This project focuses on developing and maintaining Fortran programs for solving systems of linear equations and related numerical methods.
The goal is to keep the code minimal, clear, and functionally correct, with only short comments explaining the logic.

---

## Language and Environment

* **Language:** Fortran (standard: F2008+)
* **Precision:** double precision (`real64`)
* **Style:** structured, modular (prefer separate subroutines for I/O and numerical methods)
* **Compiler example:**

  ```bash
  gfortran -O2 -Wall main.f90 -o solve
  ./solve --A path/to/matrix.txt --b path/to/vector.txt --method gauss --out solution.txt
  ```

---

## Code Style Rules

* Write only essential code, avoid unnecessary optimizations or abstractions.
* Use clear and descriptive variable names.
* Comments must be **short and factual**, explaining only the purpose of key blocks.
* Each subroutine should handle **one specific task** (I/O, method, etc.).
* Always use `implicit none`.

---

## File Format Conventions

The Fortran programs must operate with plain text data files (space-separated values).

| File                    | Description                                                | Format                     |
| ----------------------- | ---------------------------------------------------------- | -------------------------- |
| `matrix.txt`            | Input matrix **A**                                         | m rows × n numbers per row |
| `vector.txt`            | Right-hand side vector **b**                               | n numbers (row or column)  |
| `solution.txt`          | Computed solution vector **x**                             | n numbers                  |
| `conds.txt`             | Optional file with condition number(s) or diagnostics      | single line or short block |
| `jordan c#.txt`         | Optional file for Jordan/Gauss–Jordan intermediate results | free format                |
| `vector right half.txt` | Alternate name for `vector.txt`                            | same format                |

---

## Program Structure

Recommended structure for Fortran sources:

```
/fortran/
  ├── main.f90          # entry point, argument parsing
  ├── io.f90            # reading/writing matrices and vectors
  ├── lin_sys.f90       # core solving routines (Gauss, Gauss-Jordan, LU)
  ├── utils.f90         # residual and error checking
  └── data/             # input/output text files
```

---

## Functional Requirements

* Support solving linear systems using:

  * Gaussian elimination with partial pivoting
  * Gauss–Jordan elimination
  * LU decomposition (Doolittle method)
* Check matrix size consistency (`A` vs `b`).
* Detect singular or nearly singular matrices.
* Output:

  * solution vector
  * optionally, residual norm or condition number
* Return nonzero exit code if failure occurs.

---

## Quality and Testing

* Always verify results using known matrices.
* Compute and print the residual norm `‖A*x - b‖₂`.
* For ill-conditioned matrices, print a short warning instead of modifying the algorithm.
* Ensure output files are formatted clearly (space-separated numbers, no extra headers).

---

## Developer Checklist

* [ ] Program compiles and runs via the provided CLI format.
* [ ] Input and output file formats strictly follow the table above.
* [ ] Code is short, modular, and readable.
* [ ] Comments are minimal and relevant.
* [ ] No unnecessary edits beyond the current prompt instructions.

## Working Directory
All work must be done only in:
/fortran/