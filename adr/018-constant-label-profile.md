# The Constant Label Profile · `rec:constants:value-accountability-profile`

**Status:** Decided

This record makes selected production constants answerable to authored warrants and deterministic value pins. The declared policy selects the participating owners and programs; the algorithms below define the stable program identities cited by source documentation.

## Constant identity · `sec:constants:identity`

**Signature (Constant kind extension)** · `sig:constants:kind-extension`

The reserved local kind `const` names a selected production constant under its owning package. A source declaration mints the constant identity, cites an authored semantic warrant, and carries the current derived pin.

**Definition (Digest word)** · `def:const:digest-word`

A digest word is the lowercase hexadecimal suffix obtained from the declared constant-pin recipe over a program's canonical byte form. It detects value drift under that recipe and carries no authenticity claim.

## Programs · `sec:constants:programs`

**Algorithm (Codepoint program)** · `alg:const:codepoint`

The codepoint program accepts one Unicode scalar and canonicalizes it as its scalar value before deriving the pin suffix.

**Algorithm (Count program)** · `alg:const:count`

The count program accepts one nonnegative integral quantity and canonicalizes its ordinary decimal representation without padding or sign.

**Algorithm (Form program)** · `alg:const:form`

The form program accepts a finite ordered structured value and canonicalizes every element, delimiter, and ordering choice fixed by the constant's declaration. It is used where rearrangement would change semantics.

**Algorithm (Text program)** · `alg:const:text`

The text program accepts an exact UTF-8 string and derives its pin from those bytes. Case, whitespace, and punctuation remain significant.

**Algorithm (Word program)** · `alg:const:word`

The word program accepts one nonempty lowercase alphanumeric policy word and rejects values outside that lexical class before pinning.

**Convention (Program invocation)** · `conv:constants:invocation`

A constant invokes exactly one catalogued program by citing its algorithm label beside the constant mint. The declared pin identity carries the same program name, so a reader can distinguish value drift from a program change.

## Accountability · `sec:constants:accountability`

**Requirement (Mechanization)** · `req:constants:mechanization`

The checker derives pins from parsed source values, never from copied documentation text. It reports a missing warrant, malformed identity, unsupported program, stale pin, or refused value separately.

**Gate (Constant conformance)** · `gate:constants:conformance`

A selected constant conforms only when its mint, semantic warrant, program citation, value parsing, derived pin, and committed pin agree under one owner and one source revision.
