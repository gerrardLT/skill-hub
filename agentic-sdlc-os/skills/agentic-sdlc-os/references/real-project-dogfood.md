# Real-project dogfooding

Use this protocol before claiming the system works on real software.

1. Select a user-owned project and a bounded vertical slice with observable failure conditions.
2. Preserve the original requirement sources and hashes.
3. Produce executable code, automated tests, a deployment smoke, runtime metrics and rollback evidence.
4. Register accepted artifacts, qualifying evidence and directed trace paths for every applicable Gate.
5. Traverse all six OSs without force or waiver unless a human formally approves an exception.
6. Record Evolution learning and re-enter the OS that owns the largest remaining evidence gap.
7. Separate three claims:
   - control plane works;
   - real-project slice works in the observed environment;
   - workflow causally improves outcomes versus a baseline.
8. Treat only the first two as L5-A. Require a preregistered matched comparison for the third.

The repository reference pilot is `validation/l5/pilots/venue-reservation`; its evidence boundary is documented in `validation/l5/REAL_PROJECT_DOGFOOD_REPORT.md`.
