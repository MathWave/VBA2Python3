def GetIntGraph(graph, cons):
    intgraph = {}
    for i in graph.keys():
        ii = cons[i]
        intgraph[ii] = []
        for j in graph[i]:
            intgraph[ii].append(cons[j])
    return intgraph


def FindNodeWayZ3(graph):
    cons = Coding(graph)
    intgraph = graph
    for i in range(len(graph.keys()), 1000):
        s = Solver()
        X = [Int('x%s' % i) for i in range(i)]
        cond1 = [Or([X[j] == i for j in range(len(X))]) for i in intgraph.keys()]
        cond2 = []
        #'''
        threads = []
        for j in range(len(X) - 1):
            threads.append(CalcNodeFirst(j, X, intgraph))
        for thread in threads:
            thread.start()
        while True:
            stop = False
            for i in threads:
                stop += i.is_alive()
            if not stop:
                break
        for j in threads:
            cond2 += j.condition
        #'''
        '''
        cond2 = [Or([And(X[i] == j, X[i + 1] == k)
                     for j in intgraph.keys() for k in intgraph[j]]) for i in range(len(X) - 1)]
        '''                                                                                                             #print("condition 2 ready for " + str(i) + " position")
        cond3 = [X[0] == 0]
        s.add(cond1 + cond2 + cond3)
        #print("for " + str(i) + " checked")
        if s.check() == sat:
            #print('\n\nway:\n')
            m = s.model()
            model_str = str(s.model()).split(',\n ')
            model_str[0] = model_str[0][1:len(model_str[0])]
            model_str[-1] = model_str[-1][0:len(model_str[-1])-1]
            row = {}
            for i in range(len(model_str)):
                #print(model_str[i])
                new_arr = model_str[i].split(' ')
                row[int(new_arr[0][1::])] = int(new_arr[2])
            new_row = []
            back_cons = {}
            for i in cons.keys():
                back_cons[cons[i]] = i
            for i in range(len(row)):
                new_row.append(back_cons[row[i]])
            return new_row


def FindConnectionWayZ3(graph):
    allconnections = []
    cons = Coding(graph)
    intgraph = GetIntGraph(graph, cons)
    for i in intgraph.keys():
        for j in intgraph[i]:
            allconnections.append([i, j])
    for i in range(len(graph.keys()), 10):
        s = Solver()
        X = [Int('x%s' % j) for j in range(i)]
        cond1 = [X[0] == 0]
        cond2 = []
        threads = []
        for j in allconnections:
            threads.append(CalcEilerFirst(j, X, intgraph))
        for thread in threads:
            thread.start()
        while True:
            stop = False
            for t in threads:
                stop += t.is_alive()
            if not stop:
                break
        for j in threads:
            cond2 += j.condition
        print("thread for " + str(i) + " created")
        s.add(cond1 + cond2)
        if s.check() == sat:
            # print('\n\nway:\n')
            m = s.model()
            model_str = str(s.model()).split(',\n ')
            model_str[0] = model_str[0][1:len(model_str[0])]
            model_str[-1] = model_str[-1][0:len(model_str[-1]) - 1]
            row = {}
            for i in range(len(model_str)):
                # print(model_str[i])
                new_arr = model_str[i].split(' ')
                row[int(new_arr[0][1::])] = int(new_arr[2])
            new_row = []
            back_cons = {}
            for i in cons.keys():
                back_cons[cons[i]] = i
            for i in range(len(row)):
                new_row.append(back_cons[row[i]])
            return new_row


def GetInstruction(way):
    stop = False
    stop_position = 10000

    while not stop:
        current = GetStartPosition()  # текущее положение в ячейках
        answer = []
        for i in range(1, len(way)):
            count = 0
            while True:  # генерируем тестовый комплект
                data = []
                for j in more_info:
                    data.append(choice(j))
                if IsPossible(*current, *data):
                    nextcurrent = NextCurrent(current, data)
                    if GetHyperState(*nextcurrent) == way[i]:
                        answer.append(data)
                        current = nextcurrent
                        if len(way) == len(answer) + 1:
                            stop = True
                        break
                else:
                    count += 1
                if count == stop_position:
                    break
            if count == stop_position:
                break
    return answer


def FindConnectionWay(graph):
    arr = GetStartPosition()
    all_connections = []
    for key in graph.keys():
        for node in graph[key]:
            all_connections.append([key, node])
    q = Queue()
    q.put([GetHyperState(*arr)])
    last_in_queue = []
    while not q.empty():
        last_in_queue = q.get()
        last_top = last_in_queue[-1]
        current_cons = GetCurrentConnection(last_in_queue)
        for top in graph.keys():
            last_combo = last_in_queue.copy()
            if top in graph[last_top] and [last_in_queue[-1], top] not in current_cons:
                last_combo.append(top)
                q.put(last_combo)
                length = q.qsize()
                if length % 100000 == 0:
                    print("queue length: " + str(length))
    if len(GetCurrentConnection(last_in_queue)) == len(all_connections):
        return last_in_queue
    else:
        q = Queue()
        q.put(last_in_queue)
        while True:
            last_in_queue = q.get()
            last_top = last_in_queue[-1]
            for top in graph.keys():
                last_combo = last_in_queue.copy()
                if top in graph[last_top]:
                    last_combo.append(top)
                    q.put(last_combo)
            if set(GetCurrentConnection(last_in_queue)) == len(all_connections):
                return last_in_queue
    #return all_connections


def Coding(graph):
    cons = {}
    arr = list(graph.keys())
    for i in range(len(arr)):
        cons[arr[i]] = i
    return cons


def GetCurrentConnection(way):
    cons = []
    for i in range(len(way) - 1):
        cons.append([way[i], way[i + 1]])
    return cons


def FindNodeWay(graph):
    arr = GetStartPosition()
    q = Queue()
    q.put([GetHyperState(*arr)])
    last_in_queue = []
    while not q.empty():
        last_in_queue = q.get()
        last_top = last_in_queue[-1]
        for top in graph.keys():
            last_combo = last_in_queue.copy()
            if top in graph[last_top] and top not in last_in_queue:
                last_combo.append(top)
                q.put(last_combo)
                length = q.qsize()
                if length % 100000 == 0:
                    print("queue length: " + str(length))
    if len(last_in_queue) == len(list(graph.keys())):
        return last_in_queue
    else:
        q = Queue()
        q.put(last_in_queue)
        while True:
            last_in_queue = q.get()
            last_top = last_in_queue[-1]
            for top in graph.keys():
                last_combo = last_in_queue.copy()
                if top in graph[last_top]:
                    last_combo.append(top)
                    q.put(last_combo)
            if set(last_in_queue) == set(graph.keys()):
                return last_in_queue


def updateGraph(graph):
    arr = GetParamsArray(info)
    q = Queue()
    all_nodes = set(graph.keys())
    for i in graph.keys():
        q.put(i)
    s = Solver()
    current = arr[0:info[0]]
    add = arr[info[0] * 2:]
    find = String('find')
    s.add(z3_funcs.IsPossible(*current, *add))
    s.add(z3_funcs.GetHyperState(*z3_funcs.NextCurrent(current, add)) == find)
    while not q.empty():
        s.push()
        node = q.queue[0]
        s.add([find != StringVal(name) for name in graph[node]])
        s.add(z3_funcs.GetHyperState(*current) == StringVal(node))
        if s.check() == sat:
            m = s.model()
            newval = getValue(m, 'find')
            if newval not in all_nodes:
                graph[newval] = set()
                all_nodes.add(newval)
                print("Now there are " + str(len(all_nodes)) + " nodes")
            graph[node].add(newval)
            q.put(newval)
        else:
            print("All nodes connected with " + node + " found")
            q.get()
        s.pop()
    return graph