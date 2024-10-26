import re
import graphviz

# Function to parse the firewall rules from the markdown file
def parse_markdown_rules(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Define a regex pattern to extract firewall rule attributes from the markdown
    rule_pattern = re.compile(r'rule\s*{(.*?)}', re.DOTALL)
    rules = rule_pattern.findall(content)
    
    parsed_rules = []
    
    # Regex patterns to extract specific rule fields
    field_patterns = {
        'name': re.compile(r'name\s*=\s*"(.+?)"'),
        'source_addresses': re.compile(r'source_addresses\s*=\s*\[([^\]]+)\]'),
        'destination_addresses': re.compile(r'destination_addresses\s*=\s*\[([^\]]+)\]'),
        'protocols': re.compile(r'protocols\s*=\s*\[([^\]]+)\]'),
        'action': re.compile(r'action\s*=\s*"(.+?)"')
    }
    
    for rule in rules:
        rule_data = {}
        for key, pattern in field_patterns.items():
            match = pattern.search(rule)
            if match:
                rule_data[key] = match.group(1).strip()
                # Clean up arrays
                if key in ['source_addresses', 'destination_addresses', 'protocols']:
                    rule_data[key] = [addr.strip().strip('"') for addr in rule_data[key].split(',')]
        parsed_rules.append(rule_data)
    
    return parsed_rules

# Function to display the parsed rules (for debugging or visualization purposes)
def display_parsed_rules(parsed_rules):
    for idx, rule in enumerate(parsed_rules):
        print(f"Rule {idx + 1}:")
        print(f"  Name: {rule.get('name', 'N/A')}")
        print(f"  Action: {rule.get('action', 'N/A')}")
        print(f"  Source Addresses: {', '.join(rule.get('source_addresses', []))}")
        print(f"  Destination Addresses: {', '.join(rule.get('destination_addresses', []))}")
        print(f"  Protocols: {', '.join(rule.get('protocols', []))}")
        print()

# Function to create a mind map using the Graphviz library
def create_mind_map(parsed_rules):
    # Create a new directed graph
    dot = graphviz.Digraph(comment='Firewall Rules Mind Map')
    
    # Iterate over the parsed rules and create nodes/edges
    for rule in parsed_rules:
        for src in rule.get('source_addresses', []):
            for dest in rule.get('destination_addresses', []):
                dot.node(src, src)  # Create source node
                dot.node(dest, dest)  # Create destination node
                label = f"{', '.join(rule.get('protocols', []))} ({rule.get('action', 'N/A')})"
                dot.edge(src, dest, label=label)  # Create edge with protocol and action
    
    # Save the mind map to a PDF file
    dot.render('FW_rules_mindmap_ex', format='pdf')
    print("Mind map created and saved as 'FW_rules_mindmap_ex.pdf'")

# Path to your markdown file
file_path = 'firewallex.md'  # Update with your file path

# Parse and display the rules
parsed_rules = parse_markdown_rules(file_path)
display_parsed_rules(parsed_rules)

# Create the mind map based on the parsed rules
create_mind_map(parsed_rules)