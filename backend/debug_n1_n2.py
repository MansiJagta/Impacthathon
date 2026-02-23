from app.nodes.node1_extraction.extractor import process_documents
from app.nodes.node2_cross_validation.validator import cross_validate
from pathlib import Path
import os

print("Starting Node 1...")
files = ["sample_docs/bill.jpg"] # Test with one file
if not os.path.exists(files[0]):
    print(f"Error: {files[0]} not found")
    exit(1)

try:
    node1_output = process_documents("test_claim", files)
    print("Node 1 finished")
    print(f"Node 1 keys: {node1_output.keys()}")
    
    print("Starting Node 2...")
    node2_output = cross_validate(node1_output)
    print("Node 2 finished")
    print(f"Node 2 Output: {node2_output}")
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
