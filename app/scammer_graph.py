from app.scammer_profiles import scammer_profiles

def build_graph():
    nodes = []
    edges = []

    for sid, profile in scammer_profiles.items():
        # Add scammer node
        nodes.append({"id": sid, "label": sid, "type": "scammer"})

        entities = profile["entities"]

        for phone in entities["phones"]:
            nodes.append({"id": phone, "label": phone, "type": "phone"})
            edges.append({"source": sid, "target": phone})

        for upi in entities["upi"]:
            nodes.append({"id": upi, "label": upi, "type": "upi"})
            edges.append({"source": sid, "target": upi})

        for link in entities["links"]:
            nodes.append({"id": link, "label": link, "type": "link"})
            edges.append({"source": sid, "target": link})

    return {
        "nodes": nodes,
        "edges": edges
    }
