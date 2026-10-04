"""Independent outcome calculation, not callable by actors or public controllers."""
def grade(snapshot,horizon):
    services=snapshot['services'];directory=snapshot['directory'];faults={}
    aggregate=sum(s['pool'] for s in services.values())
    for name,s in services.items():
        failures=[];expected=directory[s['alias']]
        if s['endpoint']!=expected['endpoint']:failures.append('endpoint')
        if s['protocol']!=expected['protocol']:failures.append('protocol')
        if s['pool']<s['minimum_pool']:failures.append('capacity_minimum')
        if aggregate>snapshot['capacity']:failures.append('shared_capacity')
        faults[name]=failures
    # Compute transitive reachability independently of World.health.
    for name in services:
        frontier=list(services[name]['depends_on']);visited={name}
        while frontier:
            other=frontier.pop()
            if other in visited:
                if other==name:faults[name].append('dependency_cycle')
                continue
            visited.add(other)
            if faults[other]:faults[name].append('dependency')
            frontier.extend(services[other]['depends_on'])
    good=sum(not v for v in faults.values());complete=snapshot['tick']==horizon
    return {'success':complete and good==len(services) and not snapshot['unsafe_commits'],'quality':good/len(services),
            'faults':faults,'monitoring_complete':complete,'unsafe_commits':len(snapshot['unsafe_commits'])}
