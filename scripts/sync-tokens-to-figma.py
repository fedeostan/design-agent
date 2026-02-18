#!/usr/bin/env python3
"""
sync-tokens-to-figma.py

Reads design tokens from a JSON file and creates matching Figma variables
via the Figma REST API.

Usage:
    python3 scripts/sync-tokens-to-figma.py \
        --tokens tokens.json \
        --file-key YOUR_FIGMA_FILE_KEY \
        --token YOUR_FIGMA_PERSONAL_ACCESS_TOKEN

Token file format (JSON):
    {
      "colors": {
        "primary": "#7c3aed",
        "primary-light": "#ddd6fe",
        "background": "#fafafa"
      },
      "spacing": {
        "xs": 4,
        "sm": 8,
        "md": 16,
        "lg": 24,
        "xl": 32
      }
    }

What it does:
    1. Reads the token JSON file
    2. Creates a "Tokens" variable collection in the Figma file
    3. Creates COLOR variables for hex values, FLOAT variables for numbers
    4. Reports what was created
"""

import argparse
import json
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError


FIGMA_API = "https://api.figma.com"


def figma_request(method, path, token, data=None):
    """Make an authenticated request to the Figma REST API."""
    url = f"{FIGMA_API}{path}"
    headers = {
        "X-Figma-Token": token,
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode() if data else None
    req = Request(url, data=body, headers=headers, method=method)

    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"Figma API error ({e.code}): {error_body}", file=sys.stderr)
        sys.exit(1)


def hex_to_figma_color(hex_str):
    """Convert '#rrggbb' to Figma RGBA dict (0-1 floats)."""
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join(c * 2 for c in hex_str)
    r = int(hex_str[0:2], 16) / 255
    g = int(hex_str[2:4], 16) / 255
    b = int(hex_str[4:6], 16) / 255
    a = int(hex_str[6:8], 16) / 255 if len(hex_str) == 8 else 1.0
    return {"r": r, "g": g, "b": b, "a": a}


def is_hex_color(value):
    """Check if a string looks like a hex color."""
    if not isinstance(value, str):
        return False
    value = value.lstrip("#")
    return len(value) in (3, 6, 8) and all(c in "0123456789abcdefABCDEF" for c in value)


def parse_tokens(token_data, prefix=""):
    """
    Flatten nested token dict into a list of (name, resolved_type, value) tuples.

    Supports:
      - Hex color strings → COLOR type
      - Numbers → FLOAT type
    Nested keys are joined with '/'.
    """
    results = []
    for key, value in token_data.items():
        name = f"{prefix}/{key}" if prefix else key

        if isinstance(value, dict):
            results.extend(parse_tokens(value, prefix=name))
        elif is_hex_color(value):
            results.append((name, "COLOR", hex_to_figma_color(value)))
        elif isinstance(value, (int, float)):
            results.append((name, "FLOAT", float(value)))
        else:
            print(f"  Skipping '{name}': unsupported value type ({type(value).__name__})")

    return results


def get_existing_collections(file_key, token):
    """Get existing variable collections from the file."""
    resp = figma_request("GET", f"/v1/files/{file_key}/variables/local", token)
    return resp.get("meta", {}).get("variableCollections", {}), resp.get("meta", {}).get("variables", {})


def sync_tokens(tokens_path, file_key, token, collection_name="Tokens"):
    """Main sync: read tokens file, create/update Figma variables."""

    # 1. Read token file
    with open(tokens_path) as f:
        token_data = json.load(f)

    parsed = parse_tokens(token_data)
    if not parsed:
        print("No valid tokens found in file.")
        sys.exit(1)

    print(f"Parsed {len(parsed)} tokens from {tokens_path}")

    # 2. Check existing collections
    collections, existing_vars = get_existing_collections(file_key, token)

    # Find existing collection by name, or we'll create one
    existing_collection_id = None
    for cid, coll in collections.items():
        if coll.get("name") == collection_name:
            existing_collection_id = cid
            break

    # Build existing variable name→id map for this collection
    existing_var_names = {}
    if existing_collection_id:
        for vid, var in existing_vars.items():
            if var.get("variableCollectionId") == existing_collection_id:
                existing_var_names[var["name"]] = vid
        print(f"Found existing '{collection_name}' collection with {len(existing_var_names)} variables")

    # 3. Build the POST payload
    # The Variables REST API uses a single POST with actions
    variable_actions = []
    mode_id = None

    if existing_collection_id:
        # Get mode ID from existing collection
        modes = collections[existing_collection_id].get("modes", [])
        if modes:
            mode_id = modes[0]["modeId"]
    else:
        # Will be created — use a temporary ID
        variable_actions.append({
            "action": "CREATE_VARIABLE_COLLECTION",
            "id": "temp_collection",
            "name": collection_name,
            "initialModeId": "temp_mode",
        })
        existing_collection_id = "temp_collection"
        mode_id = "temp_mode"

    created = 0
    updated = 0

    for name, resolved_type, value in parsed:
        if name in existing_var_names:
            # Update existing variable value
            variable_actions.append({
                "action": "UPDATE_VARIABLE",
                "id": existing_var_names[name],
                "variableCollectionId": existing_collection_id,
                "resolvedType": resolved_type,
                "valueModeId": mode_id,
                "value": value,
            })
            updated += 1
        else:
            # Create new variable
            temp_id = f"temp_var_{name.replace('/', '_')}"
            variable_actions.append({
                "action": "CREATE_VARIABLE",
                "id": temp_id,
                "name": name,
                "variableCollectionId": existing_collection_id,
                "resolvedType": resolved_type,
            })
            variable_actions.append({
                "action": "UPDATE_VARIABLE_MODE_VALUE",
                "variableId": temp_id,
                "modeId": mode_id,
                "value": value,
            })
            created += 1

    if not variable_actions:
        print("Nothing to sync — all tokens already exist.")
        return

    # 4. Execute
    print(f"Syncing to Figma: {created} new, {updated} updates...")
    payload = {"variableCollections": variable_actions} if any(
        a["action"].startswith("CREATE_VARIABLE_COLLECTION") for a in variable_actions
    ) else {}
    # The correct payload structure for the Variables API
    full_payload = {"variables": variable_actions}

    figma_request("POST", f"/v1/files/{file_key}/variables", token, data=full_payload)

    print(f"Done! Created {created}, updated {updated} variables in '{collection_name}' collection.")


def main():
    parser = argparse.ArgumentParser(
        description="Sync design tokens from JSON to Figma variables"
    )
    parser.add_argument(
        "--tokens", required=True,
        help="Path to JSON token file"
    )
    parser.add_argument(
        "--file-key", required=True,
        help="Figma file key (from URL: figma.com/design/FILE_KEY/...)"
    )
    parser.add_argument(
        "--token", required=True,
        help="Figma personal access token"
    )
    parser.add_argument(
        "--collection", default="Tokens",
        help="Name of the variable collection to create/update (default: 'Tokens')"
    )
    args = parser.parse_args()

    sync_tokens(args.tokens, args.file_key, args.token, args.collection)


if __name__ == "__main__":
    main()
