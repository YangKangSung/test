  option v = {
    timeRangeStart: -3y,
    timeRangeStop: now()
}

  from(bucket: "livingRoom")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "home")
  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
  |> filter(fn: (r) => r["hum"] == 36.4) // hum 값이 36.1인 행 필터링
  |> yield(name: "debug")