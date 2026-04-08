
import pandas as pd
import numpy as np

INPUT_XLSX = "0520-PPR-0303_0825 al 0226.xlsx"
SHEET_NAME = "Tabla"
HEADER_ROW = 1  # Excel row 2

INVALID_TOKENS = ["Bad Input", "No Data", "I/O Timeout", "Pt Created"]
BEARING_COLS = ["pump_303_rtd_7_temperature_c", "pump_303_rtd_8_temperature_c"]
MOTOR_COLS = [f"pump_303_rtd_{i}_temperature_c" for i in range(1, 7)]

CURRENT_NOMINAL_A = 81.5
BEARING_ALARM_C = 140
BEARING_TRIP_C = 150
MOTOR_ALARM_C = 150
MOTOR_TRIP_C = 160

def build_clean_dataset(input_xlsx: str = INPUT_XLSX) -> pd.DataFrame:
    df = pd.read_excel(input_xlsx, sheet_name=SHEET_NAME, header=HEADER_ROW)

    # Correct confirmed unit in pressure tag
    df = df.rename(columns={"pump_303_discharge_pressure_bar": "pump_303_discharge_pressure_psi"})

    # Standardize invalid tokens
    df = df.replace(INVALID_TOKENS, np.nan)

    # Map digital tags
    df["pump_303_moisture_alarm_bool"] = df["pump_303_moisture_alarm_bool"].replace({
        "DESACTIVO": 0,
        "ACTIVO": 1,
    })
    df["pump_303_moisture_trip_bool"] = df["pump_303_moisture_trip_bool"].replace({
        "Normal": 0,
    })

    # Convert types
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    for col in df.columns:
        if col != "timestamp":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Temperature sentinels observed in historian
    temp_cols = BEARING_COLS + MOTOR_COLS
    for col in temp_cols:
        df[col] = df[col].mask(df[col] >= 200, np.nan)

    # Helper features for dashboard
    df["pump_running_flag"] = (
        df["pump_303_speed_rpm"].fillna(0).gt(100)
        | df["pump_303_current_a"].fillna(0).gt(5)
        | df["pump_303_power_kw"].fillna(0).gt(5)
    ).astype(int)

    df["bearing_temp_max_c"] = df[BEARING_COLS].max(axis=1, skipna=True)
    df["motor_temp_max_c"] = df[MOTOR_COLS].max(axis=1, skipna=True)
    df["current_pct_nominal"] = df["pump_303_current_a"] / CURRENT_NOMINAL_A * 100

    # Rule-based flags
    df["flag_bearing_alarm"] = (df["bearing_temp_max_c"] >= BEARING_ALARM_C).astype("Int64")
    df["flag_bearing_trip"] = (df["bearing_temp_max_c"] >= BEARING_TRIP_C).astype("Int64")
    df["flag_motor_alarm"] = (df["motor_temp_max_c"] >= MOTOR_ALARM_C).astype("Int64")
    df["flag_motor_trip"] = (df["motor_temp_max_c"] >= MOTOR_TRIP_C).astype("Int64")
    df["flag_current_high"] = (df["pump_303_current_a"] >= CURRENT_NOMINAL_A).astype("Int64")
    df["flag_current_near_high"] = (df["pump_303_current_a"] >= CURRENT_NOMINAL_A * 0.90).astype("Int64")
    df["flag_speed_ref_outside_recommended"] = (
        ~df["pump_303_speed_reference_pct"].between(50, 100, inclusive="both")
    ).astype("Int64")
    df["flag_moisture_alarm"] = (df["pump_303_moisture_alarm_bool"] == 1).astype("Int64")
    df["flag_moisture_trip"] = (df["pump_303_moisture_trip_bool"] == 1).astype("Int64")
    df["flag_any_critical_missing"] = df[
        ["pump_303_current_a", "pump_303_power_kw", "pump_303_speed_rpm", "pump_303_speed_reference_pct"]
    ].isna().any(axis=1).astype("Int64")
    df["flag_any_temp_missing"] = df[temp_cols].isna().any(axis=1).astype("Int64")
    df["flag_discharge_pressure_missing"] = df["pump_303_discharge_pressure_psi"].isna().astype("Int64")

    return df

if __name__ == "__main__":
    out = build_clean_dataset()
    out.to_csv("pump_303_clean_streamlit.csv", index=False)
    print("Saved pump_303_clean_streamlit.csv")
