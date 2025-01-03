const series = context.panel.data.series.map((s) => {
	const sData = s.fields.find((f) => f.type === "number").values.buffer || s.fields.find((f) => f.type === "number").values;
	const sTime = s.fields.find((f) => f.type === "time").values.buffer || s.fields.find((f) => f.type === "time").values;

	return {
		name: s.refId,
		type: "line",
		showSymbol: false,
		areaStyle: {
			opacity: 0.1,
		},
		lineStyle: {
			width: 1,
		},
		data: sData.map((d, i) => [sTime[i], d.toFixed(2)]),
	};
});

/**
 * Enable Data Zoom by default
 */
setTimeout(
	() =>
		context.panel.chart.dispatchAction({
			type: "takeGlobalCursor",
			key: "dataZoomSelect",
			dataZoomSelectActive: true,
		}),
	500
);

/**
 * Update Time Range on Zoom
 */
context.panel.chart.on("datazoom", function (params) {
	const startValue = params.batch[0]?.startValue;
	const endValue = params.batch[0]?.endValue;
	locationService.partial({ from: startValue, to: endValue });
});

console.log(window.grafana);

// if (context.panel.chart) {
//   context.panel.chart.on('click', function (params) {
//     const selectedValue = params.name; // 클릭된 데이터 포인트의 이름
//     if (grafana && grafana.__setVar) {
//       grafana.__setVar('selectedData', selectedValue); // Grafana 변수 업데이트
//     } else {
//       console.error('Grafana 변수 업데이트 함수(__setVar)를 찾을 수 없습니다.');
//     }
//   });
// }

return {
	backgroundColor: "transparent",
	tooltip: {
		trigger: "axis",
	},
	legend: {
		left: "0",
		bottom: "0",
		data: context.panel.data.series.map((s) => s.refId),
		textStyle: {
			color: "rgba(128, 128, 128, .9)",
		},
	},
	toolbox: {
		feature: {
			dataZoom: {
				yAxisIndex: "none",
				icon: {
					zoom: "path://",
					back: "path://",
				},
			},
			saveAsImage: {},
		},
	},
	xAxis: {
		type: "time",
	},
	yAxis: {
		type: "value",
		min: "dataMin",
	},
	grid: {
		left: "2%",
		right: "2%",
		top: "2%",
		bottom: 24,
		containLabel: true,
	},
	series,
};
