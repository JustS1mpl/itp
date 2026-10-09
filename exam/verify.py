import json,itertools,re,heapq
d=json.load(open('exam/task01.json',encoding='utf-8'))
def bijs(g):
    V=g['vertices'];n=len(V);T=g['table']
    adj={(a,b) for a,b in g['edges']}|{(b,a) for a,b in g['edges']}
    deg=[sum(1 for x in r if x) for r in T]
    dv={v:sum(1 for e in adj if e[0]==v) for v in V}
    res=[]
    # backtracking
    order=V
    def rec(i,m,used):
        if i==n: res.append(dict(m));return
        v=order[i]
        for k in range(n):
            if k in used or deg[k]!=dv[v]: continue
            ok=True
            for u in order[:i]:
                if ((u,v) in adj)!=(T[m[u]][k] is not None): ok=False;break
            if ok:
                m[v]=k;used.add(k);rec(i+1,m,used);used.discard(k);del m[v]
    rec(0,{},set())
    return res
bad=0
for t in d['types']:
    for e in t['examples']+t['tasks']:
        g=e['graph'];s=e['statement'];c=t['type_code'];a=e['answer']
        V=g['vertices'];T=g['table']
        if c=='1.6':
            m=re.search(r'из пункта (\S) в пункт (\S):',s);x,y=m.group(1),m.group(2)
            dist={v:1e9 for v in V};dist[x]=0;h=[(0,x)]
            while h:
                dd,u=heapq.heappop(h)
                if dd>dist[u]:continue
                for j,w in enumerate(T[V.index(u)]):
                    if w and dd+w<dist[V[j]]: dist[V[j]]=dd+w;heapq.heappush(h,(dist[V[j]],V[j]))
            ok=str(dist[y])==a;print(e['id'],ok,dist[y],a);bad+=not ok;continue
        B=bijs(g)
        if c=='1.1':
            m=re.search(r'пунктам (\S) и (\S) на',s);x,y=m.group(1),m.group(2)
            ans={''.join(sorted([str(b[x]+1),str(b[y]+1)])) for b in B}
        elif c=='1.2':
            ans={''.join(sorted(b,key=lambda v:b[v])) for b in B}
        elif c=='1.3':
            m=re.search(r'из пункта (\S) в пункт (\S)\.',s);x,y=m.group(1),m.group(2)
            ans={str(T[b[x]][b[y]]) for b in B}
        elif c=='1.4':
            ms=re.findall(r'из пункта (\S) в пункт (\S)',s)
            ans={str(sum(T[b[p]][b[q]] for p,q in ms)) for b in B}
        elif c=='1.5':
            m=re.search(r'дорога (\S)(\S) длиннее дороги (\S)(\S)\. Определите длину дороги (\S)(\S)\.',s);p,q,r,u,x,y=m.groups()
            ans={str(T[b[x]][b[y]]) for b in B if T[b[p]][b[q]] and T[b[r]][b[u]] and T[b[p]][b[q]]>T[b[r]][b[u]]}
        ok=(ans=={a});print(e['id'],ok,len(B),ans,a);bad+=not ok
print('bad',bad)
