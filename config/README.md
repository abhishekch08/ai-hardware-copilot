# Runtime Configuration

- `agents/` contains the 184 generated specialist configurations. Edit the canonical registry/handbooks, then run `python scripts/compile_agent_configs.py`; do not hand-edit generated agent YAML.
- `mandatory_review_rules.yaml` contains conservative lifecycle, consequence and domain activation rules.
- `capability_graph.yaml` expands an active specialist into interface owners and adjacent domain leads.
- `model_profiles.yaml` defines provider-neutral reasoning/compute classes.
- `tool_permissions.yaml` defines permission levels from read-only context through safety-relevant physical action.

All referenced agent IDs are validated when the runtime starts. A task may add `required_agents` for known edge cases and `excluded_keywords` for negated or misleading terms.
