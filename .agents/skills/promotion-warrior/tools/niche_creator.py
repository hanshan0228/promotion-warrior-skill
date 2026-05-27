import os
import sys
import json

def create_niche(name, category, description):
    niche_id = name.lower().replace(' ', '_')
    niche_dir = f"/Users/han/.agents/skills/promotion-warrior/niches/{niche_id}"
    
    if os.path.exists(niche_dir):
        return f"Error: Niche '{niche_id}' already exists."
    
    os.makedirs(niche_dir, exist_ok=True)
    
    # Simple logic to generate placeholders (in reality, an LLM would fill these)
    templates = {
        "config.md": f"/Users/han/.agents/skills/promotion-warrior/templates/config.md.template",
        "intel.md": f"/Users/han/.agents/skills/promotion-warrior/templates/intel.md.template"
    }
    
    for filename, template_path in templates.items():
        with open(template_path, 'r') as f:
            content = f.read()
        
        # Replace placeholders
        content = content.replace("{PRODUCT_NAME}", name)
        content = content.replace("{PRODUCT_CATEGORY}", category)
        # ... other replacements ...
        
        with open(f"{niche_dir}/{filename}", 'w') as f:
            f.write(content)
            
    return f"Successfully created custom niche: {niche_id} at {niche_dir}"

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 niche_creator.py <Name> <Category> <Description>")
    else:
        print(create_niche(sys.argv[1], sys.argv[2], sys.argv[3]))
