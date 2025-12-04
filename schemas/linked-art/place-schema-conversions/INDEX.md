# Linked Art Place - Complete Documentation Package

This package contains a complete conversion of the Linked Art Place JSON Schema to RDF/Linked Data formats, with extensive documentation and examples.

## Start Here

**New to RDF?** → Start with `comparison.md` to see JSON-LD vs Turtle side-by-side  
**Need examples?** → Start with `place-minimal.ttl` for simple cases  
**Want complete examples?** → Start with `place.ttl` with SHACL shapes  
**Need to integrate?** → Start with `code_examples.md` for your language  
**Quick lookup?** → Start with `quick_reference.md` for property mappings  

## File Inventory

### RDF Data Files

#### Full Examples (97 triples)
- **place.ttl** - Complete Turtle serialization with SHACL shapes and detailed Place examples
- **place.nt** - Same content in N-Triples format (one triple per line)
- **place.jsonld** - Same content in JSON-LD format

#### Minimal Examples (9 triples)
- **place-minimal.ttl** - Bare minimum Place examples (just required properties)
- **place-minimal.nt** - Minimal examples in N-Triples format
- **place-minimal.jsonld** - Minimal examples in JSON-LD format

### Documentation Files

- **README.md** (this file) - Overview and file inventory
- **comparison.md** - Side-by-side JSON-LD vs Turtle comparison with usage guidance
- **code_examples.md** - Practical code examples in Python, JavaScript, PHP, R, SQL
- **quick_reference.md** - Concise property mappings and common patterns

## Use Cases & Recommended Files

### For Understanding the Model
1. Read `comparison.md` - See how JSON-LD maps to Turtle
2. Open `place-minimal.ttl` - Study simple examples
3. Open `place.ttl` - Explore full-featured examples

### For Implementation
1. Check `quick_reference.md` - Property mappings and patterns
2. Review `code_examples.md` - Find code for your environment
3. Use appropriate format:
   - Web APIs: `place.jsonld`
   - Triple stores: `place.nt` or `place.ttl`
   - Documentation: `place.ttl`

### For Data Integration
1. Review `code_examples.md` - Database integration examples
2. Use `place.nt` - For bulk loading
3. Use `place.jsonld` - For document stores (MongoDB)

### For Validation
1. Check `place.ttl` - Contains SHACL shapes
2. Use examples in `code_examples.md` - pySHACL validation code

### For Teaching/Learning
1. Start with `comparison.md` - Understand both formats
2. Study `place-minimal.ttl` - Build intuition with simple examples
3. Read `quick_reference.md` - Quick lookups while learning
4. Explore `place.ttl` - See advanced patterns

## Key Concepts

### CIDOC-CRM Mappings
The conversion follows these core mappings:

```
JSON Schema Property → CIDOC-CRM Predicate
─────────────────────────────────────────────
type: "Place"        → rdf:type crm:E53_Place
_label               → rdfs:label
classified_as        → crm:P2_has_type
identified_by        → crm:P1_is_identified_by
referred_to_by       → crm:P67i_is_referred_to_by
defined_by           → crm:P168_place_is_defined_by
part_of              → crm:P89_falls_within
equivalent           → skos:exactMatch
```

### Required Properties
Every Place must have:
1. `rdf:type crm:E53_Place` - Declares it as a Place
2. `rdfs:label` - Human-readable name
3. `id` (the URI) - Unique identifier

### Optional Properties
All other properties are optional but recommended for richer descriptions.

## Format Selection Guide

| Format | Best For | Tool Support |
|--------|----------|--------------|
| **Turtle (.ttl)** | Human reading, version control, documentation | ✓ All RDF tools |
| **N-Triples (.nt)** | Bulk loading, streaming, simple parsing | ✓ All RDF tools |
| **JSON-LD (.jsonld)** | Web APIs, JavaScript, document stores | ✓ Most RDF tools |

## Quick Start Examples

### Python
```python
from rdflib import Graph

g = Graph()
g.parse('place.ttl', format='turtle')
print(f"Loaded {len(g)} triples")
```

### JavaScript
```javascript
const rdf = require('rdf-ext');
const ParserN3 = require('@rdfjs/parser-n3');
const fs = require('fs');

const parser = new ParserN3();
const quadStream = parser.import(fs.createReadStream('place.ttl'));
```

### PHP
```php
use EasyRdf\Graph;

$graph = new Graph();
$graph->parseFile('place.ttl', 'turtle');
```

### Command Line (with rapper)
```bash
# Convert Turtle to N-Triples
rapper -i turtle -o ntriples place.ttl > output.nt

# Validate syntax
rapper -i turtle -c place.ttl

# Query with SPARQL
sparql --data=place.ttl --query=query.rq
```

## Integration Workflows

### Workflow 1: Load into Triple Store
```bash
# Load into Apache Jena TDB2
tdb2.tdbloader --loc /path/to/database place.nt

# Query the data
tdb2.tdbquery --loc /path/to/database --query query.rq
```

### Workflow 2: Convert and Use
```python
# Load any format, export as desired
from rdflib import Graph

g = Graph()
g.parse('place.ttl', format='turtle')

# Export as needed
g.serialize('output.nt', format='nt')
g.serialize('output.jsonld', format='json-ld')
g.serialize('output.xml', format='xml')
```

### Workflow 3: Validate and Transform
```python
from pyshacl import validate
from rdflib import Graph

data = Graph()
data.parse('place.ttl', format='turtle')

shapes = Graph()
shapes.parse('place.ttl', format='turtle')  # Contains SHACL

conforms, results, text = validate(data, shacl_graph=shapes)
print(f"Valid: {conforms}")
```

## Standards Compliance

This conversion follows:
- **Linked Art API 1.0** - https://linked.art/api/1.0/
- **CIDOC-CRM 7.1.1** - http://www.cidoc-crm.org/
- **W3C RDF 1.1** - https://www.w3.org/TR/rdf11-concepts/
- **W3C SHACL** - https://www.w3.org/TR/shacl/
- **OGC GeoSPARQL** - http://www.opengis.net/ont/geosparql

## Common Questions

**Q: Which format should I use?**  
A: For human review use Turtle (.ttl), for bulk processing use N-Triples (.nt), for web APIs use JSON-LD (.jsonld).

**Q: Can I mix and match?**  
A: Yes! All formats represent the same RDF graph and can be converted between each other.

**Q: Do I need all the files?**  
A: No. Choose the format that fits your needs. The minimal examples are often sufficient to start.

**Q: How do I validate my data?**  
A: Use the SHACL shapes in place.ttl with a SHACL validator (see code_examples.md).

**Q: Can I extend the model?**  
A: Yes. Add custom properties, but prefer reusing existing CIDOC-CRM and standard vocabularies.

**Q: Where can I find more examples?**  
A: See the Linked Art community examples at https://linked.art/

## Next Steps

1. **Explore** the format that matches your needs
2. **Read** the relevant documentation file
3. **Try** the code examples in your environment
4. **Validate** using the SHACL shapes provided
5. **Extend** with your own data

## Getting Help

- **Linked Art**: https://linked.art/
- **CIDOC-CRM**: http://www.cidoc-crm.org/
- **RDFLib (Python)**: https://rdflib.readthedocs.io/
- **Apache Jena**: https://jena.apache.org/
- **EasyRDF (PHP)**: https://www.easyrdf.org/

## File Generation

All files were programmatically generated from the source JSON Schema (place.json) using RDFLib for format conversions. The examples use real locations (Raleigh, NC and hierarchy) to demonstrate practical usage.

**Generated:** December 3, 2024  
**Schema Source:** Linked Art Place Schema v1.0  
**Format:** RDF 1.1 / Turtle / N-Triples / JSON-LD  
