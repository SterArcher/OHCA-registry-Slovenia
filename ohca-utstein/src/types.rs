use chrono::{Duration, NaiveTime};
use sqlx::MySqlPool;

use crate::util::{QueryResult, ToQueryResultHashMap};

#[derive(Debug)]
struct Utstein {
    population_served: i64,
    cardiac_arrests_attended: i64,
    dispatcher_id_ca: DispatcherIdCA,
    dispatcher_cpr: DispatcherCPR,

    // mm:ss
    response_times: String,
    resc_attempted: RescAttempted,
    resc_not_attempted: RescNotAttempted,
    location: Location,
    patient: Patient,
    witnessed: Witnessed,
    bystander_response: BystanderResponse,
    etiology: Etiology,
    ems_process: EMSProcess,
    hospital_process: HospitalProcess,
    patient_outcomes: PatientOutcomes,
}

impl Utstein {
    pub async fn new(pool: &MySqlPool) -> Self {
        let mean_avg = sqlx::query!(
            r#"
                SELECT AVG(responseTime) as "mean!: f64" , STD(responseTime) AS "std!: f64"
                FROM cases
                WHERE responseTime IS NOT NULL;
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap();

        let fractile = 1.28 * mean_avg.std + mean_avg.mean;
        let duration = NaiveTime::from_num_seconds_from_midnight_opt(fractile as u32, 0).unwrap();

        let sum = sqlx::query!(
            r#"
                SELECT 
                    SUM(population) AS "population!: i64",
                    SUM(attendedCAs) AS "attendedCAs!: i64"
                FROM systems;
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap();

        Self {
            population_served: sum.population,
            cardiac_arrests_attended: sum.attendedCAs,
            dispatcher_id_ca: DispatcherIdCA::new(pool).await,
            dispatcher_cpr: DispatcherCPR::new(pool).await,
            response_times: duration.to_string(), // might be an incorrect format
            resc_attempted: RescAttempted::new(pool).await,
            resc_not_attempted: todo!(),
            location: todo!(),
            patient: todo!(),
            witnessed: todo!(),
            bystander_response: todo!(),
            etiology: todo!(),
            ems_process: todo!(),
            hospital_process: todo!(),
            patient_outcomes: todo!(),
        }
    }
}

#[derive(Debug)]
struct DispatcherIdCA {
    yes: i64,
    no: i64,
    unknown: i64,
}

impl DispatcherIdCA {
    async fn new(pool: &MySqlPool) -> Self {
        let records = sqlx::query_as!(
            QueryResult::<Option<i16>>,
            r#"
                SELECT 
                    dispIdentifiedCA AS value,
                    count(*) AS count
                FROM cases
                GROUP BY dispIdentifiedCA;
            "#,
        )
        .fetch_all(pool)
        .await
        .unwrap()
        .to_hashmap();

        Self {
            yes: *records.get(&Some(1)).unwrap(),
            no: *records.get(&Some(0)).unwrap(),
            unknown: *records.get(&Some(-1)).unwrap() + *records.get(&None).unwrap(),
        }
    }
}

#[derive(Debug)]
struct DispatcherCPR {
    yes: i64,
    no: i64,
    unknown: i64,
}

impl DispatcherCPR {
    async fn new(pool: &MySqlPool) -> Self {
        let records = sqlx::query_as!(
            QueryResult::<Option<i16>>,
            r#"
                SELECT 
                    dispProvidedCPRinst AS value,
                    count(*) AS count
                FROM cases
                GROUP BY dispProvidedCPRinst;
            "#,
        )
        .fetch_all(pool)
        .await
        .unwrap()
        .to_hashmap();

        Self {
            yes: *records.get(&Some(1)).unwrap(),
            no: *records.get(&Some(0)).unwrap(),
            unknown: *records.get(&Some(-1)).unwrap() + *records.get(&None).unwrap(),
        }
    }
}

#[derive(Debug)]
struct RescAttempted {
    vf: i64,
    vt: i64,
    pea: i64,
    asys: i64,
    brady: i64,
    aed_non_shockable: i64,
    aed_shockable: i64,
    not_recorded: i64,
    unknown: i64,
}

impl RescAttempted {
    async fn new(pool: &MySqlPool) -> Self {
        let records = sqlx::query_as!(
            QueryResult::<Option<i16>>,
            r#"
                SELECT 
                    firstMonitoredRhy AS value,
                    COUNT(*) AS count
                FROM cases
                WHERE bystanderResponse BETWEEN 1 AND 2
                OR bystanderAED BETWEEN 1 AND 2
                OR mechanicalCPR BETWEEN 1 AND 3
                GROUP BY firstMonitoredRhy;
            "#,
        )
        .fetch_all(pool)
        .await
        .unwrap()
        .to_hashmap();

        Self {
            vf: *records.get(&Some(1)).unwrap(),
            vt: *records.get(&Some(2)).unwrap(),
            pea: *records.get(&Some(3)).unwrap(),
            asys: *records.get(&Some(4)).unwrap(),
            brady: *records.get(&Some(5)).unwrap(),
            aed_non_shockable: *records.get(&Some(6)).unwrap(),
            aed_shockable: *records.get(&Some(7)).unwrap(),
            not_recorded: *records.get(&None).unwrap(),
            unknown: *records.get(&Some(-1)).unwrap(),
        }
    }
}

#[derive(Debug)]
struct RescNotAttempted {
    all_cases: i64,
    dnar: i64,
    obviously_dead: i64,
    signs_of_life: i64,
}

impl RescNotAttempted {
    async fn new(pool: &MySqlPool) -> Self {
        let records = sqlx::query_as!(
            QueryResult::<Option<i16>>,
            r#"
                SELECT
                    firstMonitoredRhy AS value,
                    COUNT(*) AS count
                FROM cases
                WHERE bystanderResponse BETWEEN 1 AND 2
                OR bystanderAED BETWEEN 1 AND 2
                OR mechanicalCPR BETWEEN 1 AND 3
                GROUP BY firstMonitoredRhy;
            "#,
        )
        .fetch_all(pool)
        .await
        .unwrap()
        .to_hashmap();

        let system_data = sqlx::query!(
            r#"
                SELECT 
                    SUM(attendedCAs) - SUM(attemptedResusc) AS "not_attempted!: i64",
                    SUM(casesDNR) AS "dnar!: i64",
                    SUM(casesCirculation) AS "signs_of_life!: i64"
                FROM systems;
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap();

        let obv_dead = sqlx::query!(
            r#"
                SELECT COUNT(*) AS count FROM cases WHERE deadOnArrival = 1;
            "#,
        )
        .fetch_one(pool)
        .await
        .unwrap();

        Self {
            all_cases: system_data.not_attempted,
            dnar: system_data.dnar,
            obviously_dead: obv_dead.count,
            signs_of_life: system_data.signs_of_life,
        }
    }
}

#[derive(Debug)]
struct Location {
    home: i64,
    work: i64,
    rec: i64,
    public: i64,
    educ: i64,
    nursing: i64,
    other: i64,
    unknown: i64,
}

#[derive(Debug)]
struct Patient {
    age: Age,
    sex: Sex,
}

#[derive(Debug)]
struct Age {
    mean: i64,
    unknown: i64,
}

#[derive(Debug)]
struct Sex {
    male: i64,
    female: i64,
    unknown: i64,
}

#[derive(Debug)]
struct Witnessed {
    bystander: i64,
    ems: i64,
    unwitnessed: i64,
    unknown: i64,
}

#[derive(Debug)]
struct BystanderResponse {
    bystander_cpr: BystanderCPR,
    bystander_aed: BystanderAED,
}

#[derive(Debug)]
struct BystanderCPR {
    no_bcpr: i64,
    bcpr: i64,
    cc_only: i64,
    cc_or_vent: i64,
    unknown: i64,
}

#[derive(Debug)]
struct BystanderAED {
    analyse: i64,
    shock: i64,
    unknown: i64,
}

#[derive(Debug)]
struct Etiology {
    medical: i64,
    trauma: i64,
    overdose: i64,
    drowning: i64,
    electrocution: i64,
    asphyxial: i64,
    not_recored: i64,
}

#[derive(Debug)]
struct EMSProcess {
    first_defib_time: i64,

    // targeted temp control
    indicated_done: i64,
    indicated_not_done: i64,
    not_indicated: i64,
    unknown: i64,

    // drugs given
    drugs_given: i64,
}

#[derive(Debug)]
struct HospitalProcess {
    // reperfusion
    attempted: i64,

    // targeted temp control
    indicated_done: i64,
    indicated_not_done: i64,
    not_indicated: i64,
    unknown: i64,

    // organ donation
    organ_donation: i64,
}

#[derive(Debug)]
struct PatientOutcomes {
    all_ems_treated_arrests: Columns,
    shockable_bystander_witnessed: Columns,
    shockable_bystander_cpr: Columns,
    non_shockable_witnessed: Columns,
    user_defined_subgroup: Columns,
}

#[derive(Debug)]
struct Columns {
    any_ROSC: AnyROSC,
    survived_event: SurvivedEvent,
    survival: Survival,
    fav_neurological: FavNeurological,
}

#[derive(Debug)]
struct AnyROSC {
    yes: i64,
    unknown: i64,
}

#[derive(Debug)]
struct SurvivedEvent {
    yes: i64,
    unknown: i64,
}

#[derive(Debug)]
struct Survival {
    yes: i64,
    unknown: i64,
}

#[derive(Debug)]
struct FavNeurological {
    yes: i64,
    unknown: i64,
}
