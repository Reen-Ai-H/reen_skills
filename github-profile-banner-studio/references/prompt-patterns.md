# Prompt patterns

These are reusable structures, not mandatory wording. Replace bracketed fields with the user's actual inputs.

## True split diptych

```text
Use case: compositing
Asset type: wide GitHub profile banner
Input images: Image 1 is the left-source visual; Image 2 is the right-source visual; Image 3 is the identity reference if needed.
Primary request: Create one continuous two-source composition. Use the left half of Image 1 and the right half of Image 2. Choose a seam that aligns [face / torso / letterform / object] so it appears once and continues naturally across the join.
Subject: [person or main subject], preserved as one continuous identity
Composition/framing: wide 3:1 banner, safe margins, no duplicated subject or landmarks
Style/medium: [editorial / painterly / photographic / other]
Lighting/mood: [left treatment] gradually shifting to [right treatment]
Color palette: [4–6 colors]
Text (verbatim): “[display name]” / “[monogram]” / “[signature]”
Constraints: preserve identity, keep one copy of each object and text item, exact spelling
Avoid: two full images side by side, duplicate faces, repeated landmarks, extra letters, fake UI, watermark
```

## Identity and lighting refinement

```text
Use case: identity-preserve
Asset type: existing wide banner, targeted portrait refinement
Input images: Image 1 is the banner edit target; Image 2 is the original portrait identity reference.
Primary request: Edit only the face and lighting integration. Preserve the exact composition, seam, crop, background, clothing, jewelry, and typography.
Face and lighting: natural facial proportions, subtle pores and skin variation, believable eyes and glasses reflections, soft directional light, realistic shadows, no plastic smoothing.
Constraints: keep age, expression, identity, pose, text spelling, and dimensions unchanged
Avoid: beauty filter, porcelain skin, uncanny eyes, duplicated facial features, altered wordmark
```

## Exact-text finishing layer

Use this when a generated image has good art direction but unreliable lettering:

```text
Remove or suppress all generated typography while preserving the image.
Then place the exact text in a controlled layer:
Display name: “[exact string]”
Monogram: “[exact string]”
Signature: “[exact string]”
Verify the character sequence letter by letter, including capitalization, spaces, and the number of appearances.
```

For a name crossing the seam, treat the word as one object and let the seam pass through it once. Never ask the image model to invent multiple partial copies of the same word.

## Separate split tiles

```text
Create two equal-size outputs from one continuous wide canvas.
Left tile: [exact first fragment], left half of the subject and left-source background.
Right tile: [exact second fragment], [monogram], and [signature], right half of the subject and right-source background.
Keep both crops aligned to the same canvas, with no padding or duplicated subject. The two tiles must reconstruct the full composition when placed edge-to-edge.
```
