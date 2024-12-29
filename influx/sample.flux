import "array"
import "sampledata"

SFOTemps =
    sampleData
        |> findColumn(
            fn: (key) => key._field == "temp" and key.location == "sfo",
            column: "_value",
        )

array.from(rows: [{ output: display(v: SFOTemps) }])