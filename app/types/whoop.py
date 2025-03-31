from typing import TypedDict

class WhoopUser(TypedDict):
    user_id: str
    email: str
    first_name: str
    last_name: str
    generated_password: str

class CycleScore(TypedDict, total=False):
    strain: float
    kilojoule: float
    average_heart_rate: int
    max_heart_rate: int

class Cycle(TypedDict):
    id: int
    user_id: int
    created_at: str
    updated_at: str
    start: str
    end: str | None
    timezone_offset: str
    score_state: str
    score: CycleScore | None
    strain: float
    kilojoule: float
    average_heart_rate: int
    max_heart_rate: int

class SleepScore(TypedDict, total=False):
    sleep_performance_percentage: int
    total_sleep_duration: int
    time_in_bed: int
    latency_duration: int
    rem_sleep_duration: int
    deep_sleep_duration: int
    light_sleep_duration: int
    awakenings: int
    disturbances: int
    respiratory_rate: float

class Sleep(TypedDict):
    id: int
    user_id: int
    created_at: str
    updated_at: str
    start: str
    end: str
    timezone_offset: str
    nap: bool
    score_state: str
    score: SleepScore | None

class RecoveryScore(TypedDict, total=False):
    recovery_score: float
    resting_heart_rate: float
    hrv_rmssd_milli: float
    spo2_percentage: float | None
    skin_temp_celsius: float | None

class Recovery(TypedDict):
    cycle_id: int
    sleep_id: int
    user_id: int
    created_at: str
    updated_at: str
    score_state: str
    score: RecoveryScore | None
    user_calibrating: bool

class ZoneDuration(TypedDict):
    zone_zero_milli: int
    zone_one_milli: int
    zone_two_milli: int
    zone_three_milli: int
    zone_four_milli: int
    zone_five_milli: int

class WorkoutScore(TypedDict, total=False):
    strain: float
    average_heart_rate: int
    max_heart_rate: int
    kilojoule: float
    percent_recorded: float
    distance_meter: float | None
    altitude_gain_meter: float | None
    altitude_change_meter: float | None
    zone_duration: ZoneDuration

class Workout(TypedDict):
    id: int
    user_id: int
    created_at: str
    updated_at: str
    start: str
    end: str
    timezone_offset: str
    sport_id: int
    score_state: str
    score: WorkoutScore | None