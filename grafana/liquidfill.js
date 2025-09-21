var option = {
	series: [
		{
			type: "liquidFill",
			data: [0.6, 0.5, 0.4, 0.3],
			animationDuration: 0,
			animationDurationUpdate: 2000,
			animationEasingUpdate: "Linear",
		},
	],
};
// chart.setOption(option);
setTimeout(function () {
	chart.setOption({
		series: [
			{
				type: "liquidFill",
				data: [0.8, 0.6, 0.4, 0.2],
			},
		],
	});
}, 3000);
// var option = {
//   series: [{
//     type: 'liquidFill',
//     name: 'Liquid Fill',
//     // amplitude: 15,
//     waveAnimation: 1,
//     animationDuration: 10,
//     animationDurationUpdate: 50000,
//     animationEasingUpdate: 'cubicOut',
//     data: [{
//       name: 'a',
//       value: 0.6
//     },
//     {
//       name: 'b',
//       value: 0.5,
//       itemStyle: {
//         color: 'yellow',
//         opacity: 0.6
//       },
//       emphasis: {
//         itemStyle: {
//           opacity: 0.1
//         }
//       }
//     },
//       0.4, 0.3],
//     label: {
//       formatter: '{a}\n{b}\nValue: {c}',
//       fontSize: 11
//     }
//   }]
// };
// setTimeout(function () {
//   chart.setOption({
//     series: [{
//       type: 'liquidFill',
//       data: [0.8, 0.6, 0.4, 0.2]
//     }]
//   })
// }, 3000);

return option;
