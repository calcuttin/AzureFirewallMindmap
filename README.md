# Generate a Mind Map from Parsed Rules (Using Graphviz)

This section of the project demonstrates how to parse firewall or DNAT rules from markdown files and generate a **mind map** using **Graphviz**. The mind map will visually represent the relationships between source and destination addresses, along with the associated protocols and actions.

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Steps to Generate a Mind Map](#steps-to-generate-a-mind-map)
  - [1. Parse Rules](#1-parse-rules)
  - [2. Generate a Mind Map Using Graphviz](#2-generate-a-mind-map-using-graphviz)
  - [3. Visualize the Mind Map](#3-visualize-the-mind-map)
- [Python Script](#python-script)
- [Customization](#customization)

## Overview

This Python script reads firewall or DNAT rules from a markdown file, parses the rules, and generates a **Graphviz-based mind map**. The script creates nodes for each source and destination address and draws edges labeled with the protocol and action (e.g., Allow or Deny).

## Requirements

- **Python 3.x**: Ensure Python is installed.
- **Graphviz**: You will need both the **Graphviz software** and the Python library to generate and visualize the mind map.

  - Install Graphviz using:
    ```bash
    sudo apt-get install graphviz   # For Ubuntu/Debian
    brew install graphviz           # For macOS
    choco install graphviz          # For Windows (via Chocolatey)
    ```

  - Install the Python `graphviz` library using:
    ```bash
    pip install graphviz
    ```
## Sample Terraform markdown output
### Firewall Rules
```markdown
## Network Rules

terraform
resource "firewall_rule" "internal_to_cloud" {
  name                  = "Internal_to_Cloud"
  action                = "allow"
  source_addresses      = ["192.168.1.0/24"]
  destination_addresses = ["10.0.0.1", "10.0.0.2"]
  protocols             = ["tcp", "udp"]
}

resource "firewall_rule" "cloud_to_internal" {
  name                  = "Cloud_to_Internal"
  action                = "allow"
  source_addresses      = ["10.0.0.1", "10.0.0.2"]
  destination_addresses = ["192.168.1.0/24"]
  protocols             = ["tcp"]
}

resource "firewall_rule" "block_external" {
  name                  = "Block_External_Access"
  action                = "deny"
  source_addresses      = ["0.0.0.0/0"]
  destination_addresses = ["192.168.1.10"]
  protocols             = ["tcp"]
}
```
### DNAT Rules
```markdown
nat_rule_collection {
    action   = "Dnat"
    name     = "sanitizedRuleCollection"
    priority = 100
    rule {
      destination_address = "203.0.113.5"
      destination_ports   = ["80"]
      name                = "http-traffic"
      protocols           = ["TCP"]
      source_addresses    = ["0.0.0.0/0"]
      translated_address  = "10.0.0.1"
      translated_port     = 8080
    }
    rule {
      destination_address = "203.0.113.5"
      destination_ports   = ["443"]
      name                = "https-traffic"
      protocols           = ["TCP"]
      source_addresses    = ["0.0.0.0/0"]
      translated_address  = "10.0.0.2"
      translated_port     = 8443
    }
}
```

## Steps to Generate a Mind Map

### 1. Parse Rules

The Python script reads and parses the firewall or DNAT rules from a markdown file. It extracts relevant fields such as `source_addresses`, `destination_addresses`, `protocols`, `translated_address`, etc.

### 2. Generate a Mind Map Using Graphviz

Once the rules are parsed, the script uses the **Graphviz** library to generate a mind map. The rules are visualized as nodes (representing source and destination addresses) connected by edges (representing protocols and actions).

### 3. Visualize the Mind Map

After generating the Graphviz mind map, it is saved as a **PDF** file or other image format.

#### Example:

```bash
python generate_mindmap.py
```
This will output a file called firewall_rules_mindmap.pdf containing the mind map.

# Python Script

Here is the Python script that parses the rules and generates a mind map using Graphviz:
```python
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
    print("Mind map created and saved as 'firewall_rules_mindmap.pdf'")

# Example usage
input_file_path = 'parsed_rules.md'  # Path to your markdown file
parsed_rules = parse_markdown_rules(input_file_path)
create_mind_map(parsed_rules)
```
Running the Script

	1.	Ensure you have Graphviz installed.
	2.	Place your firewall or DNAT rules in a markdown file (e.g., parsed_rules.md).
	3.	Run the script:
 ```bash
python generate_mindmap.py
```
This will generate a PDF file (firewall_rules_mindmap.pdf) containing the mind map.

# Customization

	•	Output Format: By default, the output format is PDF. You can change the output format by modifying the format argument in the dot.render() function (e.g., 'png', 'svg').
	•	Node and Edge Labels: You can adjust the labels for nodes and edges to include additional information like translated addresses or ports by modifying the string formatting in dot.edge().

This project simplifies the process of visualizing firewall and DNAT rules by using Python and Graphviz to generate readable mind maps.
