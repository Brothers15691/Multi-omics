# Shared-by-all vs shared-by-some vs unique structure (DIVAS idea)

Many methods assume one shared signal across all omics. Real biology is often **partially shared**:

- **Shared by all** blocks
- **Shared by some** blocks
- **Unique** to one block

DIVAS is one framework built around this separation.

## Practical takeaway
When you see a “shared factor”, ask:
- Is it shared by all blocks, or only a subset?
- Could it be shared technical variation (batch) instead of biology?
- Does it replicate under resampling / held-out data?

## Related methods
- **JIVE**: joint + individual + residual decomposition.
- **MOFA**: factors that can be shared or view-specific.
