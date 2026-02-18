// === 예시 데이터 ===
const nodes = [{ name: "A" }, { name: "A1" }, { name: "A2" }, { name: "B" }, { name: "B1" }, { name: "C" }, { name: "D" }];

const links = [
	{ source: "A", target: "A1", value: 1 },
	{ source: "A1", target: "C", value: 1 },
	{ source: "A", target: "A2", value: 1 },
	{ source: "A2", target: "C", value: 1 },
	{ source: "B", target: "B1", value: 1 },
	{ source: "B1", target: "C", value: 1 },
	{ source: "A1", target: "B", value: 1 },
	{ source: "A2", target: "D", value: 1 },
];

// === 보조 구조 ===
const outAdj = {};
const outdeg = {};
nodes.forEach((n) => {
	outAdj[n.name] = [];
	outdeg[n.name] = 0;
});

links.forEach((l) => {
	outAdj[l.source].push(l.target);
	outdeg[l.source] += 1;
});

// 리프 판별
const isLeaf = (name) => (outdeg[name] || 0) === 0;

// === 핵심: 각 노드의 "서브트리 내 leaf-edge 집합" 구하기 ===
// f(node) = 집합 { (u->v) | node에서 내려가 도달 가능, v는 leaf }
// 중복 카운트 방지를 위해 에지 키를 "u|v" 문자열로 저장
const memoSet = {};
function leafEdgeSet(node) {
	if (memoSet[node]) return memoSet[node];

	const set = new Set();
	for (const child of outAdj[node]) {
		if (isLeaf(child)) {
			set.add(`${node}|${child}`); // 바로 leaf로 가는 에지
		} else {
			const childSet = leafEdgeSet(child); // 자식 서브트리의 leaf-edges
			childSet.forEach((k) => set.add(k));
		}
	}
	memoSet[node] = set;
	return set;
}

// 표시값 계산(리프 제외): size of leafEdgeSet(node)
const processedNodes = nodes.map((n) => {
	const _isLeaf = isLeaf(n.name);
	const count = _isLeaf ? null : leafEdgeSet(n.name).size;
	return { ...n, displayCount: count };
});

// === ECharts 옵션 ===
option = {
	tooltip: {
		trigger: "item",
		formatter: (p) => {
			if (p.dataType === "node" && p.data.displayCount != null) {
				return `${p.name}<br/>서브트리 내 leaf-edge 수: ${p.data.displayCount}`;
			}
		},
	},
	series: [
		{
			type: "sankey",
			orient: "vertical",
			data: processedNodes,
			links,
			label: {
				formatter: (p) => (p.data.displayCount != null ? `${p.name} (${p.data.displayCount})` : p.name), // 리프는 표시 없음
			},
			emphasis: { focus: "adjacency" },
		},
	],
};
