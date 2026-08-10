# Semantic components

This directory is the publication boundary for semantic meaning owned by Alludium Packs. A bundle
contains separately versioned ontology, mapping, constraints, projection, and profile components.
Every component has a canonical digest and exact dependencies; the bundle and catalog are also
content-addressed.

Consumers must select an exact `bundle_id`, `bundle_version`, and `bundle_sha256` from
`catalog.json`. The declared release tag is publication intent until the branch merges and the tag
is created on `main`. Runtime GitHub scraping, unpinned versions, and `latest` aliases are invalid.

Retiring a component blocks new locks but does not alter or remove the historical bundle. New
meaning is published under a new component version and digest.

Validate checked-in artifacts:

```bash
python3 -m pip install -r semantic-components/requirements.txt
python3 semantic-components/scripts/validate_components.py
```

Maintainers may refresh canonical hashes after an intentional content change with
`--write-hashes`, then must review and commit the resulting diff.
