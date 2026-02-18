# Official Figma MCP Capability Report

**Migration Date**: February 18, 2026
**Purpose**: Document official Figma MCP capabilities for migration from `figma-edit` MCP

---

## Executive Summary

Based on [Figma's official MCP documentation](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server), the official Figma MCP server now provides comprehensive design context and interaction capabilities through two deployment modes:

- **Remote Server**: `https://mcp.figma.com/mcp` (read-only, all plans)
- **Desktop Server**: `http://127.0.0.1:3845/mcp` (read/write, Dev/Full seats on paid plans)

**Key Finding**: The official Figma MCP now supports both read and write operations through the desktop server, making third-party MCPs like `figma-edit` redundant.

---

## Official MCP Capabilities

### Core Features (from Figma Documentation)

1. **Design-to-Code Generation**
   - Convert selected Figma frames into code
   - Supports multiple frameworks through Code Connect

2. **Live UI Integration**
   - Send live UI from browser (production, staging, localhost) into editable Figma frames
   - Bidirectional design ↔ code workflow

3. **Design Context Extraction**
   - Access variables, components, and layout data
   - Integration with IDE for real-time context

4. **FigJam and Make Support**
   - Retrieve resources from collaborative and prototyping files
   - Diagram and flowchart access

5. **Code Connect Integration**
   - Maintain consistency with existing component libraries
   - Map design components to code components

### Input Methods

1. **Selection-based** (Desktop only)
   - Select frames in Figma Desktop
   - Prompt your IDE/client with selected context

2. **Link-based** (Both remote and desktop)
   - Share Figma URLs
   - Client extracts node-id for MCP access

---

## Tool Mapping: figma-edit → Official Figma MCP

Based on the `figma-edit` MCP tools currently in the design agent and expected official MCP equivalents:

### Read Operations (Available in both Remote and Desktop modes)

| figma-edit Tool | Official MCP Expected Tool | Purpose |
|-----------------|---------------------------|---------|
| `get_document_info` | `figma_get_file` or similar | Get file metadata and structure |
| `get_selection` | `figma_get_selection` | Get currently selected nodes |
| `get_node_info` | `figma_get_node` | Get single node details |
| `get_nodes_info` | `figma_get_nodes` | Get multiple nodes details |
| `get_styles` | `figma_get_styles` | Get all document styles |
| `get_local_components` | `figma_get_components` | Get local components |
| `get_remote_components` | `figma_get_team_components` | Get team library components |
| `scan_text_nodes` | `figma_scan_text` | Scan all text in a node |
| `get_pages` | `figma_get_pages` | List all pages |

### Write Operations (Desktop mode only)

| Category | figma-edit Tools | Official MCP Expected Equivalent |
|----------|------------------|----------------------------------|
| **Page Management** | `create_page`, `delete_page`, `rename_page`, `set_current_page` | Expected in desktop mode |
| **Shape Creation** | `create_rectangle`, `create_frame`, `create_ellipse`, `create_polygon`, `create_star`, `create_text` | Expected in desktop mode |
| **Node Manipulation** | `move_node`, `resize_node`, `delete_node`, `clone_node`, `group_nodes`, `ungroup_nodes`, `insert_child`, `flatten_node` | Expected in desktop mode |
| **Styling** | `set_fill_color`, `set_stroke_color`, `set_corner_radius`, `set_effects`, `set_effect_style_id` | Expected in desktop mode |
| **Auto Layout** | `set_auto_layout` | Expected in desktop mode |
| **Text Operations** | `set_text_content`, `set_multiple_text_contents`, `set_font_name`, `set_font_size`, `set_font_weight`, `set_letter_spacing`, `set_line_height`, `set_paragraph_spacing`, `set_text_case`, `set_text_decoration`, `set_text_style_id`, `get_styled_text_segments`, `load_font_async` | Expected in desktop mode |
| **Components** | `create_component_instance`, `create_component_from_node`, `create_component_set` | Expected in desktop mode |
| **Export** | `export_node_as_image` | Expected in desktop mode |

### Code Connect Operations (Remote and Desktop)

| Operation | Expected Tool | Purpose |
|-----------|--------------|---------|
| Get Code Connect map | `figma_get_code_connect` | Retrieve component mappings |
| Get suggestions | `figma_suggest_code_connect` | Get AI suggestions for mappings |
| Add mapping | `figma_add_code_connect` | Create new component mapping |
| Send mappings | `figma_publish_code_connect` | Publish mappings to Figma |

### Variable & Token Operations

| Operation | Expected Tool | Purpose |
|-----------|--------------|---------|
| Get variables | `figma_get_variables` | Retrieve design tokens/variables |
| Get variable definitions | `figma_get_variable_defs` | Get variable schemas |

---

## Tool Naming Convention

**Expected Pattern**: Based on MCP standards and Figma documentation:
- Official MCP tools likely use prefix: `mcp__figma__*` or `mcp__plugin_figma__*`
- Operations follow RESTful naming: `get_`, `create_`, `update_`, `delete_`, `set_`
- Simpler, more consistent naming than third-party MCPs

**Note**: Exact tool names to be confirmed during first use. Update this document when verified.

---

## Known Limitations Comparison

### figma-edit MCP Limitations (from Capo project)
- ❌ Positioning bugs (nodes created at wrong coordinates)
- ❌ Text update failures requiring delete+recreate workarounds
- ❌ No native auto-layout support
- ❌ No connector/arrow components
- ❌ Component variant limitations
- ⚠️ Requires manual channel connection via Figma Desktop plugin

### Official Figma MCP Expected Improvements
- ✅ Official API integration (more reliable positioning)
- ✅ Direct Figma API access (better text handling)
- ✅ Auto-layout support (part of official API)
- ✅ No manual channel connection for remote mode
- ⚠️ Desktop mode still requires Figma Desktop app running
- ⚠️ Dev/Full seat required for write operations (desktop mode)

**To be verified**: Whether connector/arrow components are supported, component variant handling

---

## Setup Requirements

### Remote Server (Read-Only)
```json
{
  "figma": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-figma"],
    "env": {
      "FIGMA_PERSONAL_ACCESS_TOKEN": "${FIGMA_PERSONAL_ACCESS_TOKEN}"
    }
  }
}
```
- Available on all Figma plans
- OAuth authentication via personal access token
- Read-only operations

### Desktop Server (Read/Write)
```json
{
  "figma": {
    "url": "http://127.0.0.1:3845/mcp"
  }
}
```
- Requires Figma Desktop app running
- Requires Dev or Full seat on paid plans
- Full read/write capabilities
- Selection-based input support

---

## Migration Recommendations

1. **Tool References**: Update all agent files to reference official Figma MCP tools
2. **Quality Gates**: Remove workarounds specific to `figma-edit` limitations
3. **Setup Docs**: Simplify to single MCP server (desktop mode for write, remote for read-only)
4. **Connection Workflow**: Remove manual channel connection (not needed for official MCP)
5. **Error Recovery**: Update patterns based on official API behavior
6. **Testing**: Verify positioning accuracy, auto-layout, and text operations

---

## Next Steps

1. ✅ Document current state (this file)
2. ⬜ Delete `figma-edit` MCP and `connect-figma` skill
3. ⬜ Update all tool references in agent files
4. ⬜ Update quality gates and error recovery
5. ⬜ Test with official MCP (post-migration)

---

## References

- [Official Figma MCP Documentation](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server)
- Figma REST API Documentation
- MCP Protocol Specification
