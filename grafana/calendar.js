const layouts = [
	[[0, 0]],
	[
		[-0.25, 0],
		[0.25, 0],
	],
	[
		[0, -0.2],
		[-0.2, 0.2],
		[0.2, 0.2],
	],
	[
		[-0.25, -0.25],
		[-0.25, 0.25],
		[0.25, -0.25],
		[0.25, 0.25],
	],
];
const pathes = [
	"M101.02123,145.8035 h-1.925469 v5.96243 h-0.781347 v-5.96243 h-1.920813 v-0.70693 h4.627629 z m4.58111,5.96243 h-3.53467 v-6.66936 h3.38584 v0.70693 h-2.60449 v2.21847 h2.40916 v0.70229 h-2.40916 v2.33474 h2.75332 z m8.08323,0 h-0.7767 v-4.47415 q0,-0.5302 0.0651,-1.29759 h-0.0186 q-0.11162,0.45113 -0.19999,0.64647 l-2.27893,5.12527 h-0.38137 l-2.27428,-5.08806 q-0.0977,-0.22324 -0.19999,-0.68368 h-0.0186 q0.0372,0.39997 0.0372,1.3069 v4.46484 h-0.75345 v-6.66936 h1.0325 l2.04639,4.65088 q0.23719,0.53485 0.30695,0.79995 h0.0279 q0.19999,-0.5488 0.32091,-0.81856 l2.08824,-4.63227 h0.97669 z",
	"M75.918383,146.25982 v-0.92087 q0.15813,0.13952 0.376721,0.25114 0.223242,0.11163 0.465088,0.19069 0.246496,0.0744 0.492993,0.11627 0.246496,0.0419 0.455786,0.0419 0.720886,0 1.074353,-0.2651 0.358118,-0.26975 0.358118,-0.77205 0,-0.26975 -0.120923,-0.46973 -0.116272,-0.19999 -0.325562,-0.36277 -0.209289,-0.16743 -0.497644,-0.31626 -0.283703,-0.15348 -0.613916,-0.32091 -0.348816,-0.17674 -0.651123,-0.35812 -0.302307,-0.18139 -0.525549,-0.39998 -0.223242,-0.21859 -0.353467,-0.49299 -0.125574,-0.27905 -0.125574,-0.65112 0,-0.45579 0.199988,-0.79065 0.199988,-0.33952 0.525549,-0.55811 0.325562,-0.21859 0.73949,-0.32556 0.418579,-0.10697 0.851111,-0.10697 0.985986,0 1.437122,0.2372 v0.87901 q-0.590662,-0.40928 -1.516187,-0.40928 -0.255798,0 -0.511597,0.0558 -0.255798,0.0512 -0.455786,0.17209 -0.199988,0.12092 -0.325561,0.31161 -0.125574,0.19068 -0.125574,0.46508 0,0.2558 0.09302,0.44184 0.09767,0.18603 0.283703,0.33951 0.186035,0.15348 0.451135,0.29766 0.269751,0.14417 0.618567,0.31626 0.358118,0.17673 0.679029,0.37207 0.32091,0.19533 0.562756,0.43253 0.241846,0.23719 0.381372,0.52555 0.144177,0.28835 0.144177,0.66042 0,0.493 -0.195337,0.83716 -0.190686,0.33952 -0.520898,0.55346 -0.325562,0.21394 -0.753442,0.30695 -0.427881,0.0977 -0.902271,0.0977 -0.15813,0 -0.390674,-0.0279 -0.232544,-0.0233 -0.474389,-0.0744 -0.241846,-0.0465 -0.460437,-0.11627 -0.213941,-0.0744 -0.344165,-0.16278 z M86.452623,146.52957 h-0.865064 l-0.706933,-1.86965 h-2.827735 l-0.665075,1.86965 h-0.869714 l2.557983,-6.66936 h0.809253 z M84.624827,143.95764 l-1.046447,-2.84169 q-0.05116,-0.13953 -0.10232,-0.44649 h-0.0186 q-0.04651,0.28371 -0.10697,0.44649 l-1.037146,2.84169 z M94.233542,146.52957 h-0.776696 v-4.47414 q0,-0.5302 0.06511,-1.2976 h-0.0186 q-0.111621,0.45114 -0.199987,0.64647 l-2.278931,5.12527 h-0.381372 l-2.27428,-5.08806 q-0.09767,-0.22324 -0.199988,-0.68368 h-0.0186 q0.03721,0.39998 0.03721,1.3069 v4.46484 h-0.753442 v-6.66936 h1.032495 l2.046386,4.65088 q0.237195,0.53485 0.306958,0.79995 h0.02791 q0.199987,-0.5488 0.32091,-0.81855 l2.088245,-4.63228 h0.976684 z",
	"M0.0,0.0 H12.5 M6.25,0.0 V12.5 M15.0,0.0 V12.5 M15.0,0.0 H27.5 M15.0,6.25 H27.5 M15.0,12.5 H27.5 M30.0,12.5 V0.0 M30.0,0.0 L36.25,6.25 M36.25,6.25 L42.5,0.0 M42.5,0.0 V12.5",
	"M0.0,0.0 H25.0 C37.5,0.0 37.5,12.5 25.0,12.5 C12.5,12.5 12.5,25.0 25.0,25.0 H0.0 M30.0,0.0 V25.0 M30.0,0.0 L45.0,12.5 L30.0,25.0 M35.0,12.5 H40.0 M50.0,0.0 V25.0 M50.0,0.0 L62.5,12.5 L75.0,0.0 V25.0",
	// 'M0.0,0.0 H25.0 M12.5,0.0 V25.0 M30.0,0.0 V25.0 H45.0 M30.0,12.5 H45.0 M30.0,25.0 H45.0 M50.0,0.0 V25.0 M50.0,0.0 L62.5,12.5 L75.0,0.0 V25.0',
	// 'M0.0,0.0 H25.0 C37.5,0.0 37.5,12.5 25.0,12.5 C12.5,12.5 12.5,25.0 25.0,25.0 H0.0 M30.0,0.0 V25.0 M30.0,0.0 L45.0,12.5 L30.0,25.0 M35.0,12.5 H40.0 M50.0,0.0 V25.0 M50.0,0.0 L62.5,12.5 L75.0,0.0 V25.0',
	// 'M936.857805 523.431322c0 0-42.065715-68.89513-88.786739-68.89513-46.68416 0-95.732122 71.223091-95.732122 71.223091s-44.28544-72.503296-93.440922-71.152538c-35.565466 0.977306-62.89705 30.882406-79.124275 64.06615L579.773747 790.800797c-3.253248 37.391565-5.677568 50.904371-12.002816 69.63497-6.651802 19.698688-19.544883 35.227341-31.650099 45.909606-14.30231 12.621414-29.59831 22.066586-45.854208 27.424563-16.28969 5.362074-30.098739 6.496973-51.536794 6.496973-19.498906 0-36.95104-2.963456-52.395418-8.850534-15.410586-5.887078-28.420403-14.313984-39.034573-25.246003-10.613146-10.930995-18.757939-24.08151-24.435507-39.525171-5.676544-15.443763-8.532685-40.195482-8.532685-59.270963l0-26.232454 74.435273 0c0 24.644301-0.17705 64.452915 8.81408 77.006848 9.02697 12.515021 22.756147 18.092032 41.148826 18.791014 16.728678 0.636518 30.032179-8.061645 30.032179-8.061645s11.922022-10.5472 14.992077-19.756954c2.674995-8.025805 3.565363-22.180147 3.565363-22.180147s2.080461-21.789286 2.080461-34.234675L489.399906 514.299369c-16.678502-18.827776-43.801395-61.938688-82.756096-60.927693-54.699008 1.419366-100.422144 70.059622-100.422144 70.059622s-56.065126-70.059622-93.440922-70.059622c-37.376717 0-91.077939 70.059622-91.077939 70.059622S105.343488 156.737741 476.742042 119.363584l53.70327-74.714624 51.373056 74.714624C964.889395 142.740992 936.857805 523.431322 936.857805 523.431322z',
	// 'M533.504 268.288q33.792-41.984 71.68-75.776 32.768-27.648 74.24-50.176t86.528-19.456q63.488 5.12 105.984 30.208t67.584 63.488 34.304 87.04 6.144 99.84-17.92 97.792-36.864 87.04-48.64 74.752-53.248 61.952q-40.96 41.984-85.504 78.336t-84.992 62.464-73.728 41.472-51.712 15.36q-20.48 1.024-52.224-14.336t-69.632-41.472-79.872-61.952-82.944-75.776q-26.624-25.6-57.344-59.392t-57.856-74.24-46.592-87.552-21.504-100.352 11.264-99.84 39.936-83.456 65.536-61.952 88.064-35.328q24.576-5.12 49.152-1.536t48.128 12.288 45.056 22.016 40.96 27.648q45.056 33.792 86.016 80.896z',
	// 'M741.06368 733.310464c8.075264-29.262438 20.615373-40.632422 14.64105-162.810061C966.089728 361.789952 967.93897 72.37847 967.855002 54.693683c0.279347-0.279347 0.418509-0.419533 0.418509-0.419533s-0.17705-0.00512-0.428749-0.00512c0-0.251699 0-0.428749 0-0.428749s-0.139162 0.14633-0.418509 0.425677c-17.695744-0.083866-307.10784 1.760051-515.833958 212.142592-122.181632-5.984256-133.55305 6.563533-162.815693 14.644531C235.35063 295.798886 103.552614 436.975309 90.630758 486.076621c-12.921856 49.105408 39.634227 56.859034 58.579558 58.581197 18.953421 1.724314 121.471386-9.475789 130.09111 4.309094 0 0 16.367411 11.200102 17.226035 41.346662 0.850432 29.796659 15.173222 71.354163 37.123994 97.267302-0.028672 0.027648-0.05632 0.054272-0.083866 0.074752 0.158618 0.13097 0.316211 0.261939 0.474829 0.390861 0.129946 0.149402 0.261939 0.319283 0.393011 0.468685 0.019456-0.019456 0.04608-0.049152 0.075776-0.075674 25.918362 21.961216 67.477504 36.272128 97.269248 37.122458 30.149837 0.859546 41.354547 17.234534 41.354547 17.234534 13.779354 8.608051 2.583962 111.122842 4.302131 130.075546 1.727386 18.95168 9.477222 71.498445 58.579558 58.576077C585.12896 918.526771 726.311117 786.734182 741.06368 733.310464zM595.893555 426.206003c-39.961702-39.965184-39.961702-104.75991 0-144.720077 39.970918-39.96928 104.768307-39.96928 144.730112 0 39.970918 39.960064 39.970918 104.75479 0 144.720077C700.661862 466.171187 635.864474 466.171187 595.893555 426.206003zM358.53312 769.516032c-31.923302-4.573184-54.890394-18.410291-71.41847-35.402342-16.984474-16.526438-30.830387-39.495475-35.405824-71.420621-4.649062-28.082586-20.856832-41.167565-38.76649-38.763827-17.906586 2.40681-77.046886 66.714419-80.857805 89.475891-3.80887 22.752154 29.271859 12.081152 46.424166 27.654861 17.151283 15.590093-2.139853 61.93664-14.733107 86.845952-6.441984 12.735078-10.289766 26.42176-4.22953 33.76087 7.346586 6.070272 21.03593 2.222592 33.769472-4.220109 24.912384-12.585677 71.258829-31.872922 86.842368-14.731469 15.583539 17.160806 4.911002 50.229965 27.674419 46.419251 22.754099-3.807744 87.065395-62.946611 89.466163-80.85248C399.70857 790.374093 386.627072 774.166938 358.53312 769.516032z',
	// 'M848.794624 939.156685 571.780416 939.156685 571.780416 653.17123l341.897539 0 0 221.100654C913.677926 909.960704 884.482867 939.156685 848.794624 939.156685zM571.780403 318.743552c-11.861606-3.210138-31.443354-8.36864-39.829709-16.176435-0.596582-0.561766-1.016218-1.246413-1.613824-1.841971-0.560845 0.596582-1.016218 1.280205-1.613824 1.841971-8.386355 7.807795-15.96631 12.965274-27.827917 16.176435l0 263.544325L141.030675 582.287877 141.030675 355.202884c0-35.687834 29.195059-64.882688 64.883302-64.882688l150.649125 0c-16.984474-9.525965-32.846438-20.56233-46.111027-32.932045-60.250624-56.144691-71.129907-137.062605-24.283034-180.767027 19.615539-18.264986 46.252237-27.124736 75.026739-27.124736 39.933133 0 83.972915 17.070797 118.995968 49.706086 20.353331 18.983322 37.722624 43.405619 50.145075 69.056819 12.457267-25.6512 29.791744-50.074419 50.180915-69.056819 35.022029-32.63529 79.062835-49.706086 118.994944-49.706086 28.74071 0 55.410176 8.860774 75.025715 27.124736 46.882611 43.704422 35.96759 124.622336-24.283034 180.767027-13.264589 12.368691-29.127578 23.40608-46.111027 32.932045l144.649234 0c35.688243 0 64.882278 29.195981 64.882278 64.882688l0 227.084948L571.780416 582.287833 571.780416 318.743508zM435.064218 147.625267c-21.476966-19.965747-49.094144-31.913882-73.868288-31.913882-7.404954 0-21.125018 1.211597-29.863322 9.386803-2.000691 1.824563-8.070144 7.439462-8.070144 21.369754 0 15.650406 8.492749 40.24873 32.319386 62.477926 29.124506 27.12576 77.202432 47.601152 111.76704 47.601152 12.176794 0 16.492237-2.666701 16.527053-2.702541C489.524736 242.54505 475.664486 185.453773 435.064218 147.625267zM577.78135 254.790963c0 0 0.034816-0.034816 0.069632-0.034816 0.807424 0 5.50871 1.790771 15.509914 1.790771 34.564608 0 82.64151-20.47529 111.76704-47.601152 23.826637-22.229299 32.283546-46.810112 32.283546-62.442189 0-13.930291-6.033613-19.562496-8.035328-21.404467-8.77312-8.17623-22.457344-9.386803-29.864346-9.386803-24.808038 0-52.390298 11.948134-73.867264 31.913882C585.325466 185.208218 571.358822 241.73865 577.78135 254.790963zM500.89513 939.156685 205.914017 939.156685c-35.688243 0-64.883302-29.195981-64.883302-64.883712L141.030714 653.17123l359.864462 0L500.895177 939.15666z'
];
const colors = ["#c4332b", "#16B644", "#6862FD", "#FDC763"];
function getVirtulData(year) {
	year = year || "2017";
	let date = +echarts.number.parseDate(year + "-01-01");
	let end = +echarts.number.parseDate(+year + 1 + "-01-01");
	let dayTime = 3600 * 24 * 1000;
	let data = [];
	for (let time = date; time < end; time += dayTime) {
		let items = [];
		let eventCount = Math.round(Math.random() * pathes.length);
		for (let i = 0; i < eventCount; i++) {
			items.push(Math.round(Math.random() * (pathes.length - 1)));
		}
		data.push([echarts.format.formatTime("yyyy-MM-dd", time), items.join("|")]);
	}
	return data;
}
option = {
	tooltip: {},
	calendar: [
		{
			left: "center",
			top: "middle",
			cellSize: [70, 70],
			yearLabel: { show: false },
			orient: "vertical",
			dayLabel: {
				firstDay: 1,
				nameMap: "cn",
			},
			monthLabel: {
				show: false,
			},
			range: "2017-03",
		},
	],
	series: [
		{
			type: "custom",
			coordinateSystem: "calendar",
			renderItem: function (params, api) {
				const cellPoint = api.coord(api.value(0));
				const cellWidth = params.coordSys.cellWidth;
				const cellHeight = params.coordSys.cellHeight;
				const value = api.value(1);
				const events = value && value.split("|");
				if (isNaN(cellPoint[0]) || isNaN(cellPoint[1])) {
					return;
				}
				const group = {
					type: "group",
					children:
						(layouts[events.length - 1] || []).map(function (itemLayout, index) {
							return {
								type: "path",
								shape: {
									pathData: pathes[+events[index]],
									x: -8,
									y: -8,
									width: 16,
									height: 16,
								},
								position: [
									cellPoint[0] + echarts.number.linearMap(itemLayout[0], [-0.5, 0.5], [-cellWidth / 2, cellWidth / 2]),
									cellPoint[1] + echarts.number.linearMap(itemLayout[1], [-0.5, 0.5], [-cellHeight / 2 + 20, cellHeight / 2]),
								],
								style: api.style({
									fill: colors[+events[index]],
								}),
							};
						}) || [],
				};
				group.children.push({
					type: "text",
					style: {
						x: cellPoint[0],
						y: cellPoint[1] - cellHeight / 2 + 15,
						text: echarts.format.formatTime("dd", api.value(0)),
						fill: "#777",
						textFont: api.font({ fontSize: 14 }),
					},
				});
				return group;
			},
			dimensions: [undefined, { type: "ordinal" }],
			data: getVirtulData("2017"),
		},
	],
};
