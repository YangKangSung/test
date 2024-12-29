import "array"

option v = {
    timeRangeStart: -3y,
    timeRangeStop: now()
}

data = from(bucket: "livingRoom")
|> range(start: v.timeRangeStart, stop: v.timeRangeStop)
|> filter(fn: (r) => r._measurement == "home" and r.room == "Living Room")
|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
|> limit(n: 1)  // 첫 번째 데이터만 가져오기
|> findRecord(fn: (key) => true, idx: 0) // 첫 번째 레코드를 찾습니다

// |> map(fn: (r) => ({ temperature: r.hum }))
// |> findRecord(fn: (key) => true, idx: 0) // 첫 번째 값을 레코드로 가져오기
// humValue = data.hum
from(bucket: "livingRoom")
|> range(start: v.timeRangeStart, stop: v.timeRangeStop)
// |> filter(fn: (r) => r._measurement == "home" and r.room == "Living Room")
|> filter(fn: (r) => r._measurement == "home" and r.room == "Living Room" and r._value == data.hum)
// |> filter(fn: (r) => r._measurement == "home" and r.room == "Living Room" and r.hum == data.hum)


// humValue |> yield(name : "hum_value")

// data |> yield(name: "temperature_check")

// from(bucket: "livingRoom")
// |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
// |> filter(fn: (r) => r._measurement == "home" and r._value > data.temperature)
// |> yield(name: "alerts_above_temperature")

// data |> yield(name: "temperature_check")