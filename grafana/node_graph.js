const values = [
	{
		fixed: true,
		name: "A",
		label: { show: true },
		x: context.panel.chart.getWidth() / 3,
		y: context.panel.chart.getHeight() / 2,
		symbolSize: 50,
		id: "-1",
	},
	{
		fixed: true,
		name: "B",
		label: { show: true },
		x: (context.panel.chart.getWidth() / 3) * 2,
		y: context.panel.chart.getHeight() / 2,
		symbolSize: 50,
		id: "-2",
	},
	...Array.from({ length: 32 }, (_, i) => ({
		name: `agent-${i + 1}`,
		symbol: "none",
		label: {
			show: true,
			position: "inside", // 텍스트 위치
			formatter: "{b}",
			padding: [5, 10], // 텍스트 주변 여백 (사각형 크기 조절)
			backgroundColor: "black", // 사각형 배경색
			borderRadius: 3, // 둥근 모서리 (선택 사항)
			color: "white", // 텍스트 색상 (선택 사항)
			fontSize: 10, // 텍스트 크기
		},
		// itemStyle: { color: 'red' },
		symbolSize: 10,
		id: `${i + 1}`,
		symbol: "rect",
	})),
];

const edges = [];

option = {
	series: [
		{
			type: "graph",
			layout: "force",
			animation: true,
			data: values,
			force: {
				// initLayout: 'circular',
				gravity: 0.1,
				repulsion: 150,
				edgeLength: 50,
				center: [
					context.panel.chart.getWidth() / 2, // A와 B의 x 좌표 중간값
					context.panel.chart.getHeight() / 2, // A와 B의 y 좌표 중간값
				],
			},
			edges: edges,
		},
	],
};

// setInterval(function () {
//   if (values.length > 30) {
//     return;
//   }

//   values.push({
//     itemStyle: { color: 'red' },
//     symbolSize: 20,
//     id: values.length + ''
//   });
//   // var source = Math.round((values.length - 1) * Math.random());
//   // var target = Math.round((values.length - 1) * Math.random());
//   // if (source !== target) {
//   source = '-1';
//   target = values.length - 1 + '';
//   console.log(source, target);
//   edges.push({
//     source: source,
//     target: target
//   });
//   // }
//   context.panel.chart.setOption({
//     series: [
//       {
//         roam: true,
//         data: values,
//         edges: edges
//       }
//     ]
//   });
// }, 1000);

return option;
