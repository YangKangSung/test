  option v = {
    timeRangeStart: -3y,
    timeRangeStop: now()
}

data = from(bucket: "livingRoom")
|> range(start: v.timeRangeStart, stop: v.timeRangeStop)
|> filter(fn: (r) => r["_measurement"] == "home")
|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
|> filter(fn: (r) => r["hum"] == 36.4) // hum 값이 36.1인 행 필터링
|> yield(name: "debug")

times = data
|> map(fn: (r) => ({ time: r._time }))
|> keep(columns: ["time"])
|> yield(name: "debug-1")

timeList = data
|> map(fn: (r) => ({ time: r._time }))
|> keep(columns: ["time"])
|> yield(name: "debug-2")

timeVal = timeList
|> first() // 첫 번째 행에서 값 추출
|> findRecord(fn: (key) => true, idx: 0).time


from(bucket: "livingRoom")
|> range(start: v.timeRangeStart, stop: v.timeRangeStop)
|> filter(fn: (r) => r["_measurement"] == "home")
|> filter(fn: (r) => r["_time"] == timeVal.time)
