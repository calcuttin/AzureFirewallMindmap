import re
import graphviz

# Function to parse firewall or DNAT rules from a markdown file
def parse_markdown_rules(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Define a regex pattern to extract rule attributes
    rule_pattern = re.compile(r'rule\s*{(.*?)}', re.DOTALL)
    rules = rule_pattern.findall(content)
    
    parsed_rules = []
    
    # Regex patterns to extract specific rule fields
    field_patterns = {
        'name': re.compile(r'name\s*=\s*"(.+?)"'),
        'source_addresses': re.compile(r'source_addresses\s*=\s*$begin:math:display$([^$end:math:display$]+)\]'),
        'destination_addresses': re.compile(r'destination_addresses\s*=\s*$begin:math:display$([^$end:math:display$]+)\]'),
        'protocols': re.compile(r'protocols\s*=\s*$begin:math:display$([^$end:math:display$]+)\]'),
        'action': re.compile(r'action\s*=\s*"(.+?)"'),
        'translated_address': re.compile(r'translated_address\s*=\s*"(.+?)"'),
        'translated_port': re.compile(r'translated_port\s*=\s*(\d+)')
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

# Function to generate a mind map using Graphviz
def create_mind_map(parsed_rules):
    # Create a new directed graph
    dot = graphviz.Digraph(comment='Firewall & DNAT Rules Mind Map')
    
    # Iterate over the parsed rules and create nodes/edges
    for rule in parsed_rules:
        for src in rule.get('source_addresses', []):
            for dest in rule.get('destination_addresses', []):
                dot.node(src, src)  # Create source node
                dot.node(dest, dest)  # Create destination node
                label = f"{', '.join(rule.get('protocols', []))} ({rule.get('action', 'N/A')})"
                dot.edge(src, dest, label=label)  # Create edge with protocol and action
    
    # Render the mind map to a PDF file
    dot.render('firewall_rules_mindmap', format='pdf')
    print("Mind map created and saved as 'dnat_rules_ex_test.pdf'")

# Example usage
input_file_path = 'dnatrulex.md'  # Path to your markdown file
parsed_rules = parse_markdown_rules(input_file_path)
create_mind_map(parsed_rules)