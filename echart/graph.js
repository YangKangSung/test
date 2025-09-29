const LOGO_SYMBOL = 'image://data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjggMTI4Ij48cGF0aCBmaWxsPSIjMDE3Y2VlIiBkPSJtMi41NDQgMTI3IDYwLjgxLTYyLjMzMmExLjEyNCAxLjEyNCAwIDAgMCAuMTM1LTEuNDM3Yy0zLjY5OC01LjE2Mi0xMC41MjEtNi4wNTgtMTMuMDUtOS41MjctNy40OS0xMC4yNzUtOS4zOS0xNi4wOTItMTIuNjEtMTUuNzNhMSAxIDAgMCAwLS41ODUuMzA4TDE1LjI3OCA2MC44QzIuNjQgNzMuNzQ0LjgyNCAxMDIuMjc1LjQ5NiAxMjYuMTY3YTEuMTkgMS4xOSAwIDAgMCAyLjA0OC44MzMiLz48cGF0aCBmaWxsPSIjMDBhZDQ2IiBkPSJNMTI2Ljk5IDEyNS40NiA2NC42NTggNjQuNjQ3YTEuMTI0IDEuMTI0IDAgMCAwLTEuNDM5LS4xMzZjLTUuMTYyIDMuNy02LjA1OCAxMC41MjEtOS41MjcgMTMuMDUtMTAuMjc1IDcuNDktMTYuMDkyIDkuMzkxLTE1LjczIDEyLjYxYTEgMSAwIDAgMCAuMzA4LjU4M2wyMi41MTggMjEuOTY2YzEyLjk0NCAxMi42MzggNDEuNDc1IDE0LjQ1NCA2NS4zNjcgMTQuNzgyYTEuMTkgMS4xOSAwIDAgMCAuODM1LTIuMDQxeiIvPjxwYXRoIGZpbGw9IiMwNGQ2NTkiIGQ9Ik02MC43OTIgMTEyLjcyYy03LjA3Ni02LjkwMy0xMC4zNTUtMjAuNTU5IDMuMjA2LTQ4LjcxOS0yMi4wNDYgOS44NTMtMjkuNzcxIDIyLjgwMy0yNS45NzIgMjYuNTExeiIvPjxwYXRoIGZpbGw9IiMwMGM3ZDQiIGQ9Ik0xMjUuNDUgMS4wMTEgNjQuNjQzIDYzLjM0M2ExLjEyIDEuMTIgMCAwIDAtLjEzNiAxLjQzN2MzLjcgNS4xNjMgMTAuNTIgNi4wNTggMTMuMDUgOS41MjcgNy40OSAxMC4yNzUgOS4zOTMgMTYuMDkyIDEyLjYxIDE1LjczYS45OC45OCAwIDAgMCAuNTg1LS4zMDhsMjEuOTY2LTIyLjUxOGMxMi42MzgtMTIuOTQ0IDE0LjQ1NC00MS40NzUgMTQuNzgyLTY1LjM2N2ExLjE5MyAxLjE5MyAwIDAgMC0yLjA1LS44MzJ6Ii8+PHBhdGggZmlsbD0iIzExZTFlZSIgZD0iTTExMi43MyA2Ny4yMTFjLTYuOTAzIDcuMDc2LTIwLjU1OSAxMC4zNTUtNDguNzIxLTMuMjA2IDkuODUzIDIyLjA0NiAyMi44MDMgMjkuNzcxIDI2LjUxMSAyNS45NzJ6Ii8+PHBhdGggZmlsbD0iI2U0MzkyMSIgZD0ibTEuMDAyIDIuNTUgNjIuMzMyIDYwLjgwN2ExLjEyNCAxLjEyNCAwIDAgMCAxLjQzNi4xMzVjNS4xNjMtMy43IDYuMDU4LTEwLjUyIDkuNTI3LTEzLjA1IDEwLjI3NS03LjQ5IDE2LjA5Mi05LjM5IDE1LjczMS0xMi42MWExIDEgMCAwIDAtLjMwOC0uNTg0TDY3LjIwMiAxNS4yODJDNTQuMjU4IDIuNjQ0IDI1LjcyNy44MjggMS44MzUuNWExLjE5IDEuMTkgMCAwIDAtLjgzMyAyLjA1Ii8+PHBhdGggZmlsbD0iI2ZmNzU1NyIgZD0iTTY3LjIxMiAxNS4yODRjNy4wNzYgNi45MDQgMTAuMzU1IDIwLjU1OS0zLjIwNiA0OC43MjFDODYuMDUyIDU0LjE1MyA5My43NzcgNDEuMiA4OS45NzggMzcuNDk0eiIvPjxwYXRoIGZpbGw9IiMwY2I2ZmYiIGQ9Ik0xNS4yNzkgNjAuOEMyMi4xODMgNTMuNzI0IDM1LjgzOCA1MC40NDUgNjQgNjQuMDA2IDU0LjE0OCA0MS45NiA0MS4xOTcgMzQuMjM1IDM3LjQ4OSAzOC4wMzR6Ii8+PGNpcmNsZSBjeD0iNjQuMDA5IiBjeT0iNjMuOTk1IiByPSIyLjcxOCIgZmlsbD0iIzRhNDg0OCIvPjwvc3ZnPg==';

const data = [
	{
		fixed: true,
		name: "node-1",
		x: myChart.getWidth() / 4,
		y: myChart.getHeight() / 2,
		symbol: LOGO_SYMBOL,
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
