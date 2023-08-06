## Diagrams adapters

Set of adapters to generate architecture diagrams from popular text file formats using awesome tool https://github.com/mingrammer/diagrams

### Install
    pip install diagrams-adapters
    
### Usage

#### JSONAdapter Example
Please refer to the [oficial diagrams docs](https://diagrams.mingrammer.com/docs/guides/diagram) for examples of field values

```python
# main.py
from diagrams_adapters import JSONAdapter

with open('diagram.json', 'r') as file:
    json_str = file.read()

diagram = JSONAdapter(json_str)
diagram.generate()
```

```python
# diagram.json
{
  "diagram": {
    "name": "Grouped Workers",
    "show": false,
    "direction": "TB",
    "nodes": [
      {
        "id": "load_balancer",
        "provider": "aws",
        "resource_type": "network",
        "name": "ELB",
        "attrs": {
          "label": "Load Balancer"
        }
      },
      {
        "id": "db",
        "provider": "aws",
        "resource_type": "database",
        "name": "RDS",
        "attrs": {
          "label": "Events"
        }
      },
      {
        "id": "worker_1",
        "provider": "aws",
        "resource_type": "compute",
        "name": "EC2",
        "attrs": {
          "label": "Worker1"
        }
      },
      {
        "id": "worker_2",
        "provider": "aws",
        "resource_type": "compute",
        "name": "EC2",
        "attrs": {
          "label": "Worker2"
        }
      },
      {
        "id": "worker_3",
        "provider": "aws",
        "resource_type": "compute",
        "name": "EC2",
        "attrs": {
          "label": "Worker3"
        }
      }
    ],
    "links": {
      ">>": [
        ["load_balancer", "worker_1", "db"],
        ["load_balancer", "worker_2", "db"],
        ["load_balancer", "worker_3", "db"]
      ],
      "<<": [],
      "-": []
    }
  }
}
```

#### Clustering
ATM it is not supported
