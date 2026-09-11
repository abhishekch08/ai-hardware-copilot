# Local project mount

Place customer/project inputs beneath this directory for local Compose use. Its contents are ignored by Git except for this file and are mounted read-only into the service at `/projects`.

Do not commit schematics, firmware, credentials, measurements or other customer IP here. Use explicit project manifests and preserve source/revision identity in the evidence store.
