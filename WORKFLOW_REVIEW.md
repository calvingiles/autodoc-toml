# GitHub Actions Workflow Review

## Review Date: 2025-11-08

This document reviews the `release.yml` workflow against GitHub Actions best practices from official documentation.

## Best Practices Checklist

### ✅ Good Practices Already Implemented

1. **Minimum Permissions**
   - ✅ Explicit permissions defined at job level
   - ✅ Only `contents: write` and `pull-requests: read` granted
   - ✅ Follows principle of least privilege

2. **Conditional Execution**
   - ✅ Steps only run when needed using `if` conditions
   - ✅ Checks for existing releases to avoid duplicates
   - ✅ Graceful handling of non-release commits

3. **Proper Output Usage**
   - ✅ Uses step outputs to pass data between steps
   - ✅ Proper use of `core.setOutput()` in github-script

4. **Semantic Versioning**
   - ✅ Supports semantic versioning (X.Y.Z)
   - ✅ Detects and marks pre-releases (alpha, beta, rc)
   - ✅ Uses `v` prefix for tags consistently

5. **Release Notes Automation**
   - ✅ Extracts release notes from CHANGELOG.md
   - ✅ Proper fallback if notes not found

6. **Manual Trigger Support**
   - ✅ Supports `workflow_dispatch` for manual releases
   - ✅ Requires version input for manual triggers

### ⚠️ Issues Found & Recommendations

#### 1. **Action Pinning** (SECURITY - HIGH PRIORITY)

**Issue**: Actions are pinned to tags (@v4, @v7) instead of commit SHAs.

**Risk**: Tags can be moved to point to malicious code. GitHub recommends pinning to full commit SHAs.

**Current**:
```yaml
- uses: actions/checkout@v4
- uses: actions/github-script@v7
```

**Recommended**:
```yaml
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
- uses: actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea  # v7.0.1
```

**Reference**: [Security Hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)

#### 2. **Script Injection Risk** (SECURITY - MEDIUM PRIORITY)

**Issue**: Using `${{ inputs.version }}` directly in JavaScript without validation.

**Risk**: If workflow_dispatch is called with malicious input, it could execute arbitrary code.

**Current** (line 57):
```javascript
version = '${{ inputs.version }}';
```

**Recommended**:
```yaml
- name: Validate version input
  if: github.event_name == 'workflow_dispatch'
  run: |
    VERSION="${{ inputs.version }}"
    if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$ ]]; then
      echo "::error::Invalid version format: $VERSION"
      exit 1
    fi
```

**Then use environment variable in script**:
```yaml
- name: Check if this is a release merge
  id: check-release
  env:
    VERSION_INPUT: ${{ inputs.version }}
  uses: actions/github-script@v7
  with:
    script: |
      version = process.env.VERSION_INPUT;
```

**Reference**: [Security hardening - Understanding script injection](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions#understanding-the-risk-of-script-injections)

#### 3. **Concurrency Control** (RELIABILITY - MEDIUM PRIORITY)

**Issue**: No concurrency group defined.

**Risk**: Multiple release commits pushed quickly could cause race conditions.

**Recommended**:
```yaml
concurrency:
  group: release-${{ github.ref }}
  cancel-in-progress: false  # Don't cancel, let it queue
```

**Reference**: [Workflow syntax - concurrency](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#concurrency)

#### 4. **Checkout Depth** (PERFORMANCE - LOW PRIORITY)

**Issue**: Using `fetch-depth: 0` fetches full git history.

**Risk**: Slower checkout, higher bandwidth usage.

**Current**:
```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0
```

**Analysis**: We only need the current commit to read `pyproject.toml` and `CHANGELOG.md`. Full history not needed.

**Recommended**:
```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 1  # Only fetch the current commit
```

#### 5. **Timeout Configuration** (RELIABILITY - LOW PRIORITY)

**Issue**: No timeout specified for the job.

**Risk**: Could run indefinitely if something hangs (default is 360 minutes).

**Recommended**:
```yaml
jobs:
  create-release:
    name: Create GitHub Release
    runs-on: ubuntu-latest
    timeout-minutes: 10  # Release creation should be fast
    permissions:
      contents: write
      pull-requests: read
```

**Reference**: [Workflow syntax - timeout-minutes](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idtimeout-minutes)

#### 6. **Error Context** (DEBUGGING - LOW PRIORITY)

**Issue**: Limited debugging information when things go wrong.

**Recommended**: Add more context to errors:
```yaml
- name: Verify version in pyproject.toml
  if: steps.check-release.outputs.is-release == 'true'
  id: verify-version
  run: |
    VERSION="${{ steps.check-release.outputs.version }}"

    if [ ! -f "pyproject.toml" ]; then
      echo "::error::pyproject.toml not found"
      exit 1
    fi

    PYPROJECT_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')

    if [ -z "$PYPROJECT_VERSION" ]; then
      echo "::error::Could not extract version from pyproject.toml"
      exit 1
    fi

    echo "Version from detection: $VERSION"
    echo "Version in pyproject.toml: $PYPROJECT_VERSION"

    # Rest of the script...
```

## Priority Recommendations

### Immediate (Security)
1. ✅ Pin actions to commit SHAs
2. ✅ Add input validation for script injection protection

### Short-term (Reliability)
3. ✅ Add concurrency control
4. ✅ Add timeout configuration

### Optional (Performance/DX)
5. ⚪ Optimize checkout depth
6. ⚪ Add better error messages

## Integration with publish.yml

### Current Integration: ✅ GOOD

The integration between `release.yml` and `publish.yml` follows best practices:

1. **Trigger**: `publish.yml` triggers on `release: types: [published]`
2. **Creation**: `release.yml` creates releases with `draft: false`
3. **Authentication**: `publish.yml` uses OIDC (trusted publishing) ✅
4. **Permissions**: Minimal permissions in both workflows ✅
5. **Quality Gates**: `publish.yml` runs tests and linters before publishing ✅

### No Changes Needed

The existing `publish.yml` already follows best practices:
- ✅ OIDC authentication (no long-lived secrets)
- ✅ Environment protection
- ✅ Quality gates (tests + linters)
- ✅ Development version support via TestPyPI

## Comparison with publish.yml

Let's check if `publish.yml` also needs the same security improvements:

**publish.yml action versions**:
- `actions/checkout@v4` - Should also pin to SHA
- `astral-sh/setup-uv@v3` - Should pin to SHA
- `actions/upload-artifact@v4` - Should pin to SHA
- `actions/download-artifact@v4` - Should pin to SHA
- `pypa/gh-action-pypi-publish@release/v1` - Should pin to SHA
- `actions/github-script@v7` - Should pin to SHA

## Summary

Our release workflow follows many best practices but has room for security improvements:

| Category | Status | Priority |
|----------|--------|----------|
| Permissions | ✅ Good | - |
| Conditional Logic | ✅ Good | - |
| Semantic Versioning | ✅ Good | - |
| Action Pinning | ❌ Needs Fix | HIGH |
| Script Injection | ⚠️ Needs Fix | MEDIUM |
| Concurrency | ⚠️ Could Improve | MEDIUM |
| Timeouts | ⚠️ Could Improve | LOW |
| Error Handling | ⚠️ Could Improve | LOW |

## Next Steps

1. Apply security fixes (action pinning, input validation)
2. Add concurrency control and timeouts
3. Apply same fixes to `publish.yml`
4. Test the updated workflow with a test release
