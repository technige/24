import json
import re


name_pattern = re.compile(r"([\w\d_]+)", re.UNICODE)


def jsonify(data):
    return json.dumps(data, separators=",:", ensure_ascii=False)


def camel(name):
    return "_".join(name_pattern.findall(name)).lower()


class Node:

    def __init__(self, name, primary_label, primary_key, properties):
        self.name = camel(name)
        self.primary_label = primary_label
        self.primary_key = primary_key
        self.properties = dict(properties)
    
    def __repr__(self):
        return "(%s:%s!%s %s)" % (self.name, self.primary_label, self.primary_key, jsonify(self.properties))


class NodeSet:

    def __init__(self, label, key):
        self.label = label
        self.key = key
        self.nodes = {}
    
    def add(self, name, properties):
        node = Node(name, self.label, self.key, properties)
        self.nodes[node.name] = node
    
    def __repr__(self):
        s = []
        s.append("/* %s nodes */" % self.label)
        for name, node in sorted(self.nodes.items()):
            s.append(repr(node))
        return "\n".join(s)


class Path:

    def __init__(self, *parts):
        self.parts = parts

    def __repr__(self):
        s = []
        for i, part in enumerate(self.parts):
            if i % 2 == 0:
                s.append("(%s)" % camel(part))
            elif isinstance(part, tuple):
                s.append("-[:%s %s]->" % (part[0], jsonify(part[1])))
            else:
                s.append("-[:%s]->" % part)
        return "".join(s)
    
    def __len__(self):
        return (len(self.parts) - 1) // 2


class PathList(list):

    def __init__(self):
        super().__init__()
        self.comment = None
    
    def __repr__(self):
        s = []
        if self.comment:
            s.append("/* %s */" % self.comment)
        for path in self:
            s.append(repr(path))
        return "\n".join(s)

