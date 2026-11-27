# Engineering review record

| Reference | Role |
|---|---|
| `main` | Public default branch. Its tip can change. |
| `review/engineering` | Build, installation, module provenance, and QA documentation for maintainer review. |
| `testing/pre-sdr-release` | Local experimental candidate. Its additional research changes require separate maintainer review. |

The tested commit is `34921037a911051fcdb9c854644e5213cd385504`, tree `3c1ab797554d7d5ed0c30eca5481edf7139b014e`, based on `9df82064515d66ca83f6cc66442ddfdeaf30af83`. The subsequent project-identity and review-record changes affect documentation only.

On Arch Linux, a fresh clone built and installed in paths containing spaces. All 13 registered CTest entries passed, covering 26 Python cases. The moved installation prefix loaded successfully. Preloading the older native library caused the expected provenance error (91). Nine constructor tests exercise construction only.

The retained CTest log has SHA-256 `e08ff7dc86f7572ec35d817cec4585793b8b83a9b0a0a394f58375833fe59bbb`. The maintainer’s engineering patch from the base to the tested commit has SHA-256 `94978c8c6e0b99ac36639c0a5b524ca0b706eb0eb29388b8aef07481729ec2a8`. The [build guide](BUILD_QA.md) describes how to repeat the checks. Local logs are retained separately.

These checks cover the recorded Arch Linux software environment. Other platforms, hardware behavior and reconstruction from emissions remain unqualified by this review. The larger experimental candidate and its artifacts have a separate review history.
