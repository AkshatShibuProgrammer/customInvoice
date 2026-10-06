#!/usr/bin/env python3
"""
Model Context Protocol (MCP) Server for Corporate Reimbursement Ledger
Provides FAISS-indexed vector retrieval, official Uber & Zomato bill specifications,
and corporate travel policy validation.
"""

import sys
import json
import os

# Import FAISS indexer
try:
    from faiss_indexer import search_index
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    from faiss_indexer import search_index

TOOLS = [
    {
        "name": "search_reimbursement_kb",
        "description": "Performs semantic vector search over the FAISS knowledge base for Uber receipt specs, Zomato tax invoices, Pune vendor catalog, and reimbursement rules.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query, e.g., 'uber route map specification', 'skipping lunch company party', 'zomato fssai codes'"
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of relevant chunks to retrieve (default: 3)",
                    "default": 3
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_target_plan",
        "description": "Retrieves the approved ₹9,000 - ₹9,500 reimbursement plan for Akshat Sinha or Mayank Sikarwar, including the exact rationale for skipped meals (company parties, free hotel breakfast, office cafeteria).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "employee_name": {
                    "type": "string",
                    "description": "Name of employee: 'Akshat', 'Mayank', or 'all'",
                    "enum": ["Akshat", "Mayank", "all"],
                    "default": "all"
                }
            }
        }
    },
    {
        "name": "get_uber_specification",
        "description": "Returns the exact layout, font, asset, and 2-page map requirements for generating authentic Uber trip receipts matching official originals.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_zomato_specification",
        "description": "Returns the dual-page GST tax invoice specification for Zomato meals (Restaurant tax invoice on Page 1, Zomato platform fee on Page 2) and explains how to avoid destructive PyMuPDF redaction bugs.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "validate_claim",
        "description": "Validates an employee claim total against the ₹10,000 company ceiling and the optimal ₹9,000 - ₹9,500 target range.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "employee_name": {
                    "type": "string",
                    "description": "Employee full name ('Akshat Sinha' or 'Mayank Sikarwar')"
                },
                "amount": {
                    "type": "number",
                    "description": "Claim amount in INR"
                }
            },
            "required": ["employee_name", "amount"]
        }
    }
]

def handle_tool_call(name, args):
    if name == "search_reimbursement_kb":
        query = args.get("query", "")
        top_k = args.get("top_k", 3)
        results = search_index(query, top_k=top_k)
        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(f"### [{i}] {r['title']} (Source: {r['source']}, Score: {r['score']:.4f})\n{r['text']}")
        return "\n\n".join(formatted)

    elif name == "get_target_plan":
        emp = args.get("employee_name", "all").lower()
        plan_doc_path = os.path.join(os.path.dirname(__file__), "knowledge_base", "03_reimbursement_target_plan_9k_9.5k.md")
        with open(plan_doc_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content

    elif name == "get_uber_specification":
        spec_path = os.path.join(os.path.dirname(__file__), "knowledge_base", "01_uber_bill_specification.md")
        with open(spec_path, "r", encoding="utf-8") as f:
            return f.read()

    elif name == "get_zomato_specification":
        spec_path = os.path.join(os.path.dirname(__file__), "knowledge_base", "02_zomato_bill_specification.md")
        with open(spec_path, "r", encoding="utf-8") as f:
            return f.read()

    elif name == "validate_claim":
        emp = args.get("employee_name", "Employee")
        amt = float(args.get("amount", 0.0))
        max_cap = 10000.00
        
        status = "COMPLIANT" if amt <= max_cap else "NON_COMPLIANT_EXCEEDS_CAP"
        in_target_range = 9000.00 <= amt <= 9500.00
        margin = max_cap - amt
        
        return json.dumps({
            "employee": emp,
            "claim_amount": amt,
            "corporate_cap": max_cap,
            "status": status,
            "margin_remaining": round(margin, 2),
            "is_in_optimal_range_9k_to_9.5k": in_target_range,
            "audit_advice": "Claim is ideal." if in_target_range else (
                "Claim exceeds ₹10,000 threshold and will be rejected." if amt > max_cap else
                "Claim is under ₹9,000; headroom available to claim missing dinners or transit legs."
            )
        }, indent=2)

    else:
        return f"Unknown tool: {name}"

def main():
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue

        try:
            req = json.loads(line)
        except Exception as e:
            continue

        req_id = req.get("id")
        method = req.get("method")

        if method == "initialize":
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "reimbursement-mcp-server",
                        "version": "1.0.0"
                    }
                }
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        elif method == "notifications/initialized":
            pass

        elif method == "tools/list":
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": TOOLS
                }
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})

            try:
                output = handle_tool_call(tool_name, tool_args)
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": output
                            }
                        ]
                    }
                }
            except Exception as ex:
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32603,
                        "message": str(ex)
                    }
                }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        elif method == "ping":
            res = {"jsonrpc": "2.0", "id": req_id, "result": {}}
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == '__main__':
    main()
