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

rule {
    description           = null
    destination_addresses = ["192.0.2.1", "192.0.2.2"]
    destination_fqdns     = []
    destination_ip_groups = []
    destination_ports     = ["*"]
    name                  = "Rule_1"
    protocols             = ["Any"]
    source_addresses      = ["198.51.100.1"]
    source_ip_groups      = []
}
rule {
    description           = null
    destination_addresses = ["198.51.100.1"]
    destination_fqdns     = []
    destination_ip_groups = []
    destination_ports     = ["*"]
    name                  = "Rule_2"
    protocols             = ["Any"]
    source_addresses      = ["192.0.2.1", "192.0.2.2"]
    source_ip_groups      = []
}
network_rule_collection {
    action   = "Allow"
    name     = "Connector"
    priority = 100
    rule {
        description           = null
        destination_addresses = ["*"]
        destination_fqdns     = []
        destination_ip_groups = []
        destination_ports     = ["*"]
        name                  = "Rule_3"
        protocols             = ["Any"]
        source_addresses      = ["192.0.2.3"]
        source_ip_groups      = []
    }
    rule {
        description           = null
        destination_addresses = ["*"]
        destination_fqdns     = []
        destination_ip_groups = []
        destination_ports     = ["*"]
        name                  = "Allow_ICMP_Local"
        protocols             = ["ICMP"]
        source_addresses      = ["198.51.100.0/24"]
        source_ip_groups      = []
    }
    rule {
        description           = null
        destination_addresses = ["192.0.2.3"]
        destination_fqdns     = []
        destination_ip_groups = []
        destination_ports     = ["22"]
        name                  = "Allow_SSH_Local"
        protocols             = ["Any"]
        source_addresses      = ["198.51.100.0/24"]
        source_ip_groups      = []
    }
    rule {
        description           = null
        destination_addresses = ["192.0.2.3"]
        destination_fqdns     = []
        destination_ip_groups = []
        destination_ports     = ["*"]
        name                  = "Allow_ICMP_External"
        protocols             = ["ICMP"]
        source_addresses      = ["*"]
        source_ip_groups      = []
    }
    rule {
        description           = null
        destination_addresses = ["192.0.2.4"]
        destination_fqdns     = []
        destination_ip_groups = []
        destination_ports     = ["*"]
        name                  = "Allow_DataBroker_Traffic"
        protocols             = ["Any"]
        source_addresses      = ["198.51.100.0/24"]
        source_ip_groups      = []
    }
    rule {
        description           = null
        destination_addresses = ["198.51.100.0/24"]
        destination_fqdns     = []
        destination_ip_groups = []
        destination_ports     = ["*"]
        name                  = "DataBroker_To_Internal"
        protocols             = ["Any"]
        source_addresses      = ["192.0.2.4"]
        source_ip_groups      = []
    }
    rule {
        description           = null
        destination_addresses = ["192.0.2.5"]
        destination_fqdns     = []
        destination_ip_groups = []
        destination_ports     = ["*"]
        name                  = "DataBroker_To_Storage"
        protocols             = ["Any"]
        source_addresses      = ["192.0.2.4"]
        source_ip_groups      = []
    }
    rule {
        description           = null
        destination_addresses = ["192.0.2.5"]
        destination_fqdns     = []
        destination_ip_groups = []
        destination_ports     = ["*"]
        name                  = "Storage_To_Cloud"
        protocols             = ["Any"]
        source_addresses      = ["198.51.100.0/24"]
        source_ip_groups      = []
    }
    rule {
        description           = null
        destination_addresses = ["192.0.2.6"]
        destination_fqdns     = []
        destination_ip_groups = []
        destination_ports     = ["*"]
        name                  = "Storage_To_DataCenter"
        protocols             = ["Any"]
        source_addresses      = ["192.0.2.5"]
        source_ip_groups      = []
    }
    rule {
        description           = null
        destination_addresses = ["192.0.2.5"]
        destination_fqdns     = []
        destination_ip_groups = []
        destination_ports     = ["*"]
        name                  = "DataCenter_To_Storage"
        protocols             = ["Any"]
        source_addresses      = ["192.0.2.6"]
        source_ip_groups      = []
    }
    rule {
        description           = null
        destination_addresses = ["192.0.2.7"]
        destination_fqdns     = []
        destination_ip_groups = []
        destination_ports     = ["*"]
        name                  = "Allow_FileSync_Server"
        protocols             = ["Any"]
        source_addresses      = ["198.51.0.0/16"]
        source_ip_groups      = []
    }
    rule {
        description           = null
        destination_addresses = ["198.51.0.0/16"]
        destination_fqdns     = []
        destination_ip_groups = []
        destination_ports     = ["*"]
        name                  = "FileSync_Backup"
        protocols             = ["Any"]
        source_addresses      = ["192.0.2.7"]
        source_ip_groups      = []
    }
}
```
### DNAT Rules
```markdown
## DNAT Rules

nat_rule_collection {
    action   = "Dnat"
    name     = "sanitizedRuleCollection"
    priority = 100
    rule {
      destination_address = "203.0.113.1"
      destination_ports   = ["22"]
      name                = "Rule_1"
      protocols           = ["TCP"]
      source_addresses    = ["*"]
      translated_address  = "192.0.2.1"
      translated_port     = 22
    }
    rule {
      destination_address = "203.0.113.1"
      destination_ports   = ["21"]
      name                = "Rule_2"
      protocols           = ["TCP"]
      source_addresses    = ["*"]
      translated_address  = "192.0.2.1"
      translated_port     = 21
    }
    rule {
      destination_address = "203.0.113.2"
      destination_ports   = ["443"]
      name                = "Rule_3"
      protocols           = ["TCP"]
      source_addresses    = ["*"]
      translated_address  = "192.0.2.2"
      translated_port     = 443
    }
    rule {
      destination_address = "203.0.113.2"
      destination_ports   = ["80"]
      name                = "Rule_4"
      protocols           = ["TCP"]
      source_addresses    = ["*"]
      translated_address  = "192.0.2.2"
      translated_port     = 80
    }
    rule {
      destination_address = "203.0.113.3"
      destination_ports   = ["443"]
      name                = "Rule_5"
      protocols           = ["TCP"]
      source_addresses    = ["*"]
      translated_address  = "192.0.2.3"
      translated_port     = 443
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
<img width="1821" alt="firewall_mindmap_ex" src="https://github.com/user-attachments/assets/6ae45334-3bfe-4157-8a68-3cfcaacd23dd">

## Dnat Rules Mindmap Python 
```python
import re
import graphviz

# Function to parse the DNAT rules from the markdown file
def parse_markdown_rules(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Define a regex pattern to extract DNAT rule attributes from the markdown
    rule_pattern = re.compile(r'rule\s*{(.*?)}', re.DOTALL)
    rules = rule_pattern.findall(content)
    
    parsed_rules = []
    
    # Regex patterns to extract specific rule fields
    field_patterns = {
        'name': re.compile(r'name\s*=\s*"(.+?)"'),
        'source_addresses': re.compile(r'source_addresses\s*=\s*\[([^\]]+)\]'),
        'destination_address': re.compile(r'destination_address\s*=\s*"(.+?)"'),
        'destination_ports': re.compile(r'destination_ports\s*=\s*\[([^\]]+)\]'),
        'protocols': re.compile(r'protocols\s*=\s*\[([^\]]+)\]'),
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
                if key in ['source_addresses', 'destination_ports', 'protocols']:
                    rule_data[key] = [addr.strip().strip('"') for addr in rule_data[key].split(',')]
        parsed_rules.append(rule_data)
    
    return parsed_rules

# Function to display the parsed DNAT rules (for debugging or visualization purposes)
def display_parsed_rules(parsed_rules):
    for idx, rule in enumerate(parsed_rules):
        print(f"Rule {idx + 1}:")
        print(f"  Name: {rule.get('name', 'N/A')}")
        print(f"  Destination Address: {rule.get('destination_address', 'N/A')}")
        print(f"  Destination Ports: {', '.join(rule.get('destination_ports', []))}")
        print(f"  Protocols: {', '.join(rule.get('protocols', []))}")
        print(f"  Source Addresses: {', '.join(rule.get('source_addresses', []))}")
        print(f"  Translated Address: {rule.get('translated_address', 'N/A')}")
        print(f"  Translated Port: {rule.get('translated_port', 'N/A')}")
        print()

# Function to create a mind map using the Graphviz library
def create_mind_map(parsed_rules):
    # Create a new directed graph
    dot = graphviz.Digraph(comment='DNAT Rules Mind Map')
    
    # Iterate over the parsed rules and create nodes/edges
    for rule in parsed_rules:
        for src in rule.get('source_addresses', []):
            dest = rule.get('destination_address', 'N/A')
            translated_dest = rule.get('translated_address', 'N/A')
            label = f"Protocol: {', '.join(rule.get('protocols', []))}\nDest Port: {', '.join(rule.get('destination_ports', []))}\nTrans Port: {rule.get('translated_port', 'N/A')}"
            
            # Create source and destination nodes
            dot.node(src, src)  # Source node
            dot.node(dest, dest)  # Destination node
            dot.node(translated_dest, translated_dest)  # Translated address node
            
            # Create edges
            dot.edge(src, dest, label=f"Original ({label})")
            dot.edge(dest, translated_dest, label="Translated")
    
    # Save the mind map to a PDF file
    dot.render('dnat_rules_mindmap_ex', format='pdf')
    print("Mind map created and saved as 'dnat_rules_mindmap_ex.pdf'")

# Path to your markdown file
file_path = 'dnatrulex.md'  # Update with your file path

# Parse and display the rules
parsed_rules = parse_markdown_rules(file_path)
display_parsed_rules(parsed_rules)

# Create the mind map based on the parsed rules
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
<img width="1643" alt="dnat_mindmap" src="https://github.com/user-attachments/assets/f9e41dd2-410e-4478-bafd-07ec1df30d21">

# Customization

	•	Output Format: By default, the output format is PDF. You can change the output format by modifying the format argument in the dot.render() function (e.g., 'png', 'svg').
	•	Node and Edge Labels: You can adjust the labels for nodes and edges to include additional information like translated addresses or ports by modifying the string formatting in dot.edge().

This project simplifies the process of visualizing firewall and DNAT rules by using Python and Graphviz to generate readable mind maps.
