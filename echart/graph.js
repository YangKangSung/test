const data = [
	{
		fixed: true,
		name: "node-1",
		x: myChart.getWidth() / 4,
		y: myChart.getHeight() / 2,
		symbolSize: 50,
		itemStyle: {
			color: "red",
		},
		id: "x",
	},
	{
		fixed: true,
		name: "node-2",
		x: (myChart.getWidth() * 3) / 4,
		y: myChart.getHeight() / 2,
		symbolSize: 50,
		itemStyle: {
			color: "orange",
		},
		id: "y",
	},
	...Array.from({ length: 40 }, (_, i) => ({
		name: `agent-${i + 1}`,
		symbolSize: 30,
		// x: Math.random() * myChart.getWidth(),
		// y: Math.random() * myChart.getHeight(),
		itemStyle: {
			color: "green",
		},
		id: `agent-${i + 1}`,
	})),
];

edges = [];
option = {
	series: [
		{
			type: "graph",
			layout: "force",
			animation: false,
			layoutAnimation: false,
			roam: true,
			gravity: 0,
			label: {
				show: true,
			},
			data: data,
			force: {
				// initLayout: 'circular'
				// gravity: 0
				// repulsion: 300,
				edgeLength: [80, 120],
				gravity: 0.02,
				// edgeLength: 5
			},
			edges: edges,
		},
	],
};

const intervalId = setInterval(function () {
	// data.push({
	//   symbolSize: 30,
	//   name: 'agent' + data.length,
	//   itemStyle: {
	//     color: 'green',
	//   },
	//   id: data.length + ''
	// });
	// var source = Math.round((data.length - 1) * Math.random());
	// var target = Math.round((data.length - 1) * Math.random());
	var source = Math.random() < 0.5 ? "x" : "y";
	// var target = data.length - 1 + '';
	var target = `agent-${Math.floor(Math.random() * 40) + 1}`;
	if (Math.random() > 0.8) {
		if (!edges.find((e) => e.target === target)) {
			edges.push({
				source: source,
				target: target,
				customId: `${source}-${target}`,
			});
			console.log(source, target);
			// if (/* 멈추고 싶은 조건 */) {
			//   stopNext = true;
			// }

			// 플래그가 true면 다음 턴 시작 전에 종료
			// if (stopNext) {
			//   clearInterval(intervalId);
			//   console.log('다음 턴 시작 전에 멈춤');
			// }
			// clearInterval(intervalId);
			// data.push({
			//   fixed: true,
			//   name: 'node-x',
			//   x: myChart.getWidth()/2,
			//   y: myChart.getHeight()/2,
			//   symbolSize: 100,
			//   itemStyle: {
			//     color: 'blue',
			//   },
			//   id: 'x01'
			// });
		}
	} else {
		// edges = edges.filter(e => e.customId !==  `${source}-${target}`);
		if (edges.find((e) => e.source === source && e.target === target)) {
			console.log("remove edge : ", source, target);
			console.log("before removing : ", edges);
			edges = edges.filter((e) => !(e.source === source && e.target === target));
			console.log("after removing : ", edges);
			// clearInterval(intervalId);
		}
	}

	myChart.setOption({
		series: [
			{
				// layout: 'none',
				roam: true,
				data: data,
				edges: edges,
			},
		],
	});
	// console.log('nodes: ' + data.length);
	// console.log('links: ' + data.length);
}, 200);
