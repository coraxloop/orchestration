# Fictional signing record

This fictional record identifies the `alpha` loop's public signing identities by role. The hexadecimal fingerprints below are fabricated 40-digit examples; this file contains no secret key, passphrase or keyring material.

|Role|Algorithm and capability|Fictional fingerprint|State|
|----|------------------------|---------------------|-----|
|Certify root|Ed25519, certify only|`A1B2C3D4E5F60718293A4B5C6D7E8F9012345678`|Public record; private half removed after revocation certificates are checked.|
|Commit signing subkey|Ed25519, sign only|`11223344556677889900AABBCCDDEEFF00112233`|The loop's signing role; rotate before expiry.|

The instance records creation, expiry, rotation and revocation evidence when real keys are established. A repository pins the signing subkey fingerprint for its own commits; a worker never signs or handles the keyring.
