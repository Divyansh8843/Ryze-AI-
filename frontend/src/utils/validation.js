// Lightweight safety & validation helpers for generated UI code
// NOTE: This is intentionally simple string-based validation to keep
// the preview sandbox fast and dependency-free.

// Very small set of obviously dangerous patterns we never want to allow.
// Relaxed to avoid blocking common, harmless patterns while still catching
// clearly unsafe constructs like eval/Function/infinite loops.
const FORBIDDEN_PATTERNS = [
  /eval\s*\(/i,
  /Function\s*\(/i,
  /while\s*\(true\)/i,
];

/**
 * Validates generated code before we attempt to execute it in the preview.
 * Returns `{ ok: true }` when safe-enough, otherwise `{ ok: false, reason }`.
 */
export function validateGeneratedCode(code) {
  if (!code || typeof code !== 'string') {
    return { ok: false, reason: 'Empty or invalid code received from generator.' };
  }

  // Basic length guardrail
  if (code.length > 60_000) {
    return {
      ok: false,
      reason: 'Generated code is too large to safely render. Please try a more focused prompt.',
    };
  }

  for (const pattern of FORBIDDEN_PATTERNS) {
    if (pattern.test(code)) {
      return {
        ok: false,
        reason:
          'The generated code included a clearly unsafe JavaScript pattern (such as eval, Function, or an infinite loop). ' +
          'Please remove those constructs and try again.',
      };
    }
  }

  return { ok: true };
}

