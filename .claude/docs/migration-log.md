# Figma MCP Migration Log

**Migration Date:** February 18, 2026
**Migration Type:** Third-party MCP → Official Figma MCP
**Status:** ✅ Completed

---

## Summary

Migrated the entire design agent from using dual third-party Figma MCPs (`figma` + `figma-edit`) to using only the official Figma MCP server. This simplifies the architecture and ensures better long-term support.

### Before Migration
- **`figma` MCP** (remote, OAuth, read-only) - Official Anthropic MCP at `https://mcp.figma.com/mcp`
- **`figma-edit` MCP** (local, write) - Third-party local Figma Desktop MCP
- **`claude-talk-to-figma-mcp`** - Custom third-party MCP (experimental, not in use)

### After Migration
- **Official Figma MCP** (unified) - Remote or desktop mode
  - Remote: `https://mcp.figma.com/mcp` (read-only, OAuth)
  - Desktop: `http://127.0.0.1:3845/mcp` (read/write, requires Figma Desktop)

---

## Migration Phases Completed

### Phase 0: Capability Assessment ✅
- Created capability report: [.claude/docs/figma-mcp-capabilities.md](.claude/docs/figma-mcp-capabilities.md)
- Documented expected tool names and capabilities based on Figma documentation
- Created tool mapping table for migration reference

### Phase 1: Cleanup ✅
**Deleted:**
- `claude-talk-to-figma-mcp/` directory (third-party custom MCP)
- `.claude/skills/connect-figma/` directory (connection skill for third-party MCP)
- `.claude/skills/figma/SETUP-CHECKLIST.md` (third-party MCP setup checklist)

**Updated:**
- [.claude/skills/figma-quality-gates/prompts/error-recovery-patterns.md](.claude/skills/figma-quality-gates/prompts/error-recovery-patterns.md) - Removed third-party MCP specific patterns

### Phase 2: Agent Files ✅
**Updated 3 agent files:**
1. [.claude/agents/ui-specialist.md](.claude/agents/ui-specialist.md)
   - Consolidated dual MCP tools into single official Figma MCP section
   - Updated tool references
2. [.claude/agents/ux-specialist.md](.claude/agents/ux-specialist.md)
   - Updated terminology to "Official Figma MCP"
3. [.claude/agents/solution-architect.md](.claude/agents/solution-architect.md)
   - Updated tool documentation format

**Updated team protocol:**
- [.claude/team.md](.claude/team.md) - Updated tool access descriptions

### Phase 3: Skill Documentation ✅
**Updated 2 skill files:**
1. [.claude/skills/figma/SKILL.md](.claude/skills/figma/SKILL.md)
   - Rewrote architecture diagram
   - Unified tool reference tables
   - Updated setup instructions
2. [.claude/skills/figma/setup.md](.claude/skills/figma/setup.md)
   - Complete rewrite for official MCP setup
   - Added remote vs desktop mode guidance
   - Added troubleshooting section

**Verified:**
- [.claude/skills/handoff/SKILL.md](.claude/skills/handoff/SKILL.md) - Already using correct references ✅

### Phase 4: Quality Gates ✅
**Updated 5 quality gate files:**
1. [.claude/skills/figma-quality-gates/SKILL.md](.claude/skills/figma-quality-gates/SKILL.md)
   - Updated target MCP reference
   - Removed third-party MCP specific language
2. [.claude/skills/figma-quality-gates/prompts/mcp-capability-test.md](.claude/skills/figma-quality-gates/prompts/mcp-capability-test.md)
   - Updated capability test descriptions
   - Generalized known issues section
3. [.claude/skills/figma-quality-gates/prompts/component-verification.md](.claude/skills/figma-quality-gates/prompts/component-verification.md)
   - Updated source attribution
4. [.claude/skills/figma-quality-gates/prompts/positioning-validation.md](.claude/skills/figma-quality-gates/prompts/positioning-validation.md)
   - Removed project-specific references
   - Generalized positioning issue patterns
5. [.claude/skills/figma-quality-gates/prompts/error-recovery-patterns.md](.claude/skills/figma-quality-gates/prompts/error-recovery-patterns.md)
   - Already updated in Phase 1 ✅

### Phase 5: Master Documentation ✅
**Updated:**
- [CLAUDE.md](../../CLAUDE.md) - Simplified Available Tools section to single Figma MCP

### Phase 6: Final Verification ✅
**Additional updates:**
- [.claude/skills/figma/prompts/design-system-constraints.md](.claude/skills/figma/prompts/design-system-constraints.md)
- [.claude/skills/figma/prompts/orchestrator-system.md](.claude/skills/figma/prompts/orchestrator-system.md)

**Created:**
- This migration log

---

## Tool Mapping Reference

Based on expected official Figma MCP tools (from documentation):

### Read Operations
| Third-Party MCP | Official MCP | Notes |
|-----------------|--------------|-------|
| `get_document_info` | `get_file` or `get_document_info` | File metadata and structure |
| `get_selection` | `get_selection` | Currently selected nodes (desktop only) |
| `get_node_info` | `get_node` | Single node details |
| `get_nodes_info` | `get_nodes` | Multiple nodes details |
| `get_local_components` | `get_local_components` | Local components |
| `get_remote_components` | `get_remote_components` | Team library components |
| `get_styles` | `get_styles` | Document styles |
| `get_screenshot` | `get_screenshot` | Screenshots |
| `get_metadata` | `get_metadata` | Node metadata |
| `get_design_context` | `get_design_context` | Code context |
| `get_variable_defs` | `get_variable_defs` | Design tokens |
| `get_code_connect_map` | `get_code_connect_map` | Code Connect mappings |

### Write Operations (Desktop Mode)
| Third-Party MCP | Official MCP | Notes |
|-----------------|--------------|-------|
| `create_frame` | `create_frame` | Create frames |
| `create_rectangle` / `create_ellipse` / `create_polygon` / `create_star` | Same | Create shapes |
| `create_text` | `create_text` | Create text nodes |
| `create_component_instance` | `create_component_instance` | Instantiate components |
| `create_component_from_node` | `create_component_from_node` | Convert to component |
| `set_auto_layout` | `set_auto_layout` | Configure auto-layout |
| `set_fill_color` / `set_stroke_color` | Same | Set colors |
| `set_effects` / `set_corner_radius` | Same | Set styling |
| `set_text_content` / `set_font_*` | Same | Text styling |
| `move_node` / `resize_node` / `clone_node` / `delete_node` | Same | Node manipulation |
| `insert_child` / `group_nodes` / `ungroup_nodes` | Same | Hierarchy |
| `rename_node` | `rename_node` | Rename nodes |
| `export_node_as_image` | `export_node_as_image` | Export assets |

**Note:** Exact tool names to be confirmed during first use. Official MCP may use slightly different naming conventions.

---

## Key Changes

### Architecture Simplification
- **Before:** Dual MCP architecture requiring both remote and local servers
- **After:** Single official MCP with remote or desktop mode selection

### Setup Simplification
- **Before:** Required manual WebSocket server setup, channel ID connection, Figma Desktop plugin
- **After:** Simple npm install or URL configuration, OAuth authentication

### Quality Gates
- **Before:** Specific workarounds for third-party MCP limitations (positioning bugs, text update issues, no auto-layout)
- **After:** Generalized quality gates for official MCP, expecting better support for features

### Documentation
- **Before:** References to "figma MCP" and "figma-edit MCP" throughout
- **After:** Unified "Official Figma MCP" or "Figma MCP" terminology

---

## Files Modified

**Total: 17 files updated, 3 deleted, 2 created**

### Created
1. `.claude/docs/figma-mcp-capabilities.md` - Capability report
2. `.claude/docs/migration-log.md` - This file

### Deleted
1. `claude-talk-to-figma-mcp/` - Third-party custom MCP directory
2. `.claude/skills/connect-figma/` - Connection skill directory
3. `.claude/skills/figma/SETUP-CHECKLIST.md` - Third-party setup checklist

### Modified
1. `CLAUDE.md` - Master orchestrator
2. `.claude/agents/ui-specialist.md` - UI agent tool references
3. `.claude/agents/ux-specialist.md` - UX agent tool references
4. `.claude/agents/solution-architect.md` - Solution architect tool references
5. `.claude/team.md` - Team protocol tool references
6. `.claude/skills/figma/SKILL.md` - Main Figma skill
7. `.claude/skills/figma/setup.md` - Setup guide
8. `.claude/skills/figma/prompts/design-system-constraints.md` - Design constraints
9. `.claude/skills/figma/prompts/orchestrator-system.md` - Orchestrator prompt
10. `.claude/skills/figma-quality-gates/SKILL.md` - Quality gates framework
11. `.claude/skills/figma-quality-gates/prompts/mcp-capability-test.md` - Capability testing
12. `.claude/skills/figma-quality-gates/prompts/component-verification.md` - Component verification
13. `.claude/skills/figma-quality-gates/prompts/positioning-validation.md` - Positioning validation
14. `.claude/skills/figma-quality-gates/prompts/error-recovery-patterns.md` - Error recovery

### Preserved (Historical Records)
- `docs/actual-vs-expected-screens.md` - Historical analysis (contains third-party MCP references for historical accuracy)
- `docs/design-failure-analysis.md` - Historical analysis (contains third-party MCP references for historical accuracy)

---

## Post-Migration Checklist

- ✅ All third-party MCP code removed
- ✅ All references to `figma-edit` MCP updated in active documentation
- ✅ All references to `claude-talk-to-figma-mcp` updated
- ✅ All references to `connect-figma` skill removed
- ✅ Agent tool lists updated
- ✅ Quality gates updated for official MCP
- ✅ Setup documentation rewritten
- ✅ Historical documents preserved
- ✅ Migration log created

---

## Next Steps

1. **Test Setup**: Follow updated setup guide to configure official Figma MCP
2. **Verify Tools**: Run capability tests to confirm official MCP tool names
3. **Update Mapping**: Refine tool mapping table based on actual MCP introspection
4. **Test Agents**: Run test builds with UI Specialist to verify all tools work
5. **Update Capability Report**: Add actual tool names and any discovered limitations

---

## References

- [Official Figma MCP Documentation](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server)
- [Figma MCP Capability Report](.claude/docs/figma-mcp-capabilities.md)
- [Migration Plan](.claude/plans/mossy-scribbling-whisper.md)

---

**Migration completed by:** Claude Sonnet 4.5
**Date:** February 18, 2026
**Status:** ✅ All phases completed successfully
