# Move Over Dijkstra The New Algorithm That Just Rewrote 70 Years of Computer Science by The Latency Gambler Aug 2025 Medium

# 다익스트라는 물러가라: 70년 컴퓨터 과학을 다시 쓴 새로운 알고리즘 by The Latency Gambler 2025년 8월 Medium

[

![The Latency Gambler](https://miro.medium.com/v2/resize:fill:48:48/1*wMFzQ6KVGegm1kaMnFxANw.jpeg)



](https://medium.com/@kanishks772?source=post_page---byline--d670696c440d---------------------------------------)

For nearly seven decades, Dijkstra's algorithm has reigned supreme as the gold standard for finding shortest paths in graphs. Born from a 20-minute mental exercise at an Amsterdam café in 1956, Edsger Dijkstra's creation has been the backbone of everything from GPS navigation to network routing protocols. But that reign just ended.

거의 70년 동안, 다익스트라 알고리즘은 그래프에서 최단 경로를 찾는 최고 표준으로 군림해왔다. 1956년 암스테르담의 한 카페에서 20분간의 사고 실험으로 탄생한 에드거 다익스트라(Edsger Dijkstra)의 창작물은 GPS 네비게이션부터 네트워크 라우팅 프로토콜에 이르기까지 모든 것의 핵심이었다. 하지만 그 통치는 이제 끝났다.

Press enter or click to view image in full size

다음을 눌러 전체 크기로 이미지 보기

![](https://miro.medium.com/v2/resize:fit:1050/0*spGg1nvSbEgbei8h)

A research team led by Ran Duan at Tsinghua University has achieved what many considered impossible: they've broken the fundamental "sorting barrier" that has limited shortest-path algorithms for 40 years. Their new deterministic O(m log^(2/3) n)-time algorithm for single-source shortest paths represents a breakthrough that challenges textbook assumptions about algorithmic limits.

칭화대학교의 란 두안(Ran Duan)이 이끄는 연구팀이 많은 이들이 불가능하다고 여겨온 일을 해냈다: 40년간 최단 경로 알고리즘을 제한해온 근본적인 "정렬 장벽(sorting barrier)"을 깨뜨린 것이다. 단일 출발점 최단 경로에 대한 그들의 새로운 결정론적 O(m log^(2/3) n) 시간 알고리즘은 알고리즘 한계에 대한 교과서적 가정에 도전하는 돌파구를 의미한다.

### The Foundation That Held for 70 Years

### 70년간 지속된 기반

Dijkstra's algorithm works by maintaining a sorted priority queue of vertices, always selecting the closest unvisited vertex next. This greedy approach guarantees optimality because it processes vertices in order of their distance from the source.

다익스트라 알고리즘은 정점들의 정렬된 우선순위 큐를 유지하면서, 항상 다음으로 가장 가까운 미방문 정점을 선택하는 방식으로 작동한다. 이런 탐욕적 접근법은 출발점으로부터의 거리 순서로 정점들을 처리하기 때문에 최적성을 보장한다.

```
<span id="6984" data-selectable-paragraph="">def dijkstra(graph, <span>source</span>):<br>    distances = {vertex: <span>float</span>(<span>'infinity'</span>) <span>for</span> vertex <span>in</span> graph}<br>    distances[<span>source</span>] = 0<br>    priority_queue = [(0, <span>source</span>)]<br>    visited = <span>set</span>()<br>    <br>    <span>while</span> priority_queue:<br>        current_distance, current_vertex = heappop(priority_queue)<br>        <br>        <span>if</span> current_vertex <span>in</span> visited:<br>            <span>continue</span><br>            <br>        visited.add(current_vertex)<br>        <br>        <span>for</span> neighbor, weight <span>in</span> graph[current_vertex].items():<br>            distance = current_distance + weight<br>            <br>            <span>if</span> distance &lt; distances[neighbor]:<br>                distances[neighbor] = distance<br>                heappush(priority_queue, (distance, neighbor))<br>    <br>    <span>return</span> distances</span>
```

The algorithm's time complexity is O((V + E) log V) using a binary heap, or O(V log V + E) with a Fibonacci heap. This performance has been considered optimal under the sorting barrier — the theoretical limit imposed by the need to maintain sorted order.

이 알고리즘의 시간 복잡도는 이진 힙을 사용할 때 O((V + E) log V)이거나, 피보나치 힙을 사용할 때 O(V log V + E)이다. 이 성능은 정렬 장벽 하에서 최적으로 여겨져 왔다 — 정렬된 순서를 유지해야 할 필요성에 의해 부과된 이론적 한계이다.

```
<span id="bbc5" data-selectable-paragraph=""><span>Graph</span> <span>Traversal</span> <span>Pattern</span> (Dijkstra):<br><br><span>Source</span> → <span>[1]</span> → <span>[2,3]</span> → <span>[4,5,6]</span> → <span>[7,8,9,10]</span><br>         ↓      ↓       ↓          ↓<br>      <span>Always</span>   <span>Sort</span>    <span>Sort</span>       <span>Sort</span><br>      <span>closest</span>  <span>by</span>      <span>by</span>         <span>by</span>  <br>               <span>dist</span>    <span>dist</span>       <span>dist</span><br><span>Sorting</span> <span>Barrier</span>: <span>O</span>(m log n) <span>lower</span> <span>bound</span></span>
```

```
<span id="bbc5" data-selectable-paragraph="">그래프 순회 패턴 (다익스트라):<br><br>출발점 → [1] → [2,3] → [4,5,6] → [7,8,9,10]<br>         ↓      ↓       ↓          ↓<br>      항상     정렬    정렬       정렬<br>      가장     거리    거리       거리  <br>      가까운   순으로  순으로     순으로<br>정렬 장벽: O(m log n) 하한</span>
```

### The Sorting Barrier Explained

### 정렬 장벽 설명

The sorting barrier emerged from a fundamental insight: any algorithm that processes vertices in order of increasing distance from the source cannot run faster than the time it takes to sort. Since comparison-based sorting has an Ω(n log n) lower bound, shortest-path algorithms seemed fundamentally limited to O(m log n) time.

정렬 장벽은 근본적인 통찰에서 나타났다: 출발점으로부터의 거리가 증가하는 순서로 정점을 처리하는 모든 알고리즘은 정렬하는 데 걸리는 시간보다 빠르게 실행될 수 없다는 것이다. 비교 기반 정렬이 Ω(n log n) 하한을 가지므로, 최단 경로 알고리즘은 근본적으로 O(m log n) 시간으로 제한되는 것처럼 보였다.

This barrier held firm for decades. Even when researchers like Thorup developed faster algorithms in the late 1990s, they required special assumptions about edge weights or worked only on specific graph types.

이 장벽은 수십 년 동안 굳건히 유지되었다. 토룹(Thorup) 같은 연구자들이 1990년대 후반에 더 빠른 알고리즘을 개발했을 때도, 그것들은 간선 가중치에 대한 특별한 가정을 필요로 하거나 특정 그래프 유형에서만 작동했다.

### Breaking the Unbreakable

### 깨뜨릴 수 없는 것을 깨뜨리기

Duan's breakthrough came from a counterintuitive realization: what if we don't sort at all?

두안의 돌파구는 직관에 반하는 깨달음에서 나왔다: 아예 정렬하지 않으면 어떨까?

The new algorithm abandons Dijkstra's sorted approach entirely. Instead of always choosing the closest vertex, it uses a sophisticated clustering technique combined with selective applications of the slower Bellman-Ford algorithm to identify "influential nodes" vertices that lie on many shortest paths.

새로운 알고리즘은 다익스트라의 정렬된 접근법을 완전히 포기한다. 항상 가장 가까운 정점을 선택하는 대신, 많은 최단 경로 상에 위치하는 "영향력 있는 노드" 정점들을 식별하기 위해 정교한 클러스터링 기법과 더 느린 벨만-포드 알고리즘의 선택적 적용을 결합해서 사용한다.

```
<span id="677a" data-selectable-paragraph="">def new_shortest_path(graph, <span>source</span>):<br>    <br>    layers = partition_into_layers(graph, <span>source</span>)<br>    distances = {<span>source</span>: 0}<br>    <br>    <span>for</span> layer <span>in</span> layers:<br>        <br>        influential = find_influential_nodes(layer, distances)<br>        <br>        <br>        <span>for</span> node <span>in</span> influential:<br>            relax_from_node(node, distances)<br>        <br>        <br>        process_remaining_cluster(layer, distances)<br>    <br>    <span>return</span> distances</span>
```

> The key insight is that by clustering nearby vertices and processing representatives from each cluster, the algorithm can avoid the expensive sorting operations that limit traditional approaches.

> 핵심 통찰은 인근 정점들을 클러스터링하고 각 클러스터에서 대표를 처리함으로써, 기존 접근법을 제한하는 비싼 정렬 연산을 피할 수 있다는 것이다.

```
<span id="166c" data-selectable-paragraph=""><span>New</span> Algorithm <span>Pattern</span>:<br><br>Source → Cluster[<span>1</span>,<span>2</span>,<span>3</span>] → Cluster[<span>4</span>,<span>5</span>,<span>6</span>,<span>7</span>] → Cluster[<span>8</span>,<span>9</span>,<span>10</span>,<span>11</span>]<br>         ↓                ↓                  ↓<br>      Influential       Influential        Influential<br>      nodes <span>first</span>       nodes <span>first</span>        nodes <span>first</span><br>      (<span>no</span> sorting)      (<span>no</span> sorting)       (<span>no</span> sorting)<br><span>No</span> Sorting Barrier: O(m log<span>^</span>(<span>2</span><span>/</span><span>3</span>) n) achievable</span>
```

```
<span id="166c" data-selectable-paragraph="">새 알고리즘 패턴:<br><br>출발점 → 클러스터[1,2,3] → 클러스터[4,5,6,7] → 클러스터[8,9,10,11]<br>         ↓                ↓                  ↓<br>      영향력 있는       영향력 있는        영향력 있는<br>      노드 우선        노드 우선          노드 우선<br>      (정렬 없음)       (정렬 없음)        (정렬 없음)<br>정렬 장벽 없음: O(m log^(2/3) n) 달성 가능</span>
```

### The Technical Breakthrough

### 기술적 돌파구

The algorithm achieves its performance through several innovations:

이 알고리즘은 여러 혁신을 통해 성능을 달성한다:

**Layer Decomposition**: The graph is partitioned into layers based on distance from the source, similar to Dijkstra, but without maintaining strict sorting within layers.

**계층 분해(Layer Decomposition)**: 그래프가 출발점으로부터의 거리를 기반으로 계층으로 분할되는데, 다익스트라와 유사하지만 계층 내에서 엄격한 정렬을 유지하지 않는다.

**Influential Node Detection**: Using limited Bellman-Ford iterations, the algorithm identifies vertices that appear on many shortest paths , these are processed first to maximize information propagation.

**영향력 있는 노드 감지(Influential Node Detection)**: 제한된 벨만-포드 반복을 사용하여, 많은 최단 경로에 나타나는 정점들을 식별하고, 정보 전파를 최대화하기 위해 이들을 먼저 처리한다.

**Cluster Processing**: Instead of examining every frontier vertex individually, the algorithm groups them into clusters and processes representatives, reducing the computational overhead.

**클러스터 처리(Cluster Processing)**: 모든 경계 정점을 개별적으로 검사하는 대신, 알고리즘은 이들을 클러스터로 그룹화하고 대표를 처리하여 계산 오버헤드를 줄인다.

**Deterministic Design**: Unlike earlier attempts that relied on randomization, this algorithm provides guaranteed performance bounds.

**결정론적 설계(Deterministic Design)**: 무작위화에 의존했던 이전 시도들과 달리, 이 알고리즘은 보장된 성능 한계를 제공한다.

### Performance Analysis

### 성능 분석

The theoretical improvement is significant but comes with important caveats:

이론적 개선은 상당하지만 중요한 주의사항이 있다:

**Time Complexity**: O(m log^(2/3) n) vs Dijkstra's O(m log n)  
**Space Complexity**: Higher memory requirements due to auxiliary data structures  
**Practical Performance**: The algorithm is considerably more intricate, relying on many pieces that need to fit together just right

**시간 복잡도**: O(m log^(2/3) n) 대 다익스트라의 O(m log n)  
**공간 복잡도**: 보조 데이터 구조로 인한 더 높은 메모리 요구사항  
**실제 성능**: 알고리즘이 상당히 복잡하며, 정확히 맞아떨어져야 하는 많은 구성요소에 의존한다

For sparse graphs where m = o(n log n), the improvement becomes more pronounced:

m = o(n log n)인 희소 그래프에서는 개선이 더욱 두드러진다:

```
<span id="310b" data-selectable-paragraph="">Graph <span>Size</span> <span>(n)</span>    Dijkstra    New Algorithm    Speedup<br><span>1</span>,<span>000</span>             <span>13</span>,<span>816</span>      <span>8</span>,<span>660</span>            <span>1.</span>6x<br><span>10</span>,<span>000</span>            <span>151</span>,<span>294</span>     <span>75</span>,<span>858</span>           <span>2.</span>0x  <br><span>100</span>,<span>000</span>           <span>1</span>,<span>660</span>,<span>964</span>   <span>676</span>,<span>694</span>          <span>2.</span>5x<br><span>1</span>,<span>000</span>,<span>000</span>         <span>18</span>,<span>420</span>,<span>699</span>  <span>6</span>,095,<span>885</span>        <span>3.</span>0x</span>
```

```
<span id="310b" data-selectable-paragraph="">그래프 크기(n)    다익스트라    새 알고리즘      속도향상<br>1,000             13,816      8,660            1.6x<br>10,000            151,294     75,858           2.0x  <br>100,000           1,660,964   676,694          2.5x<br>1,000,000         18,420,699  6,095,885        3.0x</span>
```

### Real-World Implications

### 실제 적용 의미

This breakthrough has immediate applications across multiple domains:

이 돌파구는 여러 분야에 즉각적인 적용이 가능하다:

**Network Routing**: Internet backbone routers can compute paths more efficiently, reducing latency in data transmission.

**네트워크 라우팅**: 인터넷 백본 라우터가 경로를 더 효율적으로 계산하여 데이터 전송 지연을 줄일 수 있다.

**GPS Navigation**: Map applications can process route queries faster, especially in dense urban networks with millions of road segments.

**GPS 네비게이션**: 지도 애플리케이션이 특히 수백만 개의 도로 구간을 가진 밀집된 도시 네트워크에서 경로 쿼리를 더 빠르게 처리할 수 있다.

**Social Networks**: Platforms can compute influence propagation and shortest connection paths more efficiently across billion-user graphs.

**소셜 네트워크**: 플랫폼이 수십억 사용자 그래프에서 영향력 전파와 최단 연결 경로를 더 효율적으로 계산할 수 있다.

**Supply Chain Optimization**: Logistics companies can optimize delivery routes across complex distribution networks with improved computational efficiency.

**공급망 최적화**: 물류 회사들이 복잡한 유통 네트워크에서 개선된 계산 효율성으로 배송 경로를 최적화할 수 있다.

### The Broader Impact

### 더 넓은 영향

This breakthrough represents more than just a faster algorithm , it challenges fundamental assumptions about computational limits that have stood for decades. The sorting barrier was considered so fundamental that many researchers had stopped pursuing improvements in this direction.

이 돌파구는 단순히 더 빠른 알고리즘 이상을 의미한다 — 수십 년 동안 유지되어온 계산 한계에 대한 근본적 가정에 도전한다. 정렬 장벽은 너무 근본적인 것으로 여겨져서 많은 연구자들이 이 방향에서의 개선 추구를 중단했었다.

The success of this approach suggests other "impossible" barriers in computer science might also be conquerable. It demonstrates the value of questioning long-held assumptions and exploring seemingly unpromising directions.

이 접근법의 성공은 컴퓨터 과학의 다른 "불가능한" 장벽들도 정복할 수 있음을 시사한다. 이는 오래된 가정에 의문을 제기하고 겉보기에 희망 없어 보이는 방향을 탐구하는 가치를 보여준다.

### Implementation Challenges

### 구현 도전과제

Despite its theoretical elegance, the new algorithm faces practical hurdles:

이론적 우아함에도 불구하고, 새 알고리즘은 실제적 장애물에 직면한다:

**Complexity**: The implementation is significantly more complex than Dijkstra's straightforward approach, making it harder to debug and maintain.

**복잡성**: 구현이 다익스트라의 직관적 접근법보다 상당히 복잡하여 디버그와 유지보수가 더 어렵다.

**Memory Usage**: The auxiliary data structures required for clustering and influential node detection increase memory consumption substantially.

**메모리 사용량**: 클러스터링과 영향력 있는 노드 감지에 필요한 보조 데이터 구조가 메모리 소비를 상당히 증가시킨다.

**Constants**: The hidden constants in the O(m log^(2/3) n) bound may be large, potentially limiting practical benefits on smaller graphs.

**상수**: O(m log^(2/3) n) 한계의 숨겨진 상수가 클 수 있어, 작은 그래프에서의 실용적 이익을 제한할 가능성이 있다.

**Robustness**: The algorithm's many interconnected components may be more sensitive to edge cases and numerical precision issues.

**견고성**: 알고리즘의 많은 상호연결된 구성요소들이 엣지 케이스와 수치 정밀도 문제에 더 민감할 수 있다.

### Looking Forward

### 앞으로의 전망

With the sorting barrier vanquished, the new algorithm's runtime isn't close to any fundamental limit that computer scientists know of. This opens the door to further improvements and raises intriguing questions about the ultimate limits of shortest-path computation.

정렬 장벽이 무너진 상황에서, 새 알고리즘의 실행 시간은 컴퓨터 과학자들이 알고 있는 어떤 근본적 한계에도 가깝지 않다. 이는 추가 개선의 문을 열고 최단 경로 계산의 궁극적 한계에 대한 흥미로운 질문을 제기한다.

The research team is already exploring optimizations to reduce the algorithm's complexity and improve its practical performance. Other researchers are investigating whether similar techniques can break barriers in related problems.

연구팀은 이미 알고리즘의 복잡성을 줄이고 실용적 성능을 개선하는 최적화를 탐구하고 있다. 다른 연구자들은 유사한 기법이 관련 문제들의 장벽을 깰 수 있는지 조사하고 있다.

This breakthrough serves as a reminder that in computer science, even the most established foundations can be overturned by creative thinking and persistent effort. After 70 years, Dijkstra's algorithm finally has serious competition and the race for even faster shortest-path algorithms has just begun.

이 돌파구는 컴퓨터 과학에서 가장 확립된 기반조차도 창의적 사고와 끈질긴 노력으로 뒤집힐 수 있음을 상기시켜준다. 70년 만에, 다익스트라 알고리즘이 마침내 진지한 경쟁자를 갖게 되었고 더욱 빠른 최단 경로 알고리즘을 위한 경쟁이 이제 시작되었다.

> The story of this discovery reinforces a crucial lesson: in science, the most transformative breakthroughs often come from questioning what everyone assumes to be impossible. Sometimes, the path forward requires abandoning the very principles that brought us this far.

> 이 발견의 이야기는 중요한 교훈을 강화한다: 과학에서 가장 혁신적인 돌파구는 종종 모든 사람이 불가능하다고 가정하는 것에 의문을 제기하는 것에서 나온다. 때로는 앞으로 나아가는 길은 우리를 여기까지 이끌어온 바로 그 원칙들을 포기하는 것을 요구한다.

_The research paper "Breaking the Sorting Barrier for Directed Single-Source Shortest Paths" by Ran Duan, Xiao Mao, Hanlin Ren, and Zihan Tan represents a collaboration between Tsinghua University and Stanford University, demonstrating the power of international academic cooperation in pushing the boundaries of theoretical computer science._

_란 두안, 샤오 마오, 한린 렌, 지한 탄의 연구 논문 "방향 그래프에서 단일 출발점 최단 경로의 정렬 장벽 깨뜨리기"는 칭화대학교와 스탠포드 대학교 간의 협력을 나타내며, 이론 컴퓨터 과학의 경계를 밀어내는 데 있어 국제 학술 협력의 힘을 보여준다._
# Move Over Dijkstra The New Algorithm That Just Rewrote 70 Years of Computer Science by The Latency Gambler Aug 2025 Medium

# 다익스트라는 물러가라: 70년 컴퓨터 과학을 다시 쓴 새로운 알고리즘 by The Latency Gambler 2025년 8월 Medium

[

![The Latency Gambler](https://miro.medium.com/v2/resize:fill:48:48/1*wMFzQ6KVGegm1kaMnFxANw.jpeg)



](https://medium.com/@kanishks772?source=post_page---byline--d670696c440d---------------------------------------)

For nearly seven decades, Dijkstra's algorithm has reigned supreme as the gold standard for finding shortest paths in graphs. Born from a 20-minute mental exercise at an Amsterdam café in 1956, Edsger Dijkstra's creation has been the backbone of everything from GPS navigation to network routing protocols. But that reign just ended.

거의 70년 동안, 다익스트라 알고리즘은 그래프에서 최단 경로를 찾는 최고 표준으로 군림해왔다. 1956년 암스테르담의 한 카페에서 20분간의 사고 실험으로 탄생한 에드거 다익스트라(Edsger Dijkstra)의 창작물은 GPS 네비게이션부터 네트워크 라우팅 프로토콜에 이르기까지 모든 것의 핵심이었다. 하지만 그 통치는 이제 끝났다.

Press enter or click to view image in full size

다음을 눌러 전체 크기로 이미지 보기

![](https://miro.medium.com/v2/resize:fit:1050/0*spGg1nvSbEgbei8h)

A research team led by Ran Duan at Tsinghua University has achieved what many considered impossible: they've broken the fundamental "sorting barrier" that has limited shortest-path algorithms for 40 years. Their new deterministic O(m log^(2/3) n)-time algorithm for single-source shortest paths represents a breakthrough that challenges textbook assumptions about algorithmic limits.

칭화대학교의 란 두안(Ran Duan)이 이끄는 연구팀이 많은 이들이 불가능하다고 여겨온 일을 해냈다: 40년간 최단 경로 알고리즘을 제한해온 근본적인 "정렬 장벽(sorting barrier)"을 깨뜨린 것이다. 단일 출발점 최단 경로에 대한 그들의 새로운 결정론적 O(m log^(2/3) n) 시간 알고리즘은 알고리즘 한계에 대한 교과서적 가정에 도전하는 돌파구를 의미한다.

### The Foundation That Held for 70 Years

### 70년간 지속된 기반

Dijkstra's algorithm works by maintaining a sorted priority queue of vertices, always selecting the closest unvisited vertex next. This greedy approach guarantees optimality because it processes vertices in order of their distance from the source.

다익스트라 알고리즘은 정점들의 정렬된 우선순위 큐를 유지하면서, 항상 다음으로 가장 가까운 미방문 정점을 선택하는 방식으로 작동한다. 이런 탐욕적 접근법은 출발점으로부터의 거리 순서로 정점들을 처리하기 때문에 최적성을 보장한다.

```
<span id="6984" data-selectable-paragraph="">def dijkstra(graph, <span>source</span>):<br>    distances = {vertex: <span>float</span>(<span>'infinity'</span>) <span>for</span> vertex <span>in</span> graph}<br>    distances[<span>source</span>] = 0<br>    priority_queue = [(0, <span>source</span>)]<br>    visited = <span>set</span>()<br>    <br>    <span>while</span> priority_queue:<br>        current_distance, current_vertex = heappop(priority_queue)<br>        <br>        <span>if</span> current_vertex <span>in</span> visited:<br>            <span>continue</span><br>            <br>        visited.add(current_vertex)<br>        <br>        <span>for</span> neighbor, weight <span>in</span> graph[current_vertex].items():<br>            distance = current_distance + weight<br>            <br>            <span>if</span> distance &lt; distances[neighbor]:<br>                distances[neighbor] = distance<br>                heappush(priority_queue, (distance, neighbor))<br>    <br>    <span>return</span> distances</span>
```

The algorithm's time complexity is O((V + E) log V) using a binary heap, or O(V log V + E) with a Fibonacci heap. This performance has been considered optimal under the sorting barrier — the theoretical limit imposed by the need to maintain sorted order.

이 알고리즘의 시간 복잡도는 이진 힙을 사용할 때 O((V + E) log V)이거나, 피보나치 힙을 사용할 때 O(V log V + E)이다. 이 성능은 정렬 장벽 하에서 최적으로 여겨져 왔다 — 정렬된 순서를 유지해야 할 필요성에 의해 부과된 이론적 한계이다.

```
<span id="bbc5" data-selectable-paragraph=""><span>Graph</span> <span>Traversal</span> <span>Pattern</span> (Dijkstra):<br><br><span>Source</span> → <span>[1]</span> → <span>[2,3]</span> → <span>[4,5,6]</span> → <span>[7,8,9,10]</span><br>         ↓      ↓       ↓          ↓<br>      <span>Always</span>   <span>Sort</span>    <span>Sort</span>       <span>Sort</span><br>      <span>closest</span>  <span>by</span>      <span>by</span>         <span>by</span>  <br>               <span>dist</span>    <span>dist</span>       <span>dist</span><br><span>Sorting</span> <span>Barrier</span>: <span>O</span>(m log n) <span>lower</span> <span>bound</span></span>
```

```
<span id="bbc5" data-selectable-paragraph="">그래프 순회 패턴 (다익스트라):<br><br>출발점 → [1] → [2,3] → [4,5,6] → [7,8,9,10]<br>         ↓      ↓       ↓          ↓<br>      항상     정렬    정렬       정렬<br>      가장     거리    거리       거리  <br>      가까운   순으로  순으로     순으로<br>정렬 장벽: O(m log n) 하한</span>
```

### The Sorting Barrier Explained

### 정렬 장벽 설명

The sorting barrier emerged from a fundamental insight: any algorithm that processes vertices in order of increasing distance from the source cannot run faster than the time it takes to sort. Since comparison-based sorting has an Ω(n log n) lower bound, shortest-path algorithms seemed fundamentally limited to O(m log n) time.

정렬 장벽은 근본적인 통찰에서 나타났다: 출발점으로부터의 거리가 증가하는 순서로 정점을 처리하는 모든 알고리즘은 정렬하는 데 걸리는 시간보다 빠르게 실행될 수 없다는 것이다. 비교 기반 정렬이 Ω(n log n) 하한을 가지므로, 최단 경로 알고리즘은 근본적으로 O(m log n) 시간으로 제한되는 것처럼 보였다.

This barrier held firm for decades. Even when researchers like Thorup developed faster algorithms in the late 1990s, they required special assumptions about edge weights or worked only on specific graph types.

이 장벽은 수십 년 동안 굳건히 유지되었다. 토룹(Thorup) 같은 연구자들이 1990년대 후반에 더 빠른 알고리즘을 개발했을 때도, 그것들은 간선 가중치에 대한 특별한 가정을 필요로 하거나 특정 그래프 유형에서만 작동했다.

### Breaking the Unbreakable

### 깨뜨릴 수 없는 것을 깨뜨리기

Duan's breakthrough came from a counterintuitive realization: what if we don't sort at all?

두안의 돌파구는 직관에 반하는 깨달음에서 나왔다: 아예 정렬하지 않으면 어떨까?

The new algorithm abandons Dijkstra's sorted approach entirely. Instead of always choosing the closest vertex, it uses a sophisticated clustering technique combined with selective applications of the slower Bellman-Ford algorithm to identify "influential nodes" vertices that lie on many shortest paths.

새로운 알고리즘은 다익스트라의 정렬된 접근법을 완전히 포기한다. 항상 가장 가까운 정점을 선택하는 대신, 많은 최단 경로 상에 위치하는 "영향력 있는 노드" 정점들을 식별하기 위해 정교한 클러스터링 기법과 더 느린 벨만-포드 알고리즘의 선택적 적용을 결합해서 사용한다.

```
<span id="677a" data-selectable-paragraph="">def new_shortest_path(graph, <span>source</span>):<br>    <br>    layers = partition_into_layers(graph, <span>source</span>)<br>    distances = {<span>source</span>: 0}<br>    <br>    <span>for</span> layer <span>in</span> layers:<br>        <br>        influential = find_influential_nodes(layer, distances)<br>        <br>        <br>        <span>for</span> node <span>in</span> influential:<br>            relax_from_node(node, distances)<br>        <br>        <br>        process_remaining_cluster(layer, distances)<br>    <br>    <span>return</span> distances</span>
```

> The key insight is that by clustering nearby vertices and processing representatives from each cluster, the algorithm can avoid the expensive sorting operations that limit traditional approaches.

> 핵심 통찰은 인근 정점들을 클러스터링하고 각 클러스터에서 대표를 처리함으로써, 기존 접근법을 제한하는 비싼 정렬 연산을 피할 수 있다는 것이다.

```
<span id="166c" data-selectable-paragraph=""><span>New</span> Algorithm <span>Pattern</span>:<br><br>Source → Cluster[<span>1</span>,<span>2</span>,<span>3</span>] → Cluster[<span>4</span>,<span>5</span>,<span>6</span>,<span>7</span>] → Cluster[<span>8</span>,<span>9</span>,<span>10</span>,<span>11</span>]<br>         ↓                ↓                  ↓<br>      Influential       Influential        Influential<br>      nodes <span>first</span>       nodes <span>first</span>        nodes <span>first</span><br>      (<span>no</span> sorting)      (<span>no</span> sorting)       (<span>no</span> sorting)<br><span>No</span> Sorting Barrier: O(m log<span>^</span>(<span>2</span><span>/</span><span>3</span>) n) achievable</span>
```

```
<span id="166c" data-selectable-paragraph="">새 알고리즘 패턴:<br><br>출발점 → 클러스터[1,2,3] → 클러스터[4,5,6,7] → 클러스터[8,9,10,11]<br>         ↓                ↓                  ↓<br>      영향력 있는       영향력 있는        영향력 있는<br>      노드 우선        노드 우선          노드 우선<br>      (정렬 없음)       (정렬 없음)        (정렬 없음)<br>정렬 장벽 없음: O(m log^(2/3) n) 달성 가능</span>
```

### The Technical Breakthrough

### 기술적 돌파구

The algorithm achieves its performance through several innovations:

이 알고리즘은 여러 혁신을 통해 성능을 달성한다:

**Layer Decomposition**: The graph is partitioned into layers based on distance from the source, similar to Dijkstra, but without maintaining strict sorting within layers.

**계층 분해(Layer Decomposition)**: 그래프가 출발점으로부터의 거리를 기반으로 계층으로 분할되는데, 다익스트라와 유사하지만 계층 내에서 엄격한 정렬을 유지하지 않는다.

**Influential Node Detection**: Using limited Bellman-Ford iterations, the algorithm identifies vertices that appear on many shortest paths , these are processed first to maximize information propagation.

**영향력 있는 노드 감지(Influential Node Detection)**: 제한된 벨만-포드 반복을 사용하여, 많은 최단 경로에 나타나는 정점들을 식별하고, 정보 전파를 최대화하기 위해 이들을 먼저 처리한다.

**Cluster Processing**: Instead of examining every frontier vertex individually, the algorithm groups them into clusters and processes representatives, reducing the computational overhead.

**클러스터 처리(Cluster Processing)**: 모든 경계 정점을 개별적으로 검사하는 대신, 알고리즘은 이들을 클러스터로 그룹화하고 대표를 처리하여 계산 오버헤드를 줄인다.

**Deterministic Design**: Unlike earlier attempts that relied on randomization, this algorithm provides guaranteed performance bounds.

**결정론적 설계(Deterministic Design)**: 무작위화에 의존했던 이전 시도들과 달리, 이 알고리즘은 보장된 성능 한계를 제공한다.

### Performance Analysis

### 성능 분석

The theoretical improvement is significant but comes with important caveats:

이론적 개선은 상당하지만 중요한 주의사항이 있다:

**Time Complexity**: O(m log^(2/3) n) vs Dijkstra's O(m log n)  
**Space Complexity**: Higher memory requirements due to auxiliary data structures  
**Practical Performance**: The algorithm is considerably more intricate, relying on many pieces that need to fit together just right

**시간 복잡도**: O(m log^(2/3) n) 대 다익스트라의 O(m log n)  
**공간 복잡도**: 보조 데이터 구조로 인한 더 높은 메모리 요구사항  
**실제 성능**: 알고리즘이 상당히 복잡하며, 정확히 맞아떨어져야 하는 많은 구성요소에 의존한다

For sparse graphs where m = o(n log n), the improvement becomes more pronounced:

m = o(n log n)인 희소 그래프에서는 개선이 더욱 두드러진다:

```
<span id="310b" data-selectable-paragraph="">Graph <span>Size</span> <span>(n)</span>    Dijkstra    New Algorithm    Speedup<br><span>1</span>,<span>000</span>             <span>13</span>,<span>816</span>      <span>8</span>,<span>660</span>            <span>1.</span>6x<br><span>10</span>,<span>000</span>            <span>151</span>,<span>294</span>     <span>75</span>,<span>858</span>           <span>2.</span>0x  <br><span>100</span>,<span>000</span>           <span>1</span>,<span>660</span>,<span>964</span>   <span>676</span>,<span>694</span>          <span>2.</span>5x<br><span>1</span>,<span>000</span>,<span>000</span>         <span>18</span>,<span>420</span>,<span>699</span>  <span>6</span>,095,<span>885</span>        <span>3.</span>0x</span>
```

```
<span id="310b" data-selectable-paragraph="">그래프 크기(n)    다익스트라    새 알고리즘      속도향상<br>1,000             13,816      8,660            1.6x<br>10,000            151,294     75,858           2.0x  <br>100,000           1,660,964   676,694          2.5x<br>1,000,000         18,420,699  6,095,885        3.0x</span>
```

### Real-World Implications

### 실제 적용 의미

This breakthrough has immediate applications across multiple domains:

이 돌파구는 여러 분야에 즉각적인 적용이 가능하다:

**Network Routing**: Internet backbone routers can compute paths more efficiently, reducing latency in data transmission.

**네트워크 라우팅**: 인터넷 백본 라우터가 경로를 더 효율적으로 계산하여 데이터 전송 지연을 줄일 수 있다.

**GPS Navigation**: Map applications can process route queries faster, especially in dense urban networks with millions of road segments.

**GPS 네비게이션**: 지도 애플리케이션이 특히 수백만 개의 도로 구간을 가진 밀집된 도시 네트워크에서 경로 쿼리를 더 빠르게 처리할 수 있다.

**Social Networks**: Platforms can compute influence propagation and shortest connection paths more efficiently across billion-user graphs.

**소셜 네트워크**: 플랫폼이 수십억 사용자 그래프에서 영향력 전파와 최단 연결 경로를 더 효율적으로 계산할 수 있다.

**Supply Chain Optimization**: Logistics companies can optimize delivery routes across complex distribution networks with improved computational efficiency.

**공급망 최적화**: 물류 회사들이 복잡한 유통 네트워크에서 개선된 계산 효율성으로 배송 경로를 최적화할 수 있다.

### The Broader Impact

### 더 넓은 영향

This breakthrough represents more than just a faster algorithm , it challenges fundamental assumptions about computational limits that have stood for decades. The sorting barrier was considered so fundamental that many researchers had stopped pursuing improvements in this direction.

이 돌파구는 단순히 더 빠른 알고리즘 이상을 의미한다 — 수십 년 동안 유지되어온 계산 한계에 대한 근본적 가정에 도전한다. 정렬 장벽은 너무 근본적인 것으로 여겨져서 많은 연구자들이 이 방향에서의 개선 추구를 중단했었다.

The success of this approach suggests other "impossible" barriers in computer science might also be conquerable. It demonstrates the value of questioning long-held assumptions and exploring seemingly unpromising directions.

이 접근법의 성공은 컴퓨터 과학의 다른 "불가능한" 장벽들도 정복할 수 있음을 시사한다. 이는 오래된 가정에 의문을 제기하고 겉보기에 희망 없어 보이는 방향을 탐구하는 가치를 보여준다.

### Implementation Challenges

### 구현 도전과제

Despite its theoretical elegance, the new algorithm faces practical hurdles:

이론적 우아함에도 불구하고, 새 알고리즘은 실제적 장애물에 직면한다:

**Complexity**: The implementation is significantly more complex than Dijkstra's straightforward approach, making it harder to debug and maintain.

**복잡성**: 구현이 다익스트라의 직관적 접근법보다 상당히 복잡하여 디버그와 유지보수가 더 어렵다.

**Memory Usage**: The auxiliary data structures required for clustering and influential node detection increase memory consumption substantially.

**메모리 사용량**: 클러스터링과 영향력 있는 노드 감지에 필요한 보조 데이터 구조가 메모리 소비를 상당히 증가시킨다.

**Constants**: The hidden constants in the O(m log^(2/3) n) bound may be large, potentially limiting practical benefits on smaller graphs.

**상수**: O(m log^(2/3) n) 한계의 숨겨진 상수가 클 수 있어, 작은 그래프에서의 실용적 이익을 제한할 가능성이 있다.

**Robustness**: The algorithm's many interconnected components may be more sensitive to edge cases and numerical precision issues.

**견고성**: 알고리즘의 많은 상호연결된 구성요소들이 엣지 케이스와 수치 정밀도 문제에 더 민감할 수 있다.

### Looking Forward

### 앞으로의 전망

With the sorting barrier vanquished, the new algorithm's runtime isn't close to any fundamental limit that computer scientists know of. This opens the door to further improvements and raises intriguing questions about the ultimate limits of shortest-path computation.

정렬 장벽이 무너진 상황에서, 새 알고리즘의 실행 시간은 컴퓨터 과학자들이 알고 있는 어떤 근본적 한계에도 가깝지 않다. 이는 추가 개선의 문을 열고 최단 경로 계산의 궁극적 한계에 대한 흥미로운 질문을 제기한다.

The research team is already exploring optimizations to reduce the algorithm's complexity and improve its practical performance. Other researchers are investigating whether similar techniques can break barriers in related problems.

연구팀은 이미 알고리즘의 복잡성을 줄이고 실용적 성능을 개선하는 최적화를 탐구하고 있다. 다른 연구자들은 유사한 기법이 관련 문제들의 장벽을 깰 수 있는지 조사하고 있다.

This breakthrough serves as a reminder that in computer science, even the most established foundations can be overturned by creative thinking and persistent effort. After 70 years, Dijkstra's algorithm finally has serious competition and the race for even faster shortest-path algorithms has just begun.

이 돌파구는 컴퓨터 과학에서 가장 확립된 기반조차도 창의적 사고와 끈질긴 노력으로 뒤집힐 수 있음을 상기시켜준다. 70년 만에, 다익스트라 알고리즘이 마침내 진지한 경쟁자를 갖게 되었고 더욱 빠른 최단 경로 알고리즘을 위한 경쟁이 이제 시작되었다.

> The story of this discovery reinforces a crucial lesson: in science, the most transformative breakthroughs often come from questioning what everyone assumes to be impossible. Sometimes, the path forward requires abandoning the very principles that brought us this far.

> 이 발견의 이야기는 중요한 교훈을 강화한다: 과학에서 가장 혁신적인 돌파구는 종종 모든 사람이 불가능하다고 가정하는 것에 의문을 제기하는 것에서 나온다. 때로는 앞으로 나아가는 길은 우리를 여기까지 이끌어온 바로 그 원칙들을 포기하는 것을 요구한다.

_The research paper "Breaking the Sorting Barrier for Directed Single-Source Shortest Paths" by Ran Duan, Xiao Mao, Hanlin Ren, and Zihan Tan represents a collaboration between Tsinghua University and Stanford University, demonstrating the power of international academic cooperation in pushing the boundaries of theoretical computer science._

_란 두안, 샤오 마오, 한린 렌, 지한 탄의 연구 논문 "방향 그래프에서 단일 출발점 최단 경로의 정렬 장벽 깨뜨리기"는 칭화대학교와 스탠포드 대학교 간의 협력을 나타내며, 이론 컴퓨터 과학의 경계를 밀어내는 데 있어 국제 학술 협력의 힘을 보여준다._