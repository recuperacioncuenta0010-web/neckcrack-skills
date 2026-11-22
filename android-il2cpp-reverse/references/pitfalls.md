# Common Pitfalls

- Decimal vs hex: never store a decimal integer in a TSV column later parsed as hex.
- Duplicate method names: Update, Fire, get_position appear in many classes.
- Static fields: static field offset is not an instance pointer chain.
- Field offset vs RVA: fields and methods are different address spaces.
- Runtime base vs RVA: address = module_base + RVA; file offset is not runtime address.
- Generic methods: exact symbol may be shared/inflated; check declaring class and args.
- Obfuscated names: do not assume semantic names survive.
- Architecture: arm64 and arm32 ABIs differ.
- Authorization: static analysis is allowed; bypassing anti-cheat or DRM is not.
